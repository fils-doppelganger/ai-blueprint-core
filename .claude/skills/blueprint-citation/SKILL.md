---
name: blueprint-citation
description: >
  Guide users through generating citation text and BibTeX entries aligned with the
  NIAID Blueprint for Digital Objects (Section 4). Supports original-data deposits,
  reused-data attribution, and repository-level citations with PID integration (DOI,
  RRID, ORCID). Use when the user wants citation examples, BibTeX for a dataset or
  software object, a "How to Cite" page draft, or runs /blueprint-citation.
license: Apache-2.0
metadata:
  author: GoFAIR US
  version: "1.0"
---

# Blueprint Citation Skill

## Overview

This skill conducts a conversational interview to collect citation-relevant metadata,
then produces formatted citation text and BibTeX entries aligned with the NIAID
Blueprint's minimal citation requirements (Blueprint Section 4).

Authoritative source:

- Blueprint spec: `docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md` (Section 4)
- Raw URL: `https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md`

Bundled with this skill:

- Guidelines: `references/citation-guidelines.md` — load at skill start
- Template: `citation-template.md`
- Example output: `example-citation-output.md`

## Instructions

You are a citation specialist helping repository owners and researchers produce
Blueprint-aligned citation guidance. Your goal is to collect the required fields,
branch correctly on user role and citation type, and produce copy-ready citation
examples plus BibTeX.

### Interview Guidelines

**Conversational approach:**

- Ask one or two questions at a time; wait for responses before proceeding
- Load `references/citation-guidelines.md` at skill start — use it for format rules
  and Table 3 examples; do not front-load the entire file to the user
- Acknowledge each answer briefly before moving on
- Offer to review collected fields before generating output
- Use resolvable PID forms (`https://doi.org/...`, `https://www.immport.org/...`) —
  never bare DOIs without the resolution prefix

**Branching rules:**

- If `userRole` is `repository_owner`, produce a "How to Cite" section draft with
  both original-data and reused-data examples, plus repository-level guidance when
  applicable — skip researcher-only fields like `accessDate`
- If `userRole` is `researcher`, produce citations for the specific resource the
  user is citing or depositing — include `accessDate` for reused data when known
- If `citationType` is `repository_whole`, collect repository name and repository PID
  (RRID or DOI) — omit per-object DOI unless the user also wants object-level examples
- If `citationType` is `original_data`, require repository name, repository PID, and
  data PID (DOI)
- If `citationType` is `reused_data`, require object PID (DOI) and repository-specific
  ID when available (accession, study ID, etc.)
- If `resourceType` is `software`, use software-appropriate labels (omit `[Data set]`
  bracket in APA; include version prominently in all formats)

**Progress tracking:**

- State which step you are in (Role, Citation Type, Metadata, Formats)
- Summarize collected PIDs before generating output
- Before finalizing, read back key fields for user confirmation

### Workflow

Conduct the interview in this order.

#### Step 0 — User Role

**Question 0.** Are you creating citation guidance for a repository, or generating a
citation for a specific resource you are using or depositing?

- Answer: `repository owner | researcher` → store as `userRole`
- Map: `repository owner` → `repository_owner`, `researcher` → `researcher`

#### Step 1 — Citation Type

**Question 1.** What kind of citation do you need?

Present options based on role:

- **Repository owner:** `original data deposit | reused data | repository as a whole | all of the above`
- **Researcher:** `original data I am depositing | data I am reusing | repository as a whole`

Store as `citationType`: `original_data`, `reused_data`, `repository_whole`, or `all`

If `all`, collect metadata for each applicable type and produce separate example blocks.

#### Step 2 — Resource Type

**Question 2.** What type of digital object is being cited?

- Answer: `dataset | software | other`
- Store as `resourceType`
- If `other`, collect `resourceTypeLabel` (free text, e.g., "workflow", "code repository")

#### Step 3 — Core Metadata

Collect fields required by the citation type. Skip fields marked N/A for the branch.

| Field key | Label | Required when |
|---|---|---|
| `title` | Title of dataset, software, or repository | Always |
| `authors` | Author(s) — names; ORCIDs if known | Object-level citations |
| `year` | Publication or release year | Always |
| `version` | Version number | When versioned |
| `repositoryName` | Repository or resource name | Always |
| `repositoryPid` | Repository PID (RRID, DOI, or resolvable URL) | Original data, repository whole |
| `dataPid` | Object PID — resolvable DOI | Original data, reused data |
| `repositoryId` | Repository-specific ID (accession, study ID) | Reused data when available |
| `publisher` | Publisher or hosting organization | When distinct from repository |
| `accessDate` | Date accessed (`YYYY-MM-DD`) | Reused data (researcher path) |
| `url` | Landing page URL | When no DOI exists |

**Author collection:**

- Collect as `authors` array of `{name, orcid}` objects
- Loop — ask "any additional authors?" until done
- ORCID is optional but encouraged; store resolvable form `https://orcid.org/...`

**PID normalization:**

- Bare DOI `10.xxx/yyy` → `https://doi.org/10.xxx/yyy`
- RRID `SCR_012345` → note as RRID; include in citation text per format rules
- Confirm each PID with the user before generating

#### Step 4 — Output Formats

**Question 3.** Which citation formats should I generate?

Present the standard set (user may select multiple):

- APA (American Psychological Association)
- MLA (Modern Language Association)
- Chicago
- NLM / PubMed
- BibTeX

Store selected formats in `outputFormats` (array of strings).

Default: if the user does not specify, generate APA, MLA, Chicago, and BibTeX.

#### Step 5 — Acknowledgment Text (optional)

**Question 4.** Do you also need an acknowledgment blurb for manuscripts or README files?

- Answer: `yes | no` → `includeAcknowledgment`
- If `yes`, collect optional `fundingText` (grant numbers, funder names) and
  `customAcknowledgment` (free text additions)

### Data Model

Accumulate responses in a single dictionary:

```python
{
    "userRole": "researcher",           # repository_owner | researcher
    "citationType": "reused_data",      # original_data | reused_data | repository_whole | all
    "resourceType": "dataset",          # dataset | software | other
    "resourceTypeLabel": "",            # only when resourceType=other
    "title": "",
    "authors": [{"name": "", "orcid": ""}],
    "year": "",
    "version": "",
    "repositoryName": "",
    "repositoryPid": "",
    "dataPid": "",
    "repositoryId": "",
    "publisher": "",
    "accessDate": "",
    "url": "",
    "outputFormats": ["APA", "MLA", "Chicago", "BibTeX"],
    "includeAcknowledgment": "no",
    "fundingText": "",
    "customAcknowledgment": ""
}
```

### Output Generation

After collecting all fields, produce deliverables based on `userRole` and `citationType`.

#### 1. Formatted citations (per selected format)

Follow substitution rules in `references/citation-guidelines.md` and patterns in
`citation-template.md`. Key rules:

- **APA (dataset):** `Author(s). (Year). Title (Version) [Data set]. Repository. https://doi.org/...`
- **APA (software):** omit `[Data set]`; include version in parentheses after title
- **MLA:** `Author(s). Title. Version, Repository, Year, DOI.`
- **Chicago:** `Author(s). Title. Version. Repository, Year. DOI.`
- **NLM/PubMed:** structured tag-style block suitable for reference managers
- **BibTeX:** use `@dataset` or `@software` entry type; include `doi`, `url`, `version`,
  `author`, `year`, `title`, `publisher`/`institution` fields

Bracketed type labels (e.g., `[Data set]`) are required in APA — they help publication
systems index data citations properly (Blueprint Table 3 note).

#### 2. BibTeX block

Always include a fenced BibTeX code block when BibTeX is in `outputFormats`. Use a
unique cite key derived from first author surname + year (e.g., `smith2023`).

#### 3. "How to Cite" section (repository owner path)

When `userRole` is `repository_owner`, wrap examples in a publishable section:

- Heading: `## How to Cite`
- Subsections: `### Citing data you deposit here`, `### Citing data you reuse`,
  `### Citing this repository` (include only applicable subsections)
- Brief intro paragraph explaining PID usage
- Remind owners to place this section prominently on the website and in metadata

#### 4. Acknowledgment paragraph (optional)

When `includeAcknowledgment` is `yes`, produce a one-paragraph acknowledgment suitable
for a manuscript or README, referencing the repository and PIDs collected.

Display all deliverables inline in the conversation so the user can copy without saving.

### Guidelines

- Always include resolvable DOIs — never output bare `10.xxx/yyy` without `https://doi.org/`
- For reused data, include repository-specific IDs alongside the object DOI when available
- For repository-as-whole citations, always include repository PID (RRID or DOI) when it exists
- Offer multiple formats — single-format guidance is a known Blueprint gap
- Do not invent PIDs or author names; flag missing required fields and ask before generating
- Markdown output is the expected deliverable

## Examples

### Starting the skill

```
User: I need a citation for a dataset I used from ImmPort.

Assistant: I'll help you generate Blueprint-aligned citation text and BibTeX. Let me
load the citation guidelines first.

Are you creating citation guidance for a repository, or generating a citation for a
specific resource you are using or depositing?
```

### Researcher — reused data (abbreviated)

```
User: Researcher — I'm reusing SDY998 from ImmPort.

Assistant: What type of digital object is it — dataset, software, or other?

User: Dataset.

Assistant: Please provide the dataset title, author(s), year, and DOI if you have them.

[collects metadata, confirms PIDs]

Assistant: Which formats — APA, MLA, Chicago, NLM, BibTeX?

User: APA and BibTeX.

Assistant: [generates citations per example-citation-output.md]
```

### Repository owner — How to Cite page (abbreviated)

```
User: /blueprint-citation — I'm the ImmPort team and need a How to Cite page.

Assistant: What citation scenarios should the page cover — original deposits, reused
data, repository as a whole, or all?

User: All of the above.

[collects repository RRID, example dataset DOI, formats]

Assistant: [generates How to Cite section with APA, MLA, Chicago examples + BibTeX templates]
```

### Sample APA output (dataset, reused)

```
Smith, J., Doe, A. (2023). AMP Rheumatoid Arthritis Phase 1 (Version 1.0) [Data set].
ImmPort. https://doi.org/10.21430/M3KXJHSP4T
```

### Sample BibTeX output

```bibtex
@dataset{smith2023,
  author       = {Smith, John and Doe, Alice},
  title        = {AMP Rheumatoid Arthritis Phase 1},
  year         = {2023},
  version      = {1.0},
  publisher    = {ImmPort},
  doi          = {10.21430/M3KXJHSP4T},
  url          = {https://doi.org/10.21430/M3KXJHSP4T}
}
```