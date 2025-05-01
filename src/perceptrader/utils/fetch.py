"""
Indicator engineering for dataframes.
"""

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    # avoid circular imports at runtime
    from pandas import DataFrame


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add RSI, EMA, MACD, and drop NaNs."""
    df_out = df.copy()

    # RSI
    delta = df_out["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    df_out["rsi"] = 100 - (100 / (1 + (gain / loss)))

    # EMA
    df_out["ema50"] = df_out["close"].ewm(span=50, adjust=False).mean()
    df_out["ema200"] = df_out["close"].ewm(span=200, adjust=False).mean()

    # MACD
    ema12 = df_out["close"].ewm(span=12, adjust=False).mean()
    ema26 = df_out["close"].ewm(span=26, adjust=False).mean()
    df_out["macd"] = ema12 - ema26
    df_out["macd_signal"] = df_out["macd"].ewm(span=9, adjust=False).mean()
    df_out["macd_hist"] = df_out["macd"] - df_out["macd_signal"]

    return df_out.dropna()
