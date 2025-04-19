import logging
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

from data.fetcher import fetch_ohlcv
from data.preprocessor import clean_data, add_technical_indicators
from strategy.signal_generator import SignalGenerator
from strategy.risk_manager import RiskManager
from strategy.capital_manager import CapitalManager
from trade.executor import TradeExecutor
from trade.multi_asset_support import MultiAssetManager
from trade.mt5_connector import connect_to_mt5, shutdown_mt5
from utils.timeframe_mapper import map_timeframe


class AlgorithmicTrader:
    """
    Integrates data fetching, signal generation, risk & capital management,
    and order execution via MetaTrader5.
    """

    def __init__(self, assets: list[str]):
        self.assets = assets
        self.mm = MultiAssetManager(assets)
        self.executor = TradeExecutor()

    def run(
        self,
        creds: dict,
        symbols: list[str],
        start_date: datetime,
        timeframe: int,
        count: int = 1000
    ) -> None:
        # Convert minute-based timeframe to MT5 constant
        try:
            tf_enum = map_timeframe(timeframe)
        except ValueError as e:
            logging.error(f"Timeframe mapping error: {e}")
            return

        # Connect to MT5 terminal and log in
        if not connect_to_mt5(
            creds['mt5']['login'], creds['mt5']['password'],
            creds['mt5']['server'], creds['mt5']['terminal_path']
        ):
            return

        try:
            for symbol in symbols:
                if not self.mm.is_supported(symbol):
                    continue

                # Fetch & validate OHLCV data
                df = fetch_ohlcv(symbol, tf_enum, start_date, count)
                if df.empty or 'close' not in df.columns:
                    logging.warning(f"No valid OHLCV for {symbol}, skipping.")
                    continue

                # Preprocess data
                df = clean_data(df)
                df = add_technical_indicators(df)

                # Generate trading signals
                sg = SignalGenerator(df, timeframes=[timeframe])
                sg.compute_indicators()
                sg.generate_signals()
                signals = sg.get_signals()

                # Initialize managers
                rm = RiskManager(
                    creds['mt5']['account']['balance'],
                    var_conf=creds['mt5'].get('var_conf', 0.95),
                    cvar_conf=creds['mt5'].get('cvar_conf', 0.95)
                )
                cm = CapitalManager(
                    creds['mt5']['account']['balance'],
                    max_alloc_per_trade=creds['mt5'].get('max_alloc_per_trade', 0.05)
                )

                # Execute trades
                for timestamp, row in signals.iterrows():
                    if row.Signal == 0:
                        continue
                    side = 'buy' if row.Signal > 0 else 'sell'
                    size = rm.calculate_position_size(
                        creds['mt5']['sl_pips'], creds['mt5']['pip_value']
                    )
                    allocation = cm.allocate(size * creds['mt5']['pip_value'])
                    order = self.executor.execute_order(
                        symbol=symbol,
                        side=side,
                        quantity=allocation
                    )
                    logging.info(f"Algo trade for {symbol} at {timestamp}: {order}")
        finally:
            shutdown_mt5()
