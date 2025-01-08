import os

import cv2


def read_image(file_path):
    """
    Read an image from a given path.

    Args:
        file_path: Path to the input image.

    Returns:
        Image as a numpy array.
    """
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image at {file_path}")
    return image


def save_image(image, output_path):
    """
    Save an image to the given path.

    Args:
        image: Image as a numpy array.
        output_path: Path to save the image.
    """
    cv2.imwrite(output_path, image)
    print(f"Image saved at {output_path}")


def ensure_directory(directory_path):
    """
    Ensure a directory exists. Create it if it doesn't.

    Args:
        directory_path: Path to the directory.
    """
    os.makedirs(directory_path, exist_ok=True)
