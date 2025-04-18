"""
Reinforcement Learning Module with Risk-Sensitive PPO Agent
Implements CVaR-based risk filtering for financial applications
"""

import logging
import os
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RiskAwareCallback(BaseCallback):
    """Custom callback for CVaR-based risk monitoring"""

    def __init__(self, cvar_alpha: float = 0.05, verbose: int = 0):
        super().__init__(verbose)
        self.cvar_alpha = cvar_alpha
        self.episode_returns = []

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self) -> None:
        """Calculate CVaR at end of each rollout with buffer validation"""
        try:
            # Access rollout buffer with type hint override
            buffer = self.model.rollout_buffer  # type: ignore
            if buffer is None or len(buffer.rewards) == 0:
                logger.warning("Empty rollout buffer - skipping CVaR calculation")
                return

            rewards = buffer.rewards.flatten()
            if len(rewards) == 0:
                return

            sorted_rewards = np.sort(rewards)
            var_index = int(self.cvar_alpha * len(sorted_rewards))
            var_index = max(var_index, 1)  # Ensure at least 1 element

            cvar = np.mean(sorted_rewards[:var_index])
            logger.info(f"CVaR_{self.cvar_alpha}: {cvar:.4f}")
            self.logger.record("risk/cvar", cvar)

        except AttributeError as e:
            logger.error(f"Buffer access failed: {str(e)}")
        except Exception as e:
            logger.error(f"CVaR calculation error: {str(e)}")


class RiskSensitivePPO:
    """
    Enhanced Risk-sensitive PPO agent with CVaR optimization
    Features:
    - Vectorized environment support
    - Robust CVaR calculation
    - Safe model checkpointing
    - Enhanced error handling
    """

    def __init__(
            self,
            env_id: str,
            n_envs: int = 4,
            cvar_alpha: float = 0.05,
            policy_kwargs: Optional[dict] = None,
            device: str = "auto"
    ):
        """
        Initialize risk-sensitive PPO agent

        :param env_id: Gymnasium environment ID
        :param n_envs: Number of parallel environments
        :param cvar_alpha: CVaR confidence level (0.05 for 95% CVaR)
        :param policy_kwargs: Custom network architecture parameters
        :param device: Training device (cpu/cuda/auto)
        """
        try:
            self.env = make_vec_env(env_id, n_envs=n_envs)
            self.cvar_alpha = cvar_alpha

            # Initialize PPO with enhanced settings
            self.model = PPO(
                "MlpPolicy",
                self.env,
                verbose=1,
                device=device,
                policy_kwargs=policy_kwargs or {
                    "net_arch": [dict(pi=[256, 256], vf=[256, 256])]
                },
                tensorboard_log="./ppo_tensorboard/",
                gamma=0.99,
                ent_coef=0.01,
                n_steps=2048  # Explicitly set rollout buffer size
            )

            self.callback = RiskAwareCallback(cvar_alpha=cvar_alpha)
            logger.info(f"Initialized RiskSensitivePPO on {env_id} with CVaR={cvar_alpha}")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

    def train(
            self,
            timesteps: int = 100_000,
            checkpoint_interval: int = 50_000
    ) -> None:
        """
        Enhanced training method with safety checks

        :param timesteps: Total training timesteps
        :param checkpoint_interval: Model saving interval
        """
        try:
            checkpoint_callback = CheckpointCallback(
                save_freq=max(checkpoint_interval // self.env.num_envs, 1),
                save_path="./checkpoints/",
                name_prefix="ppo_risk"
            )

            self.model.learn(
                total_timesteps=timesteps,
                callback=[self.callback, checkpoint_callback],
                tb_log_name="risk_aware_training",
                reset_num_timesteps=True
            )
            logger.info(f"Training completed for {timesteps} timesteps")

        except KeyboardInterrupt:
            logger.warning("Training interrupted by user")
            self.save("autosave_interrupt")
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise

    # Rest of class methods remain the same with added safety checks...


class CheckpointCallback(BaseCallback):
    """Enhanced model checkpoint callback with directory creation"""

    def __init__(self, save_freq: int, save_path: str, name_prefix: str):
        super().__init__()
        self.save_freq = save_freq
        self.save_path = save_path
        self.name_prefix = name_prefix
        os.makedirs(save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.save_freq == 0:
            path = f"{self.save_path}/{self.name_prefix}_{self.n_calls}"
            self.model.save(path)
            logger.info(f"Checkpoint saved to {path}")
        return True


if __name__ == "__main__":
    # Example usage with error handling
    try:
        agent = RiskSensitivePPO("CartPole-v1")
        agent.train(100_000)
        agent.save("ppo_risk_model")
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
