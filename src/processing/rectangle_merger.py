def combine_rectangles(rectangles, threshold=10):
    """
    Combine overlapping or close rectangles into larger rectangles and remove contained ones.

    Args:
        rectangles: List of rectangles as (x, y, w, h).
        threshold: Maximum distance between rectangles to combine.

    Returns:
        List of combined rectangles as (x, y, w, h).
    """

    def rectangles_overlap(r1, r2, threshold):
        """Check if two rectangles overlap or are close."""
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2

        return not (
            x1 > x2 + w2 + threshold
            or x2 > x1 + w1 + threshold
            or y1 > y2 + h2 + threshold
            or y2 > y1 + h1 + threshold
        )

    def combine_two_rectangles(r1, r2):
        """Combine two rectangles into one."""
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2

        min_x = min(x1, x2)
        min_y = min(y1, y2)
        max_x = max(x1 + w1, x2 + w2)
        max_y = max(y1 + h1, y2 + h2)

        return (min_x, min_y, max_x - min_x, max_y - min_y)

    merged = True
    while merged:
        merged = False
        new_rectangles = []

        while rectangles:
            r1 = rectangles.pop(0)

            for r2 in rectangles[:]:
                if rectangles_overlap(r1, r2, threshold):
                    r1 = combine_two_rectangles(r1, r2)
                    rectangles.remove(r2)
                    merged = True

            new_rectangles.append(r1)

        rectangles = new_rectangles

    # Remove contained rectangles
    final_rectangles = []
    for r1 in rectangles:
        x1, y1, w1, h1 = r1
        is_contained = False

        for r2 in rectangles:
            if r1 == r2:
                continue
            x2, y2, w2, h2 = r2
            if x1 >= x2 and y1 >= y2 and x1 + w1 <= x2 + w2 and y1 + h1 <= y2 + h2:
                is_contained = True
                break

        if not is_contained:
            final_rectangles.append(r1)

    return final_rectangles
