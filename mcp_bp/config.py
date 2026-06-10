"""Configuration for the Blueprint MCP server.

All paths are resolved relative to the repository root (the parent of the
``mcp`` package directory) unless overridden via environment variables.
"""

from __future__ import annotations

import os
from pathlib import Path

# Repository root: <repo>/mcp/config.py -> <repo>
REPO_ROOT: Path = Path(__file__).resolve().parent.parent


def _env_path(var: str, default: Path) -> Path:
    value = os.environ.get(var)
    return Path(value).expanduser().resolve() if value else default


# Content roots ------------------------------------------------------------

DOCS_DIR: Path = _env_path("BLUEPRINT_DOCS_DIR", REPO_ROOT / "docs")
PROMPTS_DIR: Path = _env_path("BLUEPRINT_PROMPTS_DIR", REPO_ROOT / "prompts")

# Only Markdown is served for now.
ALLOWED_EXTENSIONS: tuple[str, ...] = (".md",)

# The canonical Blueprint specification, relative to DOCS_DIR.
BLUEPRINT_SPEC_RELPATH: str = "NIAID_Blueprint_v2_26Sep2025_forExternal.md"

# Canonical public (raw GitHub) URL for citation helpers.
BLUEPRINT_RAW_URL: str = (
    "https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/"
    "refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md"
)

# HTTP transport -----------------------------------------------------------

HOST: str = os.environ.get("MCP_HOST", "127.0.0.1")
PORT: int = int(os.environ.get("MCP_PORT", "8000"))
# Path the Streamable HTTP endpoint is mounted at.
HTTP_PATH: str = os.environ.get("MCP_PATH", "/mcp")

# Search -------------------------------------------------------------------

# Default number of ranked results returned by search_docs.
DEFAULT_SEARCH_RESULTS: int = 10
# Minimum fuzzy score (0-100) for a line to be considered a match (fuzzy fallback only).
SEARCH_SCORE_CUTOFF: float = 50.0

# Hybrid search -----------------------------------------------------------

# Reciprocal Rank Fusion constant (60 is the standard; higher = less steep ranking curve).
RRF_K: int = 60

# fastembed model name for semantic embeddings.
SEMANTIC_MODEL: str = os.environ.get(
    "BLUEPRINT_SEMANTIC_MODEL", "BAAI/bge-small-en-v1.5"
)

# Set BLUEPRINT_SEMANTIC_ENABLED=1 to enable embedding-based semantic search.
# Disabled by default to avoid model downloads on first run.
SEMANTIC_ENABLED: bool = os.environ.get(
    "BLUEPRINT_SEMANTIC_ENABLED", ""
).lower() in ("1", "true", "yes")
