import cv2

from src.processing.base_preprocessor import Preprocessor
from src.utils.rectangle_merger import combine_rectangles


class TextHighlighter(Preprocessor):
    def __init__(
        self,
        min_area=100,
        max_area_ratio=0.1,
        threshold=10,
        debug=False,
        debug_dir="data/debug",
    ):
        super().__init__(debug, debug_dir)
        self.min_area = min_area
        self.max_area_ratio = max_area_ratio
        self.threshold = threshold

    def apply(self, image, mask, step_number):
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            mask, connectivity=8
        )
        rectangles = []

        for i in range(1, num_labels):
            x, y, w, h, area = (
                stats[i, cv2.CC_STAT_LEFT],
                stats[i, cv2.CC_STAT_TOP],
                stats[i, cv2.CC_STAT_WIDTH],
                stats[i, cv2.CC_STAT_HEIGHT],
                stats[i, cv2.CC_STAT_AREA],
            )

            if self.min_area <= area <= self.max_area_ratio * mask.size:
                rectangles.append((x, y, w, h))

        combined_rectangles = combine_rectangles(rectangles, self.threshold)

        for x, y, w, h in combined_rectangles:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.save_debug_image(image, "text_highlighting", step_number)
        return image
