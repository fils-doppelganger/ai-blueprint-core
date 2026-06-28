# Citation Output Template

Substitution placeholders for generated citation text. Replace bracketed values with
collected interview fields.

## Formatted Citations

### APA — Dataset (original or reused)

```
[Author(s)]. ([Year]). [Title] (Version [version]) [Data set]. [RepositoryName]. [dataPid]
```

Omit `(Version [version])` when no version. Use `et al.` after the first author when
there are four or more authors (confirm with user if borderline).

### APA — Software

```
[Author(s)]. ([Year]). [Title] (Version [version]) [Computer software]. [RepositoryName]. [dataPid]
```

### MLA — Dataset

```
[Author(s)]. [Title]. Version [version], [RepositoryName], [Year], [dataPid].
```

### Chicago — Dataset

```
[Author(s)]. [Title]. Version [version]. [RepositoryName], [Year]. [dataPid].
```

### Chicago — Software

```
[Author(s)]. [Title]. Version [version]. [RepositoryName], [Year]. [dataPid].
```

### NLM / PubMed — Dataset (reused)

```
[Author(s)]. [Title] [Data set]. [RepositoryName]; [Year]. [dataPid]. Accessed [accessDate].
```

### Repository as a Whole

```
[RepositoryName] ([Year]). [Title or descriptive label] [Resource]. [repositoryPid].
```

When an RRID exists, include it: `[RepositoryName] (RRID: [rrid]). ...`

## BibTeX — Dataset

```bibtex
@dataset{[citeKey],
  author       = {[Author(s) as Last, First and ...]},
  title        = {[Title]},
  year         = {[Year]},
  version      = {[version]},
  publisher    = {[RepositoryName]},
  doi          = {[doi without prefix]},
  url          = {[dataPid]},
  urldate      = {[accessDate]},
  note         = {[repositoryId or other note]}
}
```

Omit `version`, `urldate`, and `note` when not applicable.

## BibTeX — Software

```bibtex
@software{[citeKey],
  author       = {[Author(s)]},
  title        = {[Title]},
  year         = {[Year]},
  version      = {[version]},
  publisher    = {[RepositoryName]},
  doi          = {[doi without prefix]},
  url          = {[dataPid]}
}
```

## How to Cite Section (repository owner)

```markdown
## How to Cite

When you use data from [RepositoryName], please cite the specific digital object
using its DOI and include the repository identifier where applicable.

### Citing data you deposit here

[APA example]
[MLA example]
[BibTeX block]

### Citing data you reuse

[APA example with access date]
[BibTeX block]

### Citing this repository

[Repository-level example with RRID/DOI]
```

## Acknowledgment Paragraph

```
The authors acknowledge [RepositoryName] ([repositoryPid]) for providing access to
[Title] ([dataPid]). [fundingText] [customAcknowledgment]
```