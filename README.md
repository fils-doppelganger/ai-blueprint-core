# ai-blueprint-core

AI agent tooling to help NIAID-funded data repositories implement the [NIAID Blueprint for Digital Objects](https://datascience.niaid.nih.gov/resources).

The Blueprint is a FAIR data initiative from NIAID/ODSET that defines minimal metadata schemas, persistent identifiers (PIDs), API standards, and citation practices for research data repositories. This project provides LLM-driven agents — guided by structured prompt personas — to help repository owners and staff assess and implement Blueprint requirements across its five areas:

1. **Metadata schema** — schema.org-based metadata elements for digital objects
2. **Persistent identifiers** — DOIs, ORCIDs, RORs, RRIDs, and ontology terms
3. **APIs and machine access** — JSON-LD endpoints, OpenAPI documentation, structured data
4. **Citation guidance** — PID-based citation examples in standard formats
5. **Outreach and training** — Contact Points, training materials, Portal onboarding

## Agents

Agents are defined as prompt personas in `prompts/`:

| Prompt | Purpose |
|--------|---------|
| `fairAssessmentInterview.md` | Conducts a structured 6-phase interview to assess a repository's current Blueprint alignment and produces a gap report with prioritized recommendations |

## Requirements

- Python 3.13+
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management

## Setup

```bash
# Clone and install
git clone <repo-url>
cd ai-blueprint-core
uv sync
```

## Usage

```bash
uv run main.py
```

## Reference

The authoritative Blueprint specification is in `docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md` (converted from the PDF via `docling`/`marker-pdf`).

## Dependencies

- [`docling`](https://github.com/docling-project/docling) — structured document parsing and extraction
- [`marker-pdf`](https://github.com/VikParuchuri/marker) — high-quality PDF-to-Markdown conversion

Both are ML-based libraries; expect a large `.venv` and model downloads on first run.
