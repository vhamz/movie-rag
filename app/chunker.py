from app import config


def split_paragraphs(text):
    return [p.strip() for p in text.split("\n") if p.strip()]


def split_long(text, max_chars, overlap):
    # длинный абзац режем кусками с перекрытием, по возможности рвем по пробелу
    parts = []
    start = 0
    while start < len(text):
        end = start + max_chars
        if end < len(text):
            space = text.rfind(" ", start, end)
            if space > start:
                end = space
        parts.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return parts


def chunk_text(text, max_chars=config.MAX_CHARS, overlap=config.OVERLAP):
    chunks = []
    current = ""
    for para in split_paragraphs(text):
        if len(para) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(split_long(para, max_chars, overlap))
        elif len(current) + len(para) + 1 <= max_chars:
            current = (current + "\n" + para).strip()
        else:
            chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks


def chunk_documents(docs, max_chars=config.MAX_CHARS, overlap=config.OVERLAP):
    for doc in docs:
        for i, text in enumerate(chunk_text(doc["text"], max_chars, overlap)):
            yield {
                "chunk_id": f"{doc['doc_id']}_{i}",
                "doc_id": doc["doc_id"],
                "name": doc["name"],
                "text": text,
            }
