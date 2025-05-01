import pytest

from perceptrader.live.base import BaseExecution
from perceptrader.live.paper import PaperExecution
from perceptrader.live.execution import LiveExecution


def test_base_execution_interface():
    assert hasattr(BaseExecution, "run")


def test_paper_execution_runs_quickly(monkeypatch):
    # Monkeypatch time.sleep to speed up
    import time
    monkeypatch.setattr(time, "sleep", lambda x: None)
    paper = PaperExecution("SYM", "M1")
    assert paper.run(duration=1) is True


@pytest.mark.skip(reason="Requires MT5 installation")
def test_live_execution_initialization():
    live = LiveExecution("EURUSD", "M1")
    assert live.symbol == "EURUSD"
