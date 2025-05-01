"""
Deep RL Strategy wrapper.
"""

from typing import Any, Dict

import numpy as np
import pandas as pd

from perceptrader.strategy.base import StrategyBase
from perceptrader.models.rl import RLAgent


class DeepRLStrategy(StrategyBase):
    """Uses a pretrained RL agent to generate actions."""

    def __init__(self, params: Dict[str, Any]) -> None:
        super().__init__(params)
        model_path = params["model_path"]
        self.agent = RLAgent.load(model_path)

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        obs = df[["close", "volume", "rsi", "macd", "macd_signal"]].values
        actions = self.agent.predict(obs)  # returns 0,1,2
        # map 0->-1, 1->0, 2->+1
        mapping = {0: -1, 1: 0, 2: 1}
        signals = np.vectorize(mapping.get)(actions)
        return pd.Series(signals, index=df.index, dtype=int)

    def name(self) -> str:
        return "deeprl"
