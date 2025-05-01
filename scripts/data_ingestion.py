#!/usr/bin/env python3
import argparse
from datetime import datetime
import pandas as pd
from perceptrader.config import settings
from perceptrader.data import HistoricalFetcher, RealtimeFetcher, DataPipeline


def validate_data(df: pd.DataFrame, timeframe: str) -> bool:
    """Validate OHLCV data integrity"""
    timeframe_map = {
        "M1": "1T", "M5": "5T", "M15": "15T",
        "H1": "1H", "H4": "4H", "D1": "1D"
    }
    expected_freq = timeframe_map.get(timeframe, "1H")
    full_range = pd.date_range(df.index.min(), df.index.max(), freq=expected_freq)
    return full_range.difference(df.index).empty


def main():
    parser = argparse.ArgumentParser(description="Data ingestion pipeline")
    parser.add_argument("--symbols", nargs="+", default=settings.SYMBOLS)
    parser.add_argument("--timeframes", nargs="+", default=settings.TIMEFRAMES)
    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()
    fetcher = HistoricalFetcher()
    pipeline = DataPipeline()

    for symbol in args.symbols:
        for timeframe in args.timeframes:
            print(f"Ingesting {symbol} {timeframe} data...")
            df = fetcher.get_ohlcv(symbol, timeframe,
                                   pd.to_datetime(args.start),
                                   pd.to_datetime(args.end))
            if validate_data(df, timeframe):
                pipeline.cache_dataframe(symbol, timeframe, df)
                print(f"Successfully cached {symbol} {timeframe}")
            else:
                print(f"Validation failed for {symbol} {timeframe}")


if __name__ == "__main__":
    main()
