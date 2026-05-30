# PID Help — Finding Identifiers During the Interview

Load this reference when a user doesn't know a PID and needs help finding it. Walk them through the relevant section without leaving the conversation.

---

## Finding an ORCID

**What it is:** A unique 16-digit identifier for researchers. Format: `https://orcid.org/0000-0000-0000-0000`

**If the researcher knows they have one:**
> "You can find your ORCID by logging in at orcid.org — it's displayed prominently on your profile page."

**If they're not sure they have one:**
> "You can check by searching your name at orcid.org/orcid-search. If you don't have one, registration is free at orcid.org/register and takes about two minutes."

**Acceptable fallback:** If the user cannot find their ORCID during the interview, collect their name only and flag the missing ORCID in Metadata Notes. Do not block progress.

---

## Finding a ROR ID

**What it is:** A unique identifier for research organizations. Format: `https://ror.org/XXXXXXX`

**Lookup:** Search by organization name at ror.org

**Pre-populated common funders:**
| Organization | ROR |
|---|---|
| NIAID | `https://ror.org/043z4tv69` |
| NIH | `https://ror.org/01cwqze88` |
| NIAMS | `https://ror.org/006zn3t30` |
| NHLBI | `https://ror.org/012pb6c26` |
| NCI | `https://ror.org/040gcmg81` |
| NCATS | `https://ror.org/04pw6fb54` |
| NSF | `https://ror.org/021nxhr62` |
| BARDA | `https://ror.org/033xnrm25` |
| Wellcome Trust | `https://ror.org/029chgv08` |
| Bill & Melinda Gates Foundation | `https://ror.org/0456r8d26` |

> "If you mention NIAID, I already have their ROR on hand. For other funders, you can search at ror.org."

**Acceptable fallback:** Collect the organization name without a ROR and flag in Metadata Notes.

---

## Finding an NCBITaxon ID

**What it is:** A taxonomic identifier from NCBI's taxonomy database for organisms (infectious agents, hosts). Format: `https://www.ncbi.nlm.nih.gov/taxonomy/{taxid}`

**Lookup:** Search at ncbi.nlm.nih.gov/taxonomy

**Pre-populated common organisms:**

| Organism | TaxID | IRI |
|---|---|---|
| SARS-CoV-2 | 2697049 | `https://www.ncbi.nlm.nih.gov/taxonomy/2697049` |
| HIV-1 | 11676 | `https://www.ncbi.nlm.nih.gov/taxonomy/11676` |
| HIV-2 | 11709 | `https://www.ncbi.nlm.nih.gov/taxonomy/11709` |
| Mycobacterium tuberculosis | 1773 | `https://www.ncbi.nlm.nih.gov/taxonomy/1773` |
| Influenza A virus | 11320 | `https://www.ncbi.nlm.nih.gov/taxonomy/11320` |
| Plasmodium falciparum | 5833 | `https://www.ncbi.nlm.nih.gov/taxonomy/5833` |
| Homo sapiens | 9606 | `https://www.ncbi.nlm.nih.gov/taxonomy/9606` |
| Mus musculus | 10090 | `https://www.ncbi.nlm.nih.gov/taxonomy/10090` |
| Macaca mulatta | 9544 | `https://www.ncbi.nlm.nih.gov/taxonomy/9544` |
| Rattus norvegicus | 10116 | `https://www.ncbi.nlm.nih.gov/taxonomy/10116` |

> "Tell me the organism name and I can look up the TaxID for common ones, or you can search at ncbi.nlm.nih.gov/taxonomy."

**Acceptable fallback:** Use the plain organism name and flag in Metadata Notes.

---

## Finding a MONDO ID

**What it is:** A disease/health condition identifier from the Mondo Disease Ontology. Format: `https://purl.obolibrary.org/obo/MONDO_{id}`

**Lookup:** Search at monarchinitiative.org/mondo or obofoundry.org

**Pre-populated common conditions:**

| Condition | MONDO ID | IRI |
|---|---|---|
| COVID-19 | MONDO:0100096 | `https://purl.obolibrary.org/obo/MONDO_0100096` |
| HIV infection | MONDO:0005109 | `https://purl.obolibrary.org/obo/MONDO_0005109` |
| Tuberculosis | MONDO:0018076 | `https://purl.obolibrary.org/obo/MONDO_0018076` |
| Influenza | MONDO:0005812 | `https://purl.obolibrary.org/obo/MONDO_0005812` |
| Rheumatoid arthritis | MONDO:0008383 | `https://purl.obolibrary.org/obo/MONDO_0008383` |
| Systemic lupus erythematosus | MONDO:0007263 | `https://purl.obolibrary.org/obo/MONDO_0007263` |
| Malaria | MONDO:0005136 | `https://purl.obolibrary.org/obo/MONDO_0005136` |
| Ebola hemorrhagic fever | MONDO:0005737 | `https://purl.obolibrary.org/obo/MONDO_0005737` |
| Osteoarthritis | MONDO:0005178 | `https://purl.obolibrary.org/obo/MONDO_0005178` |
| Type 1 diabetes | MONDO:0005147 | `https://purl.obolibrary.org/obo/MONDO_0005147` |

**Acceptable fallback:** Use the plain condition name and flag in Metadata Notes.

---

## Finding an SPDX License Identifier

**What it is:** A standardized short identifier for open licenses. Full list at spdx.org/licenses

**Common identifiers:**

| License | SPDX ID |
|---|---|
| Creative Commons Zero (public domain) | `CC0-1.0` |
| Creative Commons Attribution 4.0 | `CC-BY-4.0` |
| Creative Commons Attribution-NonCommercial 4.0 | `CC-BY-NC-4.0` |
| Creative Commons Attribution-ShareAlike 4.0 | `CC-BY-SA-4.0` |
| Open Database License | `ODbL-1.0` |
| MIT License | `MIT` |
| Apache 2.0 | `Apache-2.0` |

> "If none of these match, provide the URL to your license document and I'll use that instead."

---

## Finding an NCIT Term

**What it is:** An identifier from the NCI Thesaurus for measurement techniques and other biomedical concepts. Format: `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#{code}`

**Lookup:** Search at ncithesaurus.nci.nih.gov

**Common measurement techniques:**

| Technique | NCIT Code |
|---|---|
| Flow cytometry | C16585 |
| RNA sequencing | C101289 |
| Mass cytometry (CyTOF) | C126893 |
| ELISA | C25426 |
| Western blot | C18445 |
| PCR | C17003 |
| Single-cell RNA sequencing | C163995 |
| Whole genome sequencing | C101294 |

**Acceptable fallback:** Use the plain technique name without an NCIT code and flag in Metadata Notes.
