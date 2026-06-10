"""Parse the Blueprint Markdown into addressable sections.

Supports extracting a single section by its numeric prefix (e.g. ``"3"`` or
``"2.1"``) or by a heading substring (case-insensitive), keeping responses
token-efficient.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .config import BLUEPRINT_SPEC_RELPATH
from .content import read_doc

# Matches ATX headings like "## 3. Minimal API Specifications ..."
_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
# Leading numeric label, e.g. "3.", "2.1", "1.2.3"
_NUMBER_RE = re.compile(r"^(?P<num>\d+(?:\.\d+)*)\.?\s+")


@dataclass(frozen=True)
class Section:
    """A single heading and the body text that follows it."""

    level: int
    number: str | None
    title: str
    body: str

    def render(self) -> str:
        return f"{'#' * self.level} {self.title}\n\n{self.body}".rstrip() + "\n"


def _heading_number(title: str) -> str | None:
    match = _NUMBER_RE.match(title)
    return match.group("num") if match else None


def parse_sections(markdown: str) -> list[Section]:
    """Split Markdown into a flat list of sections keyed by their headings."""

    lines = markdown.splitlines()
    sections: list[Section] = []

    current_level: int | None = None
    current_title: str = ""
    current_number: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        if current_level is not None:
            sections.append(
                Section(
                    level=current_level,
                    number=current_number,
                    title=current_title,
                    body="\n".join(buffer).strip(),
                )
            )

    for line in lines:
        match = _HEADING_RE.match(line)
        if match:
            flush()
            current_level = len(match.group("hashes"))
            current_title = match.group("title").strip()
            current_number = _heading_number(current_title)
            buffer = []
        else:
            if current_level is not None:
                buffer.append(line)

    flush()
    return sections


def find_section(markdown: str, query: str) -> Section | None:
    """Find a section by numeric prefix or heading substring.

    Number matching is exact on the heading's numeric label. Text matching is
    a case-insensitive substring against the heading title; the shortest
    matching title wins (most specific heading).
    """

    query = query.strip()
    sections = parse_sections(markdown)
    if not query:
        return None

    # 1) Exact numeric match.
    if re.fullmatch(r"\d+(?:\.\d+)*", query):
        normalized = query
        for section in sections:
            if section.number == normalized:
                return section
        # Fall through to text match if no numeric heading found.

    # 2) Case-insensitive substring on title; prefer the shortest title.
    lowered = query.lower()
    candidates = [s for s in sections if lowered in s.title.lower()]
    if not candidates:
        return None
    return min(candidates, key=lambda s: len(s.title))


def get_blueprint_section(query: str) -> str:
    """Return the rendered Blueprint section matching ``query``.

    Raises ``ValueError`` if no matching section is found.
    """

    markdown = read_doc(BLUEPRINT_SPEC_RELPATH)
    section = find_section(markdown, query)
    if section is None:
        raise ValueError(
            f"No Blueprint section matched {query!r}. "
            "Try a number like '3' or '2.1', or a heading keyword like 'Citation'."
        )
    return section.render()


def list_blueprint_sections() -> list[dict[str, object]]:
    """Return a lightweight index of the Blueprint's headings."""

    markdown = read_doc(BLUEPRINT_SPEC_RELPATH)
    return [
        {"level": s.level, "number": s.number, "title": s.title}
        for s in parse_sections(markdown)
    ]


# Maps canonical pillar keys to lowercase heading keywords for matching.
_PILLAR_QUERIES: dict[str, tuple[str, ...]] = {
    "metadata": ("metadata schema", "minimal metadata", "metadata"),
    "identifiers": ("persistent identifier", "pid", "identifier"),
    "api": ("api specification", "machine access", "api"),
    "citation": ("citation",),
    "outreach": ("outreach", "training"),
}

KNOWN_PILLARS: list[str] = list(_PILLAR_QUERIES.keys())


def get_blueprint_requirements(
    pillar: str | None = None,
) -> dict[str, object]:
    """Return Blueprint sections covering a FAIR pillar's requirements.

    Pass a pillar name (``"metadata"``, ``"identifiers"``, ``"api"``,
    ``"citation"``, ``"outreach"``) to get its matching sections with full
    content.  Pass ``None`` to get a summary index of all pillars and their
    matched headings.

    Raises ``ValueError`` for unknown pillar names.
    """
    markdown = read_doc(BLUEPRINT_SPEC_RELPATH)
    all_sections = parse_sections(markdown)

    if pillar is None:
        summary: dict[str, list[dict[str, object]]] = {}
        for key, queries in _PILLAR_QUERIES.items():
            summary[key] = [
                {"title": s.title, "number": s.number}
                for s in all_sections
                if any(q in s.title.lower() for q in queries)
            ]
        return {"pillars": summary, "available_pillars": KNOWN_PILLARS}

    p = pillar.lower().strip()
    for pillar_key, queries in _PILLAR_QUERIES.items():
        if p == pillar_key or p in queries:
            matched_key, matched_queries = pillar_key, queries
            break
    else:
        raise ValueError(
            f"Unknown pillar {pillar!r}. "
            f"Valid options: {KNOWN_PILLARS}"
        )

    matching = [
        {"title": s.title, "number": s.number, "content": s.body}
        for s in all_sections
        if any(q in s.title.lower() for q in matched_queries)
    ]
    return {"pillar": matched_key, "sections": matching}
