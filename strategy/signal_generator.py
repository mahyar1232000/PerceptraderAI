# strategy/signal_generator.py

import pandas as pd
import numpy as np
import logging


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
            df = self.raw['close'].resample(f"{tf}T").last().dropna()
            self.signals[f"ma{tf}"] = df.rolling(window=int(tf)).mean()
            # اضافه کردن RSI و دیگر اندیکاتورها...
        logging.info("Indicators computed for timeframes.")

    def generate_signals(self):
        """
        ترکیب سیگنال‌ها از همه تایم‌فریم‌ها.
        """
        combined = np.sign(self.signals.filter(like="ma").diff().sum(axis=1))
        self.signals["Signal"] = combined
        logging.info("Signals generated.")

    def get_signals(self) -> pd.DataFrame:
        return self.signals[["Signal"]]
