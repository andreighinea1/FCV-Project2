import logging

import cv2
import numpy as np

from src.preprocessing.base_preprocessor import Preprocessor


class DocumentDetector(Preprocessor):
    def __init__(self, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)

    def detect_and_warp(self, image, step_number=1, step_name="document_detection"):
        """
        Detect the document in the image and warp it to an A4 aspect ratio.

        Args:
            image: Input image as a numpy array.
            step_number: Count of the debug step.
            step_name: Name for the debug step.

        Returns:
            Warped image with an A4 aspect ratio.
        """
        # Step 1: Convert to LAB color space to separate light regions
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        self.save_debug_image(l, f"{step_name}_lightness", step_number)

        # Step 2: Threshold the lightness channel to isolate white areas
        # Adjust min value as needed
        _, mask = cv2.threshold(l, 150, 255, cv2.THRESH_BINARY)
        self.save_debug_image(mask, f"{step_name}_white_mask", step_number)

        # Step 3: Apply morphological operations to consolidate white regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(mask, kernel, iterations=2)
        eroded = cv2.erode(dilated, kernel, iterations=2)
        self.save_debug_image(eroded, f"{step_name}_morphology", step_number)

        # Step 4: Find contours in the white mask
        contours, _ = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        logging.info(f"Found {len(contours)} contours")

        # Step 5: Focus on the largest contour only
        largest_contour = contours[0]

        # Fit a minimum area rectangle
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)  # Get four corners of the rectangle
        box = np.array(box, dtype=int)  # Convert to integer type

        # Draw the rectangle for debugging
        debug_image = image.copy()
        cv2.drawContours(debug_image, [box], -1, (0, 255, 0), 2)  # Green rectangle
        self.save_debug_image(debug_image, f"{step_name}_min_area_rect", step_number)

        # Refine the rectangle
        aspect_ratio = max(rect[1]) / min(rect[1])
        if aspect_ratio < 1.0:
            aspect_ratio = 1 / aspect_ratio

        if aspect_ratio > 1.8 or aspect_ratio < 1.2:  # Check for A4-like aspect ratio
            raise ValueError("Detected rectangle does not resemble a document.")

        # Step 6: Warp perspective
        dst = np.array(
            [[0, 0], [2480, 0], [2480, 3508], [0, 3508]], dtype="float32"  # A4 size
        )
        matrix = cv2.getPerspectiveTransform(np.float32(box), dst)
        warped = cv2.warpPerspective(image, matrix, (2480, 3508))
        self.save_debug_image(warped, f"{step_name}_warped", step_number)

        return warped
