import math

import numpy as np


def FSK_modulation(bits: np.array, f_n1: float, f_n2: float, time: np.ndarray) -> np.ndarray:
    """
    Frequency Shift Keying (FSK) modulation.

    :param bits: List of bits to modulate.
    :param f_n1: Frequency for bit 0.
    :param f_n2: Frequency for bit 1.
    :param time: Array of time points.
    :return: Modulated signal.
    """
    signal = []
    time_per_bit = np.array_split(time, len(bits))
    for i, bit in enumerate(bits):
        frequency = f_n1 if bit == 0 else f_n2
        signal.append(np.sin(2 * math.pi * frequency * time_per_bit[i]))
    return np.concatenate(signal)


def FSK_demodulation(analog_signal: np.array, f_n1: float, f_n2: float, samples_per_bit: int, sampling_period: float, num_samples: int):
    """
    Frequency Shift Keying (FSK) demodulation.

    :param analog_signal: Received analog signal.
    :param f_n1: Frequency for bit 0.
    :param f_n2: Frequency for bit 1.
    :param samples_per_bit: Samples per bit.
    :param sampling_period: Sampling period.
    :param num_samples: Total number of samples.
    :return: Array of demodulated bits.
    """
    time = sampling_period * np.arange(num_samples)

    x_1 = analog_signal * np.sin(2 * np.pi * f_n1 * time)
    x_2 = analog_signal * np.sin(2 * np.pi * f_n2 * time)

    bit_length = num_samples // samples_per_bit
    p = np.zeros(bit_length * samples_per_bit)
    p1 = np.zeros(bit_length * samples_per_bit)
    p2 = np.zeros(bit_length * samples_per_bit)
    s_1 = 0
    s_2 = 0
    current_sample = 0

    for i in range(bit_length):
        for j in range(samples_per_bit):
            s_1 += x_1[current_sample]
            s_2 += x_2[current_sample]
            p1[current_sample] = s_1
            p2[current_sample] = s_2
            p[current_sample] = -s_1 + s_2
            current_sample += 1
        s_1 = 0
        s_2 = 0

    demodulated_bits = [1 if sample > 0 else 0 for sample in p]
    return demodulated_bits
