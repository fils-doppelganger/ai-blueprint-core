"""Tests for prompt loading and instruction-block injection."""

from __future__ import annotations

import pytest

from mcp_bp import prompts_registry


def test_render_without_args_returns_body(content_tree) -> None:
    rendered = prompts_registry.render_prompt("fair_web_assessor")
    assert "FAIR assessor" in rendered
    assert "Session parameters" not in rendered


def test_render_with_url_prepends_instruction_block(content_tree) -> None:
    rendered = prompts_registry.render_prompt(
        "fair_web_assessor", url="https://example.org/new"
    )
    assert rendered.startswith("> **Session parameters")
    assert "https://example.org/new" in rendered
    # Original persona body still present after the block.
    assert "FAIR assessor" in rendered


def test_render_ignores_blank_optional_args(content_tree) -> None:
    rendered = prompts_registry.render_prompt(
        "fair_web_assessor", url="https://example.org/new", blueprint_url=None
    )
    assert "Blueprint Url" not in rendered


def test_unknown_prompt_raises(content_tree) -> None:
    with pytest.raises(ValueError):
        prompts_registry.render_prompt("nope")


def test_list_prompt_specs_shape() -> None:
    specs = prompts_registry.list_prompt_specs()
    names = {s["name"] for s in specs}
    assert "fair_assessment_interview" in names
    assert "work_plan_interview" in names
    web = next(s for s in specs if s["name"] == "fair_web_assessor")
    assert any(arg["name"] == "url" for arg in web["arguments"])
