import numpy as np
from core.blc_interpreter import interpret_blc


def generate_full_image(binary_value, z_value):
    width, height = 256, 256
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    result = interpret_blc_vectorized(binary_value, x, y, z_value)

    image = np.stack([
        result,
        (x + result) & 255,
        (y + result) & 255
    ], axis=-1).astype(np.uint8)

    return image


def interpret_blc_vectorized(code, x, y, z):
    tokens = [code[i:i + 2] for i in range(0, len(code), 2)]
    result = np.zeros_like(x)

    for token in tokens:
        if token == '0':
            result = (result + x) & 255
        elif token == '1':
            result = (result + y) & 255
        elif token == '00':
            result = (result + z) & 255
        elif token == '01':
            result = (result * 2) & 255
        elif token == '10':
            pass  # Identity function
        elif token == '11':
            result = (result ^ (x * y)) & 255
        else:
            result = (result ^ z) & 255

    return result


def select_quadrant(full_image, quadrant):
    height, width = full_image.shape[:2]
    half_h, half_w = height // 2, width // 2
    if quadrant == 0:
        return full_image[:half_h, :half_w]
    elif quadrant == 1:
        return full_image[:half_h, half_w:]
    elif quadrant == 2:
        return full_image[half_h:, :half_w]
    else:
        return full_image[half_h:, half_w:]


def flip_image(image):
    return np.flip(image, axis=1)  # Flip across y-axis


def rotate_image(image, rotation):
    return np.rot90(image, k=rotation // 90)


def combine_images(images, operations):
    result = images[0]
    for i, op in enumerate(operations):
        if op == 'xor':
            result = np.bitwise_xor(result, images[i + 1])
        elif op == 'or':
            result = np.bitwise_or(result, images[i + 1])
        elif op == 'and':
            result = np.bitwise_and(result, images[i + 1])
    return result