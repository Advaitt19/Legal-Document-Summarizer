import os
from data_ingestion import load_contracts
from preprocessing import clean_text,chunk_text
from extractive import extractive_summary
from abstractive import abstractive_summary
from evaluation import rouge_scores
# Go from code/src → project root
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "CUAD_v1.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
def run_pipeline():
    contracts = load_contracts(DATA_PATH, limit=5)
    print(f"Number of contracts to process: {len(contracts)}")

    if not contracts:
        print(" No text found in dataset")
        return

    for idx, text in enumerate(contracts):
        print(f"Processing contract {idx + 1}")

        text = clean_text(text)
        chunks = chunk_text(text)

        ext = extractive_summary(text)
        abs_sum = abstractive_summary(chunks)

        scores = rouge_scores(ext, abs_sum)

        print("ROUGE Evaluation Results")
        print("-" * 30)
        for metric, score in scores.items():
            print(f"{metric.upper():8} | F1 Score: {score.fmeasure:.3f}")

        with open(f"{OUTPUT_DIR}/contract_{idx + 1}.txt", "w", encoding="utf-8") as f:
            f.write("EXTRACTIVE SUMMARY\n")
            f.write(ext + "\n\n")
            f.write("ABSTRACTIVE SUMMARY\n")
            f.write(abs_sum + "\n\n")
            f.write("ROUGE SCORES\n")
            f.write(str(scores))

        print(f"Saved → outputs/contract_{idx + 1}.txt")

if __name__ == "__main__":
    run_pipeline()
