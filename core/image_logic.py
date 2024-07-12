import random
from core.image_generator import (generate_full_image, select_quadrant, flip_image,
                                  rotate_image, combine_images)
from utils.binary_utils import decimal_to_binary
from core.ml_model import ImageParamModel

class ImageLogic:
    def __init__(self, binary_digits=11):
        self.binary_digits = binary_digits
        self.images = [None, None]
        self.model = ImageParamModel()
        self.current_seed = self.generate_random_seed()
        self.seed_iteration = 0
        self.max_seed_iterations = 10
        self.generate_new_images()

    def generate_random_seed(self):
        return random.randint(0, 2**32 - 1)

    def generate_new_images(self):
        if self.seed_iteration >= self.max_seed_iterations:
            self.current_seed = self.generate_random_seed()
            self.seed_iteration = 0
        self.seed_iteration += 1

        image_params = self.model.generate_params(self.current_seed)
        processed_images = []
        for params in image_params:
            #print(params)
            binary, z_value, quadrant, flip, rotation = self.convert_output_to_image_params(params)
            #print(binary, z_value, quadrant, flip, rotation)
            full_image = generate_full_image(binary, z_value)
            image = select_quadrant(full_image, quadrant)
            if flip:
                image = flip_image(image)
            image = rotate_image(image, rotation)
            processed_images.append(image)

        self.images[0] = combine_images(processed_images[:2], ['xor'])
        self.images[1] = combine_images(processed_images[2:], ['xor'])

    def convert_output_to_image_params(self, output):
        binary_val = int(output[:11].sum() * (2 ** self.binary_digits - 1))
        binary = decimal_to_binary(binary_val, self.binary_digits)
        z_value = int(output[11:19].sum() * 255)  # Sum 8 values and scale to 0-255
        quadrant = int(output[19:21].sum() * 3)
        flip = output[21] > 0.5

        # Use last two bits for rotation
        rotation_val = int(output[22] > 0.5) + 2 * int(output[23] > 0.5)
        rotation_map = {0: 0, 1: 90, 2: 270, 3: 0}
        rotation = rotation_map[rotation_val]

        return binary, z_value, quadrant, flip, rotation

    def select_image(self, index):
        self.model.update_model(index)
        self.generate_new_images()
        return self.images