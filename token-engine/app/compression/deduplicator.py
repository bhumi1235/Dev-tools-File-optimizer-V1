from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.config import SIMILARITY_THRESHOLD

def remove_duplicates(selected_chunks):

    unique_chunks = []

    embeddings = []

    threshold = SIMILARITY_THRESHOLD

    for chunk in selected_chunks:

        content = chunk["content"]

        current_embedding = embed_text(
            content
        )

        is_duplicate = False

        for previous_embedding in embeddings:

            similarity = cosine_similarity(
                current_embedding,
                previous_embedding
            )

            if similarity > threshold:

                is_duplicate = True

                break

        if not is_duplicate:

            unique_chunks.append(
                chunk
            )

            embeddings.append(
                current_embedding
            )

    return unique_chunks