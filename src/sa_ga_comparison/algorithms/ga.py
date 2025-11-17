from collections.abc import Callable
import random
from typing import Any


class GeneticAlgorithm:

    def __init__(self, 
                 population_size: int, 
                 mutation_rate: float, 
                 crossover_rate: float, 
                 fitness_fn: Callable[[Any], float], 
                 mutation_fn: Callable[[Any, random.Random], Any], 
                 crossover_fn: Callable[[Any, Any, random.Random], Any], 
                 generation_fn: Callable[[random.Random], Any],
                 selection_fn: Callable[[list[Any], random.Random], Any],
                 rng: random.Random = random.Random()):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.fitness_fn = fitness_fn
        self.mutation_fn = mutation_fn
        self.crossover_fn = crossover_fn
        self.generation_fn = generation_fn
        self.selection_fn = selection_fn
        self.rng = rng
        self.history = []


    def get_solution(self, max_iters: int) -> Any:
        self.history = []

        if self.generation_fn is None:
            raise ValueError("Generation function is not set")

        if self.mutation_fn is None:
            raise ValueError("Mutation function is not set")

        if self.fitness_fn is None:
            raise ValueError("Fitness function is not set")

        current_population = [self.generation_fn(self.rng) for _ in range(self.population_size)]
        current_population.sort(key=lambda x: self.fitness_fn(x))
        best_individual = current_population[0]
        best_fitness = self.fitness_fn(best_individual)

        for iteration in range(max_iters):
            new_population = []
            for ind in current_population:
                if self.rng.random() < self.mutation_rate:
                    new_population.append(self.mutation_fn(ind, self.rng))

                if self.rng.random() < self.crossover_rate and self.crossover_fn is not None:
                    partner = self.rng.choice(current_population)
                    new_population.append(self.crossover_fn(ind, partner, self.rng))

                new_population.append(ind)

            current_population = new_population
            current_population = self.selection_fn(current_population, self.rng, self.fitness_fn)
            current_population.sort(key=lambda x: self.fitness_fn(x))
            current_population = current_population[:self.population_size]
            if best_fitness > self.fitness_fn(current_population[0]):
                best_individual = current_population[0]
                best_fitness = self.fitness_fn(best_individual)
            self.history.append((current_population[0].copy(), self.fitness_fn(current_population[0])))

        return best_individual, best_fitness, self.history