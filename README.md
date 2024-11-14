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
2. **Background Removal**: Eliminates the paper background while preserving text clarity using adaptive thresholding and
   morphological operations.
3. **Text Highlighting**: Marks text regions with overlays or bounding boxes to enhance visibility.
4. **Edge Enhancement**: Sharpens faint text edges using filters like Sobel or Laplacian for improved clarity.

---

## **3. Implementation Details**

- **Languages and Tools**: Python 3.x with OpenCV for image processing, and NumPy for computations.
- **Input Requirements**: Images of documents on a contrasting surface with all edges visible, including varying
  lighting conditions.
- **Output**: Enhanced, cleaned images with text highlighted and backgrounds removed, saved in grayscale or binarized
  formats.

---

## **4. Expected Outcome**

- Improve text clarity with preprocessing and edge sharpening.
- Remove uneven backgrounds while maintaining readability.
- Correct camera-induced skew for better alignment.
- Provide digitized outputs suitable for archiving or analysis.