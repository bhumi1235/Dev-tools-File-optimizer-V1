"""
LangChain wrapper for the Token Engine optimizer.
"""

from langchain.tools import BaseTool
from app.core.optimizer import optimize


"""
Exposes Token Engine as a LangChain tool.
"""

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