from langchain.tools import BaseTool

from app.ingestion.file_reader import read_file
from app.ingestion.pdf_reader import read_pdf
from app.chunking.chunker import chunk_text
from app.chunking.markdown_chunker import chunk_markdown
from app.chunking.code_chunker import chunk_python_code
from app.compression.file_compressor import compress_file
from app.embeddings.embedder import embed_text
from app.ranking.scorer import cosine_similarity
from app.compression.selector import select_chunks_by_budget
from app.compression.deduplicator import remove_duplicates
from app.compression.context_builder import build_context
from app.llm.llm_client import generate_response


class FileOptimizerTool(BaseTool):

    name: str = "file_optimizer"

    description: str = (
        "Optimizes file context and answers questions using the provided files."
    )

    def _run(
        self,
        agent_task,
        files,
        max_context_tokens=2000
    ):

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

        query_embedding = embed_text(
            agent_task
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

            ranked_chunks.append(
                {
                    **chunk,
                    "score": float(score)
                }
            )

        selected_chunks, _ = select_chunks_by_budget(
            ranked_chunks,
            max_context_tokens
        )

        selected_chunks = remove_duplicates(
            selected_chunks
        )

        optimized_context = build_context(
            selected_chunks
        )

        response = generate_response(
            agent_task,
            optimized_context
        )

        return response

    async def _arun(
        self,
        *args,
        **kwargs
    ):

        raise NotImplementedError(
            "Async not implemented."
        )