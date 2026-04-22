"""Core agent loop for Claude Engineer.

The Agent keeps a rolling message history and drives a conversation
with the Claude API. When the model emits `tool_use` blocks, the agent
executes the corresponding local tool, feeds the result back as a
`tool_result`, and continues until the model produces a final
assistant turn with no more tool calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from anthropic import Anthropic
from anthropic.types import Message

from claude_engineer.config import Config
from claude_engineer.tools import BUILTIN_TOOLS
from claude_engineer.tools.base import Tool, ToolError
from claude_engineer.tools.search import WebSearch


MAX_TOOL_ITERATIONS = 25


@dataclass
class Agent:
    """Stateful conversation agent."""

    config: Config
    tools: list[Tool] = field(default_factory=lambda: list(BUILTIN_TOOLS))
    history: list[dict[str, Any]] = field(default_factory=list)
    _client: Anthropic | None = None

    def __post_init__(self) -> None:
        self._client = Anthropic(api_key=self.config.api_key)
        self._tool_by_name = {t.name: t for t in self.tools}

    # ---------- public API ----------

    def send(self, user_message: str) -> str:
        """Send a user message, run the tool-use loop, return final text."""
        self.history.append({"role": "user", "content": user_message})
        return self._run_loop()

    def reset(self) -> None:
        """Clear conversation history."""
        self.history.clear()

    # ---------- internals ----------

    def _build_api_tools(self) -> list[dict[str, Any]]:
        """Build the `tools` payload for the Anthropic API."""
        payload: list[dict[str, Any]] = []
        for tool in self.tools:
            if isinstance(tool, WebSearch):
                # Server-side tool — use Anthropic's built-in type tag.
                payload.append({
                    "type": tool.server_tool_type,
                    "name": tool.name,
                })
            else:
                payload.append(tool.to_schema())
        return payload

    def _run_loop(self) -> str:
        assert self._client is not None
        api_tools = self._build_api_tools()

        for _ in range(MAX_TOOL_ITERATIONS):
            response: Message = self._client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                system=self.config.system_prompt,
                tools=api_tools,
                messages=self.history,
            )

            # Record the assistant turn verbatim so tool_use IDs line up
            # with the tool_result we send back.
            self.history.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                return _collect_text(response)

            tool_results = self._handle_tool_uses(response)
            self.history.append({"role": "user", "content": tool_results})

        raise RuntimeError(
            f"Agent exceeded {MAX_TOOL_ITERATIONS} tool iterations without a final answer."
        )

    def _handle_tool_uses(self, response: Message) -> list[dict[str, Any]]:
        """Execute every tool_use block in `response` and collect results."""
        results: list[dict[str, Any]] = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            name = block.name
            tool_input = block.input or {}
            if self.config.verbose:
                print(f"[tool] {name}({tool_input})")

            tool = self._tool_by_name.get(name)
            if tool is None:
                results.append(_tool_result_block(block.id, f"Unknown tool: {name}", is_error=True))
                continue

            if isinstance(tool, WebSearch):
                # Should not happen — server-side tool results are inlined
                # into the assistant turn by the API.
                continue

            try:
                out = tool.run(**tool_input)
                results.append(_tool_result_block(block.id, out.content, is_error=out.is_error))
            except ToolError as exc:
                results.append(_tool_result_block(block.id, str(exc), is_error=True))
            except Exception as exc:  # noqa: BLE001
                results.append(_tool_result_block(block.id, f"Tool crashed: {exc}", is_error=True))

        return results


def _tool_result_block(tool_use_id: str, content: str, *, is_error: bool) -> dict[str, Any]:
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": content,
        "is_error": is_error,
    }


def _collect_text(response: Message) -> str:
    parts = [b.text for b in response.content if getattr(b, "type", None) == "text"]
    return "\n".join(parts).strip()
