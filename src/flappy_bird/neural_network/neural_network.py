import random
from typing import Iterable, Sequence, Callable, List, Tuple

import numpy as np
from deap import creator, base, tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


class Evolution:
    def __init__(
            self,
            genes_count_by_individual: int,
            population_size: int,
            crossover_probability: float,
            mutation_probability: float,
    ):
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

        self.population = self.toolbox.get_initial_population()

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


def get_slice(sequence: Sequence, first_index: int, length: int):
    last_index = first_index + length
    return sequence[first_index:last_index]


class PlayersPopulation:
    JUMP_THRESHOLD = 0.5

    def __init__(self, individuals_count_by_generation: int, neurons_disposition: Sequence[int],
                 activation_functions: Sequence[Callable]):
        self.individuals_count_by_generation = individuals_count_by_generation
        self.neurons_disposition = neurons_disposition
        self.activation_functions = activation_functions

        genes_count_by_individual = 0
        self.weights_shapes: List[Tuple[int, int]] = []
        self.biases_lengths: List[int] = []

        for i in range(len(self.neurons_disposition) - 1):
            size_layer_in = self.neurons_disposition[i]
            size_layer_out = self.neurons_disposition[i + 1]

            genes_count_by_individual += size_layer_in * size_layer_out + size_layer_out
            self.weights_shapes.append((size_layer_out, size_layer_in))
            self.biases_lengths.append(size_layer_out)

        self.evolution = Evolution(genes_count_by_individual, self.individuals_count_by_generation,
                                   mutation_probability=0.2, crossover_probability=0.2)

        self.weights: List[np.ndarray] = []
        self.biases: List[np.ndarray] = []
        self.update_weights_and_biases_from_evolution()

        self.output_layer: np.ndarray = None

        first_input = np.zeros(
            (self.individuals_count_by_generation, self.neurons_disposition[0])
        )
        self.feed_forward(first_input)

    def deserialize_arrays_from_individual(self, individual: Sequence[float]):
        individual_weights: List[np.ndarray] = []
        individual_biases: List[np.ndarray] = []

        current_index = 0
        for shape in self.weights_shapes:
            slice_length = int(np.prod(shape))
            genes_slice = get_slice(individual, current_index, slice_length)
            array = np.reshape(genes_slice, shape)
            individual_weights.append(array)
            current_index += slice_length

        for length in self.biases_lengths:
            shape = (length, 1)
            genes_slice = get_slice(individual, current_index, length)
            array = np.reshape(genes_slice, shape)
            individual_biases.append(array)
            current_index += length

        return individual_weights, individual_biases

    def update_weights_and_biases_from_evolution(self):
        weights: List[List[np.ndarray]] = [[] for _ in range(len(self.weights_shapes))]
        biases: List[List[np.ndarray]] = [[] for _ in range(len(self.biases_lengths))]

        for individual in self.evolution.population:
            arrays = self.deserialize_arrays_from_individual(individual)
            individual_weights, individual_biases = arrays
            for i in range(len(weights)):
                weights[i].append(individual_weights[i])
                biases[i].append(individual_biases[i])

        self.weights = [np.stack(w) for w in weights]
        self.biases = [np.stack(b) for b in biases]

    def feed_forward(self, input_data: Sequence[Sequence[float]]):
        result = np.reshape(input_data, (self.individuals_count_by_generation, self.neurons_disposition[0], 1))

        for layer_weights, layer_biases, activation_function in zip(self.weights, self.biases,
                                                                    self.activation_functions):
            result = activation_function(np.matmul(layer_weights, result) + layer_biases)
        self.output_layer = np.reshape(result, (self.individuals_count_by_generation,))

    def should_jump(self, player_index: int):
        return self.output_layer[player_index] >= self.JUMP_THRESHOLD
