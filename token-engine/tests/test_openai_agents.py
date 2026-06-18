from app.agents.openai_agents_tool import FileOptimizerAgentTool

tool = FileOptimizerAgentTool()

response = tool.run(
    "Explain the authentication system.",
    [
        {
            "file_path": "data/auth.txt",
            "type": "txt"
        }
    ]
)

print(response)