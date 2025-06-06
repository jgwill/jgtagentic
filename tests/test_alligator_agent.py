import sys
import os
import types
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jgtagentic import alligator_agent


def test_alligator_agent_placeholder(monkeypatch, capsys):
    monkeypatch.setattr(alligator_agent, "_ALLIGATOR_AVAILABLE", False)
    monkeypatch.setattr(alligator_agent, "alligator_cli", None)
    agent = alligator_agent.AlligatorAgent()
    agent.run(["-i", "SPX500", "-t", "D1", "-d", "B"])
    out = capsys.readouterr().out
    assert "Would run: alligator_cli.py" in out


def test_alligator_agent_invokes_real(monkeypatch):
    called = {}

    def dummy_main():
        called["ran"] = True

    monkeypatch.setattr(alligator_agent, "_ALLIGATOR_AVAILABLE", True)
    dummy_module = types.SimpleNamespace(main=dummy_main)
    monkeypatch.setattr(alligator_agent, "alligator_cli", dummy_module)

    agent = alligator_agent.AlligatorAgent()
    agent.run(["--help"])
    assert called.get("ran")
