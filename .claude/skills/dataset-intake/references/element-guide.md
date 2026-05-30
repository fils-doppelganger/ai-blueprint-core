# Element Guide — Dataset Intake

Per-element reference: what to ask, required format, and a real example value. Read at skill start.

Fields marked **Required** must appear in the output. Fields marked **Conditional** are required when applicable to the dataset. Fields marked **Optional** are collected if the user has them.

---

## Group 1 — Identity

### `name` — Required
**Ask:** "What is the title or name of your dataset?"
**Format:** Free text string
**Example:** `"AMP Rheumatoid Arthritis Phase 1"`

---

### `description` — Required
**Ask:** "Provide a description or abstract for the dataset — what does it contain, and what was it collected for?"
**Format:** Free text string; paragraph-length is fine
**Example:** `"Patient-level data from the ACTT-4 study, covering demographics, treatment arms, and clinical outcomes for COVID-19 patients."`

---

### `identifier` (DOI) — Required
**Ask:** "Does your dataset have a DOI? If so, please share it."
**Format:** Resolvable IRI — must be prefixed with `https://doi.org/`
**Bare DOI fix:** If the user gives `10.1234/abcd`, store as `https://doi.org/10.1234/abcd`
**No DOI:** Use `""` as placeholder, flag in Metadata Notes
**Example:** `"https://doi.org/10.21430/M3KXJHSP4T"`

JSON-LD structure for identifier:
```json
{
  "@type": "PropertyValue",
  "@id": "https://doi.org/10.21430/M3KXJHSP4T",
  "propertyID": "https://registry.identifiers.org/registry/doi",
  "value": "doi:10.21430/M3KXJHSP4T",
  "url": "https://doi.org/10.21430/M3KXJHSP4T"
}
```

---

## Group 2 — Provenance

### `author` — Conditional (required when dataset has named creators)
**Ask:** "Who are the authors or creators of this dataset? For each, I'll need their name and ORCID if available."
**Format:** Array of `Person` objects with `@type`, `name`, and `identifier` (ORCID as IRI)
**ORCID format:** `https://orcid.org/0000-0000-0000-0000`
**If no ORCID:** Use `name` only; flag in Metadata Notes
**Example:**
```json
{
  "@type": "Person",
  "name": "Jane Smith",
  "identifier": "https://orcid.org/0000-0002-1825-0097"
}
```

---

### `funder` — Conditional (required for NIAID-funded datasets)
**Ask:** "Which organization(s) funded this dataset? I'll need the organization name and, ideally, their ROR identifier."
**Format:** Array of `Organization` objects with `@type`, `name`, and `url` (ROR as IRI)
**Known ROR IDs:**
- NIAID: `https://ror.org/043z4tv69`
- NIH: `https://ror.org/01cwqze88`
- NIAMS: `https://ror.org/006zn3t30`
**Example:**
```json
{
  "@type": "Organization",
  "name": "National Institute of Allergy and Infectious Diseases",
  "alternateName": "NIAID",
  "url": "https://ror.org/043z4tv69"
}
```

---

### `grant` — Conditional (required when funded by a grant)
**Ask:** "What grant number(s) supported this dataset?"
**Format:** Array of alphanumeric strings
**Example:** `["UM1AI148684", "UM1AI148576"]`

---

### `dateCreated` — Required
**Ask:** "When was the dataset created, or when was it added to the repository?"
**Format:** ISO 8601 date — `YYYY-MM-DD` or `YYYY-MM` or `YYYY`
**Conversion:** "May 2024" → `"2024-05"`, "January 15, 2023" → `"2023-01-15"`
**Example:** `"2022-05-01"`

---

## Group 3 — Content

### `measurementTechnique` — Conditional (for experimental datasets)
**Ask:** "What measurement techniques or technologies were used to generate this data?"
**Format:** Array of `DefinedTerm` objects; NCIT terms preferred
**If NCIT ID unknown:** Use plain name and flag in Metadata Notes
**Example:**
```json
[
  { "@type": "DefinedTerm", "name": "flow cytometry", "inDefinedTermSet": "http://ncicb.nci.nih.gov", "url": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16585" },
  { "@type": "DefinedTerm", "name": "RNA sequencing" }
]
```

---

### `infectiousAgent` — Conditional (for IID datasets)
**Ask:** "Is there an infectious agent associated with this dataset? If so, which one(s)?"
**Format:** Array of `DefinedTerm` objects; NCBITaxon terms preferred
**Format for NCBITaxon:** `https://www.ncbi.nlm.nih.gov/taxonomy/{taxid}`
**Common IDs:**
- SARS-CoV-2: taxid 2697049
- HIV-1: taxid 11676
- Mycobacterium tuberculosis: taxid 1773
- Influenza A: taxid 11320
**Example:**
```json
{ "@type": "DefinedTerm", "name": "SARS-CoV-2", "inDefinedTermSet": "https://www.ncbi.nlm.nih.gov/taxonomy", "url": "https://www.ncbi.nlm.nih.gov/taxonomy/2697049" }
```

---

### `host` — Conditional (for IID datasets)
**Ask:** "What is the host organism for this dataset?"
**Format:** Array of `DefinedTerm` objects; NCBITaxon preferred
**Common IDs:**
- Homo sapiens: taxid 9606
- Mus musculus: taxid 10090
- Macaca mulatta: taxid 9544
**Example:**
```json
{ "@type": "DefinedTerm", "name": "Homo sapiens", "inDefinedTermSet": "https://www.ncbi.nlm.nih.gov/taxonomy", "url": "https://www.ncbi.nlm.nih.gov/taxonomy/9606" }
```

---

### `healthCondition` — Conditional (for IID datasets)
**Ask:** "What health condition or disease is this dataset related to?"
**Format:** Array of `DefinedTerm` objects; MONDO terms preferred
**MONDO format:** `https://purl.obolibrary.org/obo/MONDO_{id}`
**Common IDs:**
- COVID-19: MONDO:0100096
- Rheumatoid arthritis: MONDO:0008383
- Tuberculosis: MONDO:0018076
- HIV infection: MONDO:0005109
**Example:**
```json
{ "@type": "DefinedTerm", "name": "COVID-19", "inDefinedTermSet": "https://purl.obolibrary.org/obo/mondo.owl", "url": "https://purl.obolibrary.org/obo/MONDO_0100096" }
```

---

## Group 4 — Access

### `conditionsOfAccess` — Required
**Ask:** "Under what conditions can this dataset be accessed — is it open, registered, or controlled? Is there a URL that describes the access conditions?"
**Format:** IRI to access policy page preferred; plain-text label acceptable as fallback (`"open"`, `"registered"`, `"controlled"`)
**Example:** `"https://accessclinicaldata.niaid.nih.gov/dashboard/Public/files/NIAID_DAR.pdf"`
**Fallback example:** `"open"`

---

### `license` — Required
**Ask:** "What license applies to this dataset? An SPDX identifier (like CC-BY-4.0 or CC0-1.0) is preferred, or a URL to the license document."
**Format:** SPDX identifier string or IRI to license document
**Common SPDX IDs:** `CC0-1.0`, `CC-BY-4.0`, `CC-BY-NC-4.0`, `ODbL-1.0`
**Example:** `"CC-BY-4.0"` or `"https://creativecommons.org/licenses/by/4.0/"`

---

### `distribution` — Conditional (when data is downloadable or accessible)
**Ask:** "Where can the dataset or its files be accessed or downloaded? Please share the URL(s)."
**Format:** Array of `DataDownload` objects with `@type`, `contentUrl`, and optionally `encodingFormat`
**Example:**
```json
{
  "@type": "DataDownload",
  "contentUrl": "https://immport.org/shared/study/SDY998",
  "encodingFormat": "URL"
}
```

---

## Group 5 — Context

### `temporalCoverage` — Optional
**Ask:** "Does the dataset have a temporal coverage — the time period the data was collected over?"
**Format:** ISO 8601 date range `YYYY-MM-DD/YYYY-MM-DD`, or single date `YYYY-MM-DD`
**Example:** `"2020-11-24/2021-06-30"`

---

### `spatialCoverage` — Optional
**Ask:** "Does the dataset have a geographic coverage? Which country or region?"
**Format:** ISO 3166 country code(s) as `Place` object(s)
**Special values:** `ZZ` for international/unknown
**Common codes:** `US`, `GB`, `DE`, `ZZ`
**Example:**
```json
{ "@type": "Place", "name": "United States", "identifier": "ISO 3166-2:US" }
```

---

### `citation` — Optional
**Ask:** "Are there any related publications or resources that should be cited alongside this dataset?"
**Format:** Array of `ScholarlyArticle` or IRI strings; PubMed URLs or DOI IRIs preferred
**Example:**
```json
{
  "@type": "ScholarlyArticle",
  "name": "Methods for high-dimensional immune profiling",
  "url": "https://pubmed.ncbi.nlm.nih.gov/29996944",
  "identifier": {
    "@type": "PropertyValue",
    "propertyID": "https://registry.identifiers.org/registry/doi",
    "value": "doi:10.1186/s13075-018-1631-y",
    "url": "https://doi.org/10.1186/s13075-018-1631-y"
  }
}
```
