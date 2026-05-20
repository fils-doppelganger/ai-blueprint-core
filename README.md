# ai-blueprint-core

AI agent tooling to help NIAID-funded data repositories implement the [NIAID Blueprint for Digital Objects](https://datascience.niaid.nih.gov/resources).

The Blueprint is a FAIR data initiative from NIAID/ODSET that defines minimal metadata schemas, persistent identifiers (PIDs), API standards, and citation practices for research data repositories. This project provides LLM-driven agents — guided by structured prompt personas — to help repository owners and staff assess and implement Blueprint requirements across its five areas:

1. **Metadata schema** — schema.org-based metadata elements for digital objects
2. **Persistent identifiers** — DOIs, ORCIDs, RORs, RRIDs, and ontology terms
3. **APIs and machine access** — JSON-LD endpoints, OpenAPI documentation, structured data
4. **Citation guidance** — PID-based citation examples in standard formats
5. **Outreach and training** — Contact Points, training materials, Portal onboarding

## Flipped Interaction Pattern  

This is not an agent, rather just a pattern that inverts the normal chat mode to where
the language model initializes with a prompt and waits for user input to continue the conversation.

I have an example in the prompts directory, but it's long and verbose, so it would likely be good to 
make a version that is more concise and easier to understand.

| Prompt | Purpose |
|--------|---------|
| `fairAssessmentInterview.md` | Conducts a structured 6-phase interview to assess a repository's current Blueprint alignment and produces a gap report with prioritized recommendations |

Paste the above document into your prompt, and all modern models should begin the interview 
process and then conclude with a summary of the responses.    Again, this can get long, so if you get to a point
you want to stop, tell the model something like; "stop the interview and give me the summary now".


## Usage

There is no executable code in this repository at this time that you need to run.   This is just
used to convert PDF to Markdown, and the results are already in the __docs__ directory. 


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


## Reference

The authoritative Blueprint specification is in `docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md` (converted from the PDF via `docling`/`marker-pdf`).

If you wish to pass this to a model, use the GitHub raw link: https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md

## Dependencies

- [`docling`](https://github.com/docling-project/docling) — structured document parsing and extraction
- [`marker-pdf`](https://github.com/VikParuchuri/marker) — high-quality PDF-to-Markdown conversion

Both are ML-based libraries; expect a large `.venv` and model downloads on first run.
