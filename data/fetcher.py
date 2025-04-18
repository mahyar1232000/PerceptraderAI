# data/fetcher.py

import logging
from datetime import datetime
import pytz
import MetaTrader5 as mt5
import pandas as pd


def fetch_ohlcv(symbol: str, timeframe: int, start_date: datetime, count: int = 1000) -> pd.DataFrame:
    """
    دریافت داده‌های OHLCV از ترمینال MetaTrader5.
    از متد mt5.copy_rates_from برای دریافت داده مطابق مستندات رسمی استفاده می‌کند. :contentReference[oaicite:6]{index=6}
    """
    timezone = pytz.timezone("Etc/UTC")
    utc_from = start_date.replace(tzinfo=timezone)
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, count)
    if rates is None:
        logging.error(f"Failed to fetch data for {symbol}: {mt5.last_error()}")
        return pd.DataFrame()
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'],
                                unit='s')  # تبدیل زمان از ثانیه به datetime :contentReference[oaicite:7]{index=7}
    df.set_index('time', inplace=True)
    return df
