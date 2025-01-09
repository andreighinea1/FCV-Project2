import cv2
import numpy as np
import os


def adjust_canny():
    """
    Interactively adjust the Canny edge detection thresholds for a given image.
    """
    # Ask the user to select an image
    input_dir = "../data/input"
    images = [
        f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))
    ]

    if not images:
        print("No images found in the input directory!")
        return

    print("Available images:")
    for idx, img_name in enumerate(images):
        print(f"{idx}: {img_name}")

    try:
        selected_idx = int(input("Enter the number of the image you want to test: "))
        if selected_idx < 0 or selected_idx >= len(images):
            print("Invalid selection.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    image_path = os.path.join(input_dir, images[selected_idx])
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Resize image to fit the screen
    def resize_image(img, width=900):
        """Resize image to fit within the specified width while maintaining aspect ratio."""
        h, w = img.shape[:2]
        scale = width / w
        resized = cv2.resize(img, (width, int(h * scale)))
        return resized

    # Preprocessing for consistent lighting
    def normalize_lighting(img):
        """Automatically adjust lighting to normalize brightness and contrast."""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the L-channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        # Merge back and convert to BGR
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Normalize lighting
    image = normalize_lighting(image)

    # Convert to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Create a combined display for original and edges
    def create_combined_display(original, edges):
        """Merge original and edge-detection images side-by-side."""
        original_resized = resize_image(original)
        edges_resized = resize_image(edges, width=original_resized.shape[1])
        combined = np.hstack(
            (original_resized, cv2.cvtColor(edges_resized, cv2.COLOR_GRAY2BGR))
        )
        return combined

    # Interactive function to adjust thresholds
    def on_change(_):
        t1 = cv2.getTrackbarPos("Threshold1", "Canny Adjust")
        t2 = cv2.getTrackbarPos("Threshold2", "Canny Adjust")
        edges = cv2.Canny(blurred, t1, t2)
        combined = create_combined_display(image, edges)
        cv2.imshow("Canny Adjust", combined)

    # Create interactive window
    cv2.namedWindow("Canny Adjust")
    cv2.createTrackbar("Threshold1", "Canny Adjust", 50, 300, on_change)
    cv2.createTrackbar("Threshold2", "Canny Adjust", 150, 300, on_change)
    on_change(0)  # Initialize with default thresholds

    # Wait for user interaction
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    adjust_canny()
