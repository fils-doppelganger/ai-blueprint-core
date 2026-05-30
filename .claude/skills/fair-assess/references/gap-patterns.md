# Gap Patterns by Blueprint Area

Use this after each interview phase to cross-check that no high-priority gap was missed before advancing. Each table covers one Blueprint area.

---

## Phase 2 — Metadata Schema Gaps

| Gap | Priority | Common cause |
|---|---|---|
| `identifier` field absent or not a PID | High | No DOI minting; using internal IDs only |
| `conditionsOfAccess` absent | High | Not considered during schema design |
| `license` absent | High | Assumed open but not stated explicitly |
| `@type` absent or incorrect schema.org type | High | Custom schema without schema.org mapping |
| Author stored as free-text name (not ORCID) | Medium | ORCID collection not enforced at submission |
| Funder stored as free-text (not ROR) | Medium | Grant number captured; organization not resolved to ROR |
| IID-specific fields (infectiousAgent, host, healthCondition) use free text | Medium | No ontology lookup integrated at submission |
| Metadata format is not machine-readable (e.g., PDF, DOCX) | High | Legacy submission forms |
| Metadata co-mingled with data rather than separated | Low | Convenience packaging |
| Metadata captured inconsistently (some objects missing fields) | Medium | No enforced schema at ingest |

---

## Phase 3 — Persistent Identifier Gaps

| Gap | Priority | Common cause |
|---|---|---|
| No PID assigned to digital objects | High | Resource predates DOI requirement |
| DOI stored in bare format, not as `https://doi.org/` IRI | High | DataCite/Crossref returns bare DOI; not transformed |
| No DOI minting capability | High | No Crossref/DataCite membership |
| ORCID collection optional at submission | Medium | Friction concern during onboarding |
| No ROR for funder fields | Medium | Grant number collected; org not resolved |
| No ontology terms for infectiousAgent / host / healthCondition | Medium | No ontology lookup at submission |
| Repository has no RRID | Medium | Not registered with Research Resource Identification Initiative |

---

## Phase 4 — API & Machine Access Gaps

| Gap | Priority | Common cause |
|---|---|---|
| No machine-accessible metadata at all | High | Portal cannot harvest — blocking for integration |
| API returns plain JSON, not JSON-LD | High | JSON-LD context never added |
| API endpoints use verb-based or query-parameter-heavy URLs | Medium | RPC-style design; not resource-oriented |
| No OpenAPI/Swagger documentation | Medium | API built before documentation standards adopted |
| API URLs not stable (change with versioning) | Medium | Cannot serve as `@id` in JSON-LD |
| HTML pages lack embedded JSON-LD | Medium | No structured data markup |
| No downloadable metadata index | Low | Not prioritized; harvest requires per-object API calls |

---

## Phase 5 — Citation Guidance Gaps

| Gap | Priority | Common cause |
|---|---|---|
| No citation guidance at all | High | Attribution not considered; assumed users figure it out |
| Citation guidance exists but omits PIDs (no RRID, no DOI) | High | Guidance predates PID adoption |
| Guidance exists but is buried (not linked from homepage) | Medium | Added to documentation but not promoted |
| Only one citation format provided | Medium | Single format copied from a single journal style |
| No guidance on citing the repository as a whole | Medium | Resource designed for per-object queries |
| Citation guidance not communicated in workshops or submissions | Low | Exists on website only |

---

## Phase 6 — Outreach & Training Gaps

| Gap | Priority | Common cause |
|---|---|---|
| No designated Contact Point | High | Blocking for Portal onboarding — no coordination path |
| CP exists but contact info not publicly listed | High | Internal knowledge only; Portal cannot reach them |
| No training materials | Medium | Resource assumed to be self-explanatory |
| Training materials lack contact info for support | Medium | Created without support pathway |
| CP cannot engage with NIAID training activities | Medium | Role not scoped to include outreach |
