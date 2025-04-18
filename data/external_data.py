# data/external_data.py

import requests
import pandas as pd
import logging


def fetch_alpha_vantage(symbol: str, interval: str, api_key: str) -> pd.DataFrame:
    url = "https://www.alphavantage.co/query"
    params = {"function": "TIME_SERIES_INTRADAY", "symbol": symbol, "interval": interval,
              "apikey": api_key, "outputsize": "compact"}
    r = requests.get(url, params=params)
    data = r.json().get(f"Time Series ({interval})", {})
    df = pd.DataFrame.from_dict(data, orient='index').astype(float)
    df.index = pd.to_datetime(df.index)
    return df


def fetch_finnhub(symbol: str, resolution: str, from_ts: int, to_ts: int, api_key: str) -> pd.DataFrame:
    url = "https://finnhub.io/api/v1/forex/candle"
    params = {"symbol": f"OANDA:{symbol}", "resolution": resolution, "from": from_ts,
              "to": to_ts, "token": api_key}
    r = requests.get(url, params=params).json()
    df = pd.DataFrame({
        "time": pd.to_datetime(r['t'], unit='s'),
        "open": r['o'], "high": r['h'], "low": r['l'], "close": r['c'], "volume": r['v']
    }).set_index("time")
    return df
