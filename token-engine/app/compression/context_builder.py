import re


def build_context(selected_chunks):

    source_groups = {}

    for chunk in selected_chunks:

        source = chunk["source_file"]

        heading = chunk.get("heading")

        content = chunk["content"]

        block = ""

        if heading:

            block += f"{heading}\n{content}"

        else:

            block += content

        if source not in source_groups:

            source_groups[source] = []

        source_groups[source].append(
            block
        )

    context = []

    for source, blocks in source_groups.items():

        seen_sentences = set()

        cleaned_sentences = []

        for block in blocks:

            sentences = re.split(
                r'(?<=[.!?])\s+',
                block
            )

            for sentence in sentences:

                sentence = sentence.strip()

                if (
                    sentence
                    and sentence not in seen_sentences
                ):

                    seen_sentences.add(
                        sentence
                    )

                    cleaned_sentences.append(
                        sentence
                    )

        context.append(

            f"[Source: {source}]\n\n"

            + "\n\n".join(
                cleaned_sentences
            )

        )

    return "\n\n".join(
        context
    )