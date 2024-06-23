import numpy as np
from typing import List, Optional

from .ask import ASK_modulation, ASK_demodulation
from .psk import PSK_modulation, PSK_demodulation
from .fsk import FSK_modulation, FSK_demodulation

modulation_funcs = {
    'ASK': (ASK_modulation, ASK_demodulation),
    'PSK': (PSK_modulation, PSK_demodulation),
    'FSK': (FSK_modulation, FSK_demodulation)
}


def modulate_signal(bits: List[int], modulation_type: str, fn: float, t: np.ndarray,
                    fn1: Optional[float] = None, fn2: Optional[float] = None) -> np.ndarray:
    """
    Modulate a signal based on the specified modulation type.

    :param bits: List of bits to modulate.
    :param modulation_type: Type of modulation ('ASK', 'PSK', 'FSK').
    :param fn: Carrier frequency.
    :param t: Time array.
    :param fn1: Frequency for FSK bit 0 (optional).
    :param fn2: Frequency for FSK bit 1 (optional).
    :return: Modulated signal as a numpy array.
    """
    if modulation_type == 'ASK':
        return modulation_funcs['ASK'][0](bits, fn, t)
    elif modulation_type == 'PSK':
        return modulation_funcs['PSK'][0](bits, fn, t)
    elif modulation_type == 'FSK':
        return modulation_funcs['FSK'][0](bits, fn1, fn2, t)
    else:
        return np.zeros_like(t)


def demodulate_signal(signal: np.ndarray, modulation_type: str, fn: float, samples_per_bit: int,
                      sampling_period: float, num_samples: int,
                      fn1: Optional[float] = None, fn2: Optional[float] = None) -> List[int]:
    """
    Demodulate a signal based on the specified modulation type.

    :param signal: Received signal to demodulate.
    :param modulation_type: Type of modulation ('ASK', 'PSK', 'FSK').
    :param fn: Carrier frequency.
    :param samples_per_bit: Number of samples per bit.
    :param sampling_period: Sampling period.
    :param num_samples: Total number of samples.
    :param fn1: Frequency for FSK bit 0 (optional).
    :param fn2: Frequency for FSK bit 1 (optional).
    :return: List of demodulated bits.
    """
    if modulation_type == 'ASK':
        return modulation_funcs['ASK'][1](signal, fn, samples_per_bit, sampling_period, num_samples)
    elif modulation_type == 'PSK':
        return modulation_funcs['PSK'][1](signal, fn, samples_per_bit, sampling_period, num_samples)
    elif modulation_type == 'FSK':
        return modulation_funcs['FSK'][1](signal, fn1, fn2, samples_per_bit, sampling_period, num_samples)
    else:
        return np.zeros_like(signal).tolist()


__all__ = [
    'ASK_modulation',
    'ASK_demodulation',
    'PSK_modulation',
    'PSK_demodulation',
    'FSK_modulation',
    'FSK_demodulation',
    'modulate_signal',
    'demodulate_signal'
]
