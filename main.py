import logging
import os

from src.pipeline import process_image
from src.utils.io_operations import ensure_directory

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Define input and output directories
    input_dir = "data/input"
    output_dir = "data/output"

    # Debug mode flag
    debug_mode = True

    # Ensure output directory exists
    ensure_directory(output_dir)

    # Get all files in the input directory
    input_files = [
        f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))
    ]

    # Check if there are no files to process
    if not input_files:
        logging.info("No files detected in the input directory!")
    else:
        # Process all images in the input directory
        for filename in input_files:
            input_path = os.path.join(input_dir, filename)
            logging.info(f"Processing {input_path}...")
            try:
                process_image(input_path, output_dir, debug=debug_mode)
            except Exception as e:
                logging.error(f"Error processing {input_path}: {e}")
