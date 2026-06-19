"""
OpenAI Agents integration for the Token Engine optimizer.
"""
from app.core.optimizer import optimize

"""
Enables OpenAI Agents to use Token Engine for context optimization.
"""
class FileOptimizerAgentTool:

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