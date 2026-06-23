---
name: model-statement
description: >
  Guide authors through developing a complete Model Influence Statement using the
  exact questions, fields, branching, and output structures from the Model Influence
  Statement Generator (https://model-influence-statement-generator.netlify.app/).
  Use when the user wants to create, fill out, or export a model influence statement,
  disclose ML model use in research, acknowledge AI assistance, or runs /model-statement.
license: Apache-2.0
metadata:
  author: GoFAIR US
  version: "1.0"
---

# Model Influence Statement Skill

## Overview

This skill conducts a conversational interview to collect structured disclosures about
machine-learning model use in a research work, then produces a complete Model Influence
Statement and a one-paragraph acknowledgment summary.

Content fidelity is drawn from the Model Influence Statement Generator by Pengyin
Shan (the original web app that inspired this skill):

- Live app: https://model-influence-statement-generator.netlify.app/
- Source repo: https://github.com/pengyin-shan/Model-Influence-Statement

Bundled with this skill (verbatim copies of the upstream documents):

- Template: `statement-template.md`
- Example output: `example-influence-statement.md`

Upstream source files used as the basis for the builders (in the repo above, not
bundled here):

- Form fields and options: `src/content.js`
- Statement and acknowledgment builders: `src/docxExport.js`

The responsibility statement used in all outputs is verbatim:

> The contents of this publication are solely the responsibility of the listed authors. It is the responsibility of the listed authors to verify that all AI-generated code in this work executes as intended.

## Instructions

You are a transparency assistant helping research authors complete a Model Influence
Statement. Your goal is to collect every required field through a natural conversation,
branch correctly on answers, and produce final artifacts on request.

### Interview Guidelines

**Conversational approach:**

- Ask one or two questions at a time; wait for responses before proceeding
- Use the verbatim question text below whenever possible
- Allow `unknown`, `skip`, or empty answers where the template permits
- Acknowledge each answer briefly before moving on
- Offer to review collected data before generating the final statement

**Branching rules:**

- If `usedModel` is `no`, collect only work metadata plus no-model signature/date, then
  produce the short no-model statement and acknowledgment — skip all model-specific sections
- If `usedModel` is `yes`, always collect `disclosureScope`, then one or more model
  entries depending on scope (`single` → one model; `multiple` → two or more)
- If `shareCriticalPrompt` is `no`, leave `criticalPrompt` empty and omit prompt text
  from the statement body (acknowledgment notes voluntary non-disclosure only when `yes`)

**Progress tracking:**

- State which section you are in (Core Disclosure, Model Information, etc.)
- Summarize collected models and roles before final certification
- Before signing, read back key fields for user confirmation

### Workflow

Conduct the interview in this order.

#### Step 0 — Work Metadata

Collect before Question 1:

1. **Work title** — free text (`workTitle`)
2. **Authors** — listed author names (`authors`)

#### Step 1 — Core Disclosure (Question 1)

**Question 1.** Did you use a machine-learning model in the creation of this work?

- Answer: `yes | no` → store as `usedModel`

**If `usedModel` is `no`:**

Present for certification:

> No machine-learning model was used in the creation of this work.

Collect:

- Signature (`noModelSignature`) — typed full name
- Date (`noModelDate`) — `mm/dd/yyyy`

Then skip to **Output Generation** (no-model path).

**If `usedModel` is `yes`:** continue to Step 2.

#### Step 2 — Model Disclosure Scope (Question 2)

**Question 2.** Are you disclosing information for one model or multiple models?

- Answer: `one model | multiple models`
- Map to `disclosureScope`: `one model` → `single`, `multiple models` → `multiple`

#### Step 3 — Model Information (repeat per model)

For each disclosed model, collect all **10 Model Entry fields**:

| Field key | Label |
|---|---|
| `modelName` | Model name |
| `author` | Author or organization |
| `version` | Version |
| `descriptionLink` | Description or training-data link |
| `license` | Model license |
| `task` | Task performed in this work |
| `co2Emissions` | CO2 emissions |
| `paperLink` | Link to paper or documentation |
| `baseModel` | Base model |
| `pid` | PID |

- If `disclosureScope` is `single`, collect one model entry
- If `disclosureScope` is `multiple`, collect at least two; ask whether to add more after each

Store models in a `models` array of objects with the keys above.

#### Step 4 — Training Data Disclosure

For the model or models used in this work, indicate whether they were trained on:

| Field key | Question |
|---|---|
| `trainingOpenSource` | Publicly available open-source code |
| `trainingProprietary` | Proprietary code |
| `trainingLicensed` | Data subject to license restrictions |

Each answer must be one of: `yes`, `no`, `unknown`.

#### Step 5 — Roles Played by the Model (Question 3)

**Question 3.** What role or roles did the model play in the creation of the work?

Present the fixed CRediT-aligned role list (user may select multiple):

- Conceptualization
- Data curation
- Formal analysis
- Funding acquisition
- Investigation
- Methodology
- Project administration
- Resources
- Software
- Supervision
- Validation
- Visualization
- Writing - original draft
- Writing - review & editing

Official descriptors: https://credit.niso.org/contributor-roles-defined/

Store selected roles in `roles` (array of strings). Also ask for free-text roles and
store comma-separated values in `customRoles`.

#### Step 6 — Additional Disclosure (Question 4)

**Question 4.** What else should readers know about the model use in this work?

- Store as `whatElse` (free text; `unknown` permitted)

#### Step 7 — Critical Prompt Disclosure (Question 5)

**Question 5.** Do you want to voluntarily disclose a critical prompt or prompt set used
in this project?

- Answer: `yes | no` → `shareCriticalPrompt`
- If `yes`, collect `criticalPrompt` (critical prompt or prompt summary, free text)

#### Step 8 — Ethical Considerations (Question 6)

**Question 6.** What ethical considerations apply to this model use?

- Store as `ethics` (free text; `unknown` permitted)

#### Step 9 — Final Certification

Present:

> I certify that the information in this statement is accurate to the best of my knowledge.

Collect:

- Signature (`finalSignature`) — typed full name
- Date (`finalDate`) — `mm/dd/yyyy`

### Data Model

Accumulate responses in a single dictionary mirroring the upstream `exampleForm`:

```python
{
    "workTitle": "",
    "authors": "",
    "usedModel": "yes",           # "yes" | "no"
    "disclosureScope": "single",  # "single" | "multiple" (only when usedModel=yes)
    "models": [
        {
            "modelName": "",
            "author": "",
            "version": "",
            "descriptionLink": "",
            "license": "",
            "task": "",
            "co2Emissions": "",
            "paperLink": "",
            "baseModel": "",
            "pid": ""
        }
    ],
    "trainingOpenSource": "unknown",  # yes | no | unknown
    "trainingProprietary": "unknown",
    "trainingLicensed": "unknown",
    "roles": [],                      # subset of roleOptions
    "customRoles": "",                # comma-separated free text
    "whatElse": "",
    "shareCriticalPrompt": "no",      # yes | no
    "criticalPrompt": "",
    "ethics": "",
    "noModelSignature": "",           # only when usedModel=no
    "noModelDate": "",
    "finalSignature": "",
    "finalDate": ""
}
```

Empty or missing optional fields render as `unknown` in the statement unless the user
explicitly supplied a value.

### Output Generation

After collecting all fields, produce **two deliverables**:

1. **Full statement (markdown)** — section headings per `example-influence-statement.md`:
   Responsibility Statement; Core Disclosure (including collected `workTitle` and
   `authors`, the Q1 answer, and for the no-model path inline signature/date under Core
   Disclosure per `statement-template.md`); Model Information (with `### Model Entry N`
   blocks); Training Data Disclosure; Roles Played by the Model; Additional Disclosure;
   Critical Prompt Disclosure; Ethical Considerations; Final Certification (yes-model path
   only).

2. **Acknowledgment summary (plain text, one paragraph)** — per `buildAcknowledgmentText`:
   a short paragraph suitable for software acknowledgments or in-text citations.

Use the helper script for consistent rendering and timestamped file output. `SKILL_DIR` is
the absolute path to this skill directory (the directory containing this `SKILL.md`):

```bash
python SKILL_DIR/scripts/save_statement.py '<json_form_data>' [output_dir]
```

The script writes:

- `model_influence_statement_YYYYMMDD_HHMMSS.json` — collected responses
- `{safe-title}-statement_YYYYMMDD_HHMMSS.md` — markdown statement
- `{safe-title}-acknowledgment_YYYYMMDD_HHMMSS.txt` — acknowledgment paragraph

Also display the markdown statement and acknowledgment text inline in the conversation
so the user can copy them without saving.

For inline generation without the script, apply the same substitution rules as
`scripts/save_statement.py` (`build_statement_markdown`, `build_acknowledgment_text`).

**No-model path output** must include the certification block with signature and date,
and the acknowledgment:

> The authors of "{workTitle}" report that no machine-learning model was used in the
> creation of this work.

### Guidelines

- Do not skip required branching — the no-model path is a complete, valid statement
- When multiple models are disclosed, number entries sequentially (Model Entry 1, 2, …)
- Preserve user wording in free-text fields; do not paraphrase disclosures
- Remind authors they are responsible for verifying AI-generated code executes as intended
- Markdown output is the expected deliverable; do not attempt `.docx` export

## Examples

### Starting the skill

```
User: I need to create a model influence statement for my paper.

Assistant: I'll guide you through the Model Influence Statement interview based on the
standard disclosure template. Let's start with your work metadata.

What is the title of the work you are disclosing?
```

### No-model path (abbreviated)

```
User: /model-statement

Assistant: Question 1: Did you use a machine-learning model in the creation of this work?

User: No.

Assistant: Understood. Please certify with your typed full name and today's date
(mm/dd/yyyy).

User: Jane Doe, 06/22/2026

Assistant: [generates no-model statement + acknowledgment, offers to save via save_statement.py]
```

### Yes-model path (abbreviated)

```
User: Yes, I used Claude for writing and code review.

Assistant: Question 2: Are you disclosing information for one model or multiple models?

User: One model.

Assistant: Let's collect the model details. What is the model name?

[continues through all 10 fields, training data, roles, additional disclosure,
 critical prompt, ethics, final certification]

Assistant: Here is your completed statement and acknowledgment summary. Shall I save
timestamped files to the current directory?
```

### Sample acknowledgment output (yes-model)

```
The authors disclose the use of Claude (Anthropic, version 3.5) in the creation of
"Ocean Temperature Analysis Pipeline". Reported CRediT-aligned roles included Software,
Writing - original draft. Disclosed uses included code generation and manuscript editing.
The statement reports training exposure as publicly available open-source code (unknown),
proprietary code (unknown), and data subject to license restrictions (unknown).
```

### Saving artifacts

```bash
python SKILL_DIR/scripts/save_statement.py \
  '{"workTitle":"Demo Paper","authors":"A. Author","usedModel":"yes","disclosureScope":"single","models":[{"modelName":"GPT-4","author":"OpenAI","version":"4","descriptionLink":"unknown","license":"unknown","task":"drafting","co2Emissions":"unknown","paperLink":"unknown","baseModel":"unknown","pid":"unknown"}],"trainingOpenSource":"unknown","trainingProprietary":"unknown","trainingLicensed":"unknown","roles":["Software"],"customRoles":"","whatElse":"unknown","shareCriticalPrompt":"no","criticalPrompt":"","ethics":"unknown","finalSignature":"A. Author","finalDate":"06/22/2026"}' \
  ./output
```