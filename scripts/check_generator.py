import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.generator import generate_answer
from app.retriever import Retriever


def main():
    retriever = Retriever()

    print("=== релевантный вопрос")
    results = retriever.search("vampire falls in love with a girl")
    out = generate_answer(results)
    print(out["answer"][:500])
    assert not out["refused"], "ожидался ответ, получен отказ"

    print("\n=== нерелевантный вопрос")
    results = retriever.search("как испечь шарлотку с яблоками")
    out = generate_answer(results)
    print(out["answer"])
    assert out["refused"], "ожидался отказ"

    print("\nok")


if __name__ == "__main__":
    main()
