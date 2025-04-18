# trade/high_frequency_trading.py

import logging
import time
from trade.executor import TradeExecutor
from strategy.signal_generator import SignalGenerator


class HighFrequencyTrader:
    """
    اجرای معاملات با فرکانس بالا در چرخۀ پیوسته.
    """

    def __init__(self, data_feed, timeframes):
        self.data_feed = data_feed
        self.timeframes = timeframes
        self.executor = TradeExecutor()
        logging.info("HighFrequencyTrader initialized.")

    def run(self):
        """
        حلقۀ اصلی HFT: خواندن دادهٔ زنده → تولید سیگنال → ارسال سفارش → تأخیر کوتاه.
        """
        while True:
            data = self.data_feed.get_latest_data()
            sg = SignalGenerator(data, self.timeframes)
            sg.compute_indicators()
            sg.generate_signals()
            signals = sg.get_signals()

            for timestamp, row in signals.iterrows():
                signal = row.Signal
                if signal == 0:
                    continue
                side = "buy" if signal > 0 else "sell"
                alloc = 0.01  # حجم ثابت HFT یا برحسب استراتژی
                order = self.executor.execute_order(
                    symbol=row.name,  # یا نماد از data_feed
                    side=side,
                    quantity=alloc
                )
                logging.info(f"HFT order: {order}")
            time.sleep(0.01)
