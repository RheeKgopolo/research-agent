"""Research agent: plan -> research with tools -> draft -> reflect -> revise.

Demonstrates three patterns from the DeepLearning.AI *Agentic AI* course:
planning, tool use, and reflection.

Run:
    python agent.py "How do heat pumps work in cold climates?"
    python agent.py --offline "any topic"     # no API keys needed (mock LLM)
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path

from dotenv import load_dotenv

from tools import TOOLS

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
load_dotenv(ENV_FILE)                                  # project .env (see .env.example)
if (HERE.parents[1] / "setup_env.sh").exists():        # running inside the Agentic workspace:
    load_dotenv(HERE.parents[1] / ".env")              # fall back to its shared .env
OUT_DIR = Path(__file__).parent / "outputs"
DEFAULT_MODEL = os.getenv("AGENT_MODEL", "anthropic:claude-sonnet-5-5")


# --------------------------------------------------------------------------- LLM
class LLM:
    """Thin wrapper so the same pipeline runs against aisuite or a mock."""

    def __init__(self, model: str = DEFAULT_MODEL, offline: bool = False):
        self.model, self.offline = model, offline
        if not offline:
            _require_key(model)
            import aisuite as ai
            self.client = ai.Client()

    def chat(self, system: str, user: str, tools=None, max_turns: int = 6) -> str:
        if self.offline:
            return _mock_reply(system, user)
        kwargs = dict(model=self.model,
                      messages=[{"role": "system", "content": system},
                                {"role": "user", "content": user}])
        if tools:
            kwargs.update(tools=tools, max_turns=max_turns)   # aisuite runs the tool loop
        resp = self.client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ""


KEY_FOR_PROVIDER = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "mistral": "MISTRAL_API_KEY",
}


def _require_key(model: str) -> None:
    """Stop early with a clear message if the provider's API key is missing."""
    provider = model.split(":", 1)[0]
    var = KEY_FOR_PROVIDER.get(provider)
    if var and not os.getenv(var, "").strip():
        raise SystemExit(
            f"\n{var} is not set, so '{model}' can't be called.\n"
            f"  1. Open {ENV_FILE}  (copy .env.example if it doesn't exist)\n"
            f"  2. Add your key:  {var}=...\n"
            f"  3. Run again.\n"
            f"Or run without a key:  python agent.py --offline \"your topic\""
        )


def _mock_reply(system: str, user: str) -> str:
    topic = re.search(r"TOPIC: (.*)", user)
    topic = topic.group(1) if topic else "the topic"
    if "planner" in system:
        return f"1. Define {topic}\n2. Key mechanisms\n3. Pros, cons and open questions"
    if "researcher" in system:
        from tools import calculator
        return f"[offline notes] 3 facts about {topic}. calculator('2*21') -> {calculator('2*21')}"
    if "critic" in system:
        return "- Add a concrete example\n- Cite sources inline"
    return f"# {topic}\n\n## Overview\nOffline draft about {topic}.\n\n## Sources\n- (offline mode)"


# ---------------------------------------------------------------------- pipeline
def plan(llm: LLM, topic: str) -> str:
    return llm.chat(
        "You are a research planner. Return 3-5 numbered sub-questions, nothing else.",
        f"TOPIC: {topic}")


def research(llm: LLM, topic: str, steps: str) -> str:
    return llm.chat(
        "You are a researcher. Use the tools to answer each sub-question. "
        "Return concise bullet notes with the source URL after each fact.",
        f"TOPIC: {topic}\nSUB-QUESTIONS:\n{steps}", tools=TOOLS)


def write(llm: LLM, topic: str, notes: str, feedback: str = "", draft: str = "") -> str:
    task = "Revise the draft using the feedback." if feedback else "Write the report."
    return llm.chat(
        "You are a technical writer. Produce a clear Markdown report (~400 words) "
        "with headings and a Sources section. Use only facts from the notes.",
        f"TOPIC: {topic}\nNOTES:\n{notes}\n\nDRAFT:\n{draft}\n\nFEEDBACK:\n{feedback}\n\n{task}")


def reflect(llm: LLM, topic: str, draft: str) -> str:
    return llm.chat(
        "You are a strict critic. List up to 5 specific, actionable improvements "
        "(accuracy, missing citations, clarity). Bullets only.",
        f"TOPIC: {topic}\nDRAFT:\n{draft}")


def run(topic: str, offline: bool = False, model: str = DEFAULT_MODEL, verbose: bool = True) -> Path:
    llm = LLM(model, offline)
    log = (lambda *a: print(*a, flush=True)) if verbose else (lambda *a: None)

    log(f"Model: {'mock (offline)' if offline else model}\n[1/5] Planning…")
    steps = plan(llm, topic)
    log(steps, "\n[2/5] Researching with tools…")
    notes = research(llm, topic, steps)
    log("[3/5] Drafting…")
    draft = write(llm, topic, notes)
    log("[4/5] Reflecting…")
    feedback = reflect(llm, topic, draft)
    log(feedback, "\n[5/5] Revising…")
    final = write(llm, topic, notes, feedback, draft)

    OUT_DIR.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:50] or "report"
    path = OUT_DIR / f"{dt.datetime.now():%Y%m%d-%H%M}-{slug}.md"
    path.write_text(final + "\n\n---\n## Research notes\n" + notes
                    + "\n\n## Critique applied\n" + feedback + "\n")
    log(f"Saved {path}")
    return path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("topic", nargs="?", help="research topic (you'll be asked if omitted)")
    p.add_argument("--offline", action="store_true", help="use a mock LLM (no API keys)")
    p.add_argument("--model", default=DEFAULT_MODEL, help="aisuite model id, e.g. openai:gpt-4o")
    a = p.parse_args()
    topic = a.topic
    if not topic:
        topic = input("Research topic: ").strip() or "How agentic AI workflows differ from single prompts"
    run(topic, offline=a.offline, model=a.model)
