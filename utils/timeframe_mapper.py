# utils/timeframe_mapper.py

import MetaTrader5 as mt5

TF_MAP = {
    1: mt5.TIMEFRAME_M1,
    5: mt5.TIMEFRAME_M5,
    15: mt5.TIMEFRAME_M15,
    30: mt5.TIMEFRAME_M30,
    60: mt5.TIMEFRAME_H1,
    240: mt5.TIMEFRAME_H4,
    1440: mt5.TIMEFRAME_D1,
    # add more as needed...
}


def map_timeframe(tf_minutes: int) -> int:
    """
    Convert minute-based timeframe (e.g. 60) to MT5 TIMEFRAME enum.
    """
    if tf_minutes not in TF_MAP:
        raise ValueError(f"{tf_minutes} not a valid timeframe (minutes)")  # ensures no invalid params
    return TF_MAP[tf_minutes]
