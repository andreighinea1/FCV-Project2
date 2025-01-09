import logging
import os

from src.processing.adaptive_thresholding import AdaptiveThresholder
from src.processing.color_space_conversion import ColorSpaceConverter
from src.processing.document_detection import DocumentDetector
from src.processing.mask_filling import MaskFiller
from src.processing.morphological_processing import MorphologicalProcessor
from src.processing.noise_reduction import NoiseReducer
from src.processing.text_highlighting import TextHighlighter
from src.utils.io_operations import read_image, ensure_directory, save_image


def process_image(
    input_path,
    output_dir,
    debug=False,
    force_black_text=False,
    highlight_text_regions=False,
):
    """
    Process a single image through all preprocessing steps.

    Args:
        input_path: Path to the input image.
        output_dir: Directory to save processed results.
        debug: If True, saves intermediate results for debugging.
        force_black_text: If True, replaces text color with black instead of keeping the original.
        highlight_text_regions: If True, it highlights text regions.
    """
    # Read input image
    logging.info(f"Reading image from {input_path}")
    image = read_image(input_path)
    image_name = os.path.splitext(os.path.basename(input_path))[0]

    # Define a custom debug directory for the current image
    debug_dir = os.path.join("data", "debug", image_name)
    if debug:
        ensure_directory(debug_dir)

    # Step 1: Document Detection (Cropped A4 Image)
    document_detector = DocumentDetector(debug=debug, debug_dir=debug_dir)
    cropped_image, warping_rect = document_detector.detect_and_warp(
        image, step_number=1
    )

    # Step 2: Noise Reduction
    noise_reducer = NoiseReducer(kernel_size=(5, 5), debug=debug, debug_dir=debug_dir)
    cropped_image = noise_reducer.apply(cropped_image, step_number=2)

    # Step 3: Convert to LAB color space to separate light regions
    color_converter = ColorSpaceConverter(debug=debug, debug_dir=debug_dir)
    l, a, b = color_converter.apply(cropped_image, step_number=3)

    # Step 4: Apply adaptive thresholding on the lightness channel
    thresholder = AdaptiveThresholder(
        block_size=21, C=10, debug=debug, debug_dir=debug_dir
    )
    adaptive_mask = thresholder.apply(l, step_number=4)

    # Step 5: Morphological Opening
    morph_processor = MorphologicalProcessor(
        open_kernel=(5, 5), close_kernel=(2, 2), debug=debug, debug_dir=debug_dir
    )
    final_mask = morph_processor.apply(adaptive_mask, step_number=5)

    # Tried using connected components and contour filtering to remove black dots here, without succeeding...

    # Step 6: Mask Filling
    mask_filler = MaskFiller(
        force_black_text=force_black_text, debug=debug, debug_dir=debug_dir
    )
    text_white_background = mask_filler.apply(cropped_image, final_mask, step_number=6)

    # Step 7: Additional Noise Reduction
    noise_reducer = NoiseReducer(kernel_size=(5, 5), debug=debug, debug_dir=debug_dir)
    blurred = noise_reducer.apply(text_white_background, step_number=7)

    # Step 8: Text Highlighting
    final_image = blurred
    if highlight_text_regions:
        text_highlighter = TextHighlighter(
            min_area=100,
            max_area_ratio=0.1,
            threshold=10,
            debug=debug,
            debug_dir=debug_dir,
        )
        final_image = text_highlighter.apply(final_image, final_mask, step_number=8)

    # Save the final result
    final_output_path = os.path.join(output_dir, f"{image_name}_processed_cropped.png")
    save_image(final_image, final_output_path)
    logging.info(f"Processed cropped image saved at {final_output_path}")
