import numpy as np

def minimal(fitnesses, weights):
    weighted_fitnesses = dict()
    for fit in fitnesses:
        weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

    return min(weighted_fitnesses, key=weighted_fitnesses.get)

def maximal(fitnesses, weights):
    weighted_fitnesses = dict()
    for fit in fitnesses:
        weighted_fitnesses[fit] = sum([value * wei for value, wei in zip(fit, weights)])

    return max(weighted_fitnesses, key=weighted_fitnesses.get)

def avg(fitnesses):
    average = np.average(fitnesses, axis=0)
    return round(average[0],2), round(average[1], 2)

def std(fitnesses):
    standard_deviation = np.std(fitnesses, axis=0)
    return round(standard_deviation[0], 2), round(standard_deviation[1],2)