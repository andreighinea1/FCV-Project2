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
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.save_debug_image(gray, f"{step_name}_grayscale", step_number)

        # Step 2: Apply Gaussian blur to suppress noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self.save_debug_image(blurred, f"{step_name}_blurred", step_number)

        # Step 3: Adaptive thresholding for better separation of foreground and background
        thresholded = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        self.save_debug_image(thresholded, f"{step_name}_thresholded", step_number)

        # Step 4: Find contours
        contours, _ = cv2.findContours(
            thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Step 5: Find the largest contour that resembles a quadrilateral
        page_contour = None
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4:  # Looking for quadrilaterals
                area = cv2.contourArea(approx)
                _, _, w, h = cv2.boundingRect(approx)
                aspect_ratio = max(w, h) / min(w, h)

                # Adjust thresholds
                if area > 0.5 * gray.size and 1.3 < aspect_ratio < 1.8:
                    page_contour = approx
                    break

        if page_contour is None:
            raise ValueError("No valid quadrilateral detected in the image.")

        # Draw the detected quadrilateral for debugging with a green outline
        debug_image = image.copy()
        cv2.drawContours(debug_image, [page_contour], -1, (0, 255, 0), 5)
        self.save_debug_image(debug_image, f"{step_name}_outline", step_number)

        # Step 6: Warp perspective
        pts = page_contour.reshape(4, 2)
        rect = self.order_points(pts)
        dst = np.array(
            [[0, 0], [2480, 0], [2480, 3508], [0, 3508]], dtype="float32"  # A4 size
        )
        matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, matrix, (2480, 3508))
        self.save_debug_image(warped, f"{step_name}_warped", step_number)

        return warped

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
