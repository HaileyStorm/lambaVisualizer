def interpret_blc(code, x, y, z):
    tokens = [code[i:i+2] for i in range(0, len(code), 2)]
    result = 0
    for token in tokens:
        if token == '0': result = (result + x) & 255
        elif token == '1': result = (result + y) & 255
        elif token == '00': result = (result + z) & 255
        elif token == '01': result = (result * 2) & 255
        elif token == '10': result = result  # Identity function
        elif token == '11': result = (result ^ (x * y)) & 255
        else: result = (result ^ z) & 255
    return result