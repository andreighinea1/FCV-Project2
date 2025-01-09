import logging
import os

import cv2

from src.preprocessing.document_detection import DocumentDetector
from src.utils.io_operations import read_image, ensure_directory, save_image


def process_image(input_path, output_dir, debug=False):
    """
    Process a single image through all preprocessing steps.

    Args:
        input_path: Path to the input image.
        output_dir: Directory to save processed results.
        debug: If True, saves intermediate results for debugging.
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
    inside_step = 1
    cropped_image, warping_rect = document_detector.detect_and_warp(
        image, step_number=inside_step, step_name="document_detection"
    )
    inside_step += 1

    # Step 2: Convert to LAB color space to separate light regions
    logging.info("Converting to LAB color space...")
    lab = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    if debug:
        save_image(l, os.path.join(debug_dir, f"{inside_step}_lightness.png"))
    inside_step += 1

    # Step 3: Threshold the lightness channel to isolate white areas
    logging.info("Thresholding the lightness channel...")
    _, mask = cv2.threshold(l, 150, 255, cv2.THRESH_BINARY)
    if debug:
        save_image(mask, os.path.join(debug_dir, f"{inside_step}_white_mask.png"))
    inside_step += 1

    # Step 4: Apply morphological operations to consolidate white regions
    logging.info("Applying morphological operations...")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(mask, kernel, iterations=2)
    eroded = cv2.erode(dilated, kernel, iterations=2)
    if debug:
        save_image(eroded, os.path.join(debug_dir, f"{inside_step}_morphology.png"))
    inside_step += 1

    # Step 5: Use the resulting image as a mask to fill in the whites of the image
    logging.info("Filling in the whites of the image...")
    filled_white = cv2.bitwise_and(cropped_image, cropped_image, mask=eroded)
    inverted_mask = cv2.bitwise_not(eroded)
    white_background = cv2.add(
        filled_white, cv2.cvtColor(inverted_mask, cv2.COLOR_GRAY2BGR)
    )
    if debug:
        save_image(
            white_background, os.path.join(debug_dir, f"{inside_step}_cleaned.png")
        )
    inside_step += 1

    # Save the final result
    final_output_path = os.path.join(output_dir, f"{image_name}_processed_cropped.png")
    save_image(white_background, final_output_path)
    logging.info(f"Processed cropped image saved at {final_output_path}")
