"""
PerceptraderAI Core Module

Exposes the main entrypoints:
  - settings
  - TradingEnv
  - Optimizer
  - RiskManagement
  - LiveExecution
  - PaperExecution
"""

from perceptrader.config.settings import settings
from perceptrader.environment import TradingEnv
from perceptrader.optimization import Optimizer
from perceptrader.risk.management import RiskManagement
from perceptrader.live.execution import LiveExecution
from perceptrader.live.paper import PaperExecution

__all__ = [
    "settings",
    "TradingEnv",
    "Optimizer",
    "RiskManagement",
    "LiveExecution",
    "PaperExecution",
]
