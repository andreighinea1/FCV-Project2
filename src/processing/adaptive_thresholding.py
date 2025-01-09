import logging

import cv2

from src.processing.base_preprocessor import Preprocessor


class AdaptiveThresholder(Preprocessor):
    def __init__(self, block_size=21, C=10, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)
        self.block_size = block_size
        self.C = C

    def apply(self, lightness_channel, step_number):
        logging.info("Applying adaptive thresholding...")
        adaptive_mask = cv2.adaptiveThreshold(
            lightness_channel,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=self.block_size,
            C=self.C,
        )
        self.save_debug_image(adaptive_mask, "adaptive_thresholding", step_number)
        return adaptive_mask
