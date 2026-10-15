# Tech

- Python 3.12, virtualenv at `../../.venv` (built by `../../setup_env.sh`). Always run Python as `../../.venv/bin/python`.
- LLM access through **aisuite** 0.1.11 via the `LLM` wrapper in `agent.py`; models are provider-prefixed ids (e.g. `anthropic:...`, `openai:gpt-4o`). Default from `AGENT_MODEL` in `../../.env`.
- Tools are plain functions in `tools.py`; aisuite builds tool schemas from their docstrings, so every tool needs a complete docstring with typed args.
- Tools: Wikipedia (`wikipedia` package), Tavily web search (`TAVILY_API_KEY`, falls back to Wikipedia), calculator.
- Tests: pytest, must run fully offline (`--offline` mode uses `_mock_reply`). Run: `../../.venv/bin/python -m pytest -q tests`.
- Pinned constraints: `aisuite==0.1.11`, `mistralai<2`, `mcp<2`. Do not upgrade these.
- Secrets live only in `../../.env`. Never read, print or commit it.
