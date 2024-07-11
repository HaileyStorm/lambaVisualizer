import numpy as np


def interpret_blc_vectorized(code, x, y, z):
    tokens = [code[i:i + 4] for i in range(0, len(code), 4)]
    result = np.zeros_like(x)

    for token in tokens:
        if token == '0000':
            result = (result + x) & 255
        elif token == '0001':
            result = (result + y) & 255
        elif token == '0010':
            result = (result + z) & 255
        elif token == '0011':
            result = (result * 2 + z) & 255
        elif token == '0100':
            result = (result // 2 + z) & 255
        elif token == '0101':
            result = (result * x + z) & 255
        elif token == '0110':
            result = (result * y + z) & 255
        elif token == '0111':
            result = (result * z) & 255
        elif token == '1000':
            result = (result ^ x) & 255
        elif token == '1001':
            result = (result ^ y) & 255
        elif token == '1010':
            result = (result ^ z) & 255
        elif token == '1011':
            result = np.cos(result * np.pi / 128 + z * np.pi / 128) * 127 + 128
        elif token == '1100':
            result = np.sin(result * np.pi / 128 + z * np.pi / 128) * 127 + 128
        elif token == '1101':
            result = np.abs(result - z) * 2
        elif token == '1110':
            result = np.minimum(result, z)
        elif token == '1111':
            result = np.maximum(result, z)
        result = result.astype(int)

    return result.astype(int)
