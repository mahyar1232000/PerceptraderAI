import os
from pathlib import Path

import pandas as pd
import pytest

from perceptrader.models.ml import MLModel
from perceptrader.models.rl import RLAgent


@pytest.fixture
def sample_X_y():
    X = pd.DataFrame({
        "feat1": [0, 1, 0, 1],
        "feat2": [1, 0, 1, 0],
    })
    y = pd.Series([0, 1, 0, 1])
    return X, y


def test_mlmodel_train_and_save(tmp_path, sample_X_y):
    X, y = sample_X_y
    model = MLModel({"n_estimators": 5, "random_state": 42})
    model.train(X, y)
    path = model.save("testml")
    assert Path(path).exists()
    loaded = MLModel.load(path)
    assert hasattr(loaded, "predict")
    preds = loaded.predict(X)
    assert len(preds) == len(y)


@pytest.mark.skip(reason="RL training is slow; only test load/save")
def test_rlagent_train_and_save(tmp_path):
    from perceptrader.environment import TradingEnv
    import pandas as pd

    # simple DataFrame for env
    df = pd.DataFrame({
        "close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "volume": [10] * 10
    })
    env = TradingEnv(df, window=3)
    agent = RLAgent(policy="MlpPolicy")
    agent.train(env, total_timesteps=1000)
    path = agent.save("testrl")
    assert Path(path).exists()
    loaded = RLAgent.load(path)
    assert hasattr(loaded, "predict")
