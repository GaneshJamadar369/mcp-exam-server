
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "23f3003450@ds.study.iitm.ac.in"

mcp = FastMCP("Exam Challenge Server")

app = mcp.streamable_http_app(
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "mcp-exam-server-pmln.onrender.com",
            "mcp-exam-server-pmln.onrender.com:*",
        ],
        enable_dns_rebinding_protection=True,
    )
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the required hash for the current exam challenge."""
    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    message = f"{challenge}:{EMAIL.strip().lower()}"
    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
