# NIAID Blueprint Quick Reference

Use this when orienting a non-technical respondent before Phase 2, or when verifying coverage during any phase.

---

## The Five Blueprint Areas

| Area | What it covers |
|---|---|
| **1. Metadata Schema** | A minimum set of schema.org-based fields every digital object must have |
| **2. Persistent Identifiers (PIDs)** | Stable, globally unique IDs for objects, people, organizations, and concepts |
| **3. API & Machine Access** | How metadata is exposed so systems can find and harvest it programmatically |
| **4. Citation Guidance** | Clear, PID-based instructions so users can cite the resource in publications |
| **5. Outreach & Training** | A designated Contact Point and training materials for users |

---

## Blueprint Section 1 — Metadata Schema

### Required fields (non-optional for all digital objects)

| Field | Notes |
|---|---|
| `@type` | The schema.org type (e.g., `Dataset`, `SoftwareApplication`) |
| `identifier` | A PID — DOI, RRID, or similar; formatted as a resolvable IRI |
| `name` | Human-readable title |
| `description` | Abstract or summary |
| `dateCreated` | ISO 8601 date |
| `conditionsOfAccess` | Open, controlled, embargoed, etc. |
| `license` | SPDX identifier or URL to license text |

### Applicable when relevant

| Field | When applicable |
|---|---|
| `author` | Should use ORCID, not free-text name |
| `funder` / `grant` | Should use ROR for organization; grant number as text |
| `measurementTechnique` | For experimental data |
| `distribution` | Download URLs, formats, sizes |
| `citation` | Related publications |
| `infectiousAgent` | NCBITaxon term preferred |
| `host` | NCBITaxon term preferred |
| `healthCondition` | MONDO term preferred |
| `spatialCoverage` | For geospatial data |
| `temporalCoverage` | For time-series or longitudinal data |

### Acceptable metadata formats

JSON-LD (preferred), JSON, XML, YML. Must be machine-readable.

---

## Blueprint Section 2 — Persistent Identifiers

| Identifier type | What it identifies | Required format |
|---|---|---|
| **DOI** | Dataset, software, or other digital object | `https://doi.org/10.XXXX/YYYY` (resolvable IRI) |
| **ORCID** | Individual researcher/author | `https://orcid.org/0000-0000-0000-0000` |
| **ROR** | Funding organization | `https://ror.org/XXXXXXX` |
| **RRID** | The repository itself | Register at `scicrunch.org` |
| **NCBITaxon** | Infectious agent or host organism | Ontology term with IRI |
| **MONDO** | Health condition or disease | Ontology term with IRI |

**Common error:** DOIs stored in bare format (`10.1234/abcd`) instead of as resolvable IRIs (`https://doi.org/10.1234/abcd`). The Blueprint requires the IRI form.

---

## Blueprint Section 3 — API & Machine Access

The Portal needs to harvest metadata programmatically. Acceptable approaches, in order of preference:

1. **REST API returning JSON-LD** — endpoints structured as resource IRIs (e.g., `/datasets/{id}`), documented with OpenAPI/Swagger
2. **REST API returning plain JSON** — partial compliance; JSON-LD context is missing
3. **HTML pages with embedded JSON-LD** — `<script type="application/ld+json">` blocks on each object's page; acceptable fallback
4. **Downloadable metadata index** — a CSV or JSON file listing all objects; acceptable fallback

Absence of all four is the highest-priority gap for Portal integration.

---

## Blueprint Section 4 — Citation Guidance

Minimum: a "How to Cite" page that includes the repository's RRID and DOIs for individual objects.

Best practice:
- Multiple citation formats (APA, MLA, NLM/PubMed, Chicago)
- Prominently linked from the homepage
- Communicated in workshops, newsletters, and submission workflows

---

## Blueprint Section 5 — Outreach & Training

**Contact Point (CP):** A named person or group alias designated to coordinate with the NIAID Data Ecosystem Discovery Portal. Must be publicly listed on the resource's website.

**Training materials:** Documentation, video tutorials, or workshops explaining how to access and use the resource. Must include contact information for user support.

No designated CP is a blocking gap for Portal onboarding.
