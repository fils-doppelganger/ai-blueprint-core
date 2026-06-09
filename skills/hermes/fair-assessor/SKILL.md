---
name: fair-assessment
description: Assess web resources and datasets for alignment with FAIR principles. Takes a starting URL + FAIR blueprint, crawls first-level links (using Firecrawl for JS-rendered pages), extracts content, and produces a structured alignment report.
version: 1.0.0
author: Doug Fils
license: MIT
metadata:
  hermes:
    tags: [research, data-management, FAIR, metadata, assessment]
    category: science
    requires_toolsets: [web]
---

# FAIR Principles Alignment Assessment

Evaluate how well web resources (especially scientific datasets, data portals, and repositories) align with a given FAIR principles blueprint.

## When to Use
Use this skill when the user provides:
- A starting/top-level URL for a dataset, data portal, or resource collection
- A FAIR blueprint document (either as a URL or local file path)
- A request to assess alignment to FAIR principles (Findable, Accessible, Interoperable, Reusable)

This skill is especially useful for JavaScript-rendered pages and modern data portals.

## Procedure

1. **Gather inputs**  
   Confirm the starting URL and the location of the FAIR blueprint (URL or local file path). If the blueprint is local, read it first.

2. **Fetch the starting page using Firecrawl**  
   Use Firecrawl (via `web_extract`, `firecrawl_scrape`, or equivalent) to get clean, well-structured Markdown from the top-level page. This handles JavaScript-rendered content properly.

3. **Identify first-level links**  
   Extract the most relevant first-level links from the starting page (focus on documentation, data access pages, metadata, APIs, licensing, etc.). Prioritize links that are likely to contain substantive content for FAIR evaluation.

4. **Fetch and extract content from key pages**  
   Use Firecrawl again on the most important linked pages to get clean Markdown/text. Avoid low-value pages (e.g., login walls, pure navigation).

5. **Compare against the FAIR blueprint**  
   Read the blueprint document. For each of the four FAIR principles (Findable, Accessible, Interoperable, Reusable) and their sub-criteria:
   - Check whether the resources meet, partially meet, or fail the criterion.
   - Quote specific evidence from the fetched pages.
   - Note gaps or missing elements.

6. **Produce the final report**  
   Structure the output clearly with:
   - Summary of overall alignment
   - Per-principle breakdown with evidence quotes
   - Specific gaps and recommendations
   - Overall alignment score (e.g., out of 100 or qualitative rating)
   - Any suggested next steps or improvements

## Pitfalls
- Some sites block scraping or require authentication — note these limitations clearly.
- Very large sites may have hundreds of links; be selective and focus on the most relevant ones for FAIR assessment.
- JavaScript-heavy pages without Firecrawl will return poor results — always prefer Firecrawl tools when available.
- Blueprint documents can be long; read them efficiently and focus on the core criteria.

## Verification
The final output should be a clear, structured assessment report that a human can easily review. It should contain direct quotes from the source pages as evidence and actionable recommendations.
