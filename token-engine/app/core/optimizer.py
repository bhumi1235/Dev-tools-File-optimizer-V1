"""
Core optimization engine for Token Engine.

This module orchestrates the complete context optimization
pipeline including file ingestion, chunking, compression,
semantic ranking, deduplication, context construction,
and response generation.
"""

import time

from app.utils.token_counter import count_tokens
from app.ingestion.file_reader import read_file
from app.ingestion.pdf_reader import read_pdf

from app.chunking.chunker import chunk_text
from app.chunking.markdown_chunker import chunk_markdown
from app.chunking.code_chunker import chunk_python_code

from app.compression.file_compressor import compress_file
from app.compression.selector import select_chunks_by_budget
from app.compression.deduplicator import remove_duplicates
from app.compression.context_builder import build_context

from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity

from app.llm.llm_client import generate_response
from app.planner.planner import plan_context
from typing import Any

"""
Optimize file context for a given task.

Processes input files, applies task-aware planning,
compresses context within token budgets, and generates
responses using the configured provider.

Returns metrics, debugging information, top-ranked chunks,
and the final optimized context.
"""

def optimize(
    agent_task: str,
    files: list[dict[str, Any]],
    max_context_tokens: int = 2000
) -> dict[str, Any]:

    start_time = time.time()

    plan = plan_context(
        agent_task,
        files
    )


    total_tokens = 0

    compressed_chunks = []

    for file in files:

        if file["type"] == "pdf":

            content = read_pdf(
                file["file_path"]
            )

        else:

            content = read_file(
                file["file_path"]
            )

        total_tokens += count_tokens(
            content
        )

        if file["type"] == "md":

            chunks = chunk_markdown(
                content
            )

        elif file["type"] == "py":

            chunks = chunk_python_code(
                content
            )

        else:

            chunks = chunk_text(
                content
            )

        file_chunks = []

        for chunk in chunks:

            if isinstance(chunk, dict):

                chunk["source_file"] = file["file_path"]
                chunk["source_type"] = file["type"]

                file_chunks.append(
                    chunk
                )

            else:

                file_chunks.append(
                    {
                        "heading": None,
                        "content": chunk,
                        "source_file": file["file_path"],
                        "source_type": file["type"]
                    }
                )

        compressed_file_chunks = compress_file(
            file_chunks,
            agent_task,
            max_context_tokens // len(files)
        )

        compressed_chunks.extend(
            compressed_file_chunks
        )

    ranked_chunks = []

    if plan["use_embeddings"]:

        query_embedding = embed_text(
        agent_task
    )

        for chunk in compressed_chunks:

            chunk_embedding = embed_text(
            chunk["content"]
        )

            score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

            if plan["bias_code"]:

                content = chunk["content"]

                if (
                "def " in content
                or "class " in content
                or "import " in content
            ):

                    score += 0.2

            ranked_chunks.append(
            {
                **chunk,
                "score": float(score)
            }
        )

    else:

        ranked_chunks = [

        {
            **chunk,
            "score": 1.0
        }

        for chunk in compressed_chunks
    ]

    selected_chunks, _ = select_chunks_by_budget(
        ranked_chunks,
        max_context_tokens
    )

    if plan["cross_file"]:

        seen_files = set()

        diverse_chunks = []

        for chunk in selected_chunks:

            source_file = chunk["source_file"]

            if source_file not in seen_files:

                diverse_chunks.append(
                chunk
            )

                seen_files.add(
                source_file
            )

        for chunk in selected_chunks:

            if chunk not in diverse_chunks:

                diverse_chunks.append(
                chunk
            )

        selected_chunks = diverse_chunks

    before_dedup = len(
        selected_chunks
    )

    selected_chunks = remove_duplicates(
        selected_chunks
    )

    after_dedup = len(
        selected_chunks
    )

    optimized_context = build_context(
        selected_chunks
    )

    tokens_after = count_tokens(
        optimized_context
    )

    response = generate_response(
        agent_task,
        optimized_context,
        plan["strategy"]
        )    
    

    execution_time_ms = round(
        (time.time() - start_time) * 1000,
        2
    )

    return {

        "task": agent_task,

        "metrics": {
            "files_received": len(files),
            "tokens_before": total_tokens,
            "tokens_after": tokens_after,
            "token_reduction_percent": round(
                (
                    (total_tokens - tokens_after)
                    / total_tokens
                ) * 100,
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