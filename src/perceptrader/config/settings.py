import os
from datetime import datetime
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


def parse_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    # — MT5 & Broker
    MT5_PATH: str = os.getenv("MT5_PATH", "")
    BROKER_API_KEY: str = os.getenv("BROKER_API_KEY", "")

    # — Directories
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", "logs"))
    MODEL_DIR: Path = Path(os.getenv("MODEL_DIR", "models"))

    # — Symbols & Timeframes
    SYMBOLS: List[str] = parse_list(os.getenv("SYMBOLS", "EURUSD,USDJPY"))
    TIMEFRAMES: List[str] = parse_list(os.getenv("TIMEFRAMES", "M1,M5,M15"))

    # — Risk Management
    RISK_PER_TRADE: float = float(os.getenv("RISK_PER_TRADE", "0.01"))
    MT5_DEVIATION: int = int(os.getenv("MT5_DEVIATION", "10"))
    MT5_MAGIC: int = int(os.getenv("MT5_MAGIC", "123456"))

    # — Optimization
    OPTIMIZATION_PARAMS: dict = {
        "population_size": int(os.getenv("POP_SIZE", "20")),
        "generations": int(os.getenv("GENERATIONS", "10")),
    }

    # — Paper Trading
    PAPER_DURATION: int = int(os.getenv("PAPER_DURATION", "300"))  # seconds


settings = Settings()
