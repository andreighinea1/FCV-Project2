import cv2

from src.preprocessing.base_preprocessor import Preprocessor


class MorphologicalFilter(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def apply_morphology(
        self, image, step_number=1, step_name="morphological_filtering"
    ):
        """
        Apply morphological filtering (e.g., dilation and erosion) to clean up the image.

        Args:
            image: Input image as a numpy array.
            step_number: Count of the debug step.
            step_name: Name for the debug step.

        Returns:
            Morphologically filtered image as a numpy array.
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        filtered_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        self.save_debug_image(filtered_image, step_name, step_number)
        return filtered_image
