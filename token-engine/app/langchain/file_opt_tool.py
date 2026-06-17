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
from app.core.optimizer import optimize



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

        result = optimize(
        agent_task,
        files,
        max_context_tokens
    )

        return result["response"]

    async def _arun(
        self,
        *args,
        **kwargs
    ):

        raise NotImplementedError(
            "Async not implemented."
        )