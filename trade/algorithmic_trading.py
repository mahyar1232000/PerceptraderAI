# trade/algorithmic_trading.py

import logging
from trade.executor import TradeExecutor
from strategy.signal_generator import SignalGenerator
from strategy.risk_manager import RiskManager
from strategy.capital_manager import CapitalManager
from trade.multi_asset_support import MultiAssetManager


class AlgorithmicTrader:
    """
    ادغام استراتژی‌های معاملاتی الگوریتمی با ماژول‌های سیگنال، ریسک و اجرای سفارش.
    """

    def __init__(self, assets: list[str]):
        self.multi_asset = MultiAssetManager(assets)
        self.executor = TradeExecutor()
        logging.info("AlgorithmicTrader initialized.")

    def run(self, data, timeframes, creds):
        """
        اجرای کل فرآیند: تولید سیگنال → مدیریت ریسک → تخصیص سرمایه → ارسال سفارش.
        """
        sg = SignalGenerator(data, timeframes)
        sg.compute_indicators()
        sg.generate_signals()
        signals = sg.get_signals()

        rm = RiskManager(account_balance=creds['account']['balance'])
        cm = CapitalManager(total_capital=creds['account']['balance'])

        for timestamp, row in signals.iterrows():
            symbol = creds['market_data']['symbol']
            if not self.multi_asset.is_supported(symbol):
                continue

            signal = row.Signal
            if signal == 0:
                continue

            side = "buy" if signal > 0 else "sell"
            size = rm.calculate_position_size(creds['sl_pips'], creds['pip_value'])
            allocation = cm.allocate(size * creds['pip_value'])
            order = self.executor.execute_order(
                symbol=symbol,
                side=side,
                quantity=allocation
            )
            logging.info(f"Algorithmic trade: {order}")
