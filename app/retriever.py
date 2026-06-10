import json
import pickle

import scipy.sparse
from sklearn.metrics.pairwise import cosine_similarity

from app import config


class Retriever:
    def __init__(self, index_dir=config.INDEX_DIR):
        with open(index_dir / config.VECTORIZER_PKL.name, "rb") as f:
            self.vectorizer = pickle.load(f)
        self.matrix = scipy.sparse.load_npz(index_dir / config.MATRIX_NPZ.name)
        self.chunks = []
        with open(index_dir / config.INDEX_CHUNKS_JSONL.name, encoding="utf-8") as f:
            for line in f:
                self.chunks.append(json.loads(line))

    def search(self, query, top_k=config.TOP_K):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        order = scores.argsort()[::-1][:top_k]
        results = []
        for i in order:
            chunk = self.chunks[i]
            results.append({
                "text": chunk["text"],
                "doc_id": chunk["doc_id"],
                "name": chunk["name"],
                "score": float(scores[i]),
            })
        return results


def index_exists(index_dir=config.INDEX_DIR):
    return (
        (index_dir / config.VECTORIZER_PKL.name).exists()
        and (index_dir / config.MATRIX_NPZ.name).exists()
        and (index_dir / config.INDEX_CHUNKS_JSONL.name).exists()
    )
