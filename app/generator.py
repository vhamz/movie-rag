from app import config, prompts


def generate_answer(results, min_score=config.MIN_SCORE):
    relevant = [r for r in results if r["score"] >= min_score]
    if not relevant:
        return {"answer": prompts.REFUSAL, "sources": [], "refused": True}
    return {
        "answer": prompts.format_answer(relevant),
        "sources": relevant,
        "refused": False,
    }
