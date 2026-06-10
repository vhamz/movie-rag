import json
import pickle

import pytest
import scipy.sparse
from sklearn.feature_extraction.text import TfidfVectorizer

from app.generator import generate_answer
from app.retriever import Retriever, index_exists

CHUNKS = [
    {"chunk_id": "1_0", "doc_id": "1", "name": "Time Movie",
     "text": "a man stuck in a time loop repeats the same day"},
    {"chunk_id": "2_0", "doc_id": "2", "name": "Space Movie",
     "text": "astronauts travel to a distant planet through a wormhole"},
    {"chunk_id": "3_0", "doc_id": "3", "name": "Sea Movie",
     "text": "a giant shark attacks a small beach town"},
]


@pytest.fixture
def index_dir(tmp_path):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(c["text"] for c in CHUNKS)
    with open(tmp_path / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    scipy.sparse.save_npz(tmp_path / "matrix.npz", matrix)
    with open(tmp_path / "chunks.jsonl", "w", encoding="utf-8") as f:
        for c in CHUNKS:
            f.write(json.dumps(c) + "\n")
    return tmp_path


def test_relevant_query_finds_right_doc(index_dir):
    results = Retriever(index_dir).search("time loop same day", top_k=3)
    assert results[0]["doc_id"] == "1"
    assert results[0]["score"] > 0


def test_result_has_required_fields(index_dir):
    result = Retriever(index_dir).search("shark", top_k=1)[0]
    assert set(result) == {"text", "doc_id", "name", "score"}


def test_irrelevant_query_zero_scores(index_dir):
    results = Retriever(index_dir).search("шарлотка с яблоками", top_k=3)
    assert all(r["score"] == 0 for r in results)


def test_top_k(index_dir):
    assert len(Retriever(index_dir).search("movie", top_k=2)) == 2


def test_index_exists(index_dir, tmp_path):
    assert index_exists(index_dir)
    assert not index_exists(tmp_path / "пусто")


def test_generator_answers_with_sources(index_dir):
    results = Retriever(index_dir).search("time loop", top_k=3)
    out = generate_answer(results, min_score=0.05)
    assert not out["refused"]
    assert out["sources"][0]["name"] == "Time Movie"


def test_generator_refuses_without_context(index_dir):
    results = Retriever(index_dir).search("ничего общего с корпусом", top_k=3)
    out = generate_answer(results, min_score=0.05)
    assert out["refused"]
    assert out["sources"] == []
