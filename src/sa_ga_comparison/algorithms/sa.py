from collections.abc import Callable
from math import exp
import random
from typing import Any


class SimulatedAnnealing:

    def __init__(self, 
                 generation_func: Callable[[Any,random.Random], Any], 
                 temp_fn: Callable[[int], float], 
                 mutation_fn: Callable[[Any, random.Random], Any], 
                 cost_fn: Callable[[Any], float], 
                 rng: random.Random = random.Random()):
        self.generation_func = generation_func
        self.temp_fn = temp_fn
        self.mutation_fn = mutation_fn
        self.cost_fn = cost_fn
        self.rng = rng
        self.history = []


    def get_solution(self, max_iters: int) -> Any:
        self.history = []

        if self.generation_func is None:
            raise ValueError("Generation function is not set")

        if self.temp_fn is None:
            raise ValueError("Temperature function is not set")

        if self.mutation_fn is None:
            raise ValueError("Mutation function is not set")

        if self.cost_fn is None:
            raise ValueError("Cost function is not set")

        current_solution = self.generation_func(self.rng)
        current_cost = self.cost_fn(current_solution)
        self.history.append((current_solution, current_cost))

        best_solution = current_solution
        best_cost = current_cost

        for iteration in range(1, max_iters + 1):
            temp = self.temp_fn(iteration)

            candidate_solution = self.mutation_fn(current_solution, self.rng)
            candidate_cost = self.cost_fn(candidate_solution)

            if candidate_cost < current_cost:
                current_solution = candidate_solution
                current_cost = candidate_cost
                best_solution = current_solution
                best_cost = current_cost
            elif temp > 0 and self.rng.random() < exp((current_cost - candidate_cost) / temp):
                current_solution = candidate_solution
                current_cost = candidate_cost

            self.history.append((current_solution.copy(), current_cost))

        return (best_solution, best_cost, self.history)
