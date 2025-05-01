"""
ML model training and inference.
"""

import joblib
from pathlib import Path
from typing import Any, Dict

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from perceptrader.config.settings import settings


class MLModel:
    """RandomForest-based classifier for signal prediction."""

    def __init__(self, params: Dict[str, Any]) -> None:
        self.params = params
        self.model = RandomForestClassifier(**params)

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        return self.model.predict(X)

    def save(self, name: str) -> Path:
        path = settings.MODEL_DIR / f"{name}_rf.joblib"
        joblib.dump(self.model, path)
        return path

    @classmethod
    def load(cls, path: Path) -> "MLModel":
        model = joblib.load(path)
        inst = cls(params={})
        inst.model = model
        return inst
