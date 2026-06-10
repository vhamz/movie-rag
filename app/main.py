import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import config
from app.generator import generate_answer
from app.retriever import Retriever, index_exists

st.set_page_config(page_title="Movie RAG")
st.title("Поиск по сюжетам фильмов")

if not index_exists():
    st.warning("Индекс не собран. Запустите: uv run python scripts/build_index.py")
    st.stop()


@st.cache_resource
def get_retriever():
    return Retriever()


def highlight(text, query):
    words = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
    if not words:
        return text
    pattern = re.compile("(" + "|".join(re.escape(w) for w in words) + ")", re.IGNORECASE)
    return pattern.sub(r"**\1**", text)


retriever = get_retriever()

with st.sidebar:
    st.header("Настройки")
    top_k = st.slider("top-k фрагментов", 1, 10, config.TOP_K)
    min_score = st.slider("порог score для ответа", 0.0, 0.5, config.MIN_SCORE, 0.01)

query = st.text_input(
    "Вопрос по сюжету (корпус на английском)",
    placeholder="a man stuck in a time loop",
)

if query:
    if "history" not in st.session_state:
        st.session_state.history = []
    if query not in st.session_state.history:
        st.session_state.history.insert(0, query)

    results = retriever.search(query, top_k=top_k)
    out = generate_answer(results, min_score=min_score)

    if out["refused"]:
        st.error(out["answer"])
    else:
        st.subheader("Ответ")
        for r in out["sources"]:
            st.markdown(f"**{r['name']}** (doc_id={r['doc_id']}, score={r['score']:.3f})")
            st.markdown(highlight(r["text"], query))
            st.divider()

    st.subheader(f"Найденные фрагменты (top-{top_k})")
    for r in results:
        label = f"{r['name']} | doc_id={r['doc_id']} | score={r['score']:.3f}"
        with st.expander(label):
            st.markdown(highlight(r["text"], query))

if st.session_state.get("history"):
    with st.sidebar:
        st.header("История запросов")
        for q in st.session_state.history[:10]:
            st.text(q)
