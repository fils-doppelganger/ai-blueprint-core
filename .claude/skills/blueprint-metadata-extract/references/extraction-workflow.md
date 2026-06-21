# Extraction Workflow

Apply this workflow after fetching the Blueprint specification and example record from their GitHub raw URLs.

**Target resource URL:** {{RESOURCE_URL}}

Use this URL as the primary source of evidence.

## Phase 1 — Understand the resource

- Identify the digital object type (`Dataset`, `SoftwareApplication`, etc.). Default to `Dataset` when unclear but the page describes research data.
- Capture the canonical landing page URL as top-level `url` when distinct from the persistent identifier.
- Note access model: open, registered, or controlled.

## Phase 2 — Map Blueprint Table 1 elements

Extract every element you can find evidence for. Blueprint elements (schema.org property in parentheses):

| Element | Default format | JSON-LD notes |
|---------|----------------|---------------|
| type | IRI | `@type` at root |
| identifier | Resolvable DOI (preferred) | `PropertyValue` with `propertyID` = `https://registry.identifiers.org/registry/doi` |
| name | Free text | Required |
| description | Free text | Required; use abstract/summary from page |
| dateCreated | ISO 8601 | Creation or repository deposit date |
| author | ORCID | `Person` objects; name only if ORCID not found |
| funder | ROR | `Organization` objects |
| grant | Alphanumeric string | Array of strings |
| measurementTechnique | NCIT | `DefinedTerm`; name-only if NCIT ID unknown |
| distribution | IRI (URL) | `DataDownload` with `contentUrl` |
| citation | IRI (URL) | `ScholarlyArticle` with DOI/PubMed when available |
| infectiousAgent | NCBITaxon | `DefinedTerm` |
| host | NCBITaxon | `DefinedTerm` |
| healthCondition | MONDO | `DefinedTerm`; if page uses NCIT disease terms (as in the example), you may use `keywords` with NCIT `DefinedTerm` **or** `healthCondition` with MONDO — prefer MONDO when you can resolve it |
| conditionsOfAccess | IRI or label | Policy URL preferred; `open` / `registered` / `controlled` acceptable |
| license | SPDX or IRI | SPDX ID preferred; license URL acceptable |
| temporalCoverage | ISO 8601 range | `YYYY-MM-DD/YYYY-MM-DD` |
| spatialCoverage | ISO 3166 | `Place` with country code |

**Required when evidence exists:** `name`, `description`, `identifier` (or flag missing), `conditionsOfAccess`, `license`.

**Omit** fields with no evidence. Do not emit empty arrays, `null`, or empty strings.

## Phase 3 — PID and ontology normalization

Apply these rules when populating values:

- **DOI:** Always resolvable form `https://doi.org/10.xxxx/yyyy`. Set top-level `@id` to the same IRI as `identifier.url` when a DOI exists; otherwise use the resource landing page URL or a stable page-specific IRI and flag in notes.
- **Bare DOI** `10.xxxx/yyyy` → prefix with `https://doi.org/`
- **ORCID:** `https://orcid.org/0000-0000-0000-0000`
- **ROR:** `https://ror.org/xxxxxxx` (NIAID: `https://ror.org/043z4tv69`)
- **NCBITaxon:** `https://www.ncbi.nlm.nih.gov/taxonomy/{taxid}`
- **MONDO:** `https://purl.obolibrary.org/obo/MONDO_{id}`
- **NCIT:** `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C####`
- **SPDX license:** use identifier string (e.g. `CC-BY-4.0`) when clearly stated

If a PID or ontology term cannot be resolved from the page, include the human-readable name only (as in the example's second keyword entry) and flag it in Metadata Notes.

## Phase 4 — Assemble JSON-LD

Produce a single JSON-LD document matching the structural patterns in the fetched example record:

```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "@id": "<resolvable DOI IRI or best stable IRI>",
  "name": "...",
  "description": "...",
  "url": "<landing page if applicable>",
  "identifier": { "@type": "PropertyValue", ... },
  ...
}
```

Structural rules:

- Multi-value fields (`author`, `funder`, `grant`, `citation`, `distribution`, ontology fields) → **arrays** even for one value
- `identifier` → always a `PropertyValue` object for DOIs (match example pattern)
- `distribution` → array of `DataDownload` objects
- `citation` → `ScholarlyArticle` objects when title/DOI/PubMed are known; plain IRI string only when nothing else is available
- Follow the example's citation `identifier` pattern when both DOI and PMID exist

## Phase 5 — Self-check before output

Verify:

- [ ] Valid JSON (no trailing commas, no comments)
- [ ] `@context` and `@type` present
- [ ] No empty or placeholder-only required fields unless explicitly flagged
- [ ] DOIs in resolvable IRI form
- [ ] Omitted N/A fields (not empty arrays)
- [ ] Values traceable to the fetched page or a linked authoritative page

## Output format

Respond in exactly this structure:

### 1. Resource summary

2–4 sentences: what the resource is, where you found key metadata, and any retrieval limitations.

### 2. Extracted metadata record

One fenced `json` code block containing the JSON-LD document only.

### 3. Metadata notes

Bullet list covering:

- **Found** — elements confidently extracted with source (page section, meta tag, JSON-LD embed, linked DOI page)
- **Inferred** — values you deduced without direct evidence
- **Missing** — required Blueprint elements not found on the page
- **Unresolved PIDs** — names without ORCID/ROR/ontology IDs
- **Confidence** — overall: High / Medium / Low, with one-sentence rationale