"""Shared pytest fixtures: a temporary docs/prompts content tree.

These fixtures monkeypatch the module-level roots in ``mcp_bp.config`` so the
content/search/sections helpers operate on a controlled fixture tree.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_bp import config, content, hybrid_search, search


BLUEPRINT_FIXTURE = """\
# A Blueprint for Including Digital Objects

Intro text.

## 1. NIAID Minimal Metadata Schema

Metadata is essential. Required fields include identifier and license.

## 2. Persistent Identifiers (PIDs)

PIDs make objects resolvable. DOIs, ORCIDs and RORs are preferred.

### 2.1. Motivation

Long-term persistence and traceability.

## 3. Minimal API Specifications

APIs should return JSON-LD. Endpoints should be resource-oriented IRIs.
"""

PROMPT_FIXTURE = """\
You are a FAIR assessor.

Starting top-level page: https://example.org/old
Begin the interview now.
"""


@pytest.fixture
def content_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    docs = tmp_path / "docs"
    prompts = tmp_path / "prompts"
    (docs / "sub").mkdir(parents=True)
    prompts.mkdir(parents=True)

    spec = docs / config.BLUEPRINT_SPEC_RELPATH
    spec.write_text(BLUEPRINT_FIXTURE, encoding="utf-8")
    (docs / "sub" / "extra.md").write_text(
        "# Extra Doc\n\nSome citation guidance here.\n", encoding="utf-8"
    )
    # A non-markdown sibling that must be ignored.
    (docs / "ignore.pdf").write_bytes(b"%PDF-1.4 binary")

    (prompts / "fairAssessorAgentOpenCode.md").write_text(
        PROMPT_FIXTURE, encoding="utf-8"
    )

    # Point all modules at the fixture tree.
    for module in (config, content, search, hybrid_search):
        monkeypatch.setattr(module, "DOCS_DIR", docs, raising=False)
        monkeypatch.setattr(module, "PROMPTS_DIR", prompts, raising=False)

    # Clear the hybrid search index so each test builds fresh from the fixture.
    monkeypatch.setattr(hybrid_search, "_INDEX", None)

    return {"docs": docs, "prompts": prompts, "spec": spec}
