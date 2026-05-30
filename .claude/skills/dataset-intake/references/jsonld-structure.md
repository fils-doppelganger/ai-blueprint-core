# JSON-LD Structure Reference

Annotated template showing how each collected value maps to its JSON-LD position. Use this when assembling the final output document.

The structure follows the Blueprint's Supplemental Table 7 examples and schema.org Dataset conventions.

---

## Top-level structure

```json
{
  "@context": "https://schema.org/",
  "@type": "Dataset",
  "@id": "<resolvable DOI IRI — same as identifier.url>",

  "name": "<Group 1: name>",
  "description": "<Group 1: description>",
  "identifier": { ... },       // Group 1: DOI — see below
  "dateCreated": "<Group 2>",

  "author": [ ... ],           // Group 2: array of Person objects
  "funder": [ ... ],           // Group 2: array of Organization objects
  "grant": [ ... ],            // Group 2: array of strings

  "measurementTechnique": [ ... ],  // Group 3: array of DefinedTerm
  "infectiousAgent": [ ... ],       // Group 3: array of DefinedTerm
  "host": [ ... ],                  // Group 3: array of DefinedTerm
  "healthCondition": [ ... ],       // Group 3: array of DefinedTerm

  "conditionsOfAccess": "<Group 4: IRI or plain label>",
  "license": "<Group 4: SPDX or IRI>",
  "distribution": [ ... ],          // Group 4: array of DataDownload

  "temporalCoverage": "<Group 5>",
  "spatialCoverage": { ... },       // Group 5: Place object or array
  "citation": [ ... ]               // Group 5: array of ScholarlyArticle or IRI
}
```

**Rule:** Omit any field that was skipped or answered N/A. Do not output empty arrays `[]` or `null` values.

---

## `identifier` — DOI as PropertyValue

```json
"identifier": {
  "@type": "PropertyValue",
  "@id": "https://doi.org/10.XXXX/YYYY",
  "propertyID": "https://registry.identifiers.org/registry/doi",
  "value": "doi:10.XXXX/YYYY",
  "url": "https://doi.org/10.XXXX/YYYY"
}
```

- `@id` and `url` are the same resolvable IRI
- `value` uses the `doi:` prefix (not `https://doi.org/`)
- The top-level `"@id"` of the document should match `identifier.url`

---

## `author` — Person with ORCID

```json
"author": [
  {
    "@type": "Person",
    "name": "Jane Smith",
    "identifier": "https://orcid.org/0000-0002-1825-0097"
  },
  {
    "@type": "Person",
    "name": "John Doe"
  }
]
```

- Always an array, even for a single author
- Include `identifier` only when an ORCID is known
- If no ORCID: omit `identifier` field entirely (don't set to null or empty)

---

## `funder` — Organization with ROR

```json
"funder": [
  {
    "@type": "Organization",
    "name": "National Institute of Allergy and Infectious Diseases",
    "alternateName": "NIAID",
    "url": "https://ror.org/043z4tv69"
  }
]
```

- Always an array
- `url` is the ROR IRI
- `alternateName` for well-known acronyms (NIAID, NIH, etc.)
- If no ROR: omit `url`, use `name` only

---

## `grant` — array of strings

```json
"grant": ["UM1AI148684", "UM1AI148576"]
```

- Plain alphanumeric strings — no special structure needed

---

## `measurementTechnique` — DefinedTerm with NCIT

```json
"measurementTechnique": [
  {
    "@type": "DefinedTerm",
    "name": "flow cytometry",
    "inDefinedTermSet": "http://ncicb.nci.nih.gov",
    "url": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16585"
  },
  {
    "@type": "DefinedTerm",
    "name": "RNA sequencing"
  }
]
```

- When NCIT code is unknown: omit `inDefinedTermSet` and `url`, use `name` only

---

## `infectiousAgent` and `host` — DefinedTerm with NCBITaxon

```json
"infectiousAgent": [
  {
    "@type": "DefinedTerm",
    "name": "SARS-CoV-2",
    "inDefinedTermSet": "https://www.ncbi.nlm.nih.gov/taxonomy",
    "url": "https://www.ncbi.nlm.nih.gov/taxonomy/2697049"
  }
],
"host": [
  {
    "@type": "DefinedTerm",
    "name": "Homo sapiens",
    "inDefinedTermSet": "https://www.ncbi.nlm.nih.gov/taxonomy",
    "url": "https://www.ncbi.nlm.nih.gov/taxonomy/9606"
  }
]
```

---

## `healthCondition` — DefinedTerm with MONDO

```json
"healthCondition": [
  {
    "@type": "DefinedTerm",
    "name": "COVID-19",
    "inDefinedTermSet": "https://purl.obolibrary.org/obo/mondo.owl",
    "url": "https://purl.obolibrary.org/obo/MONDO_0100096"
  }
]
```

---

## `conditionsOfAccess`

```json
"conditionsOfAccess": "https://accessclinicaldata.niaid.nih.gov/dashboard/Public/files/NIAID_DAR.pdf"
```

Plain string — either an IRI or a label like `"open"`, `"controlled"`.

---

## `license`

```json
"license": "CC-BY-4.0"
```

Or a URL if not in SPDX:

```json
"license": "https://www.immport.org/agreement"
```

---

## `distribution` — DataDownload

```json
"distribution": [
  {
    "@type": "DataDownload",
    "contentUrl": "https://immport.org/shared/study/SDY998",
    "encodingFormat": "URL"
  }
]
```

- `encodingFormat` is optional; use `"URL"` when pointing to a landing page rather than a direct file

---

## `temporalCoverage`

```json
"temporalCoverage": "2020-11-24/2021-06-30"
```

ISO 8601 interval. Single date if not a range: `"2022-05-01"`.

---

## `spatialCoverage` — Place

```json
"spatialCoverage": {
  "@type": "Place",
  "name": "United States",
  "identifier": "ISO 3166-2:US"
}
```

Multiple countries — use an array:

```json
"spatialCoverage": [
  { "@type": "Place", "name": "United States", "identifier": "ISO 3166-2:US" },
  { "@type": "Place", "name": "Kenya", "identifier": "ISO 3166-2:KE" }
]
```

International/unknown: `{ "@type": "Place", "name": "International", "identifier": "ZZ" }`

---

## `citation` — ScholarlyArticle

```json
"citation": [
  {
    "@type": "ScholarlyArticle",
    "name": "Methods for high-dimensional analysis",
    "url": "https://pubmed.ncbi.nlm.nih.gov/29996944",
    "identifier": {
      "@type": "PropertyValue",
      "propertyID": "https://registry.identifiers.org/registry/doi",
      "value": "doi:10.1186/s13075-018-1631-y",
      "url": "https://doi.org/10.1186/s13075-018-1631-y"
    }
  }
]
```

If only a URL is provided (no title or DOI): use a plain IRI string rather than a full object.
