from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any

from app.core.optimizer import optimize


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
def optimize_context(
    data: OptimizeRequest
) -> dict[str, Any]:

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