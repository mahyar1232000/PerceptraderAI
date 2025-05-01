import random
from typing import Any, Dict

import pandas as pd

from perceptrader.config.settings import settings
from perceptrader.environment import TradingEnv


class Optimizer:
    """Genetic-algorithm–based strategy optimizer."""

    def __init__(self, base_params: Dict[str, Any]):
        self.base = base_params
        self.pop_size = settings.OPTIMIZATION_PARAMS["population_size"]
        self.generations = settings.OPTIMIZATION_PARAMS["generations"]

    def _mutate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply small random perturbations to parameters."""
        mutated = params.copy()
        for key, value in params.items():
            if isinstance(value, (int, float)):
                noise = random.uniform(-0.1, 0.1) * value
                mutated[key] = type(value)(max(0, value + noise))
        return mutated

    def optimize(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run the genetic algorithm and return the best-found parameters."""
        population = [self._mutate_params(self.base) for _ in range(self.pop_size)]
        best_score = float("-inf")
        best_params = self.base

        for _ in range(self.generations):
            scores = []
            for params in population:
                env = TradingEnv(df, window=params.get("window", 50))
                # TODO: replace with real backtest/run
                score = 0.0  # placeholder for Sharpe or PnL metric
                scores.append((score, params))

            scores.sort(key=lambda x: x[0], reverse=True)
            top_score, top_params = scores[0]
            if top_score > best_score:
                best_score, best_params = top_score, top_params

            # breed next generation
            population = [
                self._mutate_params(random.choice(scores[: max(1, self.pop_size // 2)])[1])
                for _ in range(self.pop_size)
            ]

        return best_params
