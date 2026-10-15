import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent import run          # noqa: E402
from tools import calculator   # noqa: E402


def test_calculator():
    assert calculator("(2+3)*4") == "20"
    assert "Only numbers" in calculator("__import__('os')")


def test_offline_pipeline(tmp_path, monkeypatch):
    import agent
    monkeypatch.setattr(agent, "OUT_DIR", tmp_path)
    out = run("test topic", offline=True, verbose=False)
    text = out.read_text()
    assert out.exists() and "# test topic" in text and "Critique applied" in text
