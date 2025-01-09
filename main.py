import logging
import os
import shutil

from src.pipeline import process_image
from src.utils.io_operations import ensure_directory

if __name__ == "__main__":
    BYPASS = True  # Assume user gives "y" input below

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Define input and output directories
    input_dir = "data/input"
    output_dir = "data/output"
    debug_dir = "data/debug"

    # Debug mode flag
    debug_mode = True

    # Remove the debug directory if it exists
    if os.path.exists(debug_dir):
        logging.info(f"Removing existing debug directory: {debug_dir}")
        shutil.rmtree(debug_dir)

    # Check if output directory exists and contains files
    if os.path.exists(output_dir) and os.listdir(output_dir):
        if BYPASS:
            user_input = "y"
        else:
            user_input = (
                input(
                    f"The output directory '{output_dir}' is not empty. Do you want to remove it? (y/n): "
                )
                .strip()
                .lower()
            )
        if user_input == "y":
            logging.info(f"Removing output directory: {output_dir}")
            shutil.rmtree(output_dir)
        else:
            logging.error(f"Output directory '{output_dir}' must be empty to start.")
            exit(1)

    # Recreate the output and debug directories
    ensure_directory(output_dir)
    ensure_directory(debug_dir)

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
