import logging
import MetaTrader5 as mt5


class TradeExecutor:
    """
    Executes trade orders via the MetaTrader5 Python API,
    with robust handling for cases where order_send returns None.
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
        Sends an order to the MT5 terminal and handles the case where
        mt5.order_send unexpectedly returns None (instead of a trade result).

        Raises RuntimeError with the MT5 last_error() message if no result.
        """
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

        result = mt5.order_send(request)
        if result is None:
            # mt5.order_send can return None when the request dict is invalid or other internal errors occur :contentReference[oaicite:0]{index=0}
            err = mt5.last_error()
            msg = f"OrderSend returned None, last_error={err}"
            logging.error(msg)
            raise RuntimeError(msg)

        ret = result.retcode

        # Existing error handling (e.g., client disables AutoTrading)
        if ret == mt5.TRADE_RETCODE_CLIENT_DISABLES_AT:
            msg = ("OrderSend failed (10027): AutoTrading disabled by client terminal. "
                   "Please enable the AutoTrading button on the MT5 toolbar.")
            logging.error(msg)
            raise RuntimeError(msg)

        # Other retcode checks...
        if ret != mt5.TRADE_RETCODE_DONE:
            err_msg = mt5.last_error()[1] if mt5.last_error() else "Unknown error"
            msg = f"OrderSend failed (retcode={ret}): {err_msg}"
            logging.error(msg)
            raise RuntimeError(msg)

        logging.info(f"OrderSend succeeded: {result}")
        return result._asdict()
