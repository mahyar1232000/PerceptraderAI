import os
import time
import logging
import MetaTrader5 as mt5


def connect_to_mt5(
        login: int,
        password: str,
        server: str,
        terminal_path: str,
        timeout: int = 60000,
        retries: int = 3
) -> bool:
    """
    Robust connection to MetaTrader5 terminal, with retries and separate login.

    Clears any prior IPC sessions, initializes the terminal, then logs in.
    Retries initialization up to `retries` times before giving up.
    """
    # Ensure we start from a clean state (avoids stale IPC)
    mt5.shutdown()

    for attempt in range(1, retries + 1):
        if not mt5.initialize(path=terminal_path, timeout=timeout):
            logging.error(f"MT5 initialize failed (attempt {attempt}/{retries}): {mt5.last_error()}")
            time.sleep(1)
            continue

        if not mt5.login(login, password, server):
            logging.error(f"MT5 login failed: {mt5.last_error()}")
            mt5.shutdown()
            return False

        logging.info("MT5 connected successfully.")
        return True

    logging.error("Exceeded MT5 initialize retries.")
    return False


def shutdown_mt5():
    """
    Disconnects from the MetaTrader5 terminal cleanly.
    """
    mt5.shutdown()
    logging.info("MT5 connection closed.")
