REFUSAL = (
    "В базе нет информации по этому вопросу. "
    "Попробуйте переформулировать или спросить про сюжет какого-нибудь фильма."
)

ANSWER_HEADER = "Вот что нашлось по вашему вопросу:"


def format_source(result):
    return f"- {result['name']} (doc_id={result['doc_id']}, score={result['score']:.3f})"


def format_answer(results):
    lines = [ANSWER_HEADER, ""]
    for r in results:
        lines.append(f"**{r['name']}**: {r['text']}")
        lines.append("")
    lines.append("Источники:")
    lines.extend(format_source(r) for r in results)
    return "\n".join(lines)
