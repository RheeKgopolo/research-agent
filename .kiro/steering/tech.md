# Tech

- Python 3.12+, project-local virtualenv at `.venv` (built by `./setup.sh`). Always run Python as `.venv/bin/python`.
- Dependencies are pinned in `requirements.txt` (runtime) and `requirements-dev.txt` (pytest, ipykernel). Add new packages there with an exact `==` pin; never `pip install --upgrade` ad hoc.
- LLM access through **aisuite** 0.2.0 via the `LLM` wrapper in `agent.py`; models are provider-prefixed ids (e.g. `anthropic:claude-sonnet-5-5`, `openai:gpt-4o`). Default from `AGENT_MODEL` in `.env`.
- aisuite's extras pin the provider SDKs (`anthropic<1`, `openai<2`); do not install newer major versions of those directly.
- Tools are plain functions in `tools.py`; aisuite builds tool schemas from their docstrings, so every tool needs a complete docstring with typed args. aisuite runs the tool loop via `tools=` + `max_turns=`.
- Tools: Wikipedia (`wikipedia` package), Tavily web search (`TAVILY_API_KEY`, falls back to Wikipedia), calculator.
- Tests: pytest, must run fully offline (`--offline` mode uses `_mock_reply`). Run: `.venv/bin/python -m pytest -q`.
- Secrets live only in `.env` (template: `.env.example`). Never read, print or commit `.env`.
