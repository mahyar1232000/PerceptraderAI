# trade/executor.py

import logging
import MetaTrader5 as mt5


class TradeExecutor:
    """
    اجرای سفارش‌ها از طریق API رسمی MetaTrader5.
    """

    def __init__(self):
        logging.info("TradeExecutor initialized.")

    def execute_order(self, symbol: str, side: str, quantity: float,
                      order_type: str = 'market', price: float = None) -> dict:
        """
        ارسال سفارش معاملاتی (market/limit) به MetaTrader5.
        """
        # انتخاب نوع سفارش بر اساس جهت
        type_map = {
            'buy': mt5.ORDER_TYPE_BUY,
            'sell': mt5.ORDER_TYPE_SELL
        }

        # تعیین قیمت برای اردر مارکت در صورت عدم ارائه price
        tick = mt5.symbol_info_tick(symbol)
        if price is None:
            price = tick.ask if side.lower() == 'buy' else tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": quantity,
            "type": type_map.get(side.lower()),
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "PerceptraderAI",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"OrderSend failed, retcode={result.retcode}")
        else:
            logging.info(f"OrderSend succeeded: {result}")
        return result._asdict()
