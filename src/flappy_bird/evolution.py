import pickle
import random
from typing import Iterable, Sequence

from deap import base, tools, creator, algorithms
from flappy_bird.evaluate import Evaluate

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


class Evolution:
    POPULATION_BACKUP_FILE = "population.backup"

    def __init__(self, crossover_probability: float, mutation_probability: float,
                 use_backup: bool, neurons_disposition: Sequence[int], population_size: int):
        self.genes_count_by_individual = 0
        for i in range(len(neurons_disposition) - 1):
            size_layer_in = neurons_disposition[i]
            size_layer_out = neurons_disposition[i + 1]
            self.genes_count_by_individual += size_layer_in * size_layer_out + size_layer_out

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

        if use_backup:
            self.load_population_from_file()
        else:
            self.population = self.toolbox.get_initial_population()

        for individual in self.population:
            individual.fitness.values = (0,)

        self.evaluate = Evaluate(self.population, neurons_disposition,
                                 population_size)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=1)
        self.toolbox.register("select", tools.selTournament, tournsize=2)
        self.toolbox.register("evaluate", self.evaluate.run)

    def load_population_from_file(self):
        with open(self.POPULATION_BACKUP_FILE, "rb") as file:
            self.population = pickle.load(file)

    def save_population_to_file(self):
        with open(self.POPULATION_BACKUP_FILE, "wb") as file:
            pickle.dump(self.population, file)

    def get_best(self):
        best = self.population[0]
        for individual in self.population[1:]:
            if individual.fitness.dominates(best.fitness):
                best = individual
        return best

    def run_generation(self):
        self.save_population_to_file()

        self.population = algorithms.eaSimple(
            self.population, self.toolbox, self.crossover_probability, self.mutation_probability, 3
        )


    #    # Select the next generation individuals
    #    offspring = self.toolbox.select(
    #        self.population, len(self.population) - 1, len(self.population) // 10
    #    )
    #    # Clone the selected individuals
    #    offspring = list(map(self.toolbox.clone, offspring))
#
    #    # Apply crossover on the offspring
    #    for child1, child2 in zip(offspring[::2], offspring[1::2]):
    #        if random.random() < self.crossover_probability:
    #            self.toolbox.mate(child1, child2)
#
    #    # Apply mutation on the offspring
    #    for mutant in offspring:
    #        if random.random() < self.mutation_probability:
    #            self.toolbox.mutate(mutant)
#
    #    # The population is entirely replaced by the offspring
    #    self.population[:] = offspring + [self.get_best()]
