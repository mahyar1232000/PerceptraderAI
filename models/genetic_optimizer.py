import logging
import numpy as np
from functools import partial


class GeneticOptimizer:
    """
    Simple Genetic Algorithm for parameter optimization.
    """

    def __init__(self, param_bounds: dict[str, tuple[float, float]], population_size: int = 20,
                 generations: int = 50, mutation_rate: float = 0.1):
        """
        :param param_bounds: e.g. {'short_ma': (5,50), 'long_ma': (50,200)}
        :param population_size: Number of candidate solutions per generation
        :param generations: Number of generations to evolve
        :param mutation_rate: Probability of mutating a gene
        """
        self.param_names = list(param_bounds.keys())
        self.bounds = np.array(list(param_bounds.values()))
        self.pop_size = population_size
        self.gens = generations
        self.mut_rate = mutation_rate
        logging.info(f"GeneticOptimizer initialized with bounds: {param_bounds}")

    def _initialize_population(self):
        """
        Randomly initialize the population within bounds.
        """
        low, high = self.bounds[:, 0], self.bounds[:, 1]
        pop = np.random.uniform(low, high, size=(self.pop_size, len(self.bounds)))
        logging.debug(f"Initial population shape: {pop.shape}")
        return pop

    def optimize(self, fitness_fn: callable) -> dict[str, float]:
        """
        Optimize parameters by evolving the population according to
        fitness_fn, which returns a scalar cost for each candidate.
        """
        pop = self._initialize_population()
        for gen in range(self.gens):
            # Evaluate fitness
            costs = np.apply_along_axis(fitness_fn, 1, pop)
            # Select top half
            idx = np.argsort(costs)
            survivors = pop[idx[:self.pop_size // 2]]
            logging.debug(f"Generation {gen}: best cost = {costs[idx[0]]}")
            # Crossover
            children = []
            while len(children) < self.pop_size // 2:
                parents = survivors[np.random.choice(survivors.shape[0], 2, replace=False)]
                cross_pt = np.random.randint(1, len(self.bounds))
                child = np.concatenate([parents[0][:cross_pt], parents[1][cross_pt:]])
                children.append(child)
            pop = np.vstack((survivors, np.array(children)))
            # Mutation
            for individual in pop:
                if np.random.rand() < self.mut_rate:
                    gene_idx = np.random.randint(len(self.bounds))
                    low, high = self.bounds[gene_idx]
                    individual[gene_idx] = np.random.uniform(low, high)
        best = pop[np.argmin(np.apply_along_axis(fitness_fn, 1, pop))]
        best_params = dict(zip(self.param_names, best.tolist()))
        logging.info(f"GA optimization best params: {best_params}")
        return best_params
