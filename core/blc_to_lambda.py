def blc_to_lambda(code):
    tokens = [code[i:i+4] for i in range(0, len(code), 4)]
    expr = 'λx.λy.λz.'
    for token in tokens:
        if token == '0000': expr += '(λw.w+x)'
        elif token == '0001': expr += '(λw.w+y)'
        elif token == '0010': expr += '(λw.w+z)'
        elif token == '0011': expr += '(λw.w*2+z)'
        elif token == '0100': expr += '(λw.w/2+z)'
        elif token == '0101': expr += '(λw.w*x+z)'
        elif token == '0110': expr += '(λw.w*y+z)'
        elif token == '0111': expr += '(λw.w*z)'
        elif token == '1000': expr += '(λw.w^x)'
        elif token == '1001': expr += '(λw.w^y)'
        elif token == '1010': expr += '(λw.w^z)'
        elif token == '1011': expr += '(λw.cos(w*π/128+z*π/128)*127+128)'
        elif token == '1100': expr += '(λw.sin(w*π/128+z*π/128)*127+128)'
        elif token == '1101': expr += '(λw.abs(w-z)*2)'
        elif token == '1110': expr += '(λw.min(w,z))'
        elif token == '1111': expr += '(λw.max(w,z))'
    return expr