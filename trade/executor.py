import logging
import MetaTrader5 as mt5


class TradeExecutor:
    """
    Executes trade orders via the MetaTrader5 Python API,
    with detailed handling of common error codes.
    """

    def __init__(self):
        logging.info("TradeExecutor initialized.")

    def execute_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "market",
        price: float = None,
        deviation: int = 20,
        magic: int = 234000,
        comment: str = "PerceptraderAI"
    ) -> dict:
        """
        Sends an order to the MT5 terminal and handles retcodes, especially 10027.

        :param symbol: Trading instrument (e.g., "EURUSD")
        :param side: "buy" or "sell"
        :param quantity: Volume in lots
        :param order_type: 'market' or 'limit'
        :param price: Price for limit orders
        :param deviation: Max slippage
        :param magic: Expert Advisor identifier
        :param comment: Order comment
        :return: MqlTradeResult fields as dict
        """
        # Prepare the request dictionary according to MT5 Python API :contentReference[oaicite:0]{index=0}
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": quantity,
            "type": mt5.ORDER_TYPE_BUY if side.lower() == "buy" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        # Send the order
        result = mt5.order_send(request)
        ret = result.retcode

        # Handle specific error 10027: auto‑trading disabled by client terminal :contentReference[oaicite:1]{index=1}
        if ret == mt5.TRADE_RETCODE_CLIENT_DISABLES_AT:
            msg = (
                "OrderSend failed (10027): AutoTrading disabled by client terminal. "
                "Please enable the AutoTrading button on the MT5 toolbar."
            )
            logging.error(msg)
            raise RuntimeError(msg)

        # Other common error codes you might want to catch:
        elif ret == mt5.TRADE_RETCODE_TRADE_DISABLED:
            msg = "OrderSend failed (10017): Trading is disabled on the server side."  # TRADE_RETCODE_TRADE_DISABLED=10017 :contentReference[oaicite:2]{index=2}
            logging.error(msg)
            raise RuntimeError(msg)

        elif ret == mt5.TRADE_RETCODE_MARKET_CLOSED:
            msg = "OrderSend failed (10018): Market is closed."  # :contentReference[oaicite:3]{index=3}
            logging.error(msg)
            raise RuntimeError(msg)

        elif ret == mt5.TRADE_RETCODE_NO_MONEY:
            msg = "OrderSend failed (10019): Not enough funds."  # :contentReference[oaicite:4]{index=4}
            logging.error(msg)
            raise RuntimeError(msg)

        elif ret != mt5.TRADE_RETCODE_DONE:
            # Generic catch-all for other retcodes
            msg = f"OrderSend failed (retcode={ret}): {mt5.last_error()[1]}"
            logging.error(msg)
            raise RuntimeError(msg)

        # Success case
        logging.info(f"OrderSend succeeded: {result}")
        return result._asdict()
