# Structure

- `agent.py` - `LLM` wrapper, one function per pipeline stage (`plan`, `research`, `write`, `reflect`) and `run()` orchestration + CLI.
- `tools.py` - tool functions only; no LLM calls here.
- `tests/test_agent.py` - offline tests; new behaviour gets a test here.
- `demo.ipynb` - walkthrough notebook; keep it in sync when stage signatures change.
- `outputs/` - generated reports (git-ignored except `.gitkeep`).

Conventions: new pipeline stage = new top-level function taking `llm: LLM` first, called from `run()`. Keep each file small; prefer adding a new module over growing `agent.py` past ~250 lines.
