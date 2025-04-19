import logging
import MetaTrader5 as mt5

class TradeExecutor:
    """
    Executes orders via the MT5 Python API, handling market vs. pending order
    parameters to avoid 'Invalid "price" argument' errors.
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
        sl: float = None,
        tp: float = None,
        deviation: int = 20,
        magic: int = 234000,
        comment: str = "PerceptraderAI"
    ) -> dict:
        # Determine order action and type
        action = mt5.TRADE_ACTION_DEAL
        trade_type = mt5.ORDER_TYPE_BUY if side.lower() == "buy" else mt5.ORDER_TYPE_SELL

        # Build the request dict
        request = {
            "action": action,
            "symbol": symbol,
            "volume": float(quantity),              # ensure float :contentReference[oaicite:6]{index=6}
            "type": trade_type,
            "deviation": deviation,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        # For market orders, omit 'price'; if SL/TP provided, include them
        if order_type.lower() == "market":
            # If you need to reference the current price:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logging.error(f"Cannot retrieve tick for {symbol}: {mt5.last_error()}")
                raise RuntimeError(f"Tick retrieval failed: {mt5.last_error()}")
            # Optionally: request["price"] = tick.ask if trade_type == mt5.ORDER_TYPE_BUY else tick.bid
            if sl is not None:
                request["sl"] = float(sl)
            if tp is not None:
                request["tp"] = float(tp)
        else:
            # Pending orders require a valid price
            if price is None:
                raise ValueError("Limit orders require a 'price' argument.")
            request["price"] = float(price)

        # Send order
        result = mt5.order_send(request)
        if result is None:
            err = mt5.last_error()
            msg = f"OrderSend returned None, last_error={err}"
            logging.error(msg)
            raise RuntimeError(msg)

        ret = result.retcode

        # Handle specific MT5 retcodes
        if ret == mt5.TRADE_RETCODE_CLIENT_DISABLES_AT:
            msg = ("OrderSend failed (10027): AutoTrading disabled. "
                   "Enable the AutoTrading button in MT5.")  # :contentReference[oaicite:7]{index=7}
            logging.error(msg)
            raise RuntimeError(msg)

        if ret == mt5.TRADE_RETCODE_INVALID_PRICE:
            msg = "OrderSend failed (10015): Invalid price—check SL/TP and tick alignment."  # :contentReference[oaicite:8]{index=8}
            logging.error(msg)
            raise RuntimeError(msg)

        if ret != mt5.TRADE_RETCODE_DONE:
            last = mt5.last_error()
            err_msg = last[1] if last else "Unknown error"
            msg = f"OrderSend failed (retcode={ret}): {err_msg}"
            logging.error(msg)
            raise RuntimeError(msg)

        logging.info(f"OrderSend succeeded: {result}")
        return result._asdict()
