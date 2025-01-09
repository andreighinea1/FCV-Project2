import logging
import os

import cv2

from src.processing.document_detection import DocumentDetector
from src.utils.rectangle_merger import combine_rectangles
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
    inside_step = 1
    cropped_image, warping_rect = document_detector.detect_and_warp(
        image, step_number=inside_step, step_name="document_detection"
    )
    inside_step += 1

    # Step 2: Noise Reduction
    logging.info("Applying noise reduction...")
    cropped_image = cv2.GaussianBlur(cropped_image, (5, 5), 0)
    if debug:
        save_image(
            cropped_image, os.path.join(debug_dir, f"{inside_step}_noise_reduction.png")
        )
    inside_step += 1

    # Step 3: Convert to LAB color space to separate light regions
    logging.info("Converting to LAB color space...")
    lab = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    if debug:
        save_image(l, os.path.join(debug_dir, f"{inside_step}_lightness.png"))
    inside_step += 1

    # Step 4: Apply adaptive thresholding on the lightness channel
    logging.info("Applying adaptive thresholding...")
    adaptive_mask = cv2.adaptiveThreshold(
        l, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=21, C=10
    )
    if debug:
        save_image(
            adaptive_mask, os.path.join(debug_dir, f"{inside_step}_adaptive_mask.png")
        )
    inside_step += 1

    # Step 5: Remove small black dots using morphological opening
    logging.info("Removing small black dots with morphological opening...")
    small_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened_mask = cv2.morphologyEx(adaptive_mask, cv2.MORPH_OPEN, small_kernel)
    if debug:
        save_image(
            opened_mask, os.path.join(debug_dir, f"{inside_step}_morph_opening.png")
        )
    inside_step += 1

    # Step 6: Enlarge black regions using morphological closing
    logging.info("Enlarging black regions with morphological closing...")
    large_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    closed_mask = cv2.morphologyEx(opened_mask, cv2.MORPH_CLOSE, large_kernel)
    if debug:
        save_image(
            closed_mask, os.path.join(debug_dir, f"{inside_step}_morph_closing.png")
        )
    inside_step += 1
    final_mask = closed_mask

    # Tried using connected components and contour filtering to remove black dots here, without succeeding...

    # Step 7: Use the resulting image as a mask to fill in the whites of the image
    logging.info("Filling in the whites of the image...")
    inverted_mask = cv2.bitwise_not(final_mask)
    text_img = cv2.bitwise_and(cropped_image, cropped_image, mask=inverted_mask)

    # Optionally replace text with Obsidian black
    if force_black_text:
        logging.info("Replacing text with Obsidian black (#0B1215)...")
        gray_text = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
        text_img = cv2.merge((gray_text, gray_text, gray_text))  # Grayscale text
        # Replace all non-white pixels with Obsidian black
        text_img[gray_text < 255] = [11, 18, 21]

    text_white_background = cv2.add(
        text_img, cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)
    )
    if debug:
        save_image(
            text_white_background, os.path.join(debug_dir, f"{inside_step}_cleaned.png")
        )
    inside_step += 1

    # Step 8: More Noise Reduction
    logging.info("Applying more noise reduction...")
    blurred = cv2.GaussianBlur(text_white_background, (5, 5), 0)
    if debug:
        save_image(
            blurred, os.path.join(debug_dir, f"{inside_step}_noise_reduction.png")
        )
    inside_step += 1

    # Step 9: Detect and highlight text regions (if enabled)
    highlighted = blurred
    if highlight_text_regions:
        logging.info("Detecting and highlighting text regions...")

        # Use connected component analysis for text detection
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            inverted_mask, connectivity=8
        )

        # Filtering parameters (min and max area for text regions)
        min_area = 100
        max_area = 0.1 * inverted_mask.size

        # Collect all rectangles
        rectangles = []
        for i in range(1, num_labels):  # Skip the background (label 0)
            x, y, w, h, area = (
                stats[i, cv2.CC_STAT_LEFT],
                stats[i, cv2.CC_STAT_TOP],
                stats[i, cv2.CC_STAT_WIDTH],
                stats[i, cv2.CC_STAT_HEIGHT],
                stats[i, cv2.CC_STAT_AREA],
            )

            # Apply filtering criteria
            if min_area <= area <= max_area:
                rectangles.append((x, y, w, h))

        # Combine overlapping or close rectangles
        combined_rectangles = combine_rectangles(rectangles, threshold=10)

        # Draw the combined rectangles on the blurred image
        for x, y, w, h in combined_rectangles:
            cv2.rectangle(highlighted, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if debug:
        save_image(
            highlighted, os.path.join(debug_dir, f"{inside_step}_highlighted.png")
        )
    inside_step += 1
    final_image = highlighted

    # Save the final result
    final_output_path = os.path.join(output_dir, f"{image_name}_processed_cropped.png")
    save_image(final_image, final_output_path)
    logging.info(f"Processed cropped image saved at {final_output_path}")
