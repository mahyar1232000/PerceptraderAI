"""
Base classes for live and paper trading.
"""

from abc import ABC, abstractmethod


class BaseExecution(ABC):
    """Common interface for trading execution loops."""

    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe

    @abstractmethod
    def run(self, **kwargs) -> bool:
        """
        Run the execution loop.
        Return True if successful (e.g., live started), False to abort.
        """
        ...
