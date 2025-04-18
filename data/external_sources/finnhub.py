# data/external_sources/finnhub.py

import logging
import time
import requests
import pandas as pd


def fetch_finnhub_data(symbol: str, resolution: str, from_date: pd.Timestamp,
                       to_date: pd.Timestamp, api_key: str) -> pd.DataFrame:
    """
    دریافت داده‌های شمعی از Finnhub (Forex).
    """
    url = "https://finnhub.io/api/v1/forex/candle"
    params = {
        "symbol": f"OANDA:{symbol}",
        "resolution": resolution,
        "from": int(time.mktime(from_date.timetuple())),
        "to": int(time.mktime(to_date.timetuple())),
        "token": api_key
    }
    try:
        resp = requests.get(url, params=params).json()
        if resp.get('s') != 'ok':
            logging.error(f"Finnhub status: {resp.get('s')}")
            return pd.DataFrame()
        df = pd.DataFrame({
            'time': pd.to_datetime(resp['t'], unit='s'),
            'open': resp['o'],
            'high': resp['h'],
            'low': resp['l'],
            'close': resp['c'],
            'volume': resp['v']
        })
        return df.set_index('time')
    except Exception as e:
        logging.error(f"Finnhub fetch error: {e}")
        return pd.DataFrame()
