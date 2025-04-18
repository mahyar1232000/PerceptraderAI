# main.py

import logging
from prophet import Prophet  # Prophet 1.1.3 for Python 3.10+ :contentReference[oaicite:2]{index=2}
from config.settings import load_credentials  # Centralized config loader
from trade.mt5_connector import connect_to_mt5, shutdown_mt5  # MT5 API Connector
from data.fetcher import fetch_ohlcv  # OHLCV data fetcher
from data.preprocessor import clean_data, add_technical_indicators
from strategy.signal_generator import SignalGenerator
from strategy.risk_manager import RiskManager
from strategy.capital_manager import CapitalManager
from trade.executor import TradeExecutor


def main():
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    logger = logging.getLogger("PerceptraderAI")

    # Load credentials & connect to MT5
    creds = load_credentials()
    if not connect_to_mt5(**creds["mt5"]):
        logger.error("Failed MT5 login; aborting.")
        return

    try:
        # 1) Data ingestion and preprocessing
        raw = fetch_ohlcv(**creds["market_data"])
        df_clean = clean_data(raw)
        df_ind = add_technical_indicators(df_clean)

        # 2) Optional: Prophet forecast
        logger.info("Fitting Prophet model...")
        model = Prophet(**creds.get("prophet_params", {}))
        prophet_df = df_ind.reset_index().rename(columns={"time": "ds", "close": "y"})
        model.fit(prophet_df)
        future = model.make_future_dataframe(periods=creds["forecast_periods"])
        forecast = model.predict(future)
        logger.info("Prophet forecast (tail):\n%s", forecast[["ds", "yhat"]].tail())

        # 3) Signal generation
        sg = SignalGenerator(df_ind)
        sg.compute_indicators()
        sg.generate_signals()
        signals = sg.get_signals()
        logger.info("Generated signals:\n%s", signals.tail())

        # 4) Risk & capital management
        rm = RiskManager(account_balance=creds["account"]["balance"])
        cm = CapitalManager(total_capital=creds["account"]["balance"])

        # 5) Execute trades
        executor = TradeExecutor()
        for timestamp, row in signals.iterrows():
            signal_val = row.Signal if "Signal" in row else row
            if signal_val == 0:
                continue

            side = "buy" if signal_val > 0 else "sell"
            size = rm.calculate_position_size(
                stop_loss_pips=creds["sl_pips"],
                pip_value=creds["pip_value"]
            )
            allocation = cm.allocate_capital(trade_risk=size * creds["pip_value"])
            order = executor.execute_order(
                symbol=creds["symbol"],
                side=side,
                quantity=allocation,
                order_type="market"
            )
            logger.info("Executed %s at %s: %s", side.upper(), timestamp, order)

            # (Optional) Update PnL:
            # profit_loss = (row.close - row.open) * size if side == "buy" else (row.open - row.close) * size
            # rm.update_account_balance(profit_loss)
            # cm.update_total_capital(profit_loss)

    finally:
        shutdown_mt5()
        logger.info("MT5 connection closed.")


if __name__ == "__main__":
    main()
