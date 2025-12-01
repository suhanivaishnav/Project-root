import pytesseract
import cv2

def run_ocr(image):
    # Force the correct tesseract location at runtime
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    config = "--oem 3 --psm 6"
    return pytesseract.image_to_string(image, config=config)
