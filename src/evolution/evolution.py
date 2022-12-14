import pickle
import random
from typing import Sequence
from deap import base, tools, creator, algorithms
from .evaluate import Evaluate
from .statistics_functions import maximal, minimal, avg, std


class Evolution:
    POPULATION_BACKUP_FILE = "population.backup"
    HALL_OF_FAME_FILE = "hall_of_fame.pkl"

    def __init__(self, use_backup: bool, neurons_disposition: Sequence[int],
                 population_size: int, hall_of_fame_size: int, tournament_size: int,
                 crossover_probability: float, mutation_probability: float,
                 generations: int, fitness_weights: tuple[float, float], logbook_file: str):
        """
        :param use_backup: A bool to determine if a population from previous runs
                           should be used as the initial population.
        :param neurons_disposition: How many nodes each neural network layer has.
        :param population_size: How many individuals are in each generation.
        :param hall_of_fame_size: How many individuals the hall of fame has.
        :param tournament_size: Used by the selection algorithm, selTournament.
                                Determines how many individuals are be in each tournament.
        :param crossover_probability: Crossover probability, between 0 and 1
        :param mutation_probability: Mutation probability, between 0 and 1
        :param generations: Number of generations
        """

        self.population_size = population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.generations = generations
        self.logbook_file = logbook_file

        # determines how many genes a individual will have based on the neural disposition
        self.genes_count_by_individual = 0
        for i in range(len(neurons_disposition) - 1):
            size_layer_in = neurons_disposition[i]
            size_layer_out = neurons_disposition[i + 1]
            self.genes_count_by_individual += size_layer_in * size_layer_out + size_layer_out

        # creates the class Fitness
        # first fitness component is how much obstacles the bird bypassed
        # and the second one is how much frames were loaded during his lifetime
        creator.create("FitnessMulti", base.Fitness, weights=fitness_weights)

        # creates the class Individual
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        # makes the toolbox to generate the initial population randomly
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

        # loads or makes the initial population
        if use_backup:
            self.load_population_from_file()
        else:
            self.population = self.toolbox.get_initial_population()

        # sets the fitness of every individual to 0
        for individual in self.population:
            individual.fitness.values = (0, 0)

        # initializes the class used for evaluation
        self.evaluate = Evaluate(neurons_disposition)

        # registers the evolutionary tools
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.9)
        self.toolbox.register("select", tools.selTournament, tournsize=tournament_size)
        self.toolbox.register("evaluate", self.evaluate.run)

        # initializes logbook and hall of fame objects
        self.logbook: tools.Logbook
        self.logbook = None
        self.hall_of_fame: tools.HallOfFame
        self.hall_of_fame = tools.HallOfFame(hall_of_fame_size)

    def load_population_from_file(self):
        """ Initializes the initial population as a previous one saved. """
        with open(self.POPULATION_BACKUP_FILE, "rb") as file:
            self.population = pickle.load(file)

    def save_population_to_file(self):
        """ Saves the current population to file. """
        with open(self.POPULATION_BACKUP_FILE, "wb") as file:
            pickle.dump(self.population, file)

    def save_hall_of_fame_to_file(self):
        """ Saves hall of fame to file. """
        with open(self.HALL_OF_FAME_FILE, "wb") as file:
            pickle.dump(self.hall_of_fame, file)

    def save_logbook_to_file(self):
        """ Saves logbook to file. """
        with open(self.logbook_file, "wb") as file:
            pickle.dump(self.logbook, file)

    def run(self):
        """ Runs 'deap.algorithms.eaSimple' with the mate method as 'deap.tools.cxTwoPoint', the mutate method as 'deap.tools.mutGaussian', with mu=0, sigma=1 and indpb=1, the select method as 'deap.tools.selTournament' and evaluate method as the modified flappy bird game developed, in witch the individual is interpreted as a neural network. """

        # registers the methods used to calculate the statistics
        stats = tools.Statistics()
        stats.register("avg", avg)
        stats.register("std", std)
        stats.register("min", minimal)  # , weights=creator.FitnessMulti.weights)
        stats.register("max", maximal)  # , weights=creator.FitnessMulti.weights)

        # runs the algorithm from deap
        self.population, self.logbook = algorithms.eaSimple(
            population=self.population, toolbox=self.toolbox, cxpb=self.crossover_probability,
            mutpb=self.mutation_probability, ngen=self.generations, stats=stats,
            halloffame=self.hall_of_fame
        )

        # saves information to files
        self.save_population_to_file()
        self.save_hall_of_fame_to_file()
        self.save_logbook_to_file()
