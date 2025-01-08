import os

from preprocessing.noise_reduction import NoiseReducer
from utils.io_operations import save_image, read_image, ensure_directory


def process_image(input_path, output_dir, debug=False):
    """
    Process a single image by applying noise reduction.

    Args:
        input_path: Path to the input image.
        output_dir: Directory to save processed results.
        debug: If True, saves intermediate results for debugging.
    """
    # Ensure the output directory exists
    ensure_directory(output_dir)

    # Read the image
    image = read_image(input_path)

    # Initialize NoiseReducer
    noise_reducer = NoiseReducer(debug=debug)

    # Apply Gaussian Blur
    processed_image = noise_reducer.apply_gaussian_blur(image)

    # Save the final processed image
    save_image(processed_image, os.path.join(output_dir, "processed_image.png"))
