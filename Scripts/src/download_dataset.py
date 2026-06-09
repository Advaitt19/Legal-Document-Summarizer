from datasets import load_dataset
import json
import os

DATASET_NAME = "roshant080498/cuad_legal_dataset_unsloth_template"
SAVE_DIR = "data/raw"
OUTPUT_FILE = "cuad_legal_dataset.json"

os.makedirs(SAVE_DIR, exist_ok=True)

print("Downloading CUAD dataset...")
dataset = load_dataset(DATASET_NAME)

records = []
for item in dataset["train"]:
    records.append(item)

output_path = os.path.join(SAVE_DIR, OUTPUT_FILE)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("Dataset saved at:", output_path)
