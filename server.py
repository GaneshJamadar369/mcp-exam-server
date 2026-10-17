import hashlib
import os

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.transport_security import TransportSecuritySettings


EMAIL = "23f3003450@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam Challenge Server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the challenge hash from the current HTTP request header."""
    challenge = ctx.request_context.request.headers.get("x-exam-challenge")
    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()
    return hashlib.sha256(
        f"{challenge}:{normalized_email}".encode("utf-8")
    ).hexdigest()[:16]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        mcp.streamable_http_app(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
