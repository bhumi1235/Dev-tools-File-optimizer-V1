import re


def chunk_text(text: str, max_words: int = 50):

    paragraphs = text.split("\n\n")

    chunks = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if len(paragraph.split()) < 5:
            continue

        if len(paragraph.split()) <= max_words:

            chunks.append(paragraph)

        else:

            sentences = re.split(
                r'(?<=[.!?])\s+',
                paragraph
            )

            current_chunk = ""

            current_words = 0

            for sentence in sentences:

                sentence_words = len(
                    sentence.split()
                )

                if current_words + sentence_words > max_words:

                    if current_chunk:

                        chunks.append(
                            current_chunk.strip()
                        )

                    current_chunk = sentence

                    current_words = sentence_words

                else:

                    current_chunk += " " + sentence

                    current_words += sentence_words

            if current_chunk:

                chunks.append(
                    current_chunk.strip()
                )

    return chunks