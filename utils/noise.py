import numpy as np


def white_noise(t, noise_level):
    return np.random.normal(0, noise_level, len(t))


def gaussian_noise(t, mean, std_dev):
    return np.random.normal(mean, std_dev, len(t))
