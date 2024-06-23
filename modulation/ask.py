import math

import numpy as np


def ASK_modulation(bits: np.array, carrier_freq: float, time: np.ndarray, amp_high: float = 1,
                   amp_low: float = 0.5) -> np.ndarray:
    """
    Amplitude Shift Keying (ASK) modulation.

    :param bits: List of bits to modulate.
    :param carrier_freq: Carrier frequency.
    :param time: Array of time points.
    :param amp_high: Amplitude for bit 1.
    :param amp_low: Amplitude for bit 0.
    :return: Modulated signal.
    """
    signal = []
    time_per_bit = np.array_split(time, len(bits))
    for i, bit in enumerate(bits):
        amplitude = amp_high if bit == 1 else amp_low
        signal.append(amplitude * np.sin(2 * math.pi * carrier_freq * time_per_bit[i]))
    return np.concatenate(signal)


def ASK_demodulation(signal: np.ndarray, carrier_freq: float, samples_per_bit: int, sampling_period: float,
                     num_samples: int):
    """
    Amplitude Shift Keying (ASK) demodulation.

    :param signal: Received signal.
    :param carrier_freq: Carrier frequency.
    :param samples_per_bit: Number of samples per bit.
    :param sampling_period: Sampling period.
    :param num_samples: Total number of samples.
    :return: Array of demodulated bits.
    """
    time = sampling_period * np.arange(num_samples)
    x = signal * np.sin(2 * np.pi * carrier_freq * time)

    bit_length = num_samples // samples_per_bit
    p = np.zeros(bit_length * samples_per_bit)
    current_sample = 0
    for i in range(bit_length):
        s = 0
        for j in range(samples_per_bit):
            s += x[current_sample]
            p[current_sample] = s
            current_sample += 1

    threshold = np.max(p) / 2
    demodulated_bits = [1 if sample > threshold else 0 for sample in p]
    return demodulated_bits
