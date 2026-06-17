from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time
from app.core.optimizer import optimize
from app.utils.token_counter import count_tokens
from app.chunking.chunker import chunk_text
from app.chunking.markdown_chunker import chunk_markdown
from app.utils.logger import logger
from app.ingestion.file_reader import read_file
from app.ingestion.pdf_reader import read_pdf
from fastapi import HTTPException
from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.chunking.code_chunker import chunk_python_code
from app.compression.selector import select_chunks_by_budget
from app.compression.context_builder import build_context
from app.compression.deduplicator import remove_duplicates
from app.compression.file_compressor import compress_file
from app.llm.llm_client import generate_response


router = APIRouter()


class FileData(BaseModel):
    file_path: str
    type: str


class OptimizeRequest(BaseModel):
    agent_task: str
    target_compression_ratio: float
    max_context_tokens: int
    files: List[FileData]


@router.post("/file_opt")
def optimize_context(data: OptimizeRequest):

    result = optimize(
        data.agent_task,
        [
            {
                "file_path": file.file_path,
                "type": file.type
            }
            for file in data.files
        ],
        data.max_context_tokens
    )

    return result