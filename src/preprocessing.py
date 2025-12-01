import cv2
import numpy as np
from skimage.filters import threshold_local

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Adaptive thresholding for degraded text
    T = threshold_local(blur, 29, offset=5, method="gaussian")
    binary = (blur > T).astype("uint8") * 255

    # Morphological closing to fill gaps (important for OCR)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return closed
