# src/perceptrader/gui/__init__.py

"""
GUI subpackage for PerceptraderAI:
- dashboard: Matplotlib plots
- tk_dashboard: Real-time Tkinter monitor
"""

from .dashboard import Dashboard
from .tk_dashboard import TkDashboard

__all__ = ["Dashboard", "TkDashboard"]
