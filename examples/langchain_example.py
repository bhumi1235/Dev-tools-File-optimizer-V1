from app.langchain.file_opt_tool import FileOptimizerTool

tool = FileOptimizerTool()

response = tool.invoke(
    {
        "agent_task": "Explain the authentication system.",
        "files": [
            {
                "file_path": "data/auth.txt",
                "type": "txt"
            }
        ]
    }
)

print(response)