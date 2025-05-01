"""
Centralized logging configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from perceptrader.config.settings import settings


def setup_logger(name: str) -> logging.Logger:
    """
    Return a module-specific logger writing to rotating files
    under settings.LOG_DIR.
    """
    log_dir = settings.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_file = log_dir / f"{name}.log"
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    fmt = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)

    return logger
