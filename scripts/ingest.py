import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config


def main():
    with open(config.DATASETS_JSON, encoding="utf-8") as f:
        datasets = json.load(f)["datasets"]

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.DOCUMENTS_JSONL, "w", encoding="utf-8") as f:
        for item in datasets:
            doc = {
                "doc_id": item["id"],
                "name": item["name"],
                "text": item["text"],
                "source_file": config.DATASETS_JSON.name,
            }
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"документов: {len(datasets)} -> {config.DOCUMENTS_JSONL}")


if __name__ == "__main__":
    main()
