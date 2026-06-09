# NIAID Blueprint Work Plan — Interview Spec & Output Template

This file is **both** the script that drives the interview **and** the shape of the
deliverable. The runner prompt (`workPlanInterview.md`) reads this template, conducts
the interview by turning each item in **Part 1** into an `AskUserQuestion` call, records
the answers, then fills **Part 2** to produce a populated Work Plan.

> **Never edit this template in place during a session.** The runner writes a *copy*
> (default `spec.md` in the working directory) and fills that. This file stays clean
> and reusable.

Source documents this spec is derived from:
- `docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md` — the authoritative spec (five areas: metadata schema, PIDs, APIs, citation, outreach/training).
- `docs/20260515_Work-Plans_Supplementary_DSJ.pdf` — Appendix I (Pre-Interview Questionnaire, Q1–Q43) and Appendix 2 (Generic Work Plan template). Part 1 below adapts Appendix I; Part 2 mirrors Appendix 2.

---

## Conventions

**Item fields** (each interview item):
- `id` — questionnaire number (Q1–Q43).
- `audience` — `all` or `services-dev` (Appendix I marks `services-dev` items with `*`; ask them only when the respondent is a Repository Services & Development team member — see Q5).
- `type` — `single` (one choice), `multi` (choose several), `open` (free text), `numeric` (a number or `-1` if unknown), `matrix` (entity × representation grid).
- `options` — the choices to pass to `AskUserQuestion`. `AskUserQuestion` allows **max 4 options** per question plus an automatic "Other"; when a list below has more than 4 entries, the runner narrows or splits per the rules in the runner prompt.
- `follow_up` — when present, ask this as an open follow-up after a non-trivial answer (e.g., "explain", "describe", "provide an example").
- `maps_to` — `{blueprint area} | {work plan category} | {FAIR principle codes}`. Used when synthesizing Part 2.

**FAIR principle codes** (for the `FAIR Principle` column in Part 2): F1–F4 (Findable),
A1/A1.1/A1.2/A2 (Accessible), I1–I3 (Interoperable), R1/R1.1/R1.2/R1.3 (Reusable).

**Work Plan categories** (Part 2 groups tasks under these five — from Appendix 2 §1.3):
1. Persistent Identifier (PID) Implementation Strategies
2. Metadata (MD) Improvement Strategies
3. Community and Assessment Strategies
4. Architectural Strategies
5. Additional Specific Strategies

**Effort legend** (Part 2 `Effort`): ⏳ = modest (≤1 week) · ⏳⏳ = moderate (weeks–month) · ⏳⏳⏳ = major (months).

---

# Part 0 — Session Metadata (Work Plan header)

Collect at the start (mostly free text — confirm, don't over-ask):

- `Q1` Full name — `open`
- `Q2` Project or repository affiliation (the **Target Repository** name) — `open`
- `Q3` Organizational affiliation — `open`
- `Q4` Email address — `open`
- `Q5` **Are you a…** — `single` | gates the `services-dev` items
  - Repository Owner
  - Repository Services & Development team member
- `Q6` Most common role related to repository work — `single` (8 source options; runner narrows to the 3–4 most likely + Other)
  - Repository manager · Data curator/steward · Research manager · Software Developer · Web Developer · Data wrangler · Metadata Specialist · Other
- `Q7` Familiarity with the FAIR Principles — `single` | Community and Assessment | —
  - Familiar and put them into practice
  - Familiar but do not currently put them into practice
  - Heard of them but not familiar with what they mean
  - Never heard of the FAIR principles

Also capture (ask once, plainly; leave blank if unknown — these are Appendix 2 §1.2 fields):
GO FAIR US Coordinator(s), Target Repository Program Officer, Work Plan Representative,
Project Technical Lead, Division Name.

---

# Part 1 — Interview Plan

Phases follow the Blueprint's five areas. Within each, items carry their Work Plan
category so Part 2 can be assembled. Ask roughly in this order; skip `services-dev`
items if Q5 = Repository Owner (note the skip rather than dwelling).

## Phase A — Persistent Identifiers (Blueprint §2 · PID category)

- `Q8` `services-dev` `numeric` — % of your **data** that has a globally unique, persistent identifier. | PID | F1
- `Q9` `services-dev` `single` — Smallest **data** entity that has a PID. | PID | F1
  - Data set/collection · Data file · Data record · Other
- `Q10` `services-dev` `open` — Name and describe each identifier **type** your data uses, and how each is created (institutions, funder, research products, etc.). | PID | F1, I1
- `Q11` `all` `single` `follow_up`(which system / required or optional) — Does the repository use **ORCIDs** (or other personal IDs) for researchers? | PID | F1, R1.2
  - Yes · No · Not sure
- `Q12` `services-dev` `numeric` — % of your **metadata** that has a globally unique, persistent identifier. | PID | F1
- `Q13` `services-dev` `single` `follow_up`(provide an example identifier for each applicable entity) — Smallest **metadata** entity that receives a PID. | PID | F1
  - Data set/collection description · Data file description · Data record description · Other
- `Q14` `all` `single` `follow_up`(if Yes, how are versions identified?) — Do identifiers explicitly identify and record **versions** for data and metadata? | PID | F1.x, I2
  - Yes · No · Not sure

## Phase B — Metadata Schema & Quality (Blueprint §1 · MD category)

- `Q15` `services-dev` `numeric` — How many metadata fields does the repository **require** per data entry? (`-1` if unknown) | MD | R1
- `Q16` `services-dev` `open` — Point to a list of the **required** metadata fields, if available. | MD | R1
- `Q17` `services-dev` `numeric` — How many metadata fields does the repository **allow** per data entry? (`-1` if unknown) | MD | R1
- `Q18` `services-dev` `open` — Point to a list of the **allowed** metadata fields, if available. | MD | R1
- `Q19` `all` `single` `follow_up`(if not "Yes", explain) — Does the metadata sufficiently describe the data for **end-user discovery**? | MD | F2, R1
  - Yes · Sometimes · No
- `Q20` `all` `single` `follow_up`(if not "Yes", explain) — Does the metadata include the **identifier of the data** it describes? | MD | F3
  - Yes · Sometimes · No
- `Q34` `all` `single` `follow_up`(if not "Yes", explain) — Does the metadata sufficiently describe the data for **re-use** needs? | MD | R1
  - Yes · Sometimes · No
- `Q30` `services-dev` `matrix` — For each entity (A–F) describe how controlled terms are represented (Free text / Validated string / Local code or ID / CURIE / Semantic IRI / Mixed / Other). Entities: (A) data file variable names, (B) data file values from a short list, (C) data file values from a large vocabulary, (D) metadata field names, (E) metadata field values from a short list, (F) metadata field values from a large vocabulary. | MD | I1, I2
  - *Runner note:* ask as one open/structured item or a short series — do not force into a single 4-option call.
- `Q33` `services-dev` `single` `follow_up`(if Yes, provide or say how to acquire) — Is there a list of required/allowed data set **topic** descriptions? | MD | R1.3
  - Yes · No · Don't know

## Phase C — APIs, Access & Formats (Blueprint §3 · Architectural category)

- `Q22` `services-dev` `multi` — Standardized retrieval protocol(s) supported when using a **data set** identifier. | API | A1, A1.1
  - None · Direct download via UI · Direct download via API command · SFTP · Other · Don't know
- `Q23` `services-dev` `multi` — Standardized retrieval protocol(s) supported when using a **metadata record** identifier. | API | A1, A1.1
  - None · Direct download via UI · Direct download via API command · SFTP · Other · Don't know
- `Q24` `services-dev` `single` `follow_up`(if Yes, explain the difficulty) — Have users had difficulty accessing any data sets? | API | A1
  - Yes · No · Don't know
- `Q25` `all` `open` — How is authentication/authorization enforced for data download (protocols/rules)? | API | A1.2
- `Q26` `all` `single` `follow_up`(if not "Yes", explain) — Are metadata freely available for download/export? | API | A1, R1.1
  - Yes · Sometimes · No
- `Q28` `services-dev` `multi` — Standard representation format(s) for sharing **data**. | API | I1
  - CSV · JSON · XML · Other
- `Q29` `services-dev` `multi` `follow_up`(list any others) — Standard representation format(s) for sharing **metadata**. | API | I1
  - JSON · YAML · JSON-LD · RDF/XML
- `Q27` `all` `single` — "Our preservation plan assures metadata remain available after the corresponding data are removed." | Architectural | A2
  - Strongly disagree · Somewhat disagree · Neither · Somewhat agree · Strongly agree
  - *Runner note:* 5-point scale exceeds 4 options — collapse to Disagree / Neutral / Agree and capture the exact level in notes, or split.

## Phase D — Citation, Provenance & Relations (Blueprint §4 · Community + MD)

- `Q21` `all` `single` `follow_up`(if Yes, what process/method?) — Does the repository **track publications / data reuse**? | Citation | R1.2
  - Yes · No · Don't know
- `Q31` `services-dev` `single` `follow_up`(describe or point to the policy) — Does the repository specify **how to reference other data sets/resources** in data or metadata? | Citation | I3
  - Yes · No · Not sure
- `Q32` `services-dev` `single` `follow_up`(if Yes, describe the relations) — Does the repository specify a particular set of **relations** to describe related resources? | MD | I3
  - Yes · Somewhat · No
- `Q38` `all` `single` `follow_up`(if Yes, describe support and how it's exposed to users) — Does the repository describe **where and by what processes** the data were created (provenance)? | MD | R1.2
  - Yes · No · Don't know
- `Q39` `all` `multi` — Community standard(s) supported for **provenance**. | MD | I2, R1.3
  - PROV · CWLProv · None · Don't know

## Phase E — Licensing & Conditions of Access (Blueprint §1/§4 · MD)

- `Q35` `all` `open` — What conditions for access apply to the data and metadata? | MD | A1.2, R1.1
- `Q36` `all` `single` — Clear and clearly visible **data usage license**? (1-click from front page, ≤1 page, no sophisticated judgment) | MD | R1.1
  - Yes · No · Don't know
- `Q37` `all` `single` — Clear and clearly visible **metadata usage license**? | MD | R1.1
  - Yes · No · Don't know

## Phase F — Community Standards & Engagement (Blueprint §5 · Community)

- `Q40` `all` `single` `follow_up`(if Yes, list; else describe details) — Does the repository's **data** follow domain-specific community standards? | Community | R1.3
  - Yes · No · Not sure
- `Q41` `all` `single` `follow_up`(if Yes, list; else describe details) — Does the repository's **metadata** follow domain-specific community standards? | Community | R1.3
  - Yes · No · Not sure
- `Q42` `all` `single` — Interested in further discussion and collaboration with the project team? | Community | —
  - Yes · No · Maybe
- `Q43` `all` `single` — Acknowledge the survey was completed to the best of your knowledge. | Community | —
  - Yes · No

---

# Part 2 — Populated Work Plan (OUTPUT)

Synthesize this section from the recorded answers. Mirror Appendix 2.

## 1. Introduction

**Document Version:** 2.1
**Document Status:** Preliminary
**Last Updated:** {today}

### 1.2 Work Plan Summary
1. **Target Repository:** {Q2}
2. **GO FAIR US Coordinator(s):** {…}
3. **Target Repository Program Officer:** {…}
4. **Target Repository Work Plan Representative:** {…}
5. **Project Technical Lead:** {…}
6. **Division Name (if applicable):** {…}

**Respondent:** {Q1}, {Q3} — {Q6}; FAIR familiarity: {Q7}; role-type: {Q5}.

## 2. Work Plan — Detailed Strategies

For **each** of the five categories, include the strategy table below. Generate one or
more strategy rows per category, driven by the gaps surfaced in the interview. Only
include a strategy when an answer indicates a gap or an opportunity; if a category is
already strong, say so in one line and omit empty rows.

Table columns (per Appendix 2 §2.1):

| Item # | Priority | FAIRification Task Description | Expected Outcome | FAIR Principle | Metrics | Effort | Dependencies, resources & notes |
|--------|----------|-------------------------------|------------------|----------------|---------|--------|----------------------------------|
| `n.m`  | High/Med/Low | Strategy name + lettered tasks (A), (B), … | Functional result | Codes (e.g. R1, I2) | Proposed measure(s) | ⏳ / ⏳⏳ / ⏳⏳⏳ | Inputs, prerequisites, who helps |

**Priority rule:** High = a required Blueprint element is missing or it blocks NIAID
Discovery Portal integration; Medium = a preferred practice is not followed; Low = an
optional enhancement. Within a category, order strategies by dependency (earlier
strategies typically enable later ones); order lettered tasks chronologically.

**Per-category seed strategies** (use as starting points, adapt to the answers — these
echo the worked examples in Appendix 2):

- **PID** — Annotate datasets with controlled vocabulary terms (F1/I2); implement
  ORCIDs/RORs for people & organizations (F1/R1.2); implement study/dataset/file IDs as
  resolvable IRIs and expose download-by-ID via API (F1/F3/A1/R1). Driven by Q8–Q14, Q11.
- **MD** — Define/publish required & allowed field lists (R1); add data identifier into
  metadata (F3); adopt controlled terms per the Q30 matrix (I1/I2); add licenses (R1.1);
  add provenance support (R1.2). Driven by Q15–Q20, Q30–Q41.
- **Community & Assessment** — Establish/track data-reuse & citation (R1.2); adopt
  domain community standards (R1.3); designate a Contact Point and engagement cadence.
  Driven by Q21, Q40–Q42, Q7.
- **Architectural** — Expose metadata via JSON-LD / documented computable format (I1);
  resource-oriented API endpoints & retrieval protocols (A1); preservation assurance for
  metadata (A2). Driven by Q22–Q29.
- **Additional Specific** — Repository-specific simplifications surfaced anywhere in the
  interview that don't fit the four categories above.

## 3. Top Recommendation

A 2–3 sentence summary: overall Blueprint alignment and the single highest-impact next
step for NIAID Discovery Portal integration.
