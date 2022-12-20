import numpy as np
import warnings

warnings.filterwarnings('ignore')

@np.vectorize
def sigmoid(x: float):
    return 1 / (1 + np.exp(-x))


@np.vectorize
def identity(x: float):
    return x
