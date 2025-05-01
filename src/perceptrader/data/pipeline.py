"""
Pipeline orchestration for fetching and preprocessing data.
"""

from pathlib import Path
from typing import List

import pandas as pd

from perceptrader.data.fetch import HistoricalFetcher, RealtimeFetcher
from perceptrader.utils.fetch import add_indicators
from perceptrader.config.settings import settings


class DataPipeline:
    """Orchestrates full data retrieval and preprocessing."""

    def __init__(self, symbols: List[str], timeframes: List[str]):
        self.symbols = symbols
        self.timeframes = timeframes
        self.cache_dir = Path("data/raw")
        self.processed_dir = Path("data/processed")
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """Fetch raw data, apply indicators, and save processed CSVs."""
        for symbol in self.symbols:
            for tf in self.timeframes:
                hist = HistoricalFetcher(symbol, tf, self.cache_dir)
                df = hist.fetch()
                df_ind = add_indicators(df)
                out_file = self.processed_dir / f"{symbol}_{tf}.csv"
                df_ind.to_csv(out_file)
