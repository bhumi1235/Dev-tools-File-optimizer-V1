from app.core.optimizer import optimize


def optimize_context(
    task: str,
    files: list,
    max_context_tokens: int = 2000
):

    result = optimize(
        task,
        files,
        max_context_tokens
    )

    return {
        "response": result["response"],
        "metrics": result["metrics"],
        "optimized_context": result["optimized_context"]
    }