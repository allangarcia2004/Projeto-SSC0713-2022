from typing import Callable, List, Sequence, Tuple

import numpy as np


def get_slice(sequence: Sequence, first_index: int, length: int):
    last_index = first_index + length
    return sequence[first_index:last_index]


class PlayersPopulation:
    JUMP_THRESHOLD = 0.5
    DASH_THRESHOLD = 0.5

    def __init__(self, neurons_disposition: Sequence[int],
                 activation_functions: Sequence[Callable]):
        self.neurons_disposition = neurons_disposition
        self.activation_functions = activation_functions

        self.weights_shapes: List[Tuple[int, int]] = []
        self.biases_lengths: List[int] = []

        for i in range(len(self.neurons_disposition) - 1):
            size_layer_in = int(self.neurons_disposition[i])
            size_layer_out = self.neurons_disposition[i + 1]

            self.weights_shapes.append((size_layer_out, size_layer_in))
            self.biases_lengths.append(size_layer_out)

    def deserialize_arrays_from_individual(self, individual: Sequence[float]):
        individual_weights: List[np.ndarray] = []
        individual_biases: List[np.ndarray] = []

        current_index = 0
        for shape in self.weights_shapes:
            slice_length = int(np.prod(shape))
            genes_slice = individual[current_index:current_index+slice_length]
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

    def feed_forward(self, individual: Sequence[float], input_data):
        result = np.reshape(input_data, (self.neurons_disposition[0], 1))

        weights, bias = self.deserialize_arrays_from_individual(individual)
        for layer_weights, layer_biases, activation_function \
                in zip(weights, bias, self.activation_functions):
            mul = np.matmul(layer_weights, result)
            result = activation_function(mul + layer_biases)

        return result

    def should_move(self, individual: Sequence[float], input_data):
        should_jump, dash_velocity = self.feed_forward(individual, input_data)
        return should_jump >= self.JUMP_THRESHOLD, dash_velocity
