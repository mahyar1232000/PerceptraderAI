"""
Model factory for ML and RL.
"""

from pathlib import Path
from typing import Dict

from perceptrader.models.ml import MLModel
from perceptrader.models.rl import RLAgent


def create_ml_model(params: Dict) -> MLModel:
    return MLModel(params)


def create_rl_agent(params: Dict) -> RLAgent:
    agent = RLAgent(**params)
    return agent


def load_model(path: Path):
    ext = path.suffix
    if ext == ".joblib":
        return MLModel.load(path)
    else:
        return RLAgent.load(path)
