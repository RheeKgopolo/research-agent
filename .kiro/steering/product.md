# Product

Research Agent: a small learning project built from DeepLearning.AI's *Agentic AI* course.

- Input: a topic string from the CLI (`python agent.py "<topic>"`).
- Pipeline: PLAN (sub-questions) -> RESEARCH (tool use) -> DRAFT -> REFLECT (critic) -> REVISE.
- Output: a Markdown report in `outputs/<YYYYMMDD-HHMM>-<topic-slug>.md`.
- Audience: Rhee, learning agentic patterns to apply in AWS agentic solutions for clients.
- Goal of changes: teach one agentic pattern at a time (reflection, tool use, evaluation, multi-agent), keeping the code small and readable.
