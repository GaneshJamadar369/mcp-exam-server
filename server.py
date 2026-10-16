
import hashlib
import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Exam Challenge Server")

EMAIL = "23f3003450@ds.study.iitm.ac.in"


@mcp.tool()
def solve_challenge() -> str:
    """Solve the current exam challenge from HTTP request headers."""

    from mcp.server.fastmcp import Context

    # The HTTP request is available through the current request context.
    # Read the challenge from the current request, not the tool arguments.
    ctx = mcp.get_context()
    request = ctx.request_context.request
    headers = request.headers

    challenge = headers.get("x-exam-challenge")
    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()
    message = f"{challenge}:{normalized_email}"
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
