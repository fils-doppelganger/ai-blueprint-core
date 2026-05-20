# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

`ai-blueprint-core` is a Python project building AI agent tooling for the NIAID Blueprint for Digital Objects — a FAIR data initiative by NIAID/ODSET that specifies minimal metadata schemas, persistent identifiers, API standards, and citation practices for NIAID-funded research data repositories.

The project uses LLM agents (guided by prompts in `prompts/`) to help users and repository owners implement the Blueprint's five key areas: metadata schema, PIDs, APIs, citation, and outreach.

## Development Commands

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency and environment management (Python 3.13).

```bash
# Install dependencies and sync environment
uv sync

# Run the main entry point
uv run main.py

# Add a new dependency
uv add <package>

# Run a script directly
uv run <script>.py
```

## Architecture

- **`main.py`** — entry point (currently a stub; feature code goes here or in modules imported here)
- **`prompts/`** — system prompts for AI agent personas:
  - `archInterview.md` — 10-phase agent architect persona; guides users through designing production-grade AI agents (discovery → cognitive architecture → orchestration → tools → grounding → prompts → implementation → testing → deployment → delivery)
  - `interview.md` — non-technical user interview persona; conducts discovery conversations and outputs a project `CLAUDE.md`
- **`docs/`** — NIAID Blueprint reference document (PDF + Markdown conversion via `marker-pdf`/`docling`)

## Key Dependencies

- **`docling`** — document understanding and extraction (structured parsing of PDFs/docs)
- **`marker-pdf`** — high-quality PDF-to-Markdown conversion (used to produce `docs/*.md` from blueprint PDFs)

Both are heavy ML-based libraries; expect significant `.venv` size and first-run model downloads.

## Domain Context

The NIAID Blueprint (`docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md`) is the authoritative spec. Key concepts:
- **FAIR principles** — Findable, Accessible, Interoperable, Reusable
- **Digital objects** — data, software, methods, workflows produced by NIAID-funded research
- **PIDs** — persistent identifiers (e.g., ORCIDs for researchers, DOIs for datasets)
- **NIAID Data Ecosystem Discovery Portal** — the target discovery system repositories feed into
