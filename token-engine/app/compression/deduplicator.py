def remove_duplicates(selected_chunks):

    seen = set()
    unique_chunks = []

    for chunk in selected_chunks:

        content = chunk["content"].strip()

        if content not in seen:
            seen.add(content)
            unique_chunks.append(chunk)

    return unique_chunks