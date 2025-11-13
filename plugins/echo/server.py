# plugins/echo/server.py
import sys
import os

os.environ['PYTHONUNBUFFERED'] = '1'

from mcp.server.fastmcp import FastMCP

server = FastMCP("echo")

@server.tool()
def ping(text: str) -> str:
    """Echo back the text you send."""
    return text

@server.resource("echo://config")
def config_preview() -> str:
    import json
    return json.dumps({"name": "echo", "version": "1.0.0"})

if __name__ == "__main__":
    server.run(transport="stdio")
