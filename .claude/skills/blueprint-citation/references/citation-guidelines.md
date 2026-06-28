# Blueprint Citation Guidelines

Reference for the `blueprint-citation` skill. Source: NIAID Blueprint Section 4
(`docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md`).

## Core Requirements

Repository owners should provide citation guidance that:

1. **Integrates PIDs** — resolvable DOIs for objects; RRIDs or DOIs for repositories
2. **Covers both scenarios** — original data deposits and reused data
3. **Uses standard formats** — APA, MLA, Chicago, NLM/PubMed at minimum
4. **Is easy to find** — prominent "How to Cite" section on the website and in metadata

Researchers citing resources should:

- Include the **object PID** (DOI) for reused data
- Include **repository-specific IDs** (accession numbers, study IDs) when available
- Use **resolvable DOI form** (`https://doi.org/10.xxx/yyy`, not bare `10.xxx/yyy`)

## Citation Type Rules

| Type | Required elements | Notes |
|---|---|---|
| Original data deposit | Repository name, repository PID, data PID | For authors depositing new data |
| Reused data | Object PID (DOI), repository ID if available | For consumers citing existing objects |
| Repository as a whole | Repository name, repository PID (RRID/DOI) | When users query across many objects |

When users access data broadly across a repository rather than discrete objects,
repository-level citation is appropriate — but PIDs must still be included.

## Table 3 — Format Patterns (Blueprint)

### Dataset — APA

```
Author(s). (Year). Title of dataset (Version number) [Data set]. Repository. DOI
```

Example:

```
Smith, John, et al. (2023). Global Health Dataset (Version 1.0) [Data set]. DataHub. https://doi.org/10.1234/abcd1234
```

**Note:** The bracketed `[Data set]` label helps publication systems index data citations.

### Dataset — MLA

```
Author(s). Title of dataset. Version number, Repository, Year, DOI.
```

Example:

```
Smith, John, et al. Global Health Dataset. Version 1.0, DataHub, 2023, https://doi.org/10.1234/abcd1234.
```

### Software — Chicago

```
Author(s). Title of software. Version number. Repository, Year. DOI.
```

Example:

```
Johnson, Emily, et al. PathogenFinder. Version 3.2. BioTools, 2024. https://doi.org/10.5678/efgh5678
```

### NLM / PubMed (dataset)

```
Author(s). Title of dataset [Data set]. Repository; Year. DOI. Accessed YYYY Mon DD.
```

Use abbreviated month names. Include access date for reused data.

## BibTeX Conventions

Use `@dataset` for datasets and `@software` for software. Minimum fields:

| Field | Maps to |
|---|---|
| `author` | Author(s), `and`-separated |
| `title` | Object title |
| `year` | Release or publication year |
| `version` | Version number (when versioned) |
| `publisher` or `institution` | Repository name |
| `doi` | Object DOI (without URL prefix) |
| `url` | Resolvable DOI URL |
| `urldate` | Access date (reused data) |
| `note` | Repository-specific ID (e.g., `Study ID: SDY998`) |

Cite key pattern: `{firstAuthorSurname}{year}` — e.g., `smith2023`.

## PID Formats

| PID type | Citation form | Example |
|---|---|---|
| DOI | `https://doi.org/10.xxx/yyy` | `https://doi.org/10.21430/M3KXJHSP4T` |
| RRID | `RRID:SCR_xxxxxx` | `RRID:SCR_012345` |
| ORCID | `https://orcid.org/0000-0002-...` | In author field or note |
| PubMed | `https://pubmed.ncbi.nlm.nih.gov/NNNNNNN` | For related publications |

## Repository "How to Cite" Checklist

When generating guidance for repository owners, ensure the output addresses:

- [ ] Original data citation example with repository PID + data DOI
- [ ] Reused data citation example with object DOI + repository ID
- [ ] Repository-as-whole example with RRID or repository DOI (if applicable)
- [ ] At least three citation formats (APA, MLA, Chicago recommended)
- [ ] BibTeX template users can copy into reference managers
- [ ] Brief note on where to place guidance (website, metadata, training materials)

## Common Gaps (from FAIR assessment)

Flag these when reviewing user input:

- Citation examples without PIDs
- Only one citation format provided
- Guidance buried in documentation rather than prominently placed
- Bare DOIs without `https://doi.org/` prefix
- Missing repository PID in original-data citations