from app.utils.token_counter import count_tokens


def select_chunks_by_budget(ranked_chunks, max_context_tokens):

    if not ranked_chunks:
        return [], 0

    critical_chunks = []
    useful_chunks = []
    weak_chunks = []

    for chunk in ranked_chunks:

        score = chunk["score"]

        if score >= 0.6:
            critical_chunks.append(chunk)

        elif score >= 0.3:
            useful_chunks.append(chunk)

        elif score >= 0.1:
            weak_chunks.append(chunk)

    ordered_chunks = (
        critical_chunks
        + useful_chunks
        + weak_chunks
    )

    selected_chunks = []
    used_tokens = 0

    for chunk in ordered_chunks:

        chunk_tokens = count_tokens(
            chunk["content"]
        )

        if used_tokens + chunk_tokens > max_context_tokens:
            continue

        selected_chunks.append(chunk)

        used_tokens += chunk_tokens

    return selected_chunks, used_tokens