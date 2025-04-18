import pandas as pd
import numpy as np
import logging
from data.preprocessor import compute_rsi


class SignalGenerator:
    """
    تولید سیگنال با تحلیل چند تایم‌فریم.
    """

    def __init__(self, data: pd.DataFrame, timeframes: list[int]):
        self.raw = data
        self.timeframes = timeframes
        self.signals = pd.DataFrame(index=data.index)

    def compute_indicators(self):
        """
        افزودن اندیکاتورهای MA و RSI برای هر تایم‌فریم.
        """
        for tf in self.timeframes:
            # Resample close price to timeframe tf in minutes
            df_res = self.raw['close'].resample(f"{tf}T").last().dropna()
            self.signals[f"ma{tf}"] = df_res.rolling(window=int(tf)).mean()
            self.signals[f"rsi{tf}"] = compute_rsi(df_res, window=14)
        logging.info("Indicators computed for timeframes.")

    def generate_signals(self):
        """
        ترکیب سیگنال‌ها از همه تایم‌فریم‌ها.
        """
        # Sum differences of all MA series and take sign
        ma_cols = [c for c in self.signals.columns if c.startswith('ma')]
        combined = np.sign(self.signals[ma_cols].diff().sum(axis=1))
        self.signals['Signal'] = combined
        logging.info("Signals generated.")

    def get_signals(self) -> pd.DataFrame:
        return self.signals[['Signal']]
