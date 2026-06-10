import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.retriever import Retriever

QUERIES = [
    "a man stuck in a time loop living the same day",
    "детектив расследует убийство",  # слова не из корпуса, скоры должны быть ~0
    "qwerty asdfgh zxcvbn",
]


def main():
    retriever = Retriever()
    for query in QUERIES:
        print(f"\n=== {query}")
        for r in retriever.search(query, top_k=3):
            preview = r["text"][:80].replace("\n", " ")
            print(f"  [{r['score']:.3f}] {r['name']} (doc_id={r['doc_id']}) {preview}...")


if __name__ == "__main__":
    main()
