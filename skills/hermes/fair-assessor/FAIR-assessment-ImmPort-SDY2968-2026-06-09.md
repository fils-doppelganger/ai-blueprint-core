# FAIR Principles Alignment Assessment

**Resource**: ImmPort Study SDY2968  
**URL**: https://www.immport.org/shared/study/SDY2968/summary  
**Blueprint**: NIAID Blueprint v2 (26 Sep 2025)  
**Assessment Date**: 2026-06-09  
**Assessor**: Hermes Agent (fair-assessment skill)

---

## Summary

**Overall Alignment**: Moderate (estimated 55–65%)

ImmPort provides a solid foundation with persistent identifiers (DOI), structured downloads, and an API layer. However, the public-facing study summary page for SDY2968 exposes very limited metadata. Much of the rich metadata required by the NIAID Blueprint appears to exist behind the API or in downloadable packages rather than being openly discoverable on the web page itself.

---

## Per-Principle Breakdown

### 1. Findable

**Status**: Partial

**Evidence**:
- Study has a resolvable DOI: `10.21430/M3J8UMVGT6`
- Study has a clear accession (SDY2968)
- Listed in ImmPort's shared data catalog
- Monthly data releases are announced publicly

**Gaps**:
- Very little schema.org / JSON-LD metadata visible on the public summary page
- No rich metadata (authors with ORCIDs, funder ROR, measurementTechnique, etc.) exposed in HTML
- The summary page is quite sparse

**Score**: 6/10

### 2. Accessible

**Status**: Good

**Evidence**:
- Data is downloadable without login for this study
- Multiple formats available (Tab-delimited, MySQL dump, manifest files)
- GA4GH DRS API support mentioned in documentation
- Clear download instructions and deprecation notices for legacy tools

**Gaps**:
- Some studies may require controlled access (not applicable to SDY2968)

**Score**: 8/10

### 3. Interoperable

**Status**: Moderate

**Evidence**:
- Uses standardized data model with Common Data Elements (CDEs)
- Supports ontologies (mentioned in docs)
- Provides API access with Swagger documentation
- DRS IDs are used for files

**Gaps**:
- Public pages do not return JSON-LD (schema.org) by default
- Limited visible use of required NIAID fields (`infectiousAgent`, `host`, `healthCondition`, etc.) on the study page
- No obvious machine-readable metadata endpoint directly linked from the study summary

**Score**: 5/10

### 4. Reusable

**Status**: Moderate

**Evidence**:
- Clear licensing and data use agreements referenced
- Citation guidance exists on the ImmPort site
- Study has a DOI for citation
- Manifest and summary files included in downloads

**Gaps**:
- No prominent "How to Cite" section directly on the study page
- Limited visible metadata for reuse (e.g., measurement techniques, spatial/temporal coverage)
- Contact point for the specific study is not clearly listed on the summary page

**Score**: 6/10

---

## Key Gaps & Recommendations

| Area | Recommendation | Priority |
|------|----------------|----------|
| **Metadata Exposure** | Add schema.org JSON-LD (or embedded metadata) to study summary pages using the NIAID Minimal Metadata Schema | High |
| **Persistent Identifiers** | Ensure all studies prominently display both DOI and ImmPort accession | Medium |
| **API / Machine Readability** | Provide a direct link from study pages to the JSON-LD or API representation | High |
| **Citation** | Add a visible "How to Cite" box on every study page | Medium |
| **Point of Contact** | List a designated contact (or link to ImmPort support) on study pages | Low |

---

## Overall Recommendations

ImmPort is already one of the more mature NIAID repositories. With relatively modest enhancements to the public study pages (especially adding structured metadata and clear citation guidance), it could reach **strong alignment** with the NIAID Blueprint.

The current study page (SDY2968) is functional for human users but does not yet meet the "machine-actionable" expectations of the FAIR blueprint, particularly around metadata exposure and interoperability.

---

## Sources Used

- https://www.immport.org/shared/study/SDY2968/summary
- https://www.immport.org/shared/study/SDY2968/download
- https://docs.immport.org/
- https://www.immport.org/
- NIAID Blueprint v2 (https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md)