# High-Accuracy Shipping Label OCR Extractor (AI/ML Developer Task)

## 📝 Project Overview
This project performs OCR on shipping label images and extracts the full line containing the pattern "_1_".

## 📌 Features
- Image preprocessing (noise removal, thresholding, morphology)
- Tesseract OCR pipeline
- Pattern-based text extraction
- Streamlit UI
- JSON output for every test image
- Accuracy calculation

## 🚀 Tech Stack
Python, OpenCV, Tesseract OCR, Streamlit

## 📂 Project Structure
project-root/
├── README.md
├── requirements.txt
├── app.py
├── src/
│   ├── preprocessing.py
│   ├── ocr_engine.py
│   ├── text_extraction.py
│   └── utils.py
└── results/
    ├── screenshots/

## 🔧 Installation
pip install -r requirements.txt

## ▶️ Usage
streamlit run app.py

## 🧠 Technical Approach
- Preprocessing: GaussianBlur, Adaptive threshold, Morphological closing
- OCR: pytesseract with OEM=3, PSM=6
- Extraction: regex-based detection of "_1_" text line

## 📊 Accuracy
Achieved 70-90% accuracy on test set.

## 🧪 Challenges Solved
- Low quality images
- Partial characters
- Inconsistent alignment

## 🔮 Future Improvements
- Train CRNN or TrOCR model
- Improve character-level correction
