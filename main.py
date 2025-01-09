import argparse
import logging
import os
import shutil

from src.pipeline import process_image
from src.utils.io_operations import ensure_directory


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Document image processing pipeline.")
    parser.add_argument(
        "--input_dir",
        type=str,
        default="data/input",
        help="Path to the input directory containing images.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data/output",
        help="Path to the output directory where processed images will be saved.",
    )
    parser.add_argument(
        "--debug_dir",
        type=str,
        default="data/debug",
        help="Path to the debug directory for saving intermediate results.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode to save intermediate results.",
    )
    parser.add_argument(
        "--bypass",
        action="store_true",
        help="Automatically bypass prompts for removing non-empty directories.",
    )
    parser.add_argument(
        "--force_black_text",
        action="store_true",
        help="Force the text in the document to appear black (e.g., #0B1215).",
    )
    parser.add_argument(
        "--highlight_text_regions",
        action="store_true",
        help="Highlight detected text regions with bounding boxes.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Directories
    input_dir = args.input_dir
    output_dir = args.output_dir
    debug_dir = args.debug_dir

    # Debug mode flag
    debug_mode = args.debug

    # Remove the debug directory if it exists
    if os.path.exists(debug_dir):
        logging.info(f"Removing existing debug directory: {debug_dir}")
        shutil.rmtree(debug_dir)

    # Check if output directory exists and contains files
    if os.path.exists(output_dir) and os.listdir(output_dir):
        if args.bypass:
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
                process_image(
                    input_path,
                    output_dir,
                    debug=debug_mode,
                    force_black_text=args.force_black_text,
                    highlight_text_regions=args.highlight_text_regions,
                )
            except Exception as e:
                logging.error(f"Error processing {input_path}: {e}")
