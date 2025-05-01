# src/perceptrader/data/__init__.py

"""
Data subpackage for PerceptraderAI:
- fetch.py      : Central OHLCV data fetching logic
- pipeline.py   : Manages data fetching, preprocessing, and loading
- handlers/     : Future data source handlers
"""

from .fetch import HistoricalFetcher, RealtimeFetcher
from .pipeline import DataPipeline

__all__ = ["HistoricalFetcher", "RealtimeFetcher", "DataPipeline"]
