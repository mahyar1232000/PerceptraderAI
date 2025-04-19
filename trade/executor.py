import logging
import MetaTrader5 as mt5
from datetime import datetime, timedelta, time as dt_time
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


class TradeExecutor:
    """
    Robust MT5 trade executor with proper time handling and market checks
    """

    def __init__(self):
        """Initialize MT5 connection"""
        if not mt5.initialize():
            raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")
        logging.info("TradeExecutor ready (MT5 %s)", mt5.version())

    @staticmethod
    def execute_order(
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
        """Execute order with full validation"""
        # Market state check
        if order_type.lower() == "market":
            is_open, status = TradeExecutor.check_market_open(symbol)
            if not is_open:
                raise RuntimeError(f"Market closed: {status}")

        # Order preparation
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            raise RuntimeError(f"Symbol error: {mt5.last_error()}")

        try:
            filling_mode = TradeExecutor.get_filling_mode(symbol_info)
            action, order_type_mt5 = TradeExecutor.map_order_type(order_type, side)

            request = {
                "action": action,
                "symbol": symbol,
                "volume": round(float(quantity), 2),
                "type": order_type_mt5,
                "deviation": deviation,
                "magic": magic,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": filling_mode,
            }

            # Add conditional parameters
            if order_type != "market":
                if price is None:
                    raise ValueError("Pending orders require price")
                request["price"] = round(float(price), symbol_info.digits)

            if sl is not None:
                request["sl"] = round(float(sl), symbol_info.digits)
            if tp is not None:
                request["tp"] = round(float(tp), symbol_info.digits)

            # Execute and validate
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                TradeExecutor.handle_order_error(result.retcode, symbol)

            logging.info("Order executed: Ticket=%s", result.order)
            return result._asdict()

        except Exception as e:
            logging.error("Execution failed: %s", str(e), exc_info=True)
            raise

    @staticmethod
    def check_market_open(symbol: str) -> Tuple[bool, str]:
        """Comprehensive market status check"""
        try:
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return False, "Symbol unavailable"

            # Convert MT5 timestamp to datetime
            server_time = datetime.fromtimestamp(symbol_info.time)
            logging.debug("Server time: %s", server_time)

            # Basic market checks
            if symbol_info.trade_mode != mt5.SYMBOL_TRADE_MODE_FULL:
                return False, "Trading restricted"
            if symbol_info.bid == 0 or symbol_info.ask == 0:
                return False, "No market prices"

            # Session-based check
            if hasattr(symbol_info, 'sessions') and symbol_info.sessions:
                return TradeExecutor._check_sessions(server_time, symbol_info.sessions)

            # Fallback to heuristic check
            return TradeExecutor._fallback_check(server_time)

        except Exception as e:
            logging.error("Market check error: %s", str(e), exc_info=True)
            return False, "Status unknown"

    @staticmethod
    def _check_sessions(server_time: datetime, sessions: list) -> Tuple[bool, str]:
        """Check market sessions"""
        current_day = server_time.weekday()  # 0=Monday
        current_time = server_time.time()

        try:
            day_sessions = sessions[current_day]
            for i in range(0, len(day_sessions), 2):
                start, end = day_sessions[i], day_sessions[i + 1]
                if start == 0 and end == 0:
                    continue

                # Convert session seconds to time objects
                start_time = dt_time(start // 3600, (start % 3600) // 60)
                end_time = dt_time(end // 3600, (end % 3600) // 60)

                # Check time window
                if (start_time <= current_time < end_time) if start_time < end_time else \
                        (current_time >= start_time or current_time < end_time):
                    return True, "Market open"

            # Find next opening
            next_open = TradeExecutor._find_next_opening(server_time, sessions)
            if next_open:
                delta = next_open - server_time
                h, m = divmod(delta.seconds // 60, 60)
                return False, f"Opens in {h}h {m}m"

            return False, "No upcoming sessions"

        except IndexError:
            return True, "No session data"

    @staticmethod
    def _find_next_opening(current_dt: datetime, sessions: list) -> Optional[datetime]:
        """Find next valid market opening"""
        for day_offset in range(1, 8):
            check_date = current_dt + timedelta(days=day_offset)
            day_idx = check_date.weekday()

            try:
                day_sessions = sessions[day_idx]
                for i in range(0, len(day_sessions), 2):
                    start = day_sessions[i]
                    if start == 0:
                        continue

                    # Calculate start time
                    start_time = dt_time(start // 3600, (start % 3600) // 60)
                    candidate = datetime.combine(check_date.date(), start_time)

                    if candidate > current_dt:
                        return candidate
            except IndexError:
                continue
        return None

    @staticmethod
    def _fallback_check(server_time: datetime) -> Tuple[bool, str]:
        """Fallback market check"""
        try:
            # Weekend check (FX markets)
            if server_time.weekday() >= 5:  # Saturday(5) or Sunday(6)
                days_to_open = 7 - server_time.weekday()
                next_open = server_time + timedelta(days=days_to_open)
                next_open = next_open.replace(hour=17, minute=0, second=0)  # Sunday 5pm EST
                delta = next_open - server_time
                h, m = divmod(delta.seconds // 60, 60)
                return False, f"Weekend closure ({h}h {m}m)"

            # Daily maintenance break (2-3 AM)
            if dt_time(2, 0) <= server_time.time() < dt_time(3, 0):
                return False, "Daily maintenance (opens 03:00)"

            return True, "Market assumed open"

        except Exception as e:
            logging.error("Fallback check failed: %s", str(e))
            return True, "Market open (fallback error)"

    @staticmethod
    def get_filling_mode(symbol_info) -> int:
        """Proper filling mode detection"""
        allowed = symbol_info.filling_mode
        logging.debug("Filling modes: %s (%s)", allowed, bin(allowed))

        # MT5 Python API constants
        MT5_FOK = 1
        MT5_IOC = 2
        MT5_RETURN = 3

        # Priority: FOK -> IOC -> RETURN
        if allowed & 0b001:  # SYMBOL_FILLING_FOK
            return MT5_FOK
        if allowed & 0b010:  # SYMBOL_FILLING_IOC
            return MT5_IOC
        if allowed & 0b100:  # SYMBOL_FILLING_BOC
            return MT5_RETURN

        raise RuntimeError(f"No valid filling mode for {symbol_info.name}")

    @staticmethod
    def map_order_type(order_type: str, side: str) -> Tuple[int, int]:
        """Order type mapping"""
        order_type = order_type.lower()
        side = side.lower()

        mapping = {
            'market': {
                'buy': (mt5.TRADE_ACTION_DEAL, mt5.ORDER_TYPE_BUY),
                'sell': (mt5.TRADE_ACTION_DEAL, mt5.ORDER_TYPE_SELL)
            },
            'limit': {
                'buy': (mt5.TRADE_ACTION_PENDING, mt5.ORDER_TYPE_BUY_LIMIT),
                'sell': (mt5.TRADE_ACTION_PENDING, mt5.ORDER_TYPE_SELL_LIMIT)
            },
            'stop': {
                'buy': (mt5.TRADE_ACTION_PENDING, mt5.ORDER_TYPE_BUY_STOP),
                'sell': (mt5.TRADE_ACTION_PENDING, mt5.ORDER_TYPE_SELL_STOP)
            }
        }

        try:
            return mapping[order_type][side]
        except KeyError:
            raise ValueError(f"Invalid order type/side: {order_type}/{side}")

    @staticmethod
    def handle_order_error(retcode: int, symbol: str):
        """Error handling with clear instructions"""
        errors = {
            mt5.TRADE_RETCODE_INVALID_FILL: (
                f"Adjust {symbol} Fill Policy:\n"
                "1. Right-click symbol in Market Watch\n"
                "2. Select 'Specification'\n"
                "3. Enable FOK/IOC/BOC modes"
            ),
            mt5.TRADE_RETCODE_LIMIT_VOLUME: (
                f"Volume too small for {symbol}\n"
                f"Min: {mt5.symbol_info(symbol).volume_min}"
            ),
            mt5.TRADE_RETCODE_CLIENT_DISABLES_AT: (
                "Enable Algo Trading:\n"
                "MT5 -> Tools -> Options -> Trading -> Allow Algo Trading"
            )
        }
        msg = errors.get(retcode, f"Error {retcode}: {mt5.last_error()}")
        raise RuntimeError(msg)

    def __del__(self):
        """Cleanup"""
        mt5.shutdown()
        logging.info("MT5 disconnected")


# Usage Example
if __name__ == "__main__":
    try:
        executor = TradeExecutor()

        # Check market status
        symbol = "EURUSD_o"
        is_open, reason = executor.check_market_open(symbol)
        print(f"{symbol} Open: {is_open} - {reason}")

        # Execute sample order
        if is_open:
            result = executor.execute_order(
                symbol=symbol,
                side="buy",
                quantity=0.1,
                order_type="market"
            )
            print("Order Result:", result)

    except Exception as e:
        print("Error:", str(e))
