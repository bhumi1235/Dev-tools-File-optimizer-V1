from app.utils.token_counter import count_tokens


def select_chunks_by_budget(ranked_chunks, max_context_tokens):

    if not ranked_chunks:
        return [], 0

    ordered_chunks = sorted(
        ranked_chunks,
        key=lambda x: x["score"],
        reverse=True
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