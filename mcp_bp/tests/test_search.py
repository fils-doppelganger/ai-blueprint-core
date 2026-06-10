"""Tests for ranked fuzzy search across docs and prompts."""

from __future__ import annotations

from mcp_bp import search


def test_search_finds_relevant_doc(content_tree) -> None:
    hits = search.search("JSON-LD", max_results=5)
    assert hits
    top = hits[0]
    assert "API" in top.snippet or "JSON-LD" in top.snippet
    assert top.score >= 50.0


def test_search_returns_serializable_dicts(content_tree) -> None:
    results = search.search_as_dicts("persistent identifiers")
    assert results
    first = results[0]
    assert set(first) == {"source", "path", "line", "score", "snippet"}


def test_search_spans_docs_and_prompts(content_tree) -> None:
    results = search.search_as_dicts("interview assessor", max_results=20)
    sources = {r["source"] for r in results}
    assert "prompts" in sources


def test_empty_query_returns_nothing(content_tree) -> None:
    assert search.search("") == []


def test_max_results_is_respected(content_tree) -> None:
    results = search.search_as_dicts("the", max_results=2)
    assert len(results) <= 2
