import json
import os

def save_json_output(filename, extracted_text):
    os.makedirs("results/json_outputs", exist_ok=True)

    data = {
        "filename": filename,
        "extracted_text": extracted_text
    }

    with open(f"results/json_outputs/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)
