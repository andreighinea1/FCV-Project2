import cv2

from src.preprocessing.base_preprocessor import Preprocessor


class Binarizer(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def apply_threshold(self, image, step_name="binarization"):
        """
        Apply adaptive thresholding to binarize the image.

        Args:
            image: Input image as a numpy array.
            step_name: Name for the debug step.

        Returns:
            Binarized image as a numpy array.
        """
        if len(image.shape) == 3:  # Convert to grayscale if it's a color image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        binarized_image = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        self.save_debug_image(binarized_image, step_name)
        return binarized_image
