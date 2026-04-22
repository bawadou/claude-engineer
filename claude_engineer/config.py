"""Configuration for Claude Engineer.

Reads environment variables and provides defaults. Intended to be
instantiated once at startup via `Config.load()`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is optional at runtime
    load_dotenv = None


DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_MAX_TOKENS = 8192
DEFAULT_SYSTEM_PROMPT = """You are Claude Engineer, an autonomous coding assistant.

You operate inside a user's project directory and have access to tools for
reading and writing files, listing directories, running shell commands, and
searching the web. Use them deliberately:

- Read before you write. Inspect the relevant files before proposing changes.
- Prefer small, reversible edits. Show your reasoning in plain prose.
- When running shell commands, explain what you are about to do.
- If a task is ambiguous, ask one clarifying question rather than guessing.

Keep responses focused. The user is a developer — be direct."""


@dataclass
class Config:
    """Runtime configuration for the agent."""

    api_key: str
    model: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    workdir: Path = field(default_factory=Path.cwd)
    allow_shell: bool = True
    verbose: bool = False

    @classmethod
    def load(cls, env_file: str | Path | None = ".env") -> "Config":
        """Load config from environment, optionally reading an .env file first."""
        if env_file and load_dotenv is not None:
            env_path = Path(env_file)
            if env_path.exists():
                load_dotenv(env_path)

        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Put it in your environment or "
                "in a .env file next to the project."
            )

        model = os.environ.get("CE_MODEL", DEFAULT_MODEL)
        max_tokens = int(os.environ.get("CE_MAX_TOKENS", DEFAULT_MAX_TOKENS))
        allow_shell = os.environ.get("CE_ALLOW_SHELL", "1") not in ("0", "false", "False")
        verbose = os.environ.get("CE_VERBOSE", "0") not in ("0", "false", "False")

        return cls(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
            allow_shell=allow_shell,
            verbose=verbose,
        )
