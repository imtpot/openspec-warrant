import pytest

from warrant_evals import judge


@pytest.fixture(autouse=True)
def judge_off(monkeypatch):
    """No test calls the model judge unless it swaps in its own."""
    monkeypatch.setattr(judge, 'ask', lambda description, text: ('no', 'judge off in tests'))
