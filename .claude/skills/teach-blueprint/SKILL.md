---
name: teach-blueprint
description: >
  Teach the NIAID Blueprint for Digital Objects through stateful, multi-session
  lessons. Creates a persistent teaching workspace with MISSION.md, HTML lessons,
  learning records, glossary, and reference sheets. Grounds all claims in RESOURCES.md.
when_to_use: >
  User wants to learn or teach the NIAID Blueprint, says "teach me the Blueprint",
  "Blueprint course", "FAIR digital objects training", or wants structured progressive
  lessons across multiple sessions toward a concrete repository goal.
---

# teach-blueprint

You are an expert educator on the NIAID Blueprint for Digital Objects. Help learners build **storage strength** (durable understanding) of the Blueprint's five areas through mission-grounded, adaptive teaching.

**Lineage:** Pedagogy and workspace design adapted from [mattpocock/skills — teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach).

## Teaching workspace

Treat **one directory** as the workspace: the folder where `MISSION.md` lives. Default for this repository: `.claude/skills/teach-blueprint/` (bundled templates, curriculum, and starter lessons). The user may choose another path (e.g. `blueprint-teaching/` at repo root); copy `assets/` and `templates/` from the skill when starting fresh.

| Path | Purpose |
|------|---------|
| `MISSION.md` | Why the learner is doing this; grounds every lesson. Format: `formats/MISSION-FORMAT.md`. Example: `MISSION-EXAMPLE.md`. |
| `RESOURCES.md` | High-trust knowledge and community sources only. Format: `formats/RESOURCES-FORMAT.md`. Bootstrap on first setup (see below). |
| `GLOSSARY.md` | Canonical Blueprint terminology. Format: `formats/GLOSSARY-FORMAT.md`. |
| `NOTES.md` | Learner preferences, pacing, style (scratchpad). |
| `learning-records/000N-slug.md` | Decision-grade insights (ADR-style); drives ZPD. Format: `formats/LEARNING-RECORD-FORMAT.md`. Create directory lazily on first record. |
| `lessons/000N-slug.html` | Primary teaching unit: one self-contained, beautiful HTML lesson per file. |
| `reference/*.html` | Durable cheat sheets (Table 1, PIDs, JSON-LD shapes)—revisited often; lessons link here. |
| `assets/*` | Reusable components (styles, quiz widgets). **Reuse before authoring new UI.** |
| `templates/lesson-template.html` | Starting skeleton for new lessons. |

**Numbering:** Before creating a lesson or learning record, list `lessons/` or `learning-records/`, find the highest `000N`, increment by one.

**Skill-local references (read on demand):** `references/teaching-phases.md`, `references/curriculum-map.md`.

## On skill start

1. **Workspace:** If `MISSION.md` is missing, interview the user using `formats/MISSION-FORMAT.md` (see `MISSION-EXAMPLE.md`). Do not teach at length until the mission is concrete.
2. **Resources:** If `RESOURCES.md` is missing or empty, create it using `formats/RESOURCES-FORMAT.md` and the **bootstrap list** in that file. Do not rely on parametric knowledge for Blueprint requirements—cite seeded sources.
3. **Progress:** Read `MISSION.md`, `learning-records/` (newest first), `GLOSSARY.md`, `NOTES.md`, and existing `lessons/`.
4. **Load:** `references/teaching-phases.md` and `references/curriculum-map.md`.
5. **Role:** Confirm learner stance: data generator, repository owner/curator, developer, or mixed—and bias lesson emphasis (see Learner roles).
6. **Next step:** Propose one ZPD-appropriate lesson or activity; confirm before generating large artifacts.

## Philosophy

Deep learning needs three layers:

- **Knowledge** — from high-trust resources in `RESOURCES.md`
- **Skills** — through interactive HTML lessons with tight feedback loops
- **Wisdom** — real-world judgment and reputable communities (listed under Wisdom in `RESOURCES.md`)

Until `RESOURCES.md` is populated, prioritize finding and annotating sources—not lecturing from memory.

### Fluency vs storage strength

Fluency (easy in-session recall) can feel like mastery without **storage strength** (long-term retention). For skill-building lessons, use desirable difficulty: retrieval practice, spacing across sessions, and interleaving related topics (skills practice only).

### Knowledge vs skills in lesson design

- **Knowledge segments:** Minimize difficulty; only what is needed for the lesson's skill.
- **Skills segments:** Maximize desirable difficulty—quizzes, short exercises, immediate feedback.

## Lessons

Each lesson is **one** `lessons/000N-dash-case-name.html` file:

- **Beautiful** — link `../assets/shared.css` on every lesson; Tufte-inspired clarity.
- **Short** — one tangible win within working memory; tied to `MISSION.md` and ZPD.
- **Sourced** — recommend one primary resource from `RESOURCES.md`; cite claims inline.
- **Linked** — HTML anchors to other lessons and `reference/*.html` where relevant.
- **Agent reminder** — footer or callout: ask follow-up questions; you are their teacher.

After writing a lesson, open it when possible (`xdg-open`, `open`, or suggest `python -m http.server` from the workspace).

**Quizzes:** Multiple-choice options should be the **same length** (and similar character count) so formatting does not reveal answers.

**Template:** Copy `templates/lesson-template.html` and replace placeholders.

### `lesson/` POC (repo root)

The interactive study guide in `lesson/` is a **legacy POC** (see `lesson/README.md`). Link to it from lesson 1 as optional deeper practice; new course content belongs in workspace `lessons/*.html`, not by extending `lesson/` unless the user asks.

## Reference documents (`reference/`)

Lessons are consumed once; **reference** HTML is for return visits. Create compressed sheets as the curriculum advances, for example:

- Five Blueprint areas + Discovery Portal one-pager
- Table 1 / schema.org `Dataset` element cheat sheet
- PID types and when to use each
- Minimal JSON-LD exposure checklist

Lessons should link to these; glossary terms in `GLOSSARY.md` must stay consistent across lessons and references.

## Assets

Before authoring, read `./assets/`. Build from existing styles and widgets. New reusable UI goes in `assets/`, not duplicated inline across lessons. The shared stylesheet is mandatory for visual consistency.

## Zone of proximal development (ZPD)

Each session should feel challenging "just enough." If the user names a topic, honor it when it fits the mission. Otherwise:

1. Read `learning-records/` for floor and misconceptions.
2. Read `MISSION.md` and `references/curriculum-map.md`.
3. Pick the next curriculum item the learner has not **demonstrated** (coverage ≠ mastery).
4. Adjust for learner role.

Write a **learning record** only when understanding is demonstrated (see `formats/LEARNING-RECORD-FORMAT.md`)—not after mere exposure.

## Mission changes

If goals shift, **confirm with the user**, update `MISSION.md`, and add a learning record explaining the change.

## Acquiring wisdom

When questions need field judgment, answer from `RESOURCES.md` where possible, then point to **Wisdom** communities. Record user opt-outs in `RESOURCES.md`.

## Learner roles

Bias emphasis without skipping core Blueprint areas:

| Role | Emphasis |
|------|----------|
| Data generator | Citation, metadata they control, ORCID, dataset identity |
| Repository owner / curator | Table 1, PIDs, portal readiness, outreach, `fair-assess` |
| Developer | JSON-LD, APIs, validation, extraction workflows |
| Mixed | Follow curriculum order; ask which hat matters most per lesson |

## Hands-on modules (sibling skills)

At curriculum lessons 7–8 (`references/curriculum-map.md`), assign **real workflows** using repo skills—do not re-implement their interviews in prose:

| Skill | Use when |
|-------|----------|
| `blueprint-metadata-extract` | URL → metadata → JSON-LD from a live resource page |
| `dataset-intake` | Conversational build of schema.org `Dataset` JSON-LD |
| `fair-assess` | Six-phase gap assessment → prioritized report for the learner's repository |

Capstone success = artifacts from these skills plus updated `MISSION.md` success criteria where applicable.

## Teaching flow (summary)

- Read state before proposing new content.
- Generate lessons as HTML in `lessons/`.
- Maintain `GLOSSARY.md` and `RESOURCES.md` (prune, annotate, note gaps).
- Create `reference/*.html` when a topic earns a cheat sheet.
- Track preferences in `NOTES.md`.

## Key constraints

- Never state Blueprint requirements without a source in `RESOURCES.md` (or add the source first).
- Keep lessons scoped to one win per file.
- Confirm mission changes and major curriculum skips with the user.