# RESOURCES.md Format

High-trust sources only. Knowledge for lessons must be drawn from here—not from parametric guesses.

## Structure

```md
# NIAID Blueprint Teaching Resources

## Knowledge

- [Authoritative title](URL)
  Use for: one-line when to reach for this source.

## Wisdom (Communities)

- [Community name](URL)
  Use for: what to ask there; moderation/reputation note if known.

## Gaps

- Topics the mission needs but lack a good source yet (drives future search).
```

## Rules

- Annotate every entry with intended use.
- Prune ruthlessly; remove shallow or off-mission links.
- Note community opt-outs the user requests.
- Group **Knowledge** vs **Wisdom** as above.

## Bootstrap (first workspace setup)

When creating `RESOURCES.md`, seed at least these entries (update URLs if the repo moves):

### Knowledge

- [NIAID Blueprint for Digital Objects v2 (Markdown)](https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md)  
  Use for: authoritative requirements—five areas, Table 1, PIDs, APIs, citation, outreach.

- [NIAID Blueprint resources (NIAID Data Science)](https://datascience.niaid.nih.gov/resources)  
  Use for: official NIAID framing, PDF distribution, and program context when the markdown spec is insufficient.

- [GO FAIR US — ai-blueprint-core](https://github.com/go-fair-us/ai-blueprint-core)  
  Use for: skills (`fair-assess`, `dataset-intake`, `blueprint-metadata-extract`), examples, and implementation tooling in this repository.

- [NIAID Data Ecosystem Discovery Portal](https://data.niaid.nih.gov/)  
  Use for: why repositories implement the Blueprint; discovery and integration motivation.

### Wisdom (Communities)

- [GO FAIR](https://www.go-fair.org/) / [GO FAIR US](https://www.go-fair.us/)  
  Use for: FAIR implementation culture, networking; not a substitute for the Blueprint spec.

Add repository-specific forums, consortia, or NIAID program contacts as the learner identifies them.

### Gaps

Start with an explicit gaps section if anything the mission needs is missing (e.g. local repository platform docs).