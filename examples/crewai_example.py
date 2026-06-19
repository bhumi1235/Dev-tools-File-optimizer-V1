from app.agents.crewai_tool import FileOptimizerCrewTool

tool = FileOptimizerCrewTool()

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