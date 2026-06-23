# Model Influence Statement — Claude Code Skill

A conversational interview skill for developing a complete [Model Influence
Statement](https://model-influence-statement-generator.netlify.app/) — the voluntary
transparency document for disclosing machine-learning model use in research works.

## Overview

This skill replicates the disclosure workflow from the upstream web application without
porting its React UI or browser-side DOCX export. It guides authors through the exact
question sequence, collects structured responses, and produces:

- A full **markdown statement** with section headings matching the upstream template
- A one-paragraph **acknowledgment summary** for software acknowledgments or citations
- Optional **timestamped JSON + file artifacts** via a small Python helper

**Source references:**

- Live app: https://model-influence-statement-generator.netlify.app/
- GitHub: https://github.com/pengyin-shan/Model-Influence-Statement
- CRediT roles: https://credit.niso.org/contributor-roles-defined/

## Directory Layout

```
model-statement/
├── SKILL.md                        # Main skill definition (interview + output rules)
├── README.md                       # This file
├── statement-template.md           # Verbatim upstream blank template
├── example-influence-statement.md  # Verbatim upstream worked example
├── scripts/
│   └── save_statement.py           # Serialize responses and render statement files
└── tests/
    └── test_save_statement.py      # Unit tests for statement builders
```

## Installation

No extra Python dependencies are required (stdlib only).

The skill lives at `.claude/skills/model-statement/SKILL.md` in this repository. Claude
Code auto-discovers skills placed under `.claude/skills/` when it opens in the project,
so no manual registration is needed.

Optional: make the save script executable:

```bash
chmod +x .claude/skills/model-statement/scripts/save_statement.py
```

## Usage

### Starting an interview

Invoke the skill in conversation with the slash command:

```
/model-statement
```

Or ask naturally:

```
I need to create a model influence statement for my publication.
```

The assistant will ask questions one or two at a time, branch on whether a model was
used, support single or multiple model entries, and produce final outputs on completion.

### Interview sections

| Section | Upstream question | Key fields |
|---|---|---|
| Work metadata | — | `workTitle`, `authors` |
| Core Disclosure | Q1: model used? | `usedModel` |
| No-model certification | — | `noModelSignature`, `noModelDate` |
| Disclosure scope | Q2: one or multiple? | `disclosureScope` |
| Model Information | — | 10 fields per model entry |
| Training Data Disclosure | — | 3 yes/no/unknown fields |
| Roles | Q3: CRediT roles | `roles`, `customRoles` |
| Additional Disclosure | Q4 | `whatElse` |
| Critical Prompt | Q5 | `shareCriticalPrompt`, `criticalPrompt` |
| Ethical Considerations | Q6 | `ethics` |
| Final Certification | — | `finalSignature`, `finalDate` |

### Saving outputs

After the interview, pass collected JSON to the save helper:

```bash
python .claude/skills/model-statement/scripts/save_statement.py '<json_data>' [output_dir]
```

Produces timestamped files:

- `model_influence_statement_YYYYMMDD_HHMMSS.json`
- `{work-title}-statement_YYYYMMDD_HHMMSS.md`
- `{work-title}-acknowledgment_YYYYMMDD_HHMMSS.txt`

## Output Formats

### Markdown statement

Uses `##` section headings per `example-influence-statement.md`:

- Responsibility Statement (verbatim upstream text)
- Core Disclosure
- Model Information (`### Model Entry N` blocks with all 10 fields)
- Training Data Disclosure
- Roles Played by the Model
- Additional Disclosure
- Critical Prompt Disclosure
- Ethical Considerations
- Final Certification

### Acknowledgment paragraph

A single plain-text paragraph summarizing model use, roles, tasks, training exposure,
and optional ethical/prompt context — suitable for README acknowledgments or manuscript
text.

## Testing

```bash
python -m pytest .claude/skills/model-statement/tests/test_save_statement.py -v
```

## Non-goals

- Replicating the React + MUI web UI or Netlify deployment
- Producing binary `.docx` files (markdown + plain text only)
- Standalone CLI form filler outside the conversational skill pattern