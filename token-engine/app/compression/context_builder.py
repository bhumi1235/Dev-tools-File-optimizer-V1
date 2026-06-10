def build_context(selected_chunks):

    context = []

    for chunk in selected_chunks:

        heading = chunk.get("heading")

        content = chunk["content"]

        if heading:

            context.append(
                f"{heading}\n{content}"
            )

        else:

            context.append(content)

    return "\n\n".join(context)