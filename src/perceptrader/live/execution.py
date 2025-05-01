"""
Live trading execution.
"""

import time

import MetaTrader5 as mt5
from perceptrader.config import settings
from perceptrader.live.base import BaseExecution
from perceptrader.utils.mt5_utils import calculate_lot_size
from perceptrader.utils.logger import setup_logger


class LiveExecution(BaseExecution):
    """Streams live ticks and places orders."""

    def __init__(self, symbol: str, timeframe: str) -> None:
        super().__init__(symbol, timeframe)
        mt5.initialize(path=settings.MT5_PATH)
        mt5.symbol_select(symbol, True)
        self.logger = setup_logger(f"live_{symbol}_{timeframe}")

    def run(self) -> None:
        self.logger.info(f"Starting live execution for {self.symbol}")
        while True:
            tick = mt5.symbol_info_tick(self.symbol)
            price = tick.ask
            # Placeholder: decision logic here
            # lot = calculate_lot_size(...)
            # mt5.order_send(...)
            time.sleep(1)
