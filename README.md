# Sample project: Research Agent

A small agent built from the patterns in DeepLearning.AI's *Agentic AI* course:

```
topic → PLAN (sub-questions) → RESEARCH (tool use: Wikipedia, Tavily web search, calculator)
      → DRAFT → REFLECT (critic) → REVISE → outputs/<date>-<topic>.md
```

| File | Purpose |
|---|---|
| `agent.py` | the pipeline; `LLM` wrapper over **aisuite** (swap providers by model id) |
| `tools.py` | plain functions exposed as tools (aisuite builds schemas from docstrings) |
| `demo.ipynb` | step-by-step walkthrough to run in Jupyter / PyCharm |
| `tests/` | pytest, runs fully offline |

## Run
```bash
source ../../.venv/bin/activate
python agent.py --offline "anything"                 # no keys: proves the wiring
python agent.py "How do solid-state batteries work?"  # real run: needs ANTHROPIC_API_KEY
python agent.py --model openai:gpt-4o "..."           # other provider
pytest -q
```
Set `AGENT_MODEL` in `../../.env` to change the default model. `web_search` needs `TAVILY_API_KEY`;
without it the agent falls back to Wikipedia.

## Ideas to extend (maps to course modules)
- M2: add a chart-generation step with a reflection loop on the chart code
- M4: score each stage (e.g. are sources cited?) and log results
- M5: split into planner / researcher / writer agents that pass messages
