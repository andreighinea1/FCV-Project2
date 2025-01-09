import logging

import cv2
import numpy as np

from src.processing.base_preprocessor import Preprocessor


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
        inside_step = 1
        # Step 1: Convert to LAB color space to separate light regions
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        self.save_debug_image(l, f"{step_name}_{inside_step}_lightness", step_number)
        inside_step += 1

        # Step 2: Threshold the lightness channel to isolate white areas
        # Adjust min value as needed
        _, mask = cv2.threshold(l, 150, 255, cv2.THRESH_BINARY)
        self.save_debug_image(
            mask, f"{step_name}_{inside_step}_white_mask", step_number
        )
        inside_step += 1

        # Here I tried to use adaptive thresholding too, but it just didn't work...

        # Step 3: Apply morphological operations to consolidate white regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(mask, kernel, iterations=2)
        eroded = cv2.erode(dilated, kernel, iterations=2)
        self.save_debug_image(
            eroded, f"{step_name}_{inside_step}_morphology", step_number
        )
        inside_step += 1

        # Step 4: Find contours in the white mask
        contours, _ = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        logging.info(f"Found {len(contours)} contours")

        # Step 5: Focus on the largest contour only
        largest_contour = contours[0]

        # Draw the largest contour for debugging, with green
        debug_image_contour = image.copy()
        cv2.drawContours(debug_image_contour, [largest_contour], -1, (0, 255, 0), 3)
        self.save_debug_image(
            debug_image_contour,
            f"{step_name}_{inside_step}_largest_contour",
            step_number,
        )
        inside_step += 1

        # Step 6: Approximate a quadrilateral from the contour
        perimeter = cv2.arcLength(largest_contour, True)
        epsilon = 0.02 * perimeter  # Adjust this value if needed
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        if len(approx) == 4:  # Valid quadrilateral found
            quad = approx.reshape(4, 2)
        else:  # Fallback to minimum area rectangle
            rect = cv2.minAreaRect(largest_contour)
            quad = cv2.boxPoints(rect)
            quad = np.array(quad, dtype=int)

        # Draw the approximated quadrilateral for debugging, in blue
        debug_image_quad = image.copy()
        cv2.drawContours(debug_image_quad, [np.int32(quad)], -1, (255, 0, 0), 3)
        self.save_debug_image(
            debug_image_quad,
            f"{step_name}_{inside_step}_approximated_quad",
            step_number,
        )
        inside_step += 1

        # Step 7: Warp perspective using the approximated quadrilateral
        rect = self.order_points(quad)  # Order the points consistently
        dst = np.array(
            [[0, 0], [2480, 0], [2480, 3508], [0, 3508]], dtype="float32"  # A4 size
        )
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (2480, 3508))
        self.save_debug_image(warped, f"{step_name}_{inside_step}_warped", step_number)

        return warped, rect

    @staticmethod
    def order_points(pts):
        """
        Order points in a consistent manner: top-left, top-right, bottom-right, bottom-left.
        """
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect
