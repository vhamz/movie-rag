from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
INDEX_DIR = BASE_DIR / "data" / "index"

DATASETS_JSON = RAW_DIR / "datasets.json"
DOCUMENTS_JSONL = PROCESSED_DIR / "documents.jsonl"
CHUNKS_JSONL = PROCESSED_DIR / "chunks.jsonl"

VECTORIZER_PKL = INDEX_DIR / "vectorizer.pkl"
MATRIX_NPZ = INDEX_DIR / "matrix.npz"
INDEX_CHUNKS_JSONL = INDEX_DIR / "chunks.jsonl"

# chunking
MAX_CHARS = 800
OVERLAP = 200

# retrieval
TOP_K = 5
MIN_SCORE = 0.05

# подготовка данных
DATASET_SIZE = 1500
MIN_TEXT_LEN = 500
SEED = 42
