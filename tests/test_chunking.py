from app.chunker import chunk_documents, chunk_text


def test_short_text_one_chunk():
    assert chunk_text("короткий текст") == ["короткий текст"]


def test_max_chars_respected():
    text = " ".join(["слово"] * 1000)
    for chunk in chunk_text(text, max_chars=200, overlap=50):
        assert len(chunk) <= 200


def test_overlap_between_chunks():
    text = "a" * 1000
    chunks = chunk_text(text, max_chars=300, overlap=100)
    assert len(chunks) > 1
    assert chunks[1].startswith(chunks[0][-100:])


def test_small_paragraphs_grouped():
    text = "первый абзац\nвторой абзац"
    assert chunk_text(text, max_chars=100, overlap=10) == ["первый абзац\nвторой абзац"]


def test_chunk_documents_metadata():
    docs = [{"doc_id": "42", "name": "Тест", "text": "немного текста"}]
    chunks = list(chunk_documents(docs))
    assert chunks[0]["chunk_id"] == "42_0"
    assert chunks[0]["doc_id"] == "42"
    assert chunks[0]["name"] == "Тест"
