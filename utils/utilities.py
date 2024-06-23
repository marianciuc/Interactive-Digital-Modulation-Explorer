import numpy as np
from typing import List, Union


def binary_stream_to_ascii(binary_stream: Union[np.ndarray, List[int]], length: int = 8) -> str:
    """
    Convert a binary stream to an ASCII string.

    :param binary_stream: Array or list of binary bits.
    :param length: Length of each byte in bits. Default is 8.
    :return: Converted ASCII string.
    """
    chars = []
    for i in range(0, len(binary_stream), length):
        byte = binary_stream[i:i + length]
        byte_str = ''.join(str(bit) for bit in byte)
        char = chr(int(byte_str, 2))
        chars.append(char)
    return ''.join(chars)


def convert_to_binary_stream(signal: np.ndarray, samples_per_bit: int) -> List[int]:
    """
    Convert a signal to a binary stream.

    :param signal: Input signal array.
    :param samples_per_bit: Number of samples per bit.
    :return: List of binary bits.
    """
    bit_stream = []
    for i in range(0, len(signal), samples_per_bit):
        bit = 1 if np.mean(signal[i:i + samples_per_bit]) > 0.4 else 0
        bit_stream.append(bit)
    return bit_stream


def ascii_to_binary_stream(string: str, length: int = 8) -> np.ndarray:
    """
    Convert an ASCII string to a binary stream.

    :param string: Input ASCII string.
    :param length: Length of each byte in bits. Default is 8.
    :return: Binary stream as a numpy array.
    """
    binary_stream = []
    for char in string:
        binary_stream.extend([int(bit) for bit in bin(ord(char))[2:].zfill(length)])
    return np.array(binary_stream)


def calculate_ber(original_bits: Union[np.ndarray, List[int]], received_bits: Union[np.ndarray, List[int]]) -> float:
    """
    Calculate the Bit Error Rate (BER) between two binary streams.

    :param original_bits: Original binary stream.
    :param received_bits: Received binary stream.
    :return: Bit Error Rate (BER) as a percentage.
    """
    _errors = np.sum(np.array(original_bits) != np.array(received_bits))
    ber = _errors / len(original_bits)
    return np.round(ber * 100, 2)
