# Blueprint Metadata Extractor

Extract Blueprint-aligned schema.org JSON-LD metadata from a web resource URL — no user interview required.

## Claude Code skill (recommended)

Use the **`blueprint-metadata-extract`** skill in `.claude/skills/blueprint-metadata-extract/`. It loads the extraction workflow from `references/extraction-workflow.md`, fetches authoritative references from GitHub raw URLs, retrieves the target page, and produces a JSON-LD record plus metadata notes.

**Invoke:**

```
/blueprint-metadata-extract https://immport.org/shared/study/SDY998
```

Or paste a URL in natural language: "extract Blueprint metadata from https://…"

The skill requires a **resource URL** (skill argument or user message). If none is provided, it asks once and waits.

## Standalone system prompt

For a web-retrieval-capable LLM outside Claude Code, use the extraction workflow in:

`.claude/skills/blueprint-metadata-extract/references/extraction-workflow.md`

Before running, substitute `{{RESOURCE_URL}}` with the target URL. Fetch these authoritative references from GitHub (do not rely on local copies):

1. **Blueprint specification**  
   https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md

2. **Example metadata record**  
   https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/example.json

**Minimal user message:**

```text
Extract Blueprint-compliant metadata for:
https://immport.org/shared/study/SDY998
```

Or, mirroring the MCP `fair_web_assessor` session-parameter pattern:

```markdown
> **Session parameters for this run:**
> - Resource Url: https://immport.org/shared/study/SDY998
> Use the parameters above as the authoritative inputs for this session.

Extract metadata for the resource URL above.
```

## Output

Three sections (defined in the extraction workflow):

1. **Resource summary** — what the resource is and any retrieval limitations
2. **Extracted metadata record** — fenced `json` code block with JSON-LD only
3. **Metadata notes** — Found / Inferred / Missing / Unresolved PIDs / Confidence

## Related artifacts

- Blueprint spec (raw): https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md
- Example record (raw): https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/example.json
- Interview-based alternative: `.claude/skills/dataset-intake/` (user provides values, no web fetch)
- Pipeline sketch: `docs/workflowThoughts.md`