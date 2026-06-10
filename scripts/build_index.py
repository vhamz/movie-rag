import json
import pickle
import sys
from pathlib import Path

import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config
from app.chunker import chunk_documents
import ingest


def main():
    ingest.main()

    docs = []
    with open(config.DOCUMENTS_JSONL, encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))

    chunks = list(chunk_documents(docs))
    with open(config.CHUNKS_JSONL, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"чанков: {len(chunks)}")

    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
    matrix = vectorizer.fit_transform(c["text"] for c in chunks)
    print(f"матрица: {matrix.shape[0]} чанков x {matrix.shape[1]} признаков")

    config.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.VECTORIZER_PKL, "wb") as f:
        pickle.dump(vectorizer, f)
    scipy.sparse.save_npz(config.MATRIX_NPZ, matrix)
    with open(config.INDEX_CHUNKS_JSONL, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"индекс сохранен в {config.INDEX_DIR}")


if __name__ == "__main__":
    main()
