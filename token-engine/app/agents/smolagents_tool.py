"""
SmolAgents integration for the Token Engine optimizer.
"""

from app.core.optimizer import optimize

"""
Enables SmolAgents to use Token Engine for context optimization.
"""
class FileOptimizerSmolTool:

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