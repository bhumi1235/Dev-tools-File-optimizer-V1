from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.token_counter import count_tokens
from app.chunking.chunker import chunk_text
from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.compression.selector import select_chunks_by_budget

router = APIRouter()


class FileData(BaseModel):
    filename: str
    content: str
    type: str


class OptimizeRequest(BaseModel):
    agent_task: str
    target_compression_ratio: float
    max_context_tokens: int
    files: List[FileData]

@router.post("/optimize-context")
def optimize_context(data: OptimizeRequest):

    total_tokens = 0
    all_chunks = []

    for file in data.files:

        total_tokens += count_tokens(file.content)

        chunks = chunk_text(file.content)

        all_chunks.extend(chunks)

    query_embedding = embed_text(data.agent_task)

    ranked_chunks = []

    for chunk in all_chunks:

        chunk_embedding = embed_text(chunk)

        score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        ranked_chunks.append({
            "content": chunk,
            "score": float(score)
        })

    ranked_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    selected_chunks, used_tokens = select_chunks_by_budget(
    ranked_chunks,
    data.max_context_tokens
)

    return {
    "task": data.agent_task,

    "metrics": {
        "files_received": len(data.files),
        "tokens_before": total_tokens,
        "tokens_after": used_tokens,
        "token_reduction_percent": round(
            ((total_tokens - used_tokens) / total_tokens) * 100,
            2
        ) if total_tokens > 0 else 0,
        "chunks_created": len(all_chunks),
        "chunks_selected": len(selected_chunks)
    },

    "selected_context": [
        chunk["content"]
        for chunk in selected_chunks
    ]
}