def blc_to_lambda(code):
    tokens = [code[i:i+3] for i in range(0, len(code), 3)]
    expr = 'λx.λy.λz.'
    for token in tokens:
        if token == '000': expr += '(λw.w+x)'
        elif token == '001': expr += '(λw.w+y)'
        elif token == '010': expr += '(λw.w+z)'
        elif token == '011': expr += '(λw.w*2)'
        elif token == '100': expr += '(λw.w/2)'
        elif token == '101': expr += '(λw.w*x)'
        elif token == '110': expr += '(λw.w*y)'
        elif token == '111': expr += '(λw.w*z)'
        elif token == '00': expr += '(λw.w^x)'
        elif token == '01': expr += '(λw.w^y)'
        elif token == '10': expr += '(λw.w^z)'
        elif token == '11': expr += '(λw.¬w)'
        else: expr += '(λw.w+1)'
    return expr