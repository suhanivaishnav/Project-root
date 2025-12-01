import re

def extract_target_line(ocr_text):  
    """
    Extracts full line containing pattern '_1_' or ending with '_1_'
    Example expected output: 163233702292313922_1_lWV
    """

    lines = ocr_text.split("\n")

    for line in lines:
        # Enhanced regex for better matching of various patterns including leading/trailing characters 
        if "_1_" in line or re.findall(r"\b[A-Za-z0-9]*_?[_]?[A-Za-z0-9]*[ _]?[_]?[A-Za-z0-9]+\b", line):
            cleaned = line.strip()
            cleaned = cleaned.replace(" ", "")
            return cleaned

    return None
