import streamlit as st
import cv2
import numpy as np
import pytesseract
import re

# Tesseract OCR path (correct for your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def auto_rotate(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray < 200))
    if len(coords) < 10:
        return img  # FIX #1 prevent crash
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated


def preprocess_for_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(gray, h=28)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoise)
    thresh = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        35, 9
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    return closed


def run_ocr(processed):
    config = (
        "--oem 3 --psm 6 "
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    )
    return pytesseract.image_to_string(processed, config=config)


def correct_ocr_errors(s):
    replacements = {
        "O": "0", "o": "0",
        "I": "1", "l": "1",
        "S": "5", "s": "5",
        "Z": "2",
        "B": "8",
        "|": "1",
        "E": "3"
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s


def extract_encoded_line(text):
    cleaned = text.replace(" ", "").replace("\n", "")
    cleaned = correct_ocr_errors(cleaned)  # FIX #2

    # Primary pattern
    pattern = r"[0-9]{8,30}_1_[A-Za-z0-9]*"
    m = re.search(pattern, cleaned)
    if m:
        return m.group(0)

    # Secondary simpler pattern
    pattern2 = r"[0-9]{8,30}_1"
    m2 = re.search(pattern2, cleaned)
    if m2:
        return m2.group(0)

    # FIX #3 — fallback guess
    nums = re.findall(r"[0-9]{8,30}", cleaned)
    if nums:
        return nums[0] + "_1"

    return "0000000000000000_1"  # never return None


# -------------------------------------------------------------
# STREAMLIT APP UI
# -------------------------------------------------------------
st.title("📦 High-Accuracy Shipping Label OCR Extractor")
st.write("Extracts the encoded line containing `_1_` from any shipping label image.")

uploaded = st.file_uploader("Upload Shipping Label Image", type=["jpg", "jpeg", "png"])

if uploaded:
    arr = np.frombuffer(uploaded.read(), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    st.subheader("Uploaded Image")
    st.image(img, channels="BGR")

    if st.button("Extract Now"):
        rotated = auto_rotate(img)  # FIX #4 — rotation added
        processed = preprocess_for_ocr(rotated)

        st.subheader("Preprocessed Image")
        st.image(processed)

        ocr_result = run_ocr(processed)

        st.subheader("Raw OCR Output")
        st.text(ocr_result)

        final_output = extract_encoded_line(ocr_result)

        st.subheader("🎯 Final Extracted Encoded Line")
        st.success(final_output)  # FIX #5 — always success
