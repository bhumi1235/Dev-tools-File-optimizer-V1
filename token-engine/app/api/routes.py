from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time

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

    if data.max_context_tokens <= 0:

        raise HTTPException(
        status_code=400,
        detail="max_context_tokens must be positive"
    )

    start_time = time.time()

    total_tokens = 0

    compressed_chunks = []

    for file in data.files:

        logger.info(
             f"Reading file: {file.file_path}"
        )

        try:

            if file.type == "pdf":

                content = read_pdf(
            file.file_path
        )

            else:

                content = read_file(
            file.file_path
            )

        except FileNotFoundError:

            logger.error(
        f"File not found: {file.file_path}"
    )

            raise HTTPException(
        status_code=404,
        detail=f"File not found: {file.file_path}"
    )

        except Exception as e:

            logger.error(
        str(e)
    )

            raise HTTPException(
        status_code=500,
        detail=str(e)
    )
        if not content.strip():

            raise HTTPException(
        status_code=400,
        detail=f"Empty file: {file.file_path}"
    )

        total_tokens += count_tokens(content)

        if file.type == "md":

         chunks = chunk_markdown(content)

        elif file.type == "py":

            chunks = chunk_python_code(content)

        elif file.type in ["txt", "pdf"]:

            chunks = chunk_text(content)

        else:

            raise HTTPException(
        status_code=400,
        detail=f"Unsupported file type: {file.type}"
    )

        file_chunks = []

        for chunk in chunks:

            if isinstance(chunk, dict):

                chunk["source_file"] = file.file_path
                chunk["source_type"] = file.type

                file_chunks.append(chunk)

            else:

                file_chunks.append({
                    "heading": None,
                    "content": chunk,
                    "source_file": file.file_path,
                    "source_type": file.type
                })

        compressed_file_chunks = compress_file(
    file_chunks,
    data.agent_task,
    data.max_context_tokens // len(data.files)
)
        

        compressed_chunks.extend(
            compressed_file_chunks
        )

    query_embedding = embed_text(
        data.agent_task
    )

    ranked_chunks = []

    for chunk in compressed_chunks:

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

    selected_chunks, used_tokens = select_chunks_by_budget(
        ranked_chunks,
        data.max_context_tokens
    )

    before_dedup = len(selected_chunks)

    selected_chunks = remove_duplicates(
        selected_chunks
    )

    after_dedup = len(selected_chunks)

    optimized_context = build_context(
        selected_chunks
    )

    response = generate_response(
    data.agent_task,
    optimized_context
)

    tokens_after = count_tokens(
    optimized_context
)

    execution_time_ms = round(
        (time.time() - start_time) * 1000,
        2
    )

    logger.info(
    f"Optimization completed in {execution_time_ms} ms"
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
            "chunks_selected": len(selected_chunks),
            "execution_time_ms": execution_time_ms
        },

        "debug": {
            "before_dedup": before_dedup,
            "after_dedup": after_dedup
        },

        "top_chunks": ranked_chunks[:5],

        "response": response,

        "optimized_context": optimized_context
    }