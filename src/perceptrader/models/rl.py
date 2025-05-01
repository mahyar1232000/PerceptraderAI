"""
RL agent training and inference.
"""

from pathlib import Path
from typing import Any, Dict

from stable_baselines3 import PPO

from perceptrader.config.settings import settings


class RLAgent:
    """PPO-based RL agent."""

    def __init__(self, policy: str = "MlpPolicy", **kwargs: Any) -> None:
        self.policy = policy
        self.kwargs = kwargs
        self.agent: PPO = None  # type: ignore

    def train(self, env, total_timesteps: int) -> None:
        self.agent = PPO(self.policy, env, **self.kwargs)
        self.agent.learn(total_timesteps=total_timesteps)

    def predict(self, obs):
        return self.agent.predict(obs, deterministic=True)[0]

    def save(self, name: str) -> Path:
        path = settings.MODEL_DIR / f"{name}_ppo"
        self.agent.save(str(path))
        return path

    @classmethod
    def load(cls, path: Path) -> "RLAgent":
        inst = cls()
        inst.agent = PPO.load(str(path))
        return inst
