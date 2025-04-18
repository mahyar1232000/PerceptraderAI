# strategy/risk_manager.py

import numpy as np
import logging


class RiskManager:
    """
    مدیریت ریسک با VaR و CVaR برای تعیین حجم معامله.
    """

    def __init__(self, account_balance: float, var_conf: float = 0.95, cvar_conf: float = 0.95):
        self.account_balance = account_balance
        self.var_conf = var_conf
        self.cvar_conf = cvar_conf

    def calculate_var(self, pnl_series: np.ndarray) -> float:
        """
        محاسبه VaR با درصد اطمینان var_conf.
        """
        return np.percentile(pnl_series, (1 - self.var_conf) * 100)

    def calculate_cvar(self, pnl_series: np.ndarray) -> float:
        """
        محاسبه CVaR با درصد اطمینان cvar_conf.
        """
        var = self.calculate_var(pnl_series)
        return pnl_series[pnl_series <= var].mean()

    def calculate_position_size(self, stop_loss_pips: float, pip_value: float) -> float:
        """
        تعیین حجم معامله براساس ریسک مجاز.
        """
        # فرض: استفاده از CVaR برای محاسبه ریسک دلار
        risk_amount = self.account_balance * (1 - self.cvar_conf)
        size = risk_amount / (stop_loss_pips * pip_value)
        logging.debug(f"Position size: {size}")
        return size
