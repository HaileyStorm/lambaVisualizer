import random
import numpy as np
from core.blc_to_lambda import blc_to_lambda
from core.image_generator import (generate_full_image, select_quadrant, flip_image,
                                  rotate_image, combine_images)
from utils.binary_utils import decimal_to_binary


class ImageLogic:
    def __init__(self, binary_digits=11):
        self.binary_digits = binary_digits
        self.images = [None, None]
        self.generate_new_images()

    def generate_random_image_params(self):
        value = random.randint(0, 2 ** self.binary_digits - 1)
        binary = decimal_to_binary(value, self.binary_digits)
        z_value = random.randint(0, 255)
        quadrant = random.randint(0, 3)
        flip = random.choice([True, False])
        rotation = random.choice([0, 90, 270])
        return binary, z_value, quadrant, flip, rotation

    def generate_new_images(self):
        image_params = [self.generate_random_image_params() for _ in range(4)]
        # TODO: For integrating with ML, will need to convert everything into a single value per image:
        # self.binary_digits will be 11. We can use 8 bits for the z value, 2 for selecting the quadrant, 2 for
        # selecting the rotation, and one for selecting whether to flip, for a total 16 bits, which we can treat
        # as an integer of the appropriate type/size. Then of course we'll need to be able to unpack from ML model /
        # whatever in order to get it into this image_params tuple we're using here.

        processed_images = []
        for binary, z_value, quadrant, flip, rotation in image_params:
            full_image = generate_full_image(binary, z_value)
            image = select_quadrant(full_image, quadrant)
            if flip:
                image = flip_image(image)
            image = rotate_image(image, rotation)
            processed_images.append(image)

        self.images[0] = combine_images(processed_images[:2], ['xor'])
        self.images[1] = combine_images(processed_images[2:], ['xor'])

    def select_image(self, index):
        self.generate_new_images()
        return self.images