"""
Strategy factory to instantiate by name.
"""

from typing import Dict

from perceptrader.strategy.rsimacd import RsiMacdStrategy
from perceptrader.strategy.deeprl import DeepRLStrategy

_STRATEGIES = {
    "rsimacd": RsiMacdStrategy,
    "deeprl": DeepRLStrategy,
}


def create_strategy(name: str, params: Dict) -> RsiMacdStrategy:
    """Instantiate a strategy by its name."""
    cls = _STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy '{name}'")
    return cls(params)
