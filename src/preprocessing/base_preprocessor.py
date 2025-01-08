import os

from src.utils.io_operations import save_image


class Preprocessor:
    def __init__(self, debug=False, debug_dir="data/debug"):
        """
        Base class for all preprocessors.

        Args:
            debug: If True, saves intermediate images for debugging.
            debug_dir: Directory to save debug images.
        """
        self.debug = debug
        self.debug_dir = debug_dir
        if self.debug:
            os.makedirs(self.debug_dir, exist_ok=True)

    def save_debug_image(self, image, step_name):
        """
        Save an intermediate image if debug mode is enabled.

        Args:
            image: The image to save.
            step_name: Name for the debug step.
        """
        if self.debug:
            debug_path = os.path.join(self.debug_dir, f"intermediate_{step_name}.png")
            save_image(image, debug_path)
