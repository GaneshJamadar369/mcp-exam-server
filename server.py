import hashlib
import os

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.transport_security import TransportSecuritySettings
from mcp.server import types
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "23f3003450@ds.study.iitm.ac.in"
server = Server("Exam Challenge Server")


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="solve_challenge",
            description="Calculate the hash for the current exam challenge.",
            inputSchema={"type": "object", "properties": {}},
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name != "solve_challenge":
        raise ValueError(f"Unknown tool: {name}")

    # The HTTP header is accessed through the request context in FastMCP.
    # This lower-level handler needs a different request-header integration.
    raise ValueError("Use the FastMCP implementation with request context")


if __name__ == "__main__":
    import uvicorn
    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
