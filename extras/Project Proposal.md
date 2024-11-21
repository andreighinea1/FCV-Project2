# **Project Proposal: Text Highlighting and Background Removal**

## **1. Purpose**

The project aims to process scanned or photographed images of handwritten or printed documents by enhancing text
visibility and removing uneven backgrounds. The system will address issues like uneven lighting and camera angle
distortions, providing a clean, readable output suitable for digitization and further analysis.

---

## **2. Main Functionalities**

### **2.1. Preprocessing**

To improve text detection and background removal, the following preprocessing steps will be used:

1. **Noise Reduction**: Smoothens the image to remove artifacts using techniques like Gaussian Blur or Non-Local Means
   Denoising.
2. **Contrast Adjustment**: Enhances faint text visibility through local contrast enhancement.
3. **Binarization**: Separates text from the background using adaptive thresholding and Otsu's method.
4. **Edge Preservation**: Retains fine text details with Bilateral Filtering.
5. **Morphological Filtering**: Cleans and connects fragmented text using dilation and erosion.
6. **Gradient Analysis**: Highlights text transitions for better segmentation.

---

### **2.2. Post-Processing**

After preprocessing, the system applies the following steps to enhance the document:

1. **Perspective Correction**: Corrects skew caused by camera angles by detecting paper edges and applying a perspective
   transformation. Assumes the paper is fully visible and placed on a contrasting background.
2. **Background Removal**: Remove uneven backgrounds while preserving text clarity using adaptive thresholding and
   morphological operations. This process isolates text regions and ensures the output is a clean, binarized image.
3. **Text Detection and Highlighting**: Detect text regions using contour-based methods and filter based on geometric
   constraints. Highlight detected text using bounding boxes or overlays for better readability and digitization.
4. **Edge Enhancement**: Sharpens faint text edges using filters like Sobel or Laplacian for improved clarity.

---

## **3. Implementation Details**

- **Languages and Tools**: Python 3.x with OpenCV for image processing, and NumPy for computations.
- **Input Requirements**:
    - **Source of Images**: Images will be captured using a smartphone camera or scanned from printed/handwritten
      documents. The dataset will include self-captured images.
    - **Image Constraints**:
        - The document should be fully visible in the image, ideally covering an A4-sized sheet or smaller.
        - The document should be placed on a contrasting background to enhance edge detection.
        - Images should have adequate resolution (minimum 300 DPI for scanned documents or 8 MP for camera-captured
          images).
        - Avoid extreme angles; the document should be roughly parallel to the camera lens.
- **Output**: Enhanced, cleaned images with text highlighted and backgrounds removed, saved in grayscale or binarized
  formats.

---

## **4. Expected Outcome**

- Improve text clarity with preprocessing and edge sharpening.
- Remove uneven backgrounds while maintaining readability.
- Correct camera-induced skew for better alignment.
- Provide digitized outputs suitable for archiving or analysis.

---

## **5. Contributions**

The following contributions will be part of my implementation for this project:

1. **Noise Reduction**
    - **My Contribution**: Implement custom noise reduction filters based on Gaussian kernels to smooth images.
      Fine-tune parameters like kernel size to balance text clarity and background removal.
    - **Library Functions**: Use OpenCV's `cv2.GaussianBlur` and `cv2.fastNlMeansDenoising` for implementing the
      filters.

2. **Contrast Adjustment**
    - **My Contribution**: Develop a script to enhance local contrast by computing the histogram of pixel intensities
      and applying contrast stretching.
    - **Library Functions**: Use NumPy for histogram calculations and intensity scaling.

3. **Binarization**
    - **My Contribution**: Experiment with different thresholding methods (adaptive and Otsu) to select the most
      effective one for varying lighting conditions.
    - **Library Functions**: Implement using OpenCV's `cv2.adaptiveThreshold` and `cv2.threshold` for comparison and
      optimization.

4. **Morphological Filtering**
    - **My Contribution**: Design a process for using dilation and erosion to clean text regions and connect fragmented
      text. Create custom kernel shapes for specific document types.
    - **Library Functions**: Use OpenCV's `cv2.morphologyEx` with pre-defined operations like `cv2.MORPH_CLOSE` and
      `cv2.MORPH_OPEN`.

5. **Gradient Analysis**
    - **My Contribution**: Implement gradient-based text segmentation using Sobel operators to identify text edges and
      boundaries. Test combinations of gradients in different directions to refine results.
    - **Library Functions**: Use OpenCV's `cv2.Sobel` and `cv2.Laplacian` for gradient calculation.

6. **Perspective Correction**
    - **My Contribution**: Write a function to detect paper edges using contour detection and apply perspective
      transformation based on the detected quadrilateral.
    - **Library Functions**: Use OpenCV's `cv2.findContours` for edge detection and `cv2.getPerspectiveTransform` for
      transformation.

7. **Background Removal**
    - **My Contribution**: Implement a pipeline combining adaptive thresholding and morphological operations to
      eliminate uneven backgrounds while preserving text clarity. Write custom functions to identify and remove noise or
      faint background artifacts.
    - **Library Functions**: Use OpenCV's `cv2.adaptiveThreshold` for binarization and `cv2.morphologyEx` for cleanup.
    - **Possible Improvements**:
        - Use edge detection (`cv2.Canny`) to highlight abrupt intensity transitions between text and the background,
          enhancing separation.
        - Experiment with gradient-based segmentation (`cv2.Sobel`) to identify faint text regions and reduce false
          negatives.
        - Integrate a local histogram equalization step (`cv2.equalizeHist`) to improve text contrast in challenging
          conditions.

8. **Text Detection and Highlighting**
    - **My Contribution**: Implement contour-based text detection to identify text regions and filter based on size,
      aspect ratio, and stroke consistency. Develop merging logic to ensure fragmented text regions are captured
      cohesively.
    - **Library Functions**: Use OpenCV's `cv2.findContours` for region detection and `cv2.boundingRect` for creating
      bounding boxes.
    - **Possible Improvements**:
        - Preprocess with edge detection (`cv2.Canny`) or gradient analysis (`cv2.Sobel`) to improve text visibility
          before contour detection.
        - Employ connected component analysis (`cv2.connectedComponentsWithStats`) for enhanced robustness in noisy
          environments.
        - Use rotated bounding boxes (`cv2.minAreaRect`) for detecting angled or skewed text regions.
        - Introduce proximity-based merging of fragmented text components to ensure complete words or lines are
          captured.