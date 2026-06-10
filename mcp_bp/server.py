"""FastMCP server exposing NIAID Blueprint docs and prompt personas over HTTP.

Run as a module (the package uses relative imports, so launch it with
``-m`` rather than by file path)::

    uv run --extra mcp python -m mcp_bp.server

The server registers:
  * Resources: docs://list, docs://{path}, blueprint://spec,
    prompts://list, prompts://{name}
  * Tools: list_docs, read_doc, search_docs, get_context_window, kb_stats,
    get_blueprint_section, list_blueprint_sections, get_blueprint_requirements,
    list_prompts, blueprint_citation
  * Prompts: the personas defined in prompts_registry.PROMPT_SPECS
  * Transform: ResourcesAsTools (resources accessible as tools for clients
    that don't support the MCP resources protocol)
"""

from __future__ import annotations

import json

from fastmcp import FastMCP
from fastmcp.server.transforms import ResourcesAsTools
from mcp.types import ToolAnnotations

from . import config, content, hybrid_search, prompts_registry, search, sections

mcp: FastMCP = FastMCP(
    name="ai-blueprint",
    instructions=(
        "Serves the NIAID Blueprint for Digital Objects v2 and related FAIR "
        "assessment materials. The corpus includes the Blueprint specification, "
        "supporting documents, and prompt personas for FAIR assessment interviews. "
        "Use search_docs for natural-language queries across the full corpus. "
        "Use get_blueprint_section or get_blueprint_requirements for targeted "
        "retrieval of specific Blueprint content. Use the prompts to launch "
        "interactive FAIR assessment or Work Plan interviews."
    ),
)

# Expose resources as tools so clients without resource-protocol support
# (e.g. Claude Code) can still access docs and Blueprint content via tools.
mcp.add_transform(ResourcesAsTools(mcp))


# --------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------


@mcp.resource("docs://list", mime_type="application/json")
def docs_list() -> str:
    """A JSON listing of all Markdown documents under ./docs."""
    return json.dumps([entry.as_dict() for entry in content.list_docs()], indent=2)


@mcp.resource("docs://{path*}", mime_type="text/markdown")
def docs_get(path: str) -> str:
    """The raw Markdown of a document under ./docs by relative path."""
    return content.read_doc(path)


@mcp.resource("blueprint://spec", mime_type="text/markdown")
def blueprint_spec() -> str:
    """The canonical NIAID Blueprint specification Markdown."""
    return content.read_doc(config.BLUEPRINT_SPEC_RELPATH)


@mcp.resource("prompts://list", mime_type="application/json")
def prompts_list() -> str:
    """A JSON listing of the registered prompt personas."""
    return json.dumps(prompts_registry.list_prompt_specs(), indent=2)


@mcp.resource("prompts://{name}", mime_type="text/markdown")
def prompts_get(name: str) -> str:
    """The raw text of a registered prompt persona (for reading, not invoking).

    ``name`` may be a registered prompt name or a prompt filename.
    """
    spec = prompts_registry.PROMPT_SPECS_BY_NAME.get(name)
    filename = spec.filename if spec else name
    return content.read_prompt_file(filename)


# --------------------------------------------------------------------------
# Discovery & retrieval tools
# --------------------------------------------------------------------------

_READ_ONLY = ToolAnnotations(readOnlyHint=True, idempotentHint=True)
_READ_ONLY_NON_IDEMPOTENT = ToolAnnotations(readOnlyHint=True)


@mcp.tool(annotations=_READ_ONLY)
def list_docs() -> list[dict[str, object]]:
    """List all Markdown documents available in the NIAID Blueprint corpus.

    Returns path, title, and size for each document. Use the ``path`` values
    with ``read_doc`` to fetch full content, or pass a title keyword to
    ``search_docs`` to find relevant passages.
    """
    return [entry.as_dict() for entry in content.list_docs()]


@mcp.tool(annotations=_READ_ONLY)
def read_doc(path: str) -> str:
    """Read the full Markdown content of a Blueprint corpus document.

    ``path`` is a relative path returned by ``list_docs`` (e.g.
    ``"NIAID_Blueprint_v2_26Sep2025_forExternal.md"``).  For large documents,
    prefer ``get_blueprint_section`` to fetch just the relevant section.
    """
    return content.read_doc(path)


@mcp.tool(annotations=_READ_ONLY)
def kb_stats() -> dict[str, object]:
    """Return corpus statistics: document counts, total sizes, section count.

    Also reports whether semantic (embedding) search is enabled.
    Useful for understanding the available corpus before issuing queries.
    """
    docs = content.list_docs()
    prompts = content.list_prompt_files()
    section_count = len(sections.list_blueprint_sections())
    return {
        "docs": {"count": len(docs), "total_bytes": sum(d.bytes for d in docs)},
        "prompts": {
            "count": len(prompts),
            "total_bytes": sum(p.bytes for p in prompts),
        },
        "blueprint_sections": section_count,
        "semantic_search_enabled": config.SEMANTIC_ENABLED,
    }


# --------------------------------------------------------------------------
# Search tools
# --------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def search_docs(
    query: str,
    collection: str | None = None,
    max_results: int = config.DEFAULT_SEARCH_RESULTS,
) -> list[dict[str, object]]:
    """Hybrid BM25 + semantic search across the NIAID Blueprint corpus.

    Searches the Blueprint v2 specification, supporting documents, and prompt
    personas using BM25 keyword ranking fused with optional dense embeddings
    (enabled via the ``BLUEPRINT_SEMANTIC_ENABLED`` env var) via Reciprocal
    Rank Fusion (RRF).

    ``collection`` filters to ``"docs"`` (specification + supporting docs) or
    ``"prompts"`` (interview personas); omit to search both.

    Each result includes:
    - ``chunk_id``: stable ID usable with ``get_context_window``
    - ``source`` / ``path``: where the chunk comes from
    - ``section_number`` / ``section_title``: Blueprint heading context
    - ``excerpt``: up to 400 chars of the matching passage
    - ``rrf_score``: fusion score (higher = more relevant)
    - ``bm25_rank`` / ``semantic_rank``: per-signal ranks for transparency
    """
    results = hybrid_search.hybrid_search_as_dicts(
        query, collection=collection, max_results=max_results
    )
    if results:
        return results
    # Graceful fallback when BM25 index unavailable (e.g. missing rank-bm25).
    fuzzy = search.search_as_dicts(query, max_results=max_results)
    if collection:
        fuzzy = [r for r in fuzzy if r.get("source") == collection]
    return fuzzy


@mcp.tool(annotations=_READ_ONLY)
def get_context_window(
    source: str,
    path: str,
    line: int,
    radius: int = 10,
) -> dict[str, object]:
    """Expand context around a line returned by a fuzzy search result.

    Use ``source``, ``path``, and ``line`` from a ``search_docs`` fallback
    result (when results contain ``"line"`` keys).  ``radius`` controls how
    many lines above and below to include (default 10).

    Returns ``start_line``, ``end_line``, and the joined ``text`` of the window.
    """
    root = config.DOCS_DIR if source == "docs" else config.PROMPTS_DIR
    return content.read_lines_around(root, path, line, radius)


# --------------------------------------------------------------------------
# Blueprint navigation tools
# --------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def list_blueprint_sections() -> list[dict[str, object]]:
    """List the Blueprint's headings (level, number, title) for navigation.

    Use heading numbers or title keywords with ``get_blueprint_section`` to
    retrieve the content of a specific section without loading the full spec.
    """
    return sections.list_blueprint_sections()


@mcp.tool(annotations=_READ_ONLY)
def get_blueprint_section(section: str) -> str:
    """Return a single Blueprint section by number (e.g. '3', '2.1') or heading keyword.

    Extracts just the requested section from the NIAID Blueprint v2 spec,
    keeping responses token-efficient.  Use ``list_blueprint_sections`` to
    browse available headings.
    """
    return sections.get_blueprint_section(section)


@mcp.tool(annotations=_READ_ONLY)
def get_blueprint_requirements(pillar: str | None = None) -> dict[str, object]:
    """Return Blueprint requirement sections for a given FAIR pillar.

    Valid pillar names: ``"metadata"``, ``"identifiers"``, ``"api"``,
    ``"citation"``, ``"outreach"``.  Pass ``None`` (or omit) to get a summary
    index of all pillars and which Blueprint headings map to each.

    Returns ``{"pillar": ..., "sections": [{"title", "number", "content"}, ...]}``
    for a specific pillar, or ``{"pillars": {...}, "available_pillars": [...]}``
    for the overview.
    """
    return sections.get_blueprint_requirements(pillar)


@mcp.tool(annotations=_READ_ONLY)
def blueprint_citation(section: str | None = None) -> dict[str, str]:
    """Return the canonical raw GitHub URL for citing the NIAID Blueprint.

    If ``section`` is provided (number or heading keyword), the resolved
    heading title and number are included alongside the URL.
    """
    result: dict[str, str] = {"url": config.BLUEPRINT_RAW_URL}
    if section:
        match = sections.find_section(
            content.read_doc(config.BLUEPRINT_SPEC_RELPATH), section
        )
        if match is not None:
            result["section_title"] = match.title
            if match.number:
                result["section_number"] = match.number
    return result


# --------------------------------------------------------------------------
# Prompt listing tool
# --------------------------------------------------------------------------


@mcp.tool(annotations=_READ_ONLY)
def list_prompts() -> list[dict[str, object]]:
    """List the registered FAIR assessment and work-plan prompt personas.

    Returns name, title, description, and argument specs for each prompt.
    Invoke a prompt by name via the MCP prompts protocol (not this tool).
    """
    return prompts_registry.list_prompt_specs()


# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------


@mcp.prompt(
    name="fair_assessment_interview",
    description=(
        "Structured 6-phase interview assessing Blueprint alignment, ending "
        "in a prioritized gap report."
    ),
)
def fair_assessment_interview() -> str:
    return prompts_registry.render_prompt("fair_assessment_interview")


@mcp.prompt(
    name="fair_self_assessment",
    description="Verbose pillar-by-pillar Blueprint self-assessment consultant.",
)
def fair_self_assessment() -> str:
    return prompts_registry.render_prompt("fair_self_assessment")


@mcp.prompt(
    name="fair_self_assessment_short",
    description="Concise pillar-by-pillar Blueprint self-assessment consultant.",
)
def fair_self_assessment_short() -> str:
    return prompts_registry.render_prompt("fair_self_assessment_short")


@mcp.prompt(
    name="fair_web_assessor",
    description=(
        "Assess a web resource against the Blueprint. Provide a target URL "
        "and optionally an alternate Blueprint URL."
    ),
)
def fair_web_assessor(url: str, blueprint_url: str | None = None) -> str:
    return prompts_registry.render_prompt(
        "fair_web_assessor", url=url, blueprint_url=blueprint_url
    )


@mcp.prompt(
    name="work_plan_interview",
    description=(
        "Intake interview that produces a FAIRification Work Plan. Optionally "
        "provide the target repository name."
    ),
)
def work_plan_interview(repo_name: str | None = None) -> str:
    return prompts_registry.render_prompt("work_plan_interview", repo_name=repo_name)


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------


def main() -> None:
    """Run the server over HTTP (Streamable HTTP / SSE-compatible)."""
    mcp.run(
        transport="http",
        host=config.HOST,
        port=config.PORT,
        path=config.HTTP_PATH,
    )


if __name__ == "__main__":
    main()
