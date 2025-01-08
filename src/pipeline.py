import logging
import os

from src.preprocessing.binarization import Binarizer
from src.preprocessing.contrast_adjustment import ContrastAdjuster
from src.preprocessing.gradient_analysis import GradientAnalyzer
from src.preprocessing.morphological_filtering import MorphologicalFilter
from src.preprocessing.noise_reduction import NoiseReducer
from src.utils.io_operations import read_image, ensure_directory, save_image


def process_image(input_path, output_dir, debug=False):
    """
    Process a single image through all preprocessing steps.

    Args:
        input_path: Path to the input image.
        output_dir: Directory to save processed results.
        debug: If True, saves intermediate results for debugging.
    """
    # Ensure output directory exists
    ensure_directory(output_dir)

    # Read input image
    logging.info(f"Reading image from {input_path}")
    image = read_image(input_path)

    # Step 1: Noise Reduction
    noise_reducer = NoiseReducer(debug=debug)
    image = noise_reducer.apply_gaussian_blur(
        image, step_number=1, step_name="noise_reduction"
    )

    # Step 2: Contrast Adjustment
    contrast_adjuster = ContrastAdjuster(debug=debug)
    image = contrast_adjuster.adjust_contrast(
        image, step_number=2, step_name="contrast_adjustment"
    )

    # Step 3: Binarization
    binarizer = Binarizer(debug=debug)
    image = binarizer.apply_threshold(image, step_number=3, step_name="binarization")

    # Step 4: Morphological Filtering
    morphological_filter = MorphologicalFilter(debug=debug)
    image = morphological_filter.apply_morphology(
        image, step_number=4, step_name="morphological_filtering"
    )

    # Step 5: Gradient Analysis
    gradient_analyzer = GradientAnalyzer(debug=debug)
    image = gradient_analyzer.compute_gradients(
        image, step_number=5, step_name="gradient_analysis"
    )

    # Save the final processed image
    final_output_path = os.path.join(output_dir, "final_processed_image.png")
    save_image(image, final_output_path)
    logging.info(f"Final processed image saved at {final_output_path}")
