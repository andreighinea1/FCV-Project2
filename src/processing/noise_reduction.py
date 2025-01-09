import cv2

from src.processing.base_preprocessor import Preprocessor


class NoiseReducer(Preprocessor):
    def __init__(self, kernel_size=(5, 5), debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)
        self.kernel_size = kernel_size

    def apply(self, image, step_number):
        blurred = cv2.GaussianBlur(image, self.kernel_size, 0)
        self.save_debug_image(blurred, "noise_reduction", step_number)
        return blurred
