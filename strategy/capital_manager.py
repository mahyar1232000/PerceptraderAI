# strategy/capital_manager.py

import logging


class CapitalManager:
    """
    مدیریت سرمایه: مارتینگل، آنتی‌مارتینگل، فیبوناچی.
    """

    def __init__(self, total_capital: float, max_alloc_per_trade: float = 0.05):
        self.total_capital = total_capital
        self.available = total_capital
        self.max_alloc = max_alloc_per_trade
        self.fib_sequence = [1, 1, 2, 3, 5, 8, 13]

    def allocate(self, risk_amount: float, strategy: str = "martingale", fib_step: int = 0) -> float:
        """
        تخصیص سرمایه بر اساس استراتژی انتخابی.
        """
        if strategy == "martingale":
            alloc = min(self.available * self.max_alloc * (2 ** fib_step), risk_amount)
        elif strategy == "anti-martingale":
            alloc = min(self.available * self.max_alloc * (1 / (2 ** fib_step)), risk_amount)
        elif strategy == "fibonacci":
            alloc = min(self.available * self.max_alloc * self.fib_sequence[fib_step], risk_amount)
        else:
            alloc = min(self.available * self.max_alloc, risk_amount)
        self.available -= alloc
        logging.debug(f"Allocated capital: {alloc}")
        return alloc

    def release(self, amount: float):
        self.available += amount
