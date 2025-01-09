# **Project Proposal: Text Highlighting and Background Removal**

## **1. Purpose**

The project aims to process images of handwritten or printed documents by enhancing text visibility and removing uneven
backgrounds. This will address issues like uneven lighting and camera distortions, producing clean, readable outputs
suitable for digitization and analysis.

---

## **2. Main Functionalities**

<INSTRUCTION>Here try to include everything we did to the images. Also detail the document detection in its own
subsection, and then detail the rest into a separate subsection (2.1 and 2.2).</INSTRUCTION>

---

## **3. Implementation Details**

<INSTRUCTION>Try to add missing stuff from here, especially maybe some details about the input and output, and maybe
also rewrite it with better English.</INSTRUCTION>

- **Languages and Tools**: Python 3.x with OpenCV and NumPy for image processing.
- **Input Requirements**:
    - Images captured via smartphone or scanner.
    - Document fully visible, ideally A4 size, with a contrasting background.
    - Adequate resolution (min 300 DPI for scans or 8 MP for photos).
    - Minimal skew or extreme angles.
- **Output**: Cleaned, enhanced images with text highlighted and backgrounds removed, saved in grayscale. It also
  highlights the text regions, and allows the user to choose if they want to have the text replaced with Obsidian Black,
  or keep the original text color.

---

## **4. Expected Outcome**

<INSTRUCTION>Similarly, add anything missing, and improve the English</INSTRUCTION>

- Improved text clarity.
- Removal of uneven backgrounds.
- Correct camera-induced skew.
- Aligned, enhanced outputs suitable for digitization and archiving.
- Black text for document-like stuff.
- Highlighted text.

---

## **5. Contributions**

<INSTRUCTION>Here you'll need to write for every feature I have and used (like if I used noise reduction, to mention it
and mention my contribution and what libraries I used for it). Also categorize based on the document detection part and
everything I used for that part, and also for the rest of the pipeline. And also write like possible improvements,
contributions, libraries used, and issues I had with them.</INSTRUCTION>

---

## **6. Example Outputs**

<INSTRUCTION>Please give me the format for how to add images in the markdown file, and I'll add the images myself. And
make the format like to first list the input images and show them, and in a different section show the results with and
without --highlight_text_regions, another with and without the --force_black_text, and then another with all the final
results which would have 2 subsubsections for both failed and good results.</INSTRUCTION>
