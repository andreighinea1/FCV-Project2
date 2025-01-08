import logging
import os

from src.pipeline import process_image

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

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process all images in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            logging.info(f"Processing {input_path}...")
            try:
                process_image(input_path, output_dir, debug=debug_mode)
            except Exception as e:
                logging.error(f"Error processing {input_path}: {e}")
