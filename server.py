
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("Exam Challenge Server")
EMAIL = "23f3003450@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the challenge hash from the current HTTP request header."""
    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    import uvicorn

    app = mcp.streamable_http_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
