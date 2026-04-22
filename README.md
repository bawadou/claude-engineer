# Claude Engineer

Interactive coding agent powered by Claude Opus 4.7. Runs in a terminal,
reads and writes files in your project, executes shell commands, and
searches the web when it needs to.

## Install

```bash
pip install -r requirements.txt
# or
pip install -e .
```

## Setup

Copy `.env.example` to `.env` and fill in your key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Run

```bash
python -m claude_engineer
# or, if installed as a package:
claude-engineer
```

Type `/help` inside the REPL to see commands.

## Tools

| Tool         | What it does                                    |
|--------------|-------------------------------------------------|
| `read_file`  | Read a text file from the project               |
| `write_file` | Create or overwrite a text file                 |
| `list_dir`   | List a directory                                |
| `run_shell`  | Run a shell command (60s timeout)               |
| `web_search` | Search the web via Anthropic's hosted tool      |

## License

MIT
