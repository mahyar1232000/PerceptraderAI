"""
Paper trading execution for forward testing.
"""

import time

from perceptrader.live.base import BaseExecution
from perceptrader.utils.mt5_utils import calculate_lot_size


class PaperExecution(BaseExecution):
    """Runs a simulated paper-trading loop on live quotes."""

    def run(self, duration: int) -> bool:
        start = time.time()
        # Placeholder loop: in real impl, fetch quotes & simulate trades
        while time.time() - start < duration:
            # simulate...
            time.sleep(1)
        # Suppose success if we exit normally
        return True
