import math

import numpy as np


def PSK_modulation(bits: np.array, carrier_freq: float, time: np.ndarray) -> np.ndarray:
    """
    Phase Shift Keying (PSK) modulation.

    :param bits: List of bits to modulate.
    :param carrier_freq: Carrier frequency.
    :param time: Array of time points.
    :return: Modulated signal.
    """
    signal = []
    time_per_bit = np.array_split(time, len(bits))
    for i, bit in enumerate(bits):
        phase = 0 if bit == 0 else math.pi
        signal.append(np.sin(2 * math.pi * carrier_freq * time_per_bit[i] + phase))
    return np.concatenate(signal)


def PSK_demodulation(signal: np.ndarray, carrier_freq: float, samples_per_bit: int, sampling_period: float, num_samples: int):
    """
        Phase Shift Keying (PSK) demodulation.

        :param signal: Received analog signal.
        :param carrier_freq: Carrier frequency.
        :param samples_per_bit: Samples per bit.
        :param sampling_period: Sampling period.
        :param num_samples: Total number of samples.
        :return: Array of demodulated bits.
        """

    time = sampling_period * np.arange(num_samples)

    x = signal * np.sin(2 * np.pi * carrier_freq * time)

    bit_length = int(num_samples / samples_per_bit)
    p = np.zeros(int(bit_length * samples_per_bit))
    s = 0
    current_sample = 0

    for i in range(0, bit_length):
        for j in range(0, int(samples_per_bit)):
            s += x[current_sample]
            p[current_sample] = s
            current_sample += 1
        s = 0

    c = [1 if x < 0 else 0 for x in p]
    return c
