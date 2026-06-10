import csv
import json
import random
import sys
import tarfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config

CORPUS_URL = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
ARCHIVE = config.RAW_DIR / "MovieSummaries.tar.gz"


def download():
    if ARCHIVE.exists():
        print(f"архив уже скачан: {ARCHIVE}")
        return
    print(f"качаю {CORPUS_URL} ...")
    urllib.request.urlretrieve(CORPUS_URL, ARCHIVE)
    print(f"сохранено: {ARCHIVE} ({ARCHIVE.stat().st_size // 1024 // 1024} MB)")


def extract():
    plots = config.RAW_DIR / "MovieSummaries" / "plot_summaries.txt"
    if not plots.exists():
        print("распаковываю...")
        with tarfile.open(ARCHIVE) as tar:
            tar.extractall(config.RAW_DIR)
    return config.RAW_DIR / "MovieSummaries"


def load_titles(corpus_dir):
    titles = {}
    with open(corpus_dir / "movie.metadata.tsv", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            titles[row[0]] = row[2]
    return titles


def main():
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    download()
    corpus_dir = extract()
    titles = load_titles(corpus_dir)

    records = []
    with open(corpus_dir / "plot_summaries.txt", encoding="utf-8") as f:
        for line in f:
            movie_id, _, text = line.partition("\t")
            text = text.strip()
            if len(text) >= config.MIN_TEXT_LEN and movie_id in titles:
                records.append({"id": movie_id, "name": titles[movie_id], "text": text})

    print(f"подходящих сюжетов: {len(records)}")
    random.seed(config.SEED)
    sample = random.sample(records, config.DATASET_SIZE)

    with open(config.DATASETS_JSON, "w", encoding="utf-8") as f:
        json.dump({"datasets": sample}, f, ensure_ascii=False, indent=2)
    print(f"записано {len(sample)} в {config.DATASETS_JSON}")


if __name__ == "__main__":
    main()
