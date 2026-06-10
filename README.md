# Movie RAG

RAG по сюжетам фильмов: TF-IDF retrieval + demo-ответ с источниками + Streamlit.
Вопрос по сюжету — в ответ подходящие фрагменты с doc_id и score.

## Данные

CMU Movie Summary Corpus (http://www.cs.cmu.edu/~ark/personas/) — открытый корпус
сюжетов фильмов из Википедии, 42306 записей. В индекс идет случайная выборка
1500 сюжетов (seed зафиксирован), после нарезки получается ~5800 чанков.
Подробнее: [doc/DATA.md](doc/DATA.md).

## Запуск

Нужен только uv (https://docs.astral.sh/uv/).

```bash
uv sync
uv run python scripts/prepare_datasets.py   # скачивает корпус (~45 MB) и собирает datasets.json
uv run python scripts/build_index.py        # ingest + chunking + TF-IDF индекс
uv run streamlit run app/main.py
```

Тесты:

```bash
uv run pytest tests/ -v
```

Проверочные скрипты без UI:

```bash
uv run python scripts/check_retrieval.py
uv run python scripts/check_generator.py
```

## Demo-вопросы

Корпус на англ, вопросы лучше задавать на английском.

1. `Tony Stark new element arc reactor` -> Iron Man 2 (score 0.524)
2. `vampire attacks in a town during polar night` -> 30 Days of Night: Dark Days (score 0.292)
3. `bank robbery heist goes wrong` -> Thunderbolt and Lightfoot (score 0.275), Kaante (score 0.244)

Negative-вопрос: `как испечь с яблоками` -> все score 0.000, система отвечает
"В базе нет информации по этому вопросу" и не выдумывает ответ.

Лог проверки:

```
=== релевантный вопрос
Вот что нашлось по вашему вопросу:
**30 Days of Night: Dark Days**: ...vampire nest...
=== нерелевантный вопрос
В базе нет информации по этому вопросу. Попробуйте переформулировать
или спросить про сюжет какого-нибудь фильма.
ok
```

## Структура

```
app/        chunker, retriever, generator, prompts, config, main (UI)
scripts/    prepare_datasets, ingest, build_index, check_retrieval, check_generator
doc/        планирование: идея, vision, conventions, tasklist, workflow, DATA
tests/      chunking + retrieval/generator
data/       raw / processed / index (в git не коммитится, собирается скриптами)
```
