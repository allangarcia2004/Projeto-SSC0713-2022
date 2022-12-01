import pickle
import random
from typing import Iterable, Sequence
from deap import base, tools, creator, algorithms
from flappy_bird.evaluate import Evaluate

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


class Evolution:
    POPULATION_BACKUP_FILE = "population.backup"

    def __init__(self, use_backup: bool, neurons_disposition: Sequence[int], population_size: int):

        self.population_size = population_size

        # get genes count by individual
        self.genes_count_by_individual = 0
        for i in range(len(neurons_disposition) - 1):
            size_layer_in = neurons_disposition[i]
            size_layer_out = neurons_disposition[i + 1]
            self.genes_count_by_individual += size_layer_in * size_layer_out + size_layer_out

        # make the toolbox to get the initial population
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

        # load or make the initial population
        if use_backup:
            self.load_population_from_file()
        else:
            self.population = self.toolbox.get_initial_population()

        # set the fitness of every individual to 0
        for individual in self.population:
            individual.fitness.values = (0,)

        # initialize the evaluation class (runs game and NNW)
        self.evaluate = Evaluate(neurons_disposition)

        # register the evolutionary tools
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

    def run(self, crossover_probability: float, mutation_probability: float, generations: int):
        self.population = algorithms.eaSimple(
            population=self.population, toolbox=self.toolbox, cxpb=crossover_probability,
            mutpb=mutation_probability, ngen=generations
        )
        self.save_population_to_file()
