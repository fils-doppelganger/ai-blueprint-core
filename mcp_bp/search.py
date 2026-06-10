"""Ranked fuzzy search across the served Markdown documents and prompts.

Uses ``rapidfuzz`` to score the query against each line of every Markdown
file under ``DOCS_DIR`` and ``PROMPTS_DIR``, returning the best matches with
a short surrounding snippet.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rapidfuzz import fuzz

from .config import (
    DEFAULT_SEARCH_RESULTS,
    DOCS_DIR,
    PROMPTS_DIR,
    SEARCH_SCORE_CUTOFF,
)
from .content import list_markdown


@dataclass(frozen=True)
class SearchHit:
    """A single ranked search result."""

    source: str  # "docs" or "prompts"
    path: str  # relative path within its root
    line: int  # 1-based line number of the match
    score: float
    snippet: str

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "path": self.path,
            "line": self.line,
            "score": round(self.score, 1),
            "snippet": self.snippet,
        }


def _snippet(lines: list[str], index: int, radius: int = 1) -> str:
    start = max(0, index - radius)
    end = min(len(lines), index + radius + 1)
    return " ".join(part.strip() for part in lines[start:end] if part.strip())


def _score_file(
    root: Path, rel_path: str, source: str, query: str
) -> list[SearchHit]:
    full = root / rel_path
    try:
        text = full.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    lines = text.splitlines()
    hits: list[SearchHit] = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        score = fuzz.partial_ratio(query.lower(), stripped.lower())
        if score >= SEARCH_SCORE_CUTOFF:
            hits.append(
                SearchHit(
                    source=source,
                    path=rel_path,
                    line=idx + 1,
                    score=float(score),
                    snippet=_snippet(lines, idx),
                )
            )
    return hits


def search(
    query: str, max_results: int = DEFAULT_SEARCH_RESULTS
) -> list[SearchHit]:
    """Return ranked fuzzy matches for ``query`` across docs and prompts."""

    query = (query or "").strip()
    if not query:
        return []

    all_hits: list[SearchHit] = []
    for root, source in ((DOCS_DIR, "docs"), (PROMPTS_DIR, "prompts")):
        for entry in list_markdown(root):
            all_hits.extend(_score_file(root, entry.path, source, query))

    # Highest score first; for ties prefer earlier lines and shorter paths.
    all_hits.sort(key=lambda h: (-h.score, len(h.path), h.line))

    # De-duplicate so a single file doesn't crowd out others: keep the best
    # hit per (source, path), then fill remaining slots with runners-up.
    best_per_file: dict[tuple[str, str], SearchHit] = {}
    extras: list[SearchHit] = []
    for hit in all_hits:
        key = (hit.source, hit.path)
        if key not in best_per_file:
            best_per_file[key] = hit
        else:
            extras.append(hit)

    ranked = sorted(
        best_per_file.values(), key=lambda h: (-h.score, len(h.path), h.line)
    )
    ranked.extend(extras)
    return ranked[:max_results]


def search_as_dicts(
    query: str, max_results: int = DEFAULT_SEARCH_RESULTS
) -> list[dict[str, object]]:
    return [hit.as_dict() for hit in search(query, max_results)]
