# Claude Engineer

An interactive self imporving AI coding agent for creating and using AI tools with Claude.At its core, Claude Engineer introduces a dynamic tool ecosystem where the AI can autonomously create, manage, and execute its own tools during conversations. This allows the system to continuously expand its capabilities, adapting to user needs in real time and becoming more effective the more it is used.

# Features
- Dynamic tool creation and loading
- Dynamic expansion of capabilities during interactions
- Smart management of tool dependencies
- Adaptation based on tool usage patterns
- Automated generation of tool code
- Integrates with Claude of any model
- Real-time display of tool execution
- Token usage tracking via Anthropic API
- Continuous refinement of existing tools
- Improves reliability with enhanced error handling and debugging
- Dynamic module importing system

# Requirements🧷
- Windows or Linux OS
- Python 3.6+
- Anthropic API Key
- Required packages in `requirements.txt`

# Installation


```bash
git clone https://github.com/bawadou/claude-engineer
cd claude-engineer
pip install -r requirements.txt
# or
pip install -e .
```

# Configuration⚙

Create .env file and copy `.env.example` to `.env` and fill in your key:

```
ANTHROPIC_API_KEY=sk-ant-...
```
The agent supports configuration options through the Config class:

| Option        | Description                                   |
|--------------|-------------------------------------------------|
| `CE_MODEL`  | Which Claude model to use for the conversation               |
| `ANTHROPIC_API_KEY` | Your Anthropic API key from [console.anthropic.com](https://console.anthropic.com/). The agent will refuse to start without it.               |
| `CE_MAX_TOKENS`   | Maximum number of tokens the model is allowed to generate in a single response. Higher values allow longer outputs but cost more.                               |
| `CE_VERBOSE`  | When set to `1`, prints every tool invocation and its arguments as they happen. Useful for debugging the agent loop.               |
| `CE_TOOLS_DIR` | Directory for tool storage      |

# Run

```bash
python -m claude_engineer
```

Type `/help` inside the REPL to see commands.

# Built-in Tools

There are some pre-built tools available in Claude Engineer.

| Tool         | What it does                                    |
|--------------|-------------------------------------------------|
| `read_file`| Read a text file from the project               |
| `create_tool`| Create new tools using frameworks self-improvement core             |
| `write_file` | Create or overwrite a text file                 |
| `list_dir`   | List a directory                                |
| `run_shell`  | Run a shell command (60s timeout)               |
| `web_search` | Search the web via Anthropic's hosted tool      |

## Project structure
```
├── claude_engineer/          # Main package
│   ├── __init__.py           # Package exports
│   ├── __main__.py           # Entry point for `python -m claude_engineer`
│   ├── agent.py              # Core conversation loop and tool orchestration
│   ├── cli.py                # Interactive REPL and argument parsing
│   ├── config.py             # Configuration loading and defaults
│   └── tools/                # Built-in tool implementations
│       ├── __init__.py       # Tool registry
│       ├── base.py           # Abstract tool interface
│       ├── fs.py             # File system operations
│       ├── shell.py          # Shell command execution
│       └── search.py         # Web search integration
├── tests/                    # Unit tests
├── pyproject.toml            # Package metadata and dependencies
├── requirements.txt          # Runtime dependencies
├── .env.example              # Template for environment variables
├── .gitignore
└── README.md
```

# Contribution
Contributions are welcome. Whether it's a new tool, or a bug fix — open an issue first if the change is non-trivial, so we can align on the approach before you submit a Pull-Request.

## License
MIT - Use freely, modify as needed, contribute back if you can.
