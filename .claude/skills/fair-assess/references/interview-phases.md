# Interview Phases — NIAID Blueprint FAIR Assessment

Reference for the six interview phases. Work through these in order. Ask one or two questions at a time; follow up on vague answers before advancing.

---

## Phase 1: Resource Overview

Orient yourself to the resource before diving into any technical area.

Questions:
- What is the name of the repository or data resource, and what type of digital objects does it hold? (datasets, software, methods, workflows, or a mix?)
- Who are the primary users — NIAID-funded researchers, the broader scientific community, clinicians, or someone else?
- Has the resource previously engaged with FAIR principles or the NIAID Blueprint, or is this a first assessment?

Dig deeper if:
- The resource holds multiple object types — each may have different gaps; ask which types are most common and whether they are treated differently
- The respondent is unfamiliar with the Blueprint — orient them briefly (use `references/blueprint-quick-ref.md`) before proceeding to Phase 2

---

## Phase 2: Metadata Schema (Blueprint Section 1)

The Blueprint requires a minimum set of schema.org-based metadata elements. Assess current coverage.

Questions:
- Which metadata fields does your resource currently capture for each digital object? Walk through the non-optional baseline: type, identifier, name, description, dateCreated, conditionsOfAccess, license — which of these are present?
- Are the following fields captured when applicable: author, funder, grant, measurementTechnique, distribution, citation, infectiousAgent, host, healthCondition, spatialCoverage, temporalCoverage?
- What schema or standard is used to represent metadata — schema.org, Bioschemas, FHIR, or something else?
- In what format is metadata stored or exposed — JSON, JSON-LD, XML, YML, or other?
- Is metadata captured at submission time by repository staff, or are data generators expected to provide it?

Listen for:
- Missing required fields — especially `identifier`, `conditionsOfAccess`, `license`
- Free text where a controlled vocabulary or PID is preferred (e.g., author name instead of ORCID)
- Metadata stored in formats that are not machine-readable
- Whether metadata is separated from data or co-mingled (both are acceptable per Blueprint; separation is preferred)

---

## Phase 3: Persistent Identifiers (Blueprint Section 2)

PIDs make digital objects uniquely and persistently identifiable across systems.

Questions:
- Are digital objects assigned a persistent identifier? If so, what type — DOI, RRID, URL, or other?
- Are DOIs formatted as resolvable IRIs (prefixed with `https://doi.org/`)? Or stored in bare format (e.g., `10.1234/abcd`)?
- Are author fields populated with ORCIDs, or with free-text names?
- Are funder fields populated with ROR identifiers, or with free-text organization names?
- For infectious agent, host, and health condition fields — are ontology terms used (NCBITaxon, MONDO) or free text?
- Does your resource have its own RRID registered with the Research Resource Identification Initiative?

Listen for:
- DOIs assigned but not resolvable — missing `https://doi.org/` prefix is a common gap
- No DOI minting capability at all — note whether Crossref or DataCite would be an option
- ORCIDs optional rather than required at submission
- Ontology terms absent or inconsistently applied for IID-specific fields (infectiousAgent, host, healthCondition)

---

## Phase 4: API and Machine Access (Blueprint Section 3)

Assess how metadata is exposed for programmatic access.

Questions:
- Does your resource have an API for accessing metadata? If yes, what protocol — REST, GraphQL, SPARQL?
- Can the API return metadata in JSON-LD format, or only in other formats (plain JSON, XML, CSV)?
- Are API endpoints structured as resource-oriented IRIs (e.g., `/datasets/{id}`) rather than verb-based or query-parameter-heavy URLs?
- Is the API documented using an OpenAPI/Swagger specification?
- If no API exists: Is metadata embedded in HTML pages as structured data (e.g., JSON-LD in `<script>` tags)? Or is there a downloadable metadata index file (CSV, JSON, etc.)?
- Are API endpoints or metadata pages stable enough to function as persistent identifiers in the JSON-LD `@id` field?

Listen for:
- API exists but returns plain JSON without JSON-LD context — this is a gap
- Endpoints use verbs or complex query strings rather than resource IRIs
- No Swagger/OpenAPI documentation — makes machine integration harder
- Complete absence of machine-accessible metadata — this is the highest-priority gap for Portal integration
- HTML-embedded metadata (JSON-LD in `<script>` tags) — acceptable per Blueprint as a lightweight fallback

---

## Phase 5: Citation Guidance (Blueprint Section 4)

Assess whether the resource gives users clear, PID-based citation instructions.

Questions:
- Does your resource have a published "How to Cite" page or section? If so, where is it — is it easy to find from the homepage?
- Do citation examples include the repository's PID (e.g., RRID) and, where applicable, a DOI for individual digital objects?
- Are citation examples provided in multiple formats (e.g., APA, MLA, NLM/PubMed, Chicago)?
- Is citation guidance communicated beyond the website — for example, in user workshops, newsletters, data submission workflows, or documentation?
- For resources where users query across many objects rather than citing discrete items: is there guidance on citing the repository as a whole?

Listen for:
- Citation guidance exists but does not include PIDs — note as a gap
- Guidance is buried deep in documentation rather than prominently placed
- Only one citation format provided — limits usability across publication venues
- No citation guidance at all — highest-priority gap for attribution and traceability

---

## Phase 6: Outreach and Training (Blueprint Section 5)

Assess whether a Contact Point and training infrastructure exist.

Questions:
- Has your resource designated a Contact Point (CP) for outreach and collaboration with the NIAID Data Ecosystem Discovery Portal?
- Is the CP's contact information (or a group alias) prominently listed on the resource's website?
- Is the same CP or team able to engage with NIAID on training activities and Portal onboarding?
- Does your resource provide training materials explaining how to access and use the digital objects you host? If so, what format — documentation, video tutorials, workshops?
- Do training materials include contact information for user support?

Listen for:
- No designated CP — this is a critical gap for Blueprint compliance and Portal integration
- CP exists internally but contact information is not publicly listed
- Training materials exist but lack contact information
- No training materials at all — note as a gap for community adoption
