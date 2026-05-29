from app.utils.token_counter import count_tokens

def select_chunks_by_budget(ranked_chunks, max_context_tokens):

    if not ranked_chunks:
        return [], 0

    selected_chunks = [ranked_chunks[0]]
    used_tokens = count_tokens(ranked_chunks[0]["content"])

    for chunk in ranked_chunks[1:]:

        chunk_tokens = count_tokens(chunk["content"])

        if used_tokens + chunk_tokens > max_context_tokens:
            break

        selected_chunks.append(chunk)
        used_tokens += chunk_tokens

    return selected_chunks, used_tokens