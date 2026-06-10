# Vision

## Технологии

- Python 3.11+, пакеты через uv
- retrieval: TF-IDF из scikit-learn + cosine similarity
- UI: Streamlit
- тесты: pytest

Никаких внешних API и тяжелых моделей, все локально.

## Как строится индекс

1. `scripts/prepare_datasets.py` скачивает корпус и собирает `data/raw/datasets.json`
   (1500 записей: id, name, text)
2. `scripts/ingest.py` переводит его в `data/processed/documents.jsonl`
   с полями doc_id, name, text, source_file
3. `app/chunker.py` режет документы на чанки по абзацам,
   max_chars=800, overlap=200, результат в `data/processed/chunks.jsonl`
4. `scripts/build_index.py` гоняет ingest + chunking, обучает TfidfVectorizer
   и сохраняет в `data/index/`: vectorizer.pkl, matrix.npz, chunks.jsonl

## Как работает поиск

- вопрос векторизуется тем же TfidfVectorizer
- cosine similarity между вопросом и матрицей чанков
- возвращается top-k чанков (по умолчанию 5): text, doc_id, name, score
- generator собирает ответ только из чанков со score >= 0.05,
  если таких нет — фиксированный отказ

## Как запускать

```bash
uv sync
uv run python scripts/prepare_datasets.py   # один раз, скачивает данные
uv run python scripts/build_index.py
uv run streamlit run app/main.py
uv run pytest tests/ -v
```
