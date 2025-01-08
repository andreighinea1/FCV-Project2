import cv2

from src.preprocessing.base_preprocessor import Preprocessor


class GradientAnalyzer(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def compute_gradients(self, image, step_name="gradient_analysis"):
        """
        Compute image gradients using Sobel operators.

        Args:
            image: Input image as a numpy array.
            step_name: Name for the debug step.

        Returns:
            Image gradients as a numpy array.
        """
        if len(image.shape) == 3:  # Convert to grayscale if it's a color image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = cv2.magnitude(grad_x, grad_y)
        normalized_magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        self.save_debug_image(normalized_magnitude.astype("uint8"), step_name)
        return normalized_magnitude.astype("uint8")
