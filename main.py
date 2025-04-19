if __name__ == '__main__':
    from datetime import datetime
    from config.settings import load_credentials
    from trade.mt5_connector import connect_to_mt5, shutdown_mt5  # Module 'shutdown_mt5' not found
    from trade.executor import TradeExecutor
    from data.fetcher import fetch_ohlcv
    from data.preprocessor import clean_data, add_technical_indicators
    from strategy.signal_generator import SignalGenerator
    from strategy.risk_manager import RiskManager
    from strategy.capital_manager import CapitalManager

    creds = load_credentials()
    from trade.algorithmic_trading import AlgorithmicTrader
    trader = AlgorithmicTrader(assets=['EURUSD_o','USDJPY_o'])
    trader.run(
        creds=creds,
        symbols=['EURUSD_o','USDJPY_o'],
        start_date=datetime.utcnow(),
        timeframe=60,
        count=500
    )

    # (Optional) Launch GUI:
    # from gui.interface import TradingInterface
    # import tkinter as tk
    # root = tk.Tk()
    # app = TradingInterface(root)
    # root.mainloop()
