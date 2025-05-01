"""
Master Orchestrator: full pipeline from data → backtest →
optimize → retrain → forward-test → live execution.
"""

import sys
import pandas as pd
from pathlib import Path
from perceptrader.gui.tk_dashboard import start_dashboard_in_thread
from perceptrader.config.settings import settings
from perceptrader.data.pipeline import DataPipeline
from perceptrader.environment import TradingEnv
from perceptrader.optimization import Optimizer
from perceptrader.models.factory import create_ml_model, create_rl_agent
from perceptrader.strategy.factory import create_strategy
from perceptrader.live.paper import PaperExecution
from perceptrader.live.execution import LiveExecution
from perceptrader.utils.logger import setup_logger


def main() -> None:
    logger = setup_logger("orchestrator")
    logger.info("Starting PerceptraderAI pipeline")

    # 1. Data acquisition
    pipeline = DataPipeline(settings.SYMBOLS, settings.TIMEFRAMES)
    pipeline.run()
    logger.info("Data fetched and processed")

    # 2. Backtest & Optimization
    for symbol in settings.SYMBOLS:
        for tf in settings.TIMEFRAMES:
            df = (
                    Path("data/processed") / f"{symbol}_{tf}.csv"
            )
            df = TradingEnv(pd.read_csv(df, index_col=0), window=50)
            opt = Optimizer(settings.OPTIMIZATION_PARAMS)
            best_params = opt.optimize(df.df)
            logger.info(f"Best params for {symbol}-{tf}: {best_params}")

            # 3. Retrain models
            # Prepare features/labels…
            X, y = df.df.dropna().iloc[:, :-1], df.df["signal"]
            ml = create_ml_model(best_params)
            ml.train(X, y)
            ml_path = ml.save(f"{symbol}_{tf}")
            logger.info(f"Saved ML model to {ml_path}")

            rl = create_rl_agent(best_params)
            rl.train(df, total_timesteps=10_000)
            rl_path = rl.save(f"{symbol}_{tf}")
            logger.info(f"Saved RL agent to {rl_path}")

            # 4. Forward (paper) test
            paper = PaperExecution(symbol, tf)
            ok = paper.run(duration=settings.PAPER_DURATION)
            if not ok:
                logger.warning(f"Paper test failed for {symbol}-{tf}, skipping live")
                continue

            # 5. Live execution
            live = LiveExecution(symbol, tf)
            live.run()

    logger.info("Pipeline complete")


if __name__ == "__main__":
    sys.exit(main())
