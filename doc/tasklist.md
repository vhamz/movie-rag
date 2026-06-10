# Tasklist

## Прогресс

| Итерация | Что делаем | Статус |
|---|---|---|
| 0 | Scaffold | done |
| 1 | Demo data | done |
| 2 | Ingestion | done |
| 3 | Chunking | done |
| 4 | TF-IDF index | done |
| 5 | Retrieval | done |
| 6 | Demo answer | done |
| 7 | Streamlit UI | done |
| 8 | Tests + README | done |

Текущая итерация: все закрыты, MVP готов.

## Итерация 0 — Scaffold

Задачи: pyproject.toml, .gitignore, app/config.py, структура папок.

Проверка:
```bash
uv sync
uv run python -c "import app.config"
```

## Итерация 1 — Demo data

Задачи: скачать CMU Movie Summary Corpus, собрать data/raw/datasets.json (1500 записей).

Проверка:
```bash
uv run python -c "import json; d=json.load(open('data/raw/datasets.json')); print(len(d['datasets']))"
```

## Итерация 2 — Ingestion

Задачи: scripts/ingest.py, перевод datasets.json -> documents.jsonl с doc_id, name, source_file.

Проверка:
```bash
uv run python scripts/ingest.py
wc -l data/processed/documents.jsonl
```

## Итерация 3 — Chunking

Задачи: app/chunker.py (нарезка по абзацам, max_chars, overlap), tests/test_chunking.py.

Проверка:
```bash
uv run pytest tests/test_chunking.py -v
```

## Итерация 4 — TF-IDF index

Задачи: scripts/build_index.py — ingest + chunk + fit TF-IDF, артефакты в data/index/.

Проверка:
```bash
uv run python scripts/build_index.py
ls data/index/
```

## Итерация 5 — Retrieval

Задачи: app/retriever.py — top-k по cosine similarity, scripts/check_retrieval.py.

Проверка:
```bash
uv run python scripts/check_retrieval.py
```

## Итерация 6 — Demo answer

Задачи: app/prompts.py, app/generator.py — ответ только по контексту, отказ без данных.

Проверка:
```bash
uv run python scripts/check_generator.py
```

## Итерация 7 — Streamlit UI

Задачи: app/main.py — вопрос, фрагменты с doc_id/score, ответ, сообщение если индекса нет.

Проверка:
```bash
uv run streamlit run app/main.py
```
Руками: 3 demo-вопроса + 1 negative.

## Итерация 8 — Tests + README

Задачи: tests/test_retrieval.py, добить README до воспроизводимого запуска.

Проверка:
```bash
uv run pytest tests/ -v
```

## Критерии завершения MVP

- индекс собирается одной командой
- streamlit показывает фрагменты с doc_id и score
- negative-вопрос дает отказ
- тесты зеленые
- README хватает для запуска с нуля
