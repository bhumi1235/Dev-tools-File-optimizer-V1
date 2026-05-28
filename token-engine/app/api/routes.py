from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.utils.token_counter import count_tokens
from app.chunking.chunker import chunk_text

router = APIRouter()


class FileData(BaseModel):
    filename: str
    content: str
    type: str


class OptimizeRequest(BaseModel):
    agent_task: str
    target_compression_ratio: float
    files: List[FileData]

@router.post("/optimize-context")
def optimize_context(data: OptimizeRequest):

    total_tokens = 0
    all_chunks = []

    for file in data.files:

        total_tokens += count_tokens(file.content)

        chunks = chunk_text(file.content)

        all_chunks.extend(chunks)

    return {
        "message": "pipeline received",
        "task": data.agent_task,
        "files_received": len(data.files),
        "total_tokens": total_tokens,
        "chunks_created": len(all_chunks)
    }