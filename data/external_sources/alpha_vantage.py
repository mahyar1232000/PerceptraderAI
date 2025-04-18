# data/external_sources/alpha_vantage.py

import logging
import requests
import pandas as pd


def fetch_alpha_vantage_data(symbol: str, interval: str, api_key: str) -> pd.DataFrame:
    """
    دریافت داده‌های FX_INTRADAY از Alpha Vantage.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": symbol[:3],
        "to_symbol": symbol[3:],
        "interval": interval,
        "apikey": api_key,
        "outputsize": "compact"
    }
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        key = f"Time Series FX ({interval})"
        if key not in data:
            logging.error(f"AlphaVantage key '{key}' missing in response")
            return pd.DataFrame()
        df = pd.DataFrame.from_dict(data[key], orient='index')
        df.columns = ['open', 'high', 'low', 'close']
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    except Exception as e:
        logging.error(f"AlphaVantage fetch error: {e}")
        return pd.DataFrame()
