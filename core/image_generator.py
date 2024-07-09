import numpy as np
from core.blc_interpreter import interpret_blc


def generate_full_image(binary_value, z_value):
    width, height = 256, 256
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            result = interpret_blc(binary_value, x, y, z_value)
            image[y, x] = [result, (x + result) & 255, (y + result) & 255]

    return image


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