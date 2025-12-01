import json
import os

RAW_DIR = "data/raw"

def load_raw_files():
    files = [f for f in os.listdir(RAW_DIR) if f.endswith(".json")]
    datasets = []

    for file in files:
        path = os.path.join(RAW_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            datasets.append(data)
    
    return datasets
