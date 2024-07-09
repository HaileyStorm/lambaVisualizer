def blc_to_lambda(code):
    tokens = [code[i:i+2] for i in range(0, len(code), 2)]
    expr = 'λx.λy.λz.'
    for token in tokens:
        if token == '0': expr += 'x'
        elif token == '1': expr += 'y'
        elif token == '00': expr += 'z'
        elif token == '01': expr += '(λw.w+w)'
        elif token == '10': expr += '(λw.w)'
        elif token == '11': expr += '(x*y)'
        else: expr += '(x^y^z)'
    return expr