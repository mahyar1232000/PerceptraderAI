from perceptrader.config import settings


class RiskManagement:
    """Position sizing and risk limit enforcement"""

    def __init__(self):
        self.risk_per_trade = settings.RISK_PER_TRADE
        self.max_drawdown = settings.MAX_DRAWDOWN

    def calculate_position_size(self, entry_price: float, stop_loss: float, balance: float) -> float:
        """Calculate lot size based on risk parameters"""
        risk_amount = balance * self.risk_per_trade
        price_diff = abs(entry_price - stop_loss)
        if price_diff == 0:
            return 0.0
        return round(risk_amount / (price_diff * 10), 2)

    def validate_exposure(self, current_drawdown: float) -> bool:
        """Check against maximum allowed drawdown"""
        return current_drawdown <= self.max_drawdown
