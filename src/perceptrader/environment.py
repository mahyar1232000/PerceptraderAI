import gym
import numpy as np
import pandas as pd
from gym import spaces
from typing import Dict, Tuple, Any


class TradingEnv(gym.Env):
    """Gym environment for trading with OHLCV data."""

    metadata = {"render.modes": ["human"]}

    def __init__(
            self,
            df: pd.DataFrame,
            window: int = 50,
            initial_balance: float = 10_000.0,
    ):
        super().__init__()

        if "volume" not in df.columns:
            raise ValueError("DataFrame must contain a 'volume' column")

        self.df = df.reset_index(drop=True)
        self.window = window
        self.initial_balance = float(initial_balance)
        self.action_space = spaces.Discrete(3)  # sell, hold, buy
        # observation: concatenated normalized close & volume for last `window` bars
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(window * 2,), dtype=np.float32
        )

        self.reset()

    def reset(self) -> np.ndarray:
        self.balance = self.initial_balance
        self.position = 0  # in units of the asset
        self.idx = self.window
        return self._get_obs()

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        price = self.df.loc[self.idx, "close"]
        # 0: sell, 1: hold, 2: buy
        if action == 0 and self.position > 0:
            self.balance += self.position * price
            self.position = 0
        elif action == 2:
            units = self.balance / price
            self.position += units
            self.balance -= units * price

        reward = self.balance + self.position * price - self.initial_balance
        self.idx += 1
        done = self.idx >= len(self.df)
        return self._get_obs(), float(reward), done, {}

    def _get_obs(self) -> np.ndarray:
        window_df = self.df.iloc[self.idx - self.window: self.idx]
        norm_close = window_df["close"].values / window_df["close"].iloc[0] - 1.0
        norm_vol = window_df["volume"].values / window_df["volume"].max()
        return np.hstack([norm_close, norm_vol]).astype(np.float32)

    def render(self, mode: str = "human") -> None:
        print(f"Step {self.idx}: Balance={self.balance:.2f}, Position={self.position}")
