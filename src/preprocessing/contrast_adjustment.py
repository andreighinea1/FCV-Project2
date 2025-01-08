import cv2

from src.preprocessing.base_preprocessor import Preprocessor


class ContrastAdjuster(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def adjust_contrast(self, image, step_number=1, step_name="contrast_adjustment"):
        """
        Adjust the contrast of the input image using histogram equalization.

        Args:
            image: Input image as a numpy array.
            step_number: Count of the debug step.
            step_name: Name for the debug step.

        Returns:
            Contrast-enhanced image as a numpy array.
        """
        if len(image.shape) == 3:  # Convert to grayscale if it's a color image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        enhanced_image = cv2.equalizeHist(image)
        self.save_debug_image(enhanced_image, step_name, step_number)
        return enhanced_image
