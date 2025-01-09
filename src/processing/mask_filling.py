import logging

import cv2

from src.processing.base_preprocessor import Preprocessor


class MaskFiller(Preprocessor):
    def __init__(self, force_black_text=False, debug=False, debug_dir="data/debug"):
        super().__init__(debug, debug_dir)
        self.force_black_text = force_black_text

    def apply(self, cropped_image, mask, step_number):
        logging.info("Filling in the whites of the image...")
        inverted_mask = cv2.bitwise_not(mask)
        text_img = cv2.bitwise_and(cropped_image, cropped_image, mask=inverted_mask)

        if self.force_black_text:
            logging.info("Replacing text with Obsidian black (#0B1215)...")
            gray_text = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
            text_img = cv2.merge((gray_text, gray_text, gray_text))
            text_img[gray_text < 255] = [11, 18, 21]

        filled_image = cv2.add(text_img, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))
        self.save_debug_image(filled_image, "mask_filling", step_number)

        return filled_image
