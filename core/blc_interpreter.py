import numpy as np


def interpret_blc_vectorized(code, x, y, z):
    tokens = [code[i:i + 3] for i in range(0, len(code), 3)]
    result = np.zeros_like(x)

    for token in tokens:
        if token == '000':
            result = (result + x) & 255
        elif token == '001':
            result = (result + y) & 255
        elif token == '010':
            result = (result + z) & 255
        elif token == '011':
            result = (result * 2) & 255
        elif token == '100':
            result = (result // 2) & 255
        elif token == '101':
            result = (result * x) & 255
        elif token == '110':
            result = (result * y) & 255
        elif token == '111':
            result = (result * z) & 255
        elif token == '00':
            result = (result ^ x) & 255
        elif token == '01':
            result = (result ^ y) & 255
        elif token == '10':
            result = (result ^ z) & 255
        elif token == '11':
            result = (~result) & 255
        else:
            result = (result + 1) & 255

    return result