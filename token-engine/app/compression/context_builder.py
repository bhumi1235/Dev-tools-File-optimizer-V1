def build_context(selected_chunks):

    return "\n\n".join(
        chunk["content"]
        for chunk in selected_chunks
    )