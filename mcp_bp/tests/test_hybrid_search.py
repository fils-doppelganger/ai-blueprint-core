"""Tests for hybrid BM25 search across docs and prompts."""

from __future__ import annotations

from mcp_bp import hybrid_search


def test_hybrid_search_finds_relevant_section(content_tree) -> None:
    hits = hybrid_search.hybrid_search("JSON-LD API", max_results=5)
    assert hits
    assert any("api" in h.section_title.lower() or "API" in h.excerpt for h in hits)


def test_hybrid_search_returns_serializable_dicts(content_tree) -> None:
    results = hybrid_search.hybrid_search_as_dicts("persistent identifiers")
    assert results
    first = results[0]
    expected_keys = {
        "chunk_id", "source", "path", "section_number",
        "section_title", "excerpt", "rrf_score", "bm25_rank", "semantic_rank",
    }
    assert expected_keys.issubset(set(first))


def test_hybrid_search_collection_filter_docs(content_tree) -> None:
    hits = hybrid_search.hybrid_search("metadata", collection="docs")
    assert all(h.source == "docs" for h in hits)


def test_hybrid_search_collection_filter_prompts(content_tree) -> None:
    hits = hybrid_search.hybrid_search("assessor interview", collection="prompts")
    assert all(h.source == "prompts" for h in hits)


def test_hybrid_search_empty_query_returns_nothing(content_tree) -> None:
    assert hybrid_search.hybrid_search("") == []


def test_hybrid_search_max_results_respected(content_tree) -> None:
    hits = hybrid_search.hybrid_search("the", max_results=2)
    assert len(hits) <= 2


def test_invalidate_index_clears_cache(content_tree) -> None:
    hybrid_search.hybrid_search("metadata")
    assert hybrid_search._INDEX is not None
    hybrid_search.invalidate_index()
    assert hybrid_search._INDEX is None


def test_rrf_score_positive(content_tree) -> None:
    hits = hybrid_search.hybrid_search("FAIR data")
    for h in hits:
        assert h.rrf_score > 0


def test_chunk_excerpt_truncates(content_tree) -> None:
    chunk = hybrid_search.Chunk(
        chunk_id="test::file.md::root",
        source="docs",
        path="file.md",
        section_number=None,
        section_title="Test",
        body="word " * 200,
    )
    exc = chunk.excerpt(max_chars=50)
    assert len(exc) <= 55  # small slack for ellipsis
    assert exc.endswith("…")
