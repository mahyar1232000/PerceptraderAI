import matplotlib.pyplot as plt
import pandas as pd
from typing import Sequence
import numpy as np


class Dashboard:
    """Matplotlib-based visualization for backtest results"""

    @staticmethod
    def plot_equity(timestamps: Sequence[pd.Timestamp], equity: Sequence[float]) -> None:
        # Convert pd.Timestamp to datetime.datetime for plotting
        timestamps_dt = [ts.to_pydatetime() for ts in timestamps]

        # Ensure timestamps_dt is a numpy array for compatibility with plt.plot
        timestamps_dt = np.array(timestamps_dt)

        plt.figure()
        plt.plot(timestamps_dt, equity,
                 label="Equity")  # Expected type 'float | _SupportsArray[dtype] | _NestedSequence[_SupportsArray[dtype]] | bool | int | complex | str | bytes | _NestedSequence[bool | int | float | complex | str | bytes]', got 'ndarray' instead   timestamps_dt: list[datetime] = [ts.to_pydatetime() for ts in timestamps]
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.title("Equity Curve")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_signals(data: pd.DataFrame, signals: Sequence[int]) -> None:
        plt.figure()
        plt.plot(data.index, data["close"], label="Price")
        buys = [i for i, s in enumerate(signals) if s > 0]
        sells = [i for i, s in enumerate(signals) if s < 0]
        plt.scatter(data.index[buys], data["close"].iloc[buys], marker="^", color="g", label="Buy")
        plt.scatter(data.index[sells], data["close"].iloc[sells], marker="v", color="r", label="Sell")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title("Trading Signals")
        plt.legend()
        plt.show()
