import pickle
import random
from typing import Iterable

from deap import base, tools, creator

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


class Evolution:
    POPULATION_BACKUP_FILE = "population.backup"

    def __init__(self, genes_count_by_individual: int, population_size: int, crossover_probability: float,
                 mutation_probability: float, use_backup: bool):
        self.genes_count_by_individual = genes_count_by_individual
        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.toolbox = base.Toolbox()
        self.toolbox.register("get_random_gene", random.random)
        self.toolbox.register(
            "get_individual",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.get_random_gene,
            n=self.genes_count_by_individual,
        )
        self.toolbox.register(
            "get_initial_population",
            tools.initRepeat,
            list,
            self.toolbox.get_individual,
            n=self.population_size,
        )
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=1)
        self.toolbox.register("select", tools.selTournament)

        if use_backup:
            self.load_population_from_file()
        else:
            self.population = self.toolbox.get_initial_population()

    def load_population_from_file(self):
        with open(self.POPULATION_BACKUP_FILE, "rb") as file:
            self.population = pickle.load(file)

    def save_population_to_file(self):
        with open(self.POPULATION_BACKUP_FILE, "wb") as file:
            pickle.dump(self.population, file)

    def set_fitnesses_on_individuals(self, fitness_values: Iterable[float]):
        for individual, fitness_value in zip(self.population, fitness_values):
            individual.fitness.values = (fitness_value,)

    def get_best(self):
        best = self.population[0]
        for individual in self.population[1:]:
            if individual.fitness.dominates(best.fitness):
                best = individual
        return best

    def run_generation(self):
        self.save_population_to_file()

        # Select the next generation individuals
        offspring = self.toolbox.select(
            self.population, len(self.population) - 1, len(self.population) // 10
        )
        # Clone the selected individuals
        offspring = list(map(self.toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.crossover_probability:
                self.toolbox.mate(child1, child2)

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < self.mutation_probability:
                self.toolbox.mutate(mutant)

        # The population is entirely replaced by the offspring
        self.population[:] = offspring + [self.get_best()]
