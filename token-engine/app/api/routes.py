from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.token_counter import count_tokens
from app.chunking.chunker import chunk_text
from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.compression.selector import select_chunks_by_budget
from app.compression.context_builder import build_context
from app.compression.deduplicator import remove_duplicates
from app.ingestion.file_reader import read_file
from app.chunking.markdown_chunker import chunk_markdown
from app.ingestion.pdf_reader import read_pdf
import time

router = APIRouter()


class FileData(BaseModel):
    file_path: str
    type: str


class OptimizeRequest(BaseModel):
    agent_task: str
    target_compression_ratio: float
    max_context_tokens: int
    files: List[FileData]

@router.post("/optimize-context")
def optimize_context(data: OptimizeRequest):
    start_time = time.time()
    total_tokens = 0
    all_chunks = []

    for file in data.files:

        print("Reading:", file.file_path)

        if file.type == "pdf":
            content = read_pdf(file.file_path)
        else:
            content = read_file(file.file_path)

        print("Content loaded:", len(content))

        total_tokens += count_tokens(content)

        if file.type == "md":
            chunks = chunk_markdown(content)
        else:
            chunks = chunk_text(content)

        all_chunks.extend(chunks)

    query_embedding = embed_text(data.agent_task)

    ranked_chunks = []

    for chunk in all_chunks:

     if isinstance(chunk, dict):

        chunk_content = chunk["content"]

        heading = chunk["heading"]

     else:

        chunk_content = chunk

        heading = None

     chunk_embedding = embed_text(chunk_content)

     score = cosine_similarity(
        query_embedding,
        chunk_embedding
     )
     ranked_chunks.append({
        "heading": heading,
        "content": chunk_content,
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
    before_dedup = len(selected_chunks)

    selected_chunks = remove_duplicates(selected_chunks)

    after_dedup = len(selected_chunks)
    tokens_after = sum(
    count_tokens(chunk["content"])
    for chunk in selected_chunks
)
    optimized_context = build_context(selected_chunks)

    execution_time_ms = round(
    (time.time() - start_time) * 1000,
    2
)

    return {
        
        "task": data.agent_task,

    "metrics": {
        "files_received": len(data.files),
        "tokens_before": total_tokens,
        "tokens_after": tokens_after,
        "token_reduction_percent": round(
            ((total_tokens - tokens_after) / total_tokens) * 100,
            2
        ) if total_tokens > 0 else 0,
        "chunks_created": len(all_chunks),
        "chunks_selected": len(selected_chunks),
        "execution_time_ms": execution_time_ms
    },

    "debug": {
    "before_dedup": before_dedup,
    "after_dedup": after_dedup
},
    "top_chunks": ranked_chunks[:5],

    "optimized_context": optimized_context
}