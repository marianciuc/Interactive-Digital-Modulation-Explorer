import numpy as np


def decode_hamming_7_4(bits: np.array) -> np.array:
    result = np.array([], dtype=int)
    blocks = int(len(bits) // 7)
    syndrome = 0
    for i in range(blocks):
        block = bits[i * 7: (i + 1) * 7]

        x0 = np.mod(block[2] + block[4] + block[6], 2)
        x1 = np.mod(block[2] + block[5] + block[6], 2)
        x3 = np.mod(block[4] + block[5] + block[6], 2)

        _x0 = np.mod(block[0] + x0, 2)
        _x1 = np.mod(block[1] + x1, 2)
        _x3 = np.mod(block[3] + x3, 2)
        s = ((_x0 * 2 ** 0) + (_x1 * 2 ** 1) + (_x3 * 2 ** 2)) - 1

        if s > -1:
            syndrome += 1
            block[s] ^= 1
        result_block = [block[2], block[4], block[5], block[6]]
        result = np.append(result, result_block)

    return result, syndrome


def encode_hamming_7_4(bits: np.array) -> np.array:
    result = np.array([], dtype=int)
    blocks = int(len(bits) // 4)
    for i in range(0, blocks):
        block = bits[i * 4: (i + 1) * 4]
        result_block = [0, 0, block[0], 0, block[1], block[2], block[3]]
        x0 = np.mod(result_block[2] + result_block[4] + result_block[6], 2)
        x1 = np.mod(result_block[2] + result_block[5] + result_block[6], 2)
        x3 = np.mod(result_block[4] + result_block[5] + result_block[6], 2)

        result_block[0] = x0
        result_block[1] = x1
        result_block[3] = x3

        result = np.append(result, result_block)

    return result
