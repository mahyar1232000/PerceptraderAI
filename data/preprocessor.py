# data/preprocessor.py

import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    حذف ردیف‌های دارای مقادیر NaN و حجم صفر.
    از DataFrame.dropna برای حذف مقادیر گمشده استفاده می‌کند. :contentReference[oaicite:8]{index=8}
    """
    df = df.dropna()
    df = df[df['volume'] > 0]
    return df


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """
    محاسبه شاخص قدرت نسبی (RSI).
    """
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    افزودن میانگین متحرک و RSI.
    """
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma50'] = df['close'].rolling(window=50).mean()
    df['rsi'] = compute_rsi(df['close'], window=14)
    return df
