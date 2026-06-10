"""FastMCP server exposing the NIAID Blueprint docs and prompt personas.

This package serves the Markdown content in ``./docs`` and the prompt
personas in ``./prompts`` over the Model Context Protocol (MCP) using an
HTTP (Streamable HTTP / SSE-compatible) transport.
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
