import logging

import cv2

from src.processing.base_preprocessor import Preprocessor


class ColorSpaceConverter(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def apply(self, image, step_number):
        logging.info("Converting to LAB color space...")
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        self.save_debug_image(l, "lightness_channel", step_number)
        return l, a, b
