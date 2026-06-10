"""Tests for Blueprint section parsing and extraction."""

from __future__ import annotations

import pytest

from mcp_bp import sections


def test_parse_sections_counts_and_numbers(content_tree) -> None:
    from mcp_bp.tests.conftest import BLUEPRINT_FIXTURE

    parsed = sections.parse_sections(BLUEPRINT_FIXTURE)
    numbers = [s.number for s in parsed if s.number]
    assert "1" in numbers
    assert "2" in numbers
    assert "2.1" in numbers
    assert "3" in numbers


def test_get_section_by_number(content_tree) -> None:
    rendered = sections.get_blueprint_section("2")
    assert "Persistent Identifiers" in rendered
    assert "resolvable" in rendered


def test_get_subsection_by_number(content_tree) -> None:
    rendered = sections.get_blueprint_section("2.1")
    assert "Motivation" in rendered
    assert "traceability" in rendered


def test_get_section_by_heading_substring(content_tree) -> None:
    rendered = sections.get_blueprint_section("API")
    assert "JSON-LD" in rendered


def test_unknown_section_raises(content_tree) -> None:
    with pytest.raises(ValueError):
        sections.get_blueprint_section("does-not-exist-anywhere")
