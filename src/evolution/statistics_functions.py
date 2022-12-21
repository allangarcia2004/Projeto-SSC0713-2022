import numpy as np
from deap.tools import selBest, selWorst

# def minimal(fitnesses, weights):
#     """
#     :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
#     :param weights: Tuple of fitness' weights, has the same dimension as the tuples in fitnesses.
#     :return: The fitness tuple of the individual with the lowest weighted fitness.
#     """

#     weighted_fitnesses = dict()
#     for fit in fitnesses:
#         weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

#     return min(weighted_fitnesses, key=weighted_fitnesses.get)

# def maximal(fitnesses, weights):
#     """
#     :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
#     :param weights: Tuple of fitness' weights, has the same dimension as the tuples in fitnesses.
#     :return: The fitness tuple of the individual with the highest weighted fitness.
#     """

#     weighted_fitnesses = dict()
#     for fit in fitnesses:
#         weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

#     return max(weighted_fitnesses, key=weighted_fitnesses.get)

# def avg(fitnesses):
#     """
#     :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
#     :return: A tuple of the average value in each layer of the fitnesses' tuples, calculated with numpy and rounded for 2 decimal points.
#     """

#     average = np.average(fitnesses, axis=0)
#     return tuple([round(layer, 2) for layer in average])

# def std(fitnesses):
#     """
#     :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
#     :return: A tuple of the standard deviation of the values in each layer of the fitnesses' tuples, calculated with numpy and rounded for 2 decimal points..
#     """
#     standard_deviation = np.std(fitnesses, axis=0)
#     return round(standard_deviation[0], 2), round(standard_deviation[1],2)


def minimal(individuals):
    """
    :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
    :param weights: Tuple of fitness' weights, has the same dimension as the tuples in fitnesses.
    :return: The fitness tuple of the individual with the lowest weighted fitness.
    """

    # weighted_fitnesses = dict()
    # for fit in fitnesses:
    #     weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

    # return min(weighted_fitnesses, key=weighted_fitnesses.get)

    return selWorst(individuals, 1, fit_attr='fitness')[0].fitness.values


def maximal(individuals):
    """
    :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
    :param weights: Tuple of fitness' weights, has the same dimension as the tuples in fitnesses.
    :return: The fitness tuple of the individual with the highest weighted fitness.
    """

    # weighted_fitnesses = dict()
    # for fit in fitnesses:
    #     weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

    # return max(weighted_fitnesses, key=weighted_fitnesses.get)

    return selBest(individuals, 1, fit_attr='fitness')[0].fitness.values


def individuals_to_fitnesses(func):

    def wrapper(individuals):
        fitnesses = [ind.fitness.values for ind in individuals]
        return func(fitnesses)

    return wrapper


@individuals_to_fitnesses
def avg(fitnesses):
    """
    :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
    :return: A tuple of the average value in each layer of the fitnesses' tuples, calculated with numpy and rounded for 2 decimal points.
    """

    average = np.average(fitnesses, axis=0)
    return tuple([round(layer, 2) for layer in average])


@individuals_to_fitnesses
def std(fitnesses):
    """
    :param fitnesses: List of the fistness of every individual. Each fitness is a tuple.
    :return: A tuple of the standard deviation of the values in each layer of the fitnesses' tuples, calculated with numpy and rounded for 2 decimal points..
    """
    standard_deviation = np.std(fitnesses, axis=0)
    return round(standard_deviation[0], 2), round(standard_deviation[1], 2)
