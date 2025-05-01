"""
Base Strategy interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd


class StrategyBase(ABC):
    """Abstract base class for trading strategies."""

    @abstractmethod
    def __init__(self, params: Dict[str, Any]) -> None:
        self.params = params

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Given a DataFrame with indicators, return a Series of
        signals: -1 (sell), 0 (hold), +1 (buy).
        """
        ...

    @abstractmethod
    def name(self) -> str:
        """Return a unique strategy name."""
        ...
