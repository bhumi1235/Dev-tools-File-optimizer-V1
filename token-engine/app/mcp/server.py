from mcp.server.fastmcp import FastMCP

from app.mcp.tools import optimize_context


mcp = FastMCP(
    "token-engine"
)


@mcp.tool()
def optimize(
    task: str,
    files: list,
    max_context_tokens: int = 2000
):

    return optimize_context(
        task,
        files,
        max_context_tokens
    )


if __name__ == "__main__":

    mcp.run()