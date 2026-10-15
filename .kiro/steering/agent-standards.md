---
inclusion: fileMatch
fileMatchPattern: ["**/*.py"]
---
# Agent code standards

- Every new tool: docstring with purpose, each arg, return value; returns a string; never raises on bad input (return an error message instead).
- Every LLM-calling stage must work in `--offline` mode (extend `_mock_reply` if needed).
- Every change adds or updates an offline pytest.
- Prompts live as module-level constants or in the stage function, not scattered inline.
- Reference: #[[file:agent.py]]
