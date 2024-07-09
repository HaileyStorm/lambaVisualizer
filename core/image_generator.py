import numpy as np
from core.blc_interpreter import interpret_blc


def generate_image(binary_value, z_value):
    width, height = 256, 256
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            result = interpret_blc(binary_value, x, y, z_value)
            image[y, x] = [result, (x + result) & 255, (y + result) & 255]

    return image