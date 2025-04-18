# strategy/strategy_optimizer.py

import numpy as np
import pyswarms as ps
import logging


class PSOOptimizer:
    """
    بهینه‌سازی پارامترها با Particle Swarm Optimization.
    """

    def __init__(self, param_bounds: dict, fitness_fn):
        """
        :param param_bounds: {"short": (5,50), "long": (50,200), ...}
        :param fitness_fn: تابع برازندگی که سود استراتژی را حساب می‌کند
        """
        self.bounds = np.array(list(param_bounds.values())).T
        self.fitness_fn = fitness_fn

    def optimize(self, n_particles=30, iters=100):
        opt = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=self.bounds.shape[1],
                                      options={"c1": 0.5, "c2": 0.3, "w": 0.9},
                                      bounds=self.bounds)
        cost, pos = opt.optimize(self.fitness_fn, iters=iters)
        logging.info(f"Best params: {pos}, cost: {cost}")
        return pos
