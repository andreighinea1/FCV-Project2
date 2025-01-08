import cv2

from src.preprocessing.base_preprocessor import Preprocessor


class NoiseReducer(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        """
        Noise reduction processor inheriting from Preprocessor.

        Args:
            debug: If True, saves intermediate images for debugging.
            debug_dir: Directory to save debug images.
        """
        super().__init__(debug, debug_dir)

    def apply_gaussian_blur(self, image, step_number=1, step_name="noise_reduction"):
        """
        Apply Gaussian Blur to reduce noise.

        Args:
            image: Input image as a numpy array.
            step_number: Count of the debug step.
            step_name: Name for the debug step.

        Returns:
            Blurred image as a numpy array.
        """
        blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
        self.save_debug_image(blurred_image, step_name, step_number)
        return blurred_image
