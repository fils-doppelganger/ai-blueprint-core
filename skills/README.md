# NIAID Blueprint Claude Skills

Six Claude Code skills for working with the [NIAID Blueprint for Digital Objects](../docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md) and related research transparency workflows. Skills are installed automatically when Claude Code is opened in this project.

---

## `/fair-assess` — Blueprint FAIR Assessment

Conducts a structured interview across the Blueprint's five areas (metadata schema, persistent identifiers, APIs, citation, outreach) and produces a prioritized gap report with recommended next steps.

**Use when:** A repository owner, data steward, or PI wants to know how well their resource aligns with the Blueprint, or is preparing to integrate with the NIAID Data Ecosystem Discovery Portal.

**How to invoke:**
```
/fair-assess
/fair-assess MyRepositoryName
```

**Output:** A Markdown assessment report — one section per Blueprint area, each with current state, gaps, priority (High/Medium/Low), and one concrete recommended action. Ends with a 2–3 sentence overall readiness summary.

---

## `/dataset-intake` — Dataset Metadata Intake

Conducts a conversational interview to collect metadata for a dataset and produces a valid JSON-LD document (`@type: Dataset`) aligned with the Blueprint's schema.org-based metadata schema.

**Use when:** A researcher or repository manager needs to generate structured metadata for a dataset — whether depositing to a repository, preparing for Portal indexing, or creating a citable metadata record.

**How to invoke:**
```
/dataset-intake
/dataset-intake "My Dataset Name"
```

**Output:** A JSON-LD document covering up to 16 Blueprint metadata elements (name, description, DOI, author/ORCID, funder/ROR, grant, measurementTechnique, infectiousAgent, host, healthCondition, conditionsOfAccess, license, distribution, temporalCoverage, spatialCoverage, citation). Missing required fields are flagged in a Metadata Notes section.

The interview can be stopped early with "make the record with what you have" — the skill generates valid JSON-LD from whatever has been collected.

---

## `/blueprint-metadata-extract` — URL Metadata Extraction

Fetches a web resource URL and extracts Blueprint-aligned schema.org JSON-LD metadata by analyzing the page. No interview — the agent retrieves evidence from the web.

**Use when:** You have a dataset or resource landing-page URL and want a draft JSON-LD record without manually answering intake questions.

**How to invoke:**
```
/blueprint-metadata-extract https://immport.org/shared/study/SDY998
```

**Output:** Resource summary, a JSON-LD code block, and metadata notes (found / inferred / missing fields, unresolved PIDs, confidence). Authoritative references are fetched from GitHub raw URLs at run time.

See also: `docs/metadataGeneration.md`

---

## `/model-statement` — Model Influence Statement

Conducts a conversational interview to collect structured disclosures about machine-learning model use in a research work, branching on whether a model was used, then produces a complete Model Influence Statement and a one-paragraph acknowledgment summary. Mirrors the upstream [Model Influence Statement Generator](https://model-influence-statement-generator.netlify.app/).

**Use when:** An author wants to create, fill out, or export a model influence statement, disclose ML model use in a publication, or acknowledge AI assistance in research.

**How to invoke:**
```
/model-statement
```

**Output:** A Markdown statement with section headings matching the upstream template, plus a plain-text acknowledgment paragraph suitable for manuscripts or README files. Optionally, timestamped JSON and file artifacts via `scripts/save_statement.py`.

---

## `/blueprint-citation` — Citation Text and BibTeX

Conducts a conversational interview to collect citation-relevant metadata, then produces formatted citation text and BibTeX entries aligned with the Blueprint's minimal citation requirements (Section 4). Supports original-data deposits, reused-data attribution, and repository-level citations with PID integration.

**Use when:** A repository owner needs a "How to Cite" page draft, or a researcher needs copy-ready citation examples (APA, MLA, Chicago, NLM) and BibTeX for a dataset, software object, or repository.

**How to invoke:**
```
/blueprint-citation
/blueprint-citation ImmPort SDY998
```

**Output:** Formatted citations in the requested styles, a BibTeX code block, and — for repository owners — a publishable "How to Cite" section with original-data, reused-data, and repository-level examples. Optionally, a one-paragraph acknowledgment for manuscripts or README files.

---

## `/teach-blueprint` — Blueprint Teaching Course

Teaches the NIAID Blueprint through stateful, multi-session lessons grounded in a persistent teaching workspace. Creates or extends `MISSION.md`, HTML lessons, learning records, a glossary, and reference sheets — citing high-trust sources from `RESOURCES.md` rather than lecturing from memory.

**Use when:** A learner or trainer wants structured, progressive Blueprint lessons across multiple sessions toward a concrete repository goal — for example, "teach me the Blueprint" or "Blueprint course."

**How to invoke:**
```
/teach-blueprint
```

**Output:** Workspace artifacts under `.claude/skills/teach-blueprint/` by default (or a user-chosen path): `MISSION.md`, `lessons/000N-slug.html`, `learning-records/`, `GLOSSARY.md`, `reference/*.html`, and updated `NOTES.md`. Later curriculum lessons assign hands-on work using `fair-assess`, `dataset-intake`, and `blueprint-metadata-extract`.

---

## Skill files

All six skills live in `.claude/skills/` and follow the standard Claude Code skill layout:

```
.claude/skills/
├── fair-assess/
│   ├── SKILL.md
│   ├── references/
│   │   ├── interview-phases.md
│   │   ├── blueprint-quick-ref.md
│   │   └── gap-patterns.md
│   └── assets/
│       └── report-template.md
├── dataset-intake/
│   ├── SKILL.md
│   ├── references/
│   │   ├── element-guide.md
│   │   ├── pid-help.md
│   │   └── jsonld-structure.md
│   └── assets/
│       └── blank-dataset.jsonld
├── blueprint-metadata-extract/
│   ├── SKILL.md
│   └── references/
│       └── extraction-workflow.md
├── model-statement/
│   ├── SKILL.md
│   ├── statement-template.md
│   ├── example-influence-statement.md
│   ├── scripts/
│   │   └── save_statement.py
│   └── tests/
│       └── test_save_statement.py
├── blueprint-citation/
│   ├── SKILL.md
│   ├── citation-template.md
│   ├── example-citation-output.md
│   ├── scripts/
│   │   └── save_citation.py
│   └── references/
│       └── citation-guidelines.md
└── teach-blueprint/
    ├── SKILL.md
    ├── MISSION-EXAMPLE.md
    ├── references/
    │   ├── teaching-phases.md
    │   └── curriculum-map.md
    ├── formats/
    ├── templates/
    │   └── lesson-template.html
    ├── lessons/
    ├── reference/
    └── assets/
        └── shared.css
```