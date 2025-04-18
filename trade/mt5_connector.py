# trade/mt5_connector.py

import os
import logging
import MetaTrader5 as mt5


def connect_to_mt5(login: int, password: str, server: str, terminal_path: str, timeout: int = 60000) -> bool:
    """
    اتصال به ترمینال MetaTrader5 با path صریح به terminal64.exe.
    """
    logging.info(f"Initializing MT5 terminal from: {terminal_path}")
    if not mt5.initialize(path=terminal_path, timeout=timeout):
        logging.error(f"MT5 initialize failed, last_error={mt5.last_error()}")
        return False

    if not mt5.login(login=login, password=password, server=server):
        logging.error(f"MT5 login failed, last_error={mt5.last_error()}")
        mt5.shutdown()
        return False

    logging.info("MT5 connected successfully.")
    return True


def shutdown_mt5():
    """
    قطع اتصال از ترمینال MT5.
    """
    mt5.shutdown()
    logging.info("MT5 connection closed.")
