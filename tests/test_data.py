import os
from pathlib import Path

import pandas as pd
import pytest

from perceptrader.data.fetch import HistoricalFetcher, RealtimeFetcher
from perceptrader.data.pipeline import DataPipeline


@pytest.fixture
def sample_df(tmp_path):
    df = pd.DataFrame({
        "time": pd.date_range("2021-01-01", periods=5, freq="D"),
        "open": [1, 2, 3, 4, 5],
        "high": [2, 3, 4, 5, 6],
        "low": [0, 1, 2, 3, 4],
        "close": [1.5, 2.5, 3.5, 4.5, 5.5],
        "volume": [10, 20, 30, 40, 50],
    })
    df.set_index("time", inplace=True)
    return df


def test_add_indicators(sample_df):
    from perceptrader.utils.fetch import add_indicators

    df_ind = add_indicators(sample_df)
    assert "rsi" in df_ind.columns
    assert "ema50" in df_ind.columns
    assert not df_ind.isnull().any().any()


def test_historical_fetcher_cache(tmp_path, sample_df, monkeypatch):
    cache_dir = tmp_path / "cache"
    fetcher = HistoricalFetcher("EURUSD", "M1", cache_dir)

    # Monkey-patch MT5 fetch to return sample_df on first call
    monkeypatch.setattr(fetcher, "fetch", lambda start=None, end=None: sample_df)
    df1 = fetcher.fetch()
    df2 = fetcher.fetch()
    assert isinstance(df1, pd.DataFrame)
    assert df1.equals(df2)


def test_data_pipeline(tmp_path, sample_df, monkeypatch):
    # Patch HistoricalFetcher.fetch and add_indicators
    monkeypatch.setattr(
        "perceptrader.data.fetch.HistoricalFetcher.fetch",
        lambda self: sample_df
    )
    monkeypatch.setattr(
        "perceptrader.utils.fetch.add_indicators",
        lambda df: df
    )

    dp = DataPipeline(["SYM"], ["M1"])
    dp.cache_dir = tmp_path / "raw"
    dp.processed_dir = tmp_path / "processed"
    dp.run()

    out_file = dp.processed_dir / "SYM_M1.csv"
    assert out_file.exists()
    df_out = pd.read_csv(out_file, index_col=0)
    assert not df_out.empty
