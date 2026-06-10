"""Hybrid BM25 + optional semantic search with Reciprocal Rank Fusion (RRF).

Chunks the corpus by section (using the existing ``parse_sections`` parser),
builds a BM25 index at startup, and optionally a dense embedding matrix when
``BLUEPRINT_SEMANTIC_ENABLED=1`` is set. Results from both signals are fused
via RRF so documents ranked highly by *either* signal surface near the top.

The index is built lazily on the first call and cached for the process
lifetime. Call ``invalidate_index()`` to rebuild after docs change on disk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from .config import (
    DEFAULT_SEARCH_RESULTS,
    DOCS_DIR,
    PROMPTS_DIR,
    RRF_K,
    SEMANTIC_ENABLED,
    SEMANTIC_MODEL,
)
from .content import list_markdown
from .sections import parse_sections

try:
    from rank_bm25 import BM25Okapi

    _BM25_AVAILABLE = True
except ImportError:
    _BM25_AVAILABLE = False

try:
    from fastembed import TextEmbedding
    import numpy as np

    _FASTEMBED_AVAILABLE = True
except ImportError:
    _FASTEMBED_AVAILABLE = False

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Chunk:
    """A searchable unit of content — one parsed section or an entire file."""

    chunk_id: str
    source: str  # "docs" or "prompts"
    path: str  # relative path within source root
    section_number: str | None
    section_title: str
    body: str  # full text of this chunk

    def excerpt(self, max_chars: int = 400) -> str:
        text = self.body.strip()
        if len(text) <= max_chars:
            return text
        truncated = text[:max_chars]
        last_space = truncated.rfind(" ")
        return (truncated[:last_space] if last_space > 100 else truncated) + "…"


@dataclass
class HybridHit:
    """A single ranked result from hybrid search."""

    chunk_id: str
    source: str
    path: str
    section_number: str | None
    section_title: str
    excerpt: str
    rrf_score: float
    bm25_rank: int | None
    semantic_rank: int | None

    def as_dict(self) -> dict[str, object]:
        return {
            "chunk_id": self.chunk_id,
            "source": self.source,
            "path": self.path,
            "section_number": self.section_number,
            "section_title": self.section_title,
            "excerpt": self.excerpt,
            "rrf_score": round(self.rrf_score, 4),
            "bm25_rank": self.bm25_rank,
            "semantic_rank": self.semantic_rank,
        }


# ---------------------------------------------------------------------------
# Index
# ---------------------------------------------------------------------------


class _Index:
    __slots__ = ("chunks", "bm25", "embeddings", "embed_model")

    def __init__(
        self,
        chunks: list[Chunk],
        bm25: object | None,
        embeddings: object | None,
        embed_model: object | None,
    ) -> None:
        self.chunks = chunks
        self.bm25 = bm25
        self.embeddings = embeddings  # numpy float32 ndarray | None
        self.embed_model = embed_model  # TextEmbedding | None


_INDEX: _Index | None = None


def _build_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for root, source in ((DOCS_DIR, "docs"), (PROMPTS_DIR, "prompts")):
        for entry in list_markdown(root):
            try:
                text = (root / entry.path).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            parsed = parse_sections(text)
            if parsed:
                for sec in parsed:
                    if not sec.body.strip():
                        continue
                    cid = f"{source}::{entry.path}::{sec.number or sec.title[:40]}"
                    chunks.append(
                        Chunk(
                            chunk_id=cid,
                            source=source,
                            path=entry.path,
                            section_number=sec.number,
                            section_title=sec.title,
                            body=sec.body,
                        )
                    )
            else:
                # Unsectioned file — treat the whole file as one chunk.
                cid = f"{source}::{entry.path}::root"
                chunks.append(
                    Chunk(
                        chunk_id=cid,
                        source=source,
                        path=entry.path,
                        section_number=None,
                        section_title=entry.title,
                        body=text,
                    )
                )
    return chunks


def _get_index() -> _Index:
    global _INDEX
    if _INDEX is not None:
        return _INDEX

    chunks = _build_chunks()
    texts = [f"{c.section_title}\n{c.body}" for c in chunks]

    bm25 = BM25Okapi([_tokenize(t) for t in texts]) if _BM25_AVAILABLE else None

    embeddings = None
    embed_model = None
    if SEMANTIC_ENABLED and _FASTEMBED_AVAILABLE and chunks:
        embed_model = TextEmbedding(SEMANTIC_MODEL)
        embeddings = np.array(list(embed_model.embed(texts)), dtype=np.float32)

    _INDEX = _Index(chunks, bm25, embeddings, embed_model)
    return _INDEX


def invalidate_index() -> None:
    """Clear the cached index so it is rebuilt on the next search call."""
    global _INDEX
    _INDEX = None


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


def _rrf(ranks: list[int | None], k: int = RRF_K) -> float:
    return sum(1.0 / (k + r) for r in ranks if r is not None)


def hybrid_search(
    query: str,
    collection: Literal["docs", "prompts"] | None = None,
    max_results: int = DEFAULT_SEARCH_RESULTS,
) -> list[HybridHit]:
    """Return ranked results using BM25 (+ optional semantic) RRF fusion.

    ``collection`` limits results to ``"docs"`` or ``"prompts"``; omit for both.
    """
    query = (query or "").strip()
    if not query:
        return []

    idx = _get_index()

    # Filter chunks to the requested collection.
    mask = [
        i
        for i, c in enumerate(idx.chunks)
        if collection is None or c.source == collection
    ]
    if not mask:
        return []

    fc = [idx.chunks[i] for i in mask]

    # --- BM25 ranks (1-indexed within filtered set) ---
    bm25_ranks: list[int | None] = [None] * len(fc)
    if idx.bm25 is not None:
        all_scores = idx.bm25.get_scores(_tokenize(query))
        fc_scores = [float(all_scores[i]) for i in mask]
        for rank_pos, j in enumerate(
            sorted(range(len(fc)), key=lambda j: -fc_scores[j]), 1
        ):
            bm25_ranks[j] = rank_pos

    # --- Semantic ranks (1-indexed within filtered set) ---
    sem_ranks: list[int | None] = [None] * len(fc)
    if idx.embeddings is not None and idx.embed_model is not None:
        q_vec = np.array(
            list(idx.embed_model.embed([query]))[0], dtype=np.float32
        )
        fc_embs = idx.embeddings[mask]
        sims = (fc_embs @ q_vec).tolist()
        for rank_pos, j in enumerate(
            sorted(range(len(fc)), key=lambda j: -sims[j]), 1
        ):
            sem_ranks[j] = rank_pos

    # --- RRF fusion ---
    hits = [
        HybridHit(
            chunk_id=fc[j].chunk_id,
            source=fc[j].source,
            path=fc[j].path,
            section_number=fc[j].section_number,
            section_title=fc[j].section_title,
            excerpt=fc[j].excerpt(),
            rrf_score=_rrf([bm25_ranks[j], sem_ranks[j]]),
            bm25_rank=bm25_ranks[j],
            semantic_rank=sem_ranks[j],
        )
        for j in range(len(fc))
    ]

    hits.sort(key=lambda h: -h.rrf_score)
    return hits[:max_results]


def hybrid_search_as_dicts(
    query: str,
    collection: str | None = None,
    max_results: int = DEFAULT_SEARCH_RESULTS,
) -> list[dict[str, object]]:
    return [h.as_dict() for h in hybrid_search(query, collection, max_results)]
