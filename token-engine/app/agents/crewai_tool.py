from app.core.optimizer import optimize


class FileOptimizerCrewTool:

    def run(
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