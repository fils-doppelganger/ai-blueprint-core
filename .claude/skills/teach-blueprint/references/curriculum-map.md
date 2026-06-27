# NIAID Blueprint Teaching Curriculum Map

## Core Sequence (8 Lessons)

1. **Introduction to the NIAID Blueprint & FAIR for Digital Objects**
   - Background, audience, NIAID Data Ecosystem Discovery Portal
   - Five areas overview

2. **Minimal Metadata Schema**
   - schema.org/Dataset elements (identity, provenance, content, access, context)
   - Table 1 + JSON-LD examples

3. **Persistent Identifiers (PIDs)**
   - DOIs, ORCID, ROR, RRID, NCBITaxon, MONDO, etc.
   - Requirements for datasets, people, organizations, resources

4. **APIs & Machine-Accessible Metadata**
   - JSON-LD exposure requirements
   - Landing pages, OpenAPI considerations, validation

5. **Citation Requirements**
   - Minimal citation practices
   - Placement on repository sites, scholarly linking

6. **Outreach, Training & Implementation**
   - Point of contact responsibilities
   - Work-plan questionnaires and repository roles

7. **Practical Workflows**
   - URL → LLM extraction → JSON-LD → SHACL validation → HITL
   - **Run repo skills** (do not duplicate their flows in prose):
     - `blueprint-metadata-extract` — fetch and extract from a resource URL
     - `dataset-intake` — interview → `Dataset` JSON-LD
   - Add `reference/` cheat sheets for JSON-LD shape and validation steps

8. **Capstone / Hands-on Application**
   - Generate real metadata records via `dataset-intake` or `blueprint-metadata-extract`
   - Run `fair-assess` for a prioritized gap report aligned to `MISSION.md`
   - Optional: repository work plan (see `prompts/workPlanInterview.md` in repo root)

## Cross-cutting Themes
- Glossary discipline throughout
- Desirable difficulty in lessons 3, 4, 7, 8
- Progressive reuse of assets and reference materials

## Existing Lesson POC
The `lesson/` directory contains a 6-lesson interactive study guide that can be used or extended.