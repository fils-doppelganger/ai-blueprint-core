# NIAID Blueprint Claude Skills

Three Claude Code skills for working with the [NIAID Blueprint for Digital Objects](../docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md). Skills are installed automatically when Claude Code is opened in this project.

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

## Skill files

All three skills live in `.claude/skills/` and follow the standard Claude Code skill layout:

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
└── blueprint-metadata-extract/
    ├── SKILL.md
    └── references/
        └── extraction-workflow.md
```
