"""
Task-aware planning module.

Determines retrieval strategy based on the user task
and file characteristics.
"""

from app.planner.strategies import (
    RETRIEVAL,
    SUMMARIZATION,
    CODE,
    MULTI_FILE
)


from typing import Any

"""
Generate a retrieval plan for a task.

Supports retrieval, summarization,
code-focused, and multi-file strategies.
"""

def plan_context(
    task: str,
    files: list[dict[str, Any]]
) -> dict[str, Any]:

    task = task.lower()

    plan = {
        "strategy": RETRIEVAL,
        "use_embeddings": True,
        "preserve_order": False,
        "bias_code": False,
        "cross_file": False
    }

    if any(
        word in task
        for word in [
            "summarize",
            "summary",
            "overview",
            "document"
        ]
    ):

        plan["strategy"] = SUMMARIZATION

        plan["use_embeddings"] = False

        plan["preserve_order"] = True

    elif any(
        word in task
        for word in [
            "code",
            "function",
            "class",
            "readme",
            "repository"
        ]
    ):

        plan["strategy"] = CODE

        plan["preserve_order"] = True

        plan["bias_code"] = True

    if len(files) > 1:

        plan["strategy"] = MULTI_FILE

        plan["cross_file"] = True

    return plan