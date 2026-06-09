import json

def load_contracts(json_path, limit=5):
    with open(json_path, "r", encoding="utf-8") as f:
        cuad = json.load(f)

    contracts = []
    for item in cuad["data"][:limit]:
        paragraphs = item["paragraphs"]
        text = " ".join(p["context"] for p in paragraphs)
        if len(text.strip()) > 500:
            contracts.append(text)

    print(f"Loaded {len(contracts)} real contracts")
    return contracts
