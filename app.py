import streamlit as st
import cv2
import numpy as np
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Now import modules
from ocr_engine import run_ocr
from preprocessing import preprocess_image
from text_extraction import extract_target_line

st.title("Shipping Label OCR - Target Text Extractor")

uploaded = st.file_uploader("Upload Shipping Label Image", type=["png", "jpg", "jpeg"])

if uploaded:
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(img, caption="Uploaded Image")

    if st.button("Process OCR"):
        preprocessed = preprocess_image(img)
        st.image(preprocessed, caption="Preprocessed")

        ocr_text = run_ocr(preprocessed)
        st.text_area("OCR Output", ocr_text, height=200)

        extracted = extract_target_line(ocr_text)

        if extracted:
            st.success(f"Extracted Target Line: {extracted}")
        else:
            st.error("Pattern _1_ not found!")
