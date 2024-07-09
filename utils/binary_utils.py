def binary_to_decimal(binary):
    return int(binary, 2)

def decimal_to_binary(decimal, digits):
    return format(decimal, f'0{digits}b')