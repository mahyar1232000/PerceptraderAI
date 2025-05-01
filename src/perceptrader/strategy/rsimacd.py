"""
RSI + MACD Crossover Strategy.
"""

from typing import Dict

import pandas as pd

from perceptrader.strategy.base import StrategyBase


class RsiMacdStrategy(StrategyBase):
    """Simple strategy combining RSI thresholds and MACD crossovers."""

    def __init__(self, params: Dict[str, int]) -> None:
        super().__init__(params)
        self.rsi_lower = params.get("rsi_lower", 30)
        self.rsi_upper = params.get("rsi_upper", 70)

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        rsi = df["rsi"]
        macd = df["macd"]
        macd_signal = df["macd_signal"]

        buy = (rsi < self.rsi_lower) & (macd > macd_signal)
        sell = (rsi > self.rsi_upper) & (macd < macd_signal)

        signal = pd.Series(0, index=df.index, dtype=int)
        signal[buy] = 1
        signal[sell] = -1
        return signal

    def name(self) -> str:
        return "rsimacd"
