"""
MT5 symbol mapping and order helpers.
"""

from typing import List, Optional

import MetaTrader5 as mt5

from perceptrader.config.settings import settings


def map_configured_symbols(config_syms: List[str]) -> List[str]:
    """
    Resolve configured names (e.g. 'EURUSD_o') to broker-recognized
    MT5 symbols, using prefix/suffix matching heuristics.
    """
    all_syms = mt5.symbols_get()
    all_names = [s.name for s in all_syms]

    resolved: List[str] = []
    for cs in config_syms:
        matches = [name for name in all_names if cs.strip('_') in name]
        if matches:
            resolved.append(matches[0])
        else:
            resolved.append(cs)  # fallback to original
    return resolved


def calculate_lot_size(
        balance: float, risk_per_trade: float, stop_pips: float,
        symbol: str
) -> float:
    """
    Compute lot size based on account balance, risk %, and pip distance.
    """
    # Placeholder: implement pip-value lookup and calc
    pip_value = 10.0
    dollar_risk = balance * risk_per_trade
    lots = dollar_risk / (stop_pips * pip_value)
    return max(0.01, lots)
