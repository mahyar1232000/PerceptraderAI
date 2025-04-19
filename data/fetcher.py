# data/fetcher.py

import logging
from datetime import datetime
import pytz
import MetaTrader5 as mt5
import pandas as pd


def fetch_ohlcv(symbol: str, timeframe: int, start_date: datetime, count: int = 1000) -> pd.DataFrame:
    """
    Fetch OHLCV data from MetaTrader5 terminal.
    """
    timezone = pytz.timezone("Etc/UTC")
    utc_from = start_date.replace(tzinfo=timezone)
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, count)
    if rates is None:
        logging.error(f"Failed to fetch data for {symbol}: {mt5.last_error()}")
        return pd.DataFrame()
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df
