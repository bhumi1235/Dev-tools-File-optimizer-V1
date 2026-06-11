import re


def chunk_text(text: str, max_words: int = 35, overlap_sentences: int = 1):

    text = re.sub(r'\s+', ' ', text).strip()

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    chunks = []

    current_chunk = []

    current_words = 0

    for sentence in sentences:

        sentence_words = len(sentence.split())

        if sentence_words < 3:
            continue

        if current_words + sentence_words > max_words:

            if current_chunk:

                chunks.append(
                    " ".join(current_chunk)
                )

            # overlap
            current_chunk = current_chunk[-overlap_sentences:]

            current_words = sum(
                len(s.split())
                for s in current_chunk
            )

        current_chunk.append(sentence)

        current_words += sentence_words

    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )

    return chunks