from typing import Callable, List, Sequence, Tuple

import numpy as np

from flappy_bird.neural_network.evolution import Evolution


def get_slice(sequence: Sequence, first_index: int, length: int):
    last_index = first_index + length
    return sequence[first_index:last_index]


class PlayersPopulation:
    JUMP_THRESHOLD = 0.5

    def __init__(self, individuals_count_by_generation: int, neurons_disposition: Sequence[int],
                 activation_functions: Sequence[Callable], use_backup: bool):
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
                                   mutation_probability=0.2, crossover_probability=0.2, use_backup=use_backup)

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
