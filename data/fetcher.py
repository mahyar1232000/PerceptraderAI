# data/fetcher.py (updated)

import logging
from datetime import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
from utils.timeframe_mapper import map_timeframe


def fetch_ohlcv(symbol: str, timeframe: int, start_date: datetime, count: int = 1000) -> pd.DataFrame:
    """
    Fetch OHLCV bars from MT5, with symbol & timeframe validation.
    """
    # Ensure terminal is connected
    if not mt5.initialize():
        logging.error(f"MT5 not initialized: {mt5.last_error()}")
        return pd.DataFrame()

    # Validate symbol
    info = mt5.symbol_info(symbol)
    if info is None:
        logging.error(f"Symbol {symbol} not found in Market Watch.")  # symbol missing
        return pd.DataFrame()
    if not info.visible:
        mt5.symbol_select(symbol, True)  # add to Market Watch
        logging.info(f"Symbol {symbol} selected in Market Watch.")

    # Map timeframe
    tf_enum = map_timeframe(timeframe)

    # Prepare UTC-based date
    timezone = pytz.timezone("Etc/UTC")
    utc_from = start_date.replace(tzinfo=timezone)

    # Fetch bars
    rates = mt5.copy_rates_from(symbol, tf_enum, utc_from, count)
    if rates is None:
        logging.error(
            f"Failed to fetch data for {symbol}: {mt5.last_error()}")  # still logs (-2, 'Invalid params') if truly invalid :contentReference[oaicite:3]{index=3}
        return pd.DataFrame()

    # Build DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df
