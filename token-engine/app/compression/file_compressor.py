"""
Semantic compression module.

Ranks chunks using embeddings and selects
the most relevant context within token limits.
"""

from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.compression.selector import select_chunks_by_budget

"""
Compress file chunks using semantic similarity
and token budget constraints.
"""

def compress_file(chunks, task, max_tokens):

    query_embedding = embed_text(task)

    ranked_chunks = []

    for chunk in chunks:

        chunk_embedding = embed_text(
            chunk["content"]
        )

        score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        ranked_chunks.append({
            **chunk,
            "score": float(score)
        })

    ranked_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    selected_chunks, _ = select_chunks_by_budget(
        ranked_chunks,
        max_tokens
    )

    return selected_chunks