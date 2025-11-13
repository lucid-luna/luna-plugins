# sdk/server.py
from __future__ import annotations
from typing import Any, Callable, Optional
import json, os
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from .config import load_config
from .errors import mcp_safe
from .rate_limit import limit

class PluginMCPServer:
    def __init__(self, name: str, version: str = "0.2.0", config_key: Optional[str] = None):
        self.name = name
        self.version = version
        self.config_key = config_key or name
        self.config = load_config(self.config_key)
        
        try:
            self.mcp = FastMCP(name, version=version, lifespan=self._lifespan)
        except TypeError:
            self.mcp = FastMCP(name, lifespan=self._lifespan)
        
        self._bind_builtin_resources()

    @asynccontextmanager
    async def _lifespan(self, _server: FastMCP):
        yield

    def _bind_builtin_resources(self):
        @self.mcp.resource(f"{self.name}://health")
        def health() -> str:
            return "ok"

        @self.mcp.resource(f"{self.name}://status")
        def status() -> str:
            return json.dumps({"name": self.name, "version": self.version, "config": bool(self.config)})

    def tool(self, *, rate: Optional[str] = None):
        def deco(fn: Callable[..., Any]):
            wrapped = mcp_safe(fn)
            if rate:
                wrapped = limit(rate)(wrapped)
            return self.mcp.tool()(wrapped)
        return deco

    def resource(self, uri: str):
        def deco(fn: Callable[..., Any]):
            return self.mcp.resource(uri)(mcp_safe(fn))
        return deco

    def run(self, **kwargs):
        self.mcp.run(transport='stdio', **kwargs)

def run_server(mcp: PluginMCPServer):
    mcp.run()
