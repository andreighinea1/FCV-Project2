import logging

import cv2

from src.processing.base_preprocessor import Preprocessor


class MorphologicalProcessor(Preprocessor):
    def __init__(
        self,
        open_kernel=(5, 5),
        close_kernel=(2, 2),
        debug=False,
        debug_dir="data/debug",
    ):
        super().__init__(debug, debug_dir)
        self.open_kernel = open_kernel
        self.close_kernel = close_kernel

    def apply(self, mask, step_number):
        logging.info("Removing small black dots with morphological opening...")
        opened = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_RECT, self.open_kernel),
        )
        self.save_debug_image(opened, "morph_opening", step_number)

        logging.info("Enlarging black regions with morphological closing...")
        closed = cv2.morphologyEx(
            opened,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_RECT, self.close_kernel),
        )
        self.save_debug_image(closed, "morph_closing", step_number)

        return closed
