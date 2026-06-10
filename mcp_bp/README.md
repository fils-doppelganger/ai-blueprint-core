# Blueprint MCP Server

A [FastMCP](https://gofastmcp.com/) server that exposes the NIAID Blueprint
documentation in `../docs` and the prompt personas in `../prompts` over the
**Model Context Protocol (MCP)** using an HTTP (Streamable HTTP / SSE-compatible)
transport.

## What it exposes

### Resources (read-only context)

| URI | Description |
|-----|-------------|
| `docs://list` | JSON listing of all Markdown files under `../docs` |
| `docs://{path}` | Raw Markdown of a doc by relative path |
| `blueprint://spec` | The canonical Blueprint specification |
| `prompts://list` | JSON listing of registered prompt personas |
| `prompts://{name}` | Raw text of a prompt persona (by name or filename) |

Resources are also available as tools via the `list_resources` / `read_resource`
tools generated automatically by the `ResourcesAsTools` transform, so clients
that don't support the MCP resources protocol (e.g. Claude Code) can still
access all content.

### Tools (model-invoked)

All tools carry `readOnlyHint` and `idempotentHint` annotations, enabling safe
client-side caching and retry.

#### Discovery

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `list_docs()` | — | Enumerate available Markdown docs (path, title, bytes) |
| `read_doc(path)` | `path: str` | Read a doc's full Markdown content |
| `kb_stats()` | — | Corpus statistics: doc counts, total size, section count, semantic search status |
| `list_resources()` | — | Auto-generated: list all MCP resources as tools |
| `read_resource(uri)` | `uri: str` | Auto-generated: read a resource by URI |

#### Search

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `search_docs(query, collection, max_results)` | `query: str`, `collection: "docs"\|"prompts"\|None`, `max_results: int=10` | Hybrid BM25 + semantic search across docs and prompts. Returns `chunk_id`, `source`, `path`, `section_number`, `section_title`, `excerpt`, `rrf_score`, `bm25_rank`, `semantic_rank` |
| `get_context_window(source, path, line, radius)` | `source: str`, `path: str`, `line: int`, `radius: int=10` | Expand line-level context around a fuzzy-search hit |

#### Blueprint navigation

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `list_blueprint_sections()` | — | List all Blueprint headings (level, number, title) |
| `get_blueprint_section(section)` | `section: str` | Extract one section by number (`"3"`, `"2.1"`) or heading keyword |
| `get_blueprint_requirements(pillar)` | `pillar: str\|None` | Return requirement sections for a FAIR pillar: `"metadata"`, `"identifiers"`, `"api"`, `"citation"`, `"outreach"`. Omit for a summary index of all pillars. |
| `blueprint_citation(section)` | `section: str\|None` | Canonical raw GitHub citation URL (+ optional section title/number) |

#### Prompts

| Tool | Purpose |
|------|---------|
| `list_prompts()` | List registered prompt personas and their arguments |

### Prompts (user-invoked)

| Name | Arguments | Purpose |
|------|-----------|---------|
| `fair_assessment_interview` | — | Structured 6-phase interview → prioritized gap report |
| `fair_self_assessment` | — | Verbose pillar-by-pillar Blueprint self-assessment |
| `fair_self_assessment_short` | — | Concise pillar-by-pillar Blueprint self-assessment |
| `fair_web_assessor` | `url` (required), `blueprint_url` (optional) | Fetch a web resource and score it against the Blueprint |
| `work_plan_interview` | `repo_name` (optional) | Intake interview → FAIRification Work Plan |

Prompts with arguments prepend a short **instruction block** to the persona
body so the supplied values override any example values in the file.

## Search architecture

`search_docs` uses a two-signal hybrid approach:

1. **BM25** (`rank-bm25`) — keyword relevance over section-level chunks. Fast,
   no model download required. Handles exact terminology, identifiers, and
   multi-word queries with IDF weighting.

2. **Semantic embeddings** (`fastembed`, optional) — dense vector similarity
   using `BAAI/bge-small-en-v1.5` (33 MB ONNX model, no PyTorch required).
   Handles synonyms, paraphrase, and conceptual queries.

Both signals are fused via **Reciprocal Rank Fusion (RRF)**:
`score = Σ 1/(60 + rank_i)` — documents ranked highly by *either* signal
surface near the top.

The corpus is chunked at **section boundaries** (using the Blueprint's Markdown
headings), so each result maps to a coherent unit of content rather than an
arbitrary line window.

The search index is built lazily on the first query and cached for the process
lifetime.

## Install

```bash
# From the repository root
uv sync --extra mcp
```

## Run (HTTP)

```bash
# Run as a module (the package uses relative imports, so use -m, not a file path)
uv run --extra mcp python -m mcp_bp.server
```

The server listens on `http://127.0.0.1:8000/mcp` by default.

## Configuration

| Env var | Default | Description |
|---------|---------|-------------|
| `MCP_HOST` | `127.0.0.1` | Bind host |
| `MCP_PORT` | `8000` | Bind port |
| `MCP_PATH` | `/mcp` | HTTP endpoint path |
| `BLUEPRINT_DOCS_DIR` | `../docs` | Docs content root |
| `BLUEPRINT_PROMPTS_DIR` | `../prompts` | Prompts content root |
| `BLUEPRINT_SEMANTIC_ENABLED` | *(off)* | Set to `1` to enable embedding-based semantic search (downloads ~33 MB model on first run) |
| `BLUEPRINT_SEMANTIC_MODEL` | `BAAI/bge-small-en-v1.5` | fastembed model name for semantic embeddings |

## Test

```bash
uv run --extra mcp --with pytest pytest mcp_bp/tests
```

## Notes

- Only Markdown (`.md`) files are served; other files (`.pdf`, `.docx`, etc.)
  are ignored.
- BM25 search is always active when `rank-bm25` is installed (included in the
  `mcp` extra). Semantic search is opt-in via `BLUEPRINT_SEMANTIC_ENABLED=1`
  to avoid surprise model downloads.
- The `ResourcesAsTools` transform bridges the MCP resources protocol gap:
  clients that support only tools still get full read access to the corpus.
