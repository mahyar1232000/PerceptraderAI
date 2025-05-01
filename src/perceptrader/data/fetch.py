"""
Data fetchers for historical OHLCV and real-time quotes.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests
import websocket

from perceptrader.config.settings import settings


class HistoricalFetcher:
    """Fetches historical OHLCV bars via MT5 and caches to CSV."""

    def __init__(self, symbol: str, timeframe: str, cache_dir: Path):
        self.symbol = symbol
        self.timeframe = timeframe
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / f"{symbol}_{timeframe}.csv"

    def fetch(self, start: str = None, end: str = None) -> pd.DataFrame:
        """
        Load from cache if present; otherwise, fetch via MT5 and save.
        `start`/`end` in 'YYYY-MM-DD' format.
        """
        if self.cache_file.exists():
            df = pd.read_csv(self.cache_file, parse_dates=["time"], index_col="time")
            return df

        # Placeholder: implement actual MT5 data pull here
        ohlcv = []  # list of dicts: time, open, high, low, close, volume
        # e.g., mt5.copy_rates_range(...)
        df = pd.DataFrame(ohlcv).set_index("time")
        df.to_csv(self.cache_file)
        return df


class RealtimeFetcher:
    """Streams real-time quotes via Intrinio WebSocket or REST."""

    WS_URL = "wss://api.intrinio.com/stream"

    def __init__(self, symbol: str, api_key: str = settings.BROKER_API_KEY):
        self.symbol = symbol
        self.api_key = api_key
        self.ws: websocket.WebSocketApp = None  # type: ignore

    def _on_message(self, ws, message: str) -> None:
        data: Dict = json.loads(message)
        # Process tick… e.g., send to a queue or callback
        # print(data)

    def start(self) -> None:
        """Open WebSocket and subscribe to the symbol."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        self.ws = websocket.WebSocketApp(
            self.WS_URL,
            header=headers,
            on_message=self._on_message,
        )
        self.ws.run_forever()

    def fetch_snapshot(self) -> Dict:
        """Fetch current quote via REST fallback."""
        url = f"https://api.intrinio.com/quotes/{self.symbol}"
        resp = requests.get(url, auth=(self.api_key, ""))
        resp.raise_for_status()
        return resp.json()
