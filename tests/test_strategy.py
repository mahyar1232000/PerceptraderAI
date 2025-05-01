import pandas as pd
import pytest

from perceptrader.strategy.factory import create_strategy
from perceptrader.strategy.rsimacd import RsiMacdStrategy
from perceptrader.strategy.deeprl import DeepRLStrategy


@pytest.fixture
def indicator_df():
    df = pd.DataFrame({
        "rsi": [20, 80, 40],
        "macd": [1, -1, 0],
        "macd_signal": [0.5, -0.5, 0],
    }, index=[0, 1, 2])
    return df


def test_rsimacd_signals(indicator_df):
    strat = RsiMacdStrategy({"rsi_lower": 30, "rsi_upper": 70})
    sig = strat.generate_signals(indicator_df)
    assert list(sig) == [1, -1, 0]


def test_strategy_factory_unknown():
    with pytest.raises(ValueError):
        create_strategy("unknown", {})


def test_factory_returns_correct_class(indicator_df):
    strat = create_strategy("rsimacd", {"rsi_lower": 10, "rsi_upper": 90})
    assert isinstance(strat, RsiMacdStrategy)
