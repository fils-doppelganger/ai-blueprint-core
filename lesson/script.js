const COURSE = {
  title: "NIAID Blueprint for Digital Objects",
  subtitle: "Interactive Study Guide for Data Generators & Repository Owners",
  description: "A six-lesson course on the NIAID Blueprint — covering FAIR principles, metadata schemas, persistent identifiers, API standards, citation practices, and outreach requirements for infectious and immune-mediated disease (IID) research.",
  lessons: [
    {
      id: 1,
      title: "FAIR Principles & Blueprint Overview",
      goal: "Understand why the NIAID Blueprint was created and how FAIR principles frame it.",
      objectives: [
        "Define the four FAIR principles and their relevance to NIAID data",
        "Identify the five key areas of the NIAID Blueprint",
        "Distinguish the roles of data generators vs. repository owners",
        "Explain what a digital object is in the NIAID context"
      ],
      content: [
        {
          heading: "What Is the NIAID Blueprint?",
          text: "NIAID-funded research produces millions of digital objects — data, software, methods, and workflows. The Blueprint is a minimal set of specifications developed by ODSET (Office of Data Science and Emerging Technologies) in partnership with GO FAIR US to make these objects more discoverable and reusable across the NIAID Data Ecosystem."
        },
        {
          heading: "The FAIR Principles",
          text: "FAIR stands for Findable, Accessible, Interoperable, and Reusable. Findable means objects have rich metadata and persistent identifiers. Accessible means retrieval protocols are open and free. Interoperable means metadata uses shared vocabularies. Reusable means objects have clear licenses and provenance. The Blueprint translates these abstract principles into concrete, actionable requirements."
        },
        {
          heading: "Five Blueprint Areas",
          text: "The Blueprint is organized into five areas: (1) Minimal Metadata Schema — standardized fields based on schema.org; (2) Persistent Identifiers — DOIs, ORCIDs, RORs; (3) API Specifications — JSON-LD endpoints following OpenAPI; (4) Citation Requirements — standard formats with PIDs; (5) Outreach and Training — designated Contact Points at each repository."
        },
        {
          heading: "Two Audiences",
          text: "Data generators (researchers) are responsible for capturing structured metadata and PIDs during data creation. Repository owners are responsible for applying the schema, maintaining PID infrastructure, exposing metadata via API, posting citation guidance, and designating a Contact Point. Both audiences benefit from the NIAID Data Ecosystem Discovery Portal."
        }
      ],
      flashcards: [
        { front: "What does FAIR stand for?", back: "Findable, Accessible, Interoperable, Reusable — a framework for maximizing the value of scientific data." },
        { front: "What is a digital object in NIAID terms?", back: "A sequence of bits representing information (data, software, methods, or workflows), identified by a PID and described by metadata." },
        { front: "Who developed the NIAID Blueprint?", back: "ODSET (Office of Data Science and Emerging Technologies) in partnership with GO FAIR US (GFU), a group of global data sharing experts." }
      ],
      quiz: [
        {
          question: "Which of the following is NOT one of the five NIAID Blueprint areas?",
          options: ["Minimal Metadata Schema", "Persistent Identifiers", "Data Encryption Standards", "Citation Requirements"],
          answer: 2,
          explanation: "Data Encryption Standards is not a Blueprint area. The five areas are: Metadata Schema, PIDs, API Specifications, Citation Requirements, and Outreach & Training."
        },
        {
          question: "A data generator's primary Blueprint responsibility is to:",
          options: ["Build and maintain repository APIs", "Capture structured metadata and PIDs during data creation", "Designate a Contact Point for outreach", "Register DOIs with Crossref on behalf of repositories"],
          answer: 1,
          explanation: "Data generators are responsible for capturing metadata and PIDs. Repository owners handle APIs, Contact Points, and DOI infrastructure."
        }
      ],
      sources: [
        { label: "NIAID Blueprint Document (Sept 2025)", url: "https://datascience.niaid.nih.gov" },
        { label: "GO FAIR — FAIR Principles", url: "https://www.go-fair.org/fair-principles/" },
        { label: "NIAID Data Ecosystem Discovery Portal", url: "https://data.niaid.nih.gov" }
      ]
    },
    {
      id: 2,
      title: "Minimal Metadata Schema",
      goal: "Learn the required metadata elements, their formats, and how they support FAIR data discovery.",
      objectives: [
        "List the core metadata elements defined in Blueprint Table 1",
        "Identify the preferred schema and default format for each element",
        "Distinguish required from optional (multi-entry) fields",
        "Explain why schema.org is the preferred metadata framework"
      ],
      content: [
        {
          heading: "Why Metadata Matters",
          text: "Metadata provides the context that makes digital objects findable and reusable — especially when the data itself cannot be openly shared (e.g., patient health information). Even partial metadata adoption improves alignment and interoperability across NIAID repositories."
        },
        {
          heading: "The Schema.org Foundation",
          text: "Blueprint metadata elements are based on schema.org, a widely adopted framework defining relationships between data elements. Alternative schemas (Bioschemas, FHIR) are acceptable if they are interoperable with schema.org, widely used, openly available, and community-maintained. The Blueprint does not mandate a storage format — repositories may use JSON, YAML, XML, or JSON-LD."
        },
        {
          heading: "Core Required Elements",
          text: "Every digital object should have: type (IRI to type, e.g. dataset), identifier (resolvable DOI), name (free text title), description (free text), dateCreated (ISO 8601), conditionsOfAccess (URL to access terms), and license (SPDX identifier or URL)."
        },
        {
          heading: "Extended Elements (Multi-Entry)",
          text: "Additional elements marked with ** accept multiple values: author (ORCID), funder (ROR), grant (alphanumeric), measurementTechnique (NCIT), distribution (URL), citation (URL), infectiousAgent (NCBITaxon), host (NCBITaxon), healthCondition (MONDO), spatialCoverage (ISO 3166), temporalCoverage (ISO 8601 date range)."
        }
      ],
      flashcards: [
        { front: "What is the default identifier format for a digital object?", back: "A resolvable DOI — e.g., https://doi.org/10.1234/abcd. The DOI prefix makes it directly resolvable." },
        { front: "Which ontology is default for healthCondition?", back: "MONDO (Mondo Disease Ontology) — e.g., MONDO_0100096 for COVID-19." },
        { front: "What format should dateCreated use?", back: "ISO 8601 date format, e.g., 2022-05-01." }
      ],
      quiz: [
        {
          question: "Which metadata element uses ORCID as its default PID format?",
          options: ["funder", "author", "identifier", "grant"],
          answer: 1,
          explanation: "The author field uses ORCID (Open Researcher and Contributor Identifier) as its default. The funder field uses ROR, and identifier uses a resolvable DOI."
        },
        {
          question: "The Blueprint specifies which metadata storage format repositories must use.",
          options: ["True — JSON-LD is required", "False — repositories choose the format that fits their implementation", "True — XML is the required format", "False — but JSON is strongly recommended"],
          answer: 1,
          explanation: "The Blueprint does NOT specify a storage format. Repositories should select JSON, YAML, XML, or another format that best fits their needs."
        }
      ],
      sources: [
        { label: "Schema.org", url: "https://schema.org" },
        { label: "Bioschemas", url: "https://bioschemas.org" },
        { label: "MONDO Disease Ontology", url: "https://mondo.monarchinitiative.org" },
        { label: "NCBITaxon", url: "https://www.ncbi.nlm.nih.gov/taxonomy" }
      ]
    },
    {
      id: 3,
      title: "Persistent Identifiers (PIDs)",
      goal: "Understand which PIDs are required for which metadata fields and why persistence matters for reproducibility.",
      objectives: [
        "Explain what makes an identifier a GUPRI",
        "Map default PIDs to their corresponding metadata elements",
        "Describe the difference between a DOI and a resolvable DOI",
        "Identify when alternative PIDs are acceptable"
      ],
      content: [
        {
          heading: "What Is a GUPRI?",
          text: "FAIR calls for Globally Unique and Persistently Resolvable Identifiers (GUPRIs). A GUPRI is globally unique (no two objects share it), persistent (it does not break when the resource moves), and resolvable (it returns useful information when dereferenced). DOIs, ORCIDs, and RORs all qualify when used in their resolvable URL form."
        },
        {
          heading: "Making a DOI Resolvable",
          text: "A raw DOI like 10.1000/182 is not directly resolvable. Prefixing it with https://doi.org/ creates the resolvable form: https://doi.org/10.1000/182. URLs are commonly used but lack the organizational persistence guarantees of DOIs — they can break when websites change."
        },
        {
          heading: "PID-to-Field Mapping",
          text: "identifier → DOI (default), RRID, URL, or IRI. author → ORCID (default), ISNI, or ROR (for organizations). funder → ROR (default). citation → IRI/URL. If a repository does not issue DOIs, researchers can register with Crossref or DataCite directly."
        },
        {
          heading: "Ontologies as Controlled Vocabularies",
          text: "Several metadata fields are populated with ontology terms rather than free text. measurementTechnique uses NCIT (default), BAO, OBI, or MMO. infectiousAgent and host use NCBITaxon. healthCondition uses MONDO. license uses SPDX identifiers. spatialCoverage uses ISO 3166 country codes."
        }
      ],
      flashcards: [
        { front: "What PID should identify a researcher (author)?", back: "ORCID — Open Researcher and Contributor Identifier. Example: 0000-0002-1825-0097" },
        { front: "What PID identifies a funding organization?", back: "ROR — Research Organization Registry. Example: https://ror.org/043z4tv69 (NIAID)" },
        { front: "What agency can researchers use to register a DOI?", back: "Crossref or DataCite — both are DOI registration agencies usable when a repository does not provide DOI services." }
      ],
      quiz: [
        {
          question: "Which form of a DOI is recommended by the Blueprint?",
          options: ["10.1000/182", "doi:10.1000/182", "https://doi.org/10.1000/182", "urn:doi:10.1000/182"],
          answer: 2,
          explanation: "The Blueprint recommends the resolvable URL form: https://doi.org/10.1000/182. This makes the identifier directly dereferenceable in a browser or machine client."
        },
        {
          question: "Which ontology is the default for describing infectious agents?",
          options: ["MONDO", "NCIT", "NCBITaxon", "SPDX"],
          answer: 2,
          explanation: "NCBITaxon (NCBI Taxonomy) is the default for both infectiousAgent and host fields. MONDO is for healthCondition, and NCIT is for measurementTechnique."
        }
      ],
      sources: [
        { label: "ORCID", url: "https://orcid.org" },
        { label: "Research Organization Registry (ROR)", url: "https://ror.org" },
        { label: "DataCite DOI Registration", url: "https://datacite.org" },
        { label: "NCBI Taxonomy (NCBITaxon)", url: "https://www.ncbi.nlm.nih.gov/taxonomy" }
      ]
    },
    {
      id: 4,
      title: "Minimal API Specifications",
      goal: "Learn the minimum technical requirements for exposing metadata via an API that supports machine-readable discovery.",
      objectives: [
        "Describe the four minimum API objectives in the Blueprint",
        "Explain why resource-oriented IRI structure is preferred",
        "Identify when GET vs POST is appropriate for metadata retrieval",
        "Recognize valid alternatives for repositories without API capability"
      ],
      content: [
        {
          heading: "Why APIs for Metadata?",
          text: "Repositories range from those with no programmatic access to those with advanced knowledge graphs. Aligning to a common API standard maximizes metadata findability across all NIAID research areas. Even simple implementations — like HTML with embedded JSON-LD — satisfy the spirit of the requirement."
        },
        {
          heading: "Four Minimum API Objectives",
          text: "1. Metadata Encoding: responses must support JSON-LD, following schema.org types and properties. 2. IRI Structure: endpoints should be resource-oriented (e.g., /datasets/{dataset_id}), avoiding verbs. The IRI should serve as the @id in JSON-LD. 3. HTTP Method: GET for retrieval; POST is acceptable for large queries or security-sensitive submissions. 4. Documentation: must follow OpenAPI/Swagger specifications."
        },
        {
          heading: "Tiered Implementation Options",
          text: "Minimal option: add HTML with embedded JSON-LD metadata to dataset pages. Intermediate option: provide a downloadable metadata index in a machine-readable format. Advanced option: a fully queryable metadata knowledge graph. All tiers are acceptable — repositories choose based on their maturity and resources."
        },
        {
          heading: "JSON-LD @id and Knowledge Graphs",
          text: "When the API endpoint IRI matches the JSON-LD @id field of the returned document, the resource becomes directly addressable in a graph. This enables seamless integration into NIAID ecosystem knowledge graphs and external cataloging services. The @id node should resolve to the document when dereferenced."
        }
      ],
      flashcards: [
        { front: "What metadata encoding format must NIAID APIs support?", back: "JSON-LD (at minimum as an option). It follows schema.org types and properties from the minimal metadata specification." },
        { front: "What API documentation standard does the Blueprint require?", back: "OpenAPI/Swagger specifications — ensures machine-readability and ease of use for developers." },
        { front: "What is the minimal API implementation option?", back: "HTML pages with embedded structured metadata (e.g., JSON-LD in a script tag) — no dedicated API endpoint required." }
      ],
      quiz: [
        {
          question: "An API endpoint /search?type=dataset&host=human is consistent with Blueprint IRI structure guidelines.",
          options: ["True — query parameters are the standard approach", "False — endpoints should be resource-oriented IRIs without verbs or complex query parameters", "True — POST with query params is equivalent", "False — only GET with path parameters is allowed"],
          answer: 1,
          explanation: "The Blueprint recommends resource-oriented IRIs like /datasets/{dataset_id}. Avoiding verbs and complex query parameters ensures IRIs can serve as persistent identifiers in the JSON-LD @id field."
        },
        {
          question: "Which scenario justifies using HTTP POST instead of GET for metadata retrieval?",
          options: ["The developer prefers POST", "Parameters are too large or complex to include in a URL, or security requirements apply", "The repository uses XML instead of JSON-LD", "POST is always required for metadata endpoints"],
          answer: 1,
          explanation: "GET is preferred for metadata retrieval, but POST may be used when parameters must go in the message body — such as large queries, complex filters, or security/data submission requirements."
        }
      ],
      sources: [
        { label: "OpenAPI Specification", url: "https://spec.openapis.org/oas/latest.html" },
        { label: "JSON-LD Specification", url: "https://json-ld.org" },
        { label: "Schema.org Dataset", url: "https://schema.org/Dataset" },
        { label: "ImmPort API Example", url: "https://immport.org/data/query/api/study/SDY998?format=json" }
      ]
    },
    {
      id: 5,
      title: "Citation Requirements",
      goal: "Understand how to properly cite digital objects and what repository owners must provide to support citation.",
      objectives: [
        "Explain why consistent citation of digital objects matters for reproducibility",
        "List the three citation guidance requirements for repository owners",
        "Construct an APA-style citation for a dataset with a DOI",
        "Identify when to cite individual objects vs. the repository as a whole"
      ],
      content: [
        {
          heading: "Why Cite Digital Objects?",
          text: "Citation ensures proper attribution, supports reproducibility, enables repositories to track data reuse, and links publications to the data that underpins them. PIDs like ORCIDs allow repository owners to measure scientific impact and trace how specific datasets contribute to downstream research."
        },
        {
          heading: "When to Cite Objects vs. the Repository",
          text: "If a user accesses a small number of discrete datasets, cite each individual object (using its DOI). If a user queries broadly across a repository, cite the repository as a whole — but still include PIDs like RRIDs or DOIs where they exist. ITN Trialshare is an example of a repository with an assigned RRID."
        },
        {
          heading: "Three Repository Owner Requirements",
          text: "1. Integrate PIDs into citations — encourage use of resolvable DOIs. 2. Establish consistent guidelines — original data citations include repository name, repository PID (e.g., RRID), and data PID; reused data citations include object PID (DOI) and accession numbers if applicable. 3. Use standard formats — provide APA, MLA, Chicago, PubMed/NLM examples so researchers can import citations into tools."
        },
        {
          heading: "Citation Format Examples",
          text: "APA Dataset: Author(s). (Year). Title (Version) [Data set]. Repository. DOI. Example: Smith, John, et al. (2023). Global Health Dataset (Version 1.0) [Data set]. DataHub. https://doi.org/10.1234/abcd1234. The bracketed [Data set] tag helps publication indexing systems identify data citations correctly."
        }
      ],
      flashcards: [
        { front: "What does the APA bracketed tag [Data set] do in a citation?", back: "It signals to publication indexing systems that the citation refers to a dataset, enabling proper data citation tracking." },
        { front: "What PID is commonly used to identify a repository as a whole?", back: "RRID (Research Resource Identifier) — many NIAID repositories have been assigned RRIDs. DOIs may also be used when assigned to the repository." },
        { front: "Where should citation guidance be placed on a repository website?", back: "Prominently, in a dedicated section (e.g., titled How to Cite), in documentation, newsletters, training materials, and within individual dataset metadata." }
      ],
      quiz: [
        {
          question: "A researcher downloads data from 3 specific ImmPort studies. According to the Blueprint, they should:",
          options: ["Cite the ImmPort repository once with its RRID", "Cite each of the 3 studies individually using their DOIs", "No citation is needed for data repositories", "Cite only the publication associated with the data"],
          answer: 1,
          explanation: "When accessing discrete digital objects, the Blueprint recommends citing each object individually using its DOI to ensure traceability for the resulting research."
        },
        {
          question: "Which citation element distinguishes an APA data citation from a journal article citation?",
          options: ["Including the year in parentheses", "The bracketed descriptor [Data set] after the title", "Using italics for the dataset name", "Including the version number"],
          answer: 1,
          explanation: "The bracketed [Data set] tag after the title is the key distinguishing element. It signals to indexing systems that this is a data citation rather than a publication."
        }
      ],
      sources: [
        { label: "APA Citation Guide for Data", url: "https://apastyle.apa.org/style-grammar-guidelines/references/examples/data-set-references" },
        { label: "DataCite Metadata Schema", url: "https://schema.datacite.org" },
        { label: "FORCE11 Data Citation Principles", url: "https://force11.org/info/data-citation-principles/" }
      ]
    },
    {
      id: 6,
      title: "Outreach, Training & Final Review",
      goal: "Learn the Contact Point requirements and consolidate knowledge across all five Blueprint areas.",
      objectives: [
        "Describe the role and responsibilities of a repository Contact Point (CP)",
        "Explain why social-cultural factors matter alongside technical specifications",
        "Synthesize all five Blueprint areas and their interdependencies",
        "Apply Blueprint requirements to a real-world scenario"
      ],
      content: [
        {
          heading: "Beyond Technical Specifications",
          text: "The Blueprint recognizes that many barriers to data sharing are social and cultural — not just technical. A human network of points of contact bridges the gap between technical infrastructure and community adoption. Each major NIAID repository must designate a Contact Point (CP) to support this network."
        },
        {
          heading: "Contact Point Responsibilities",
          text: "The CP must: engage with NIAID and stakeholders; participate in NIAID Data Ecosystem Discovery Portal training and outreach; facilitate transfer of Blueprint implementation guidance to repository staff; be publicly reachable for researcher questions about data access; and support continuity in training activities. A group alias can supplement but not replace an individual CP designation."
        },
        {
          heading: "Training Materials",
          text: "Generators and repositories should develop training materials that explain how to effectively use their digital objects. These materials must include contact information and be shared through workshops, online trainings, newsletters, and documentation pages. This ensures the community can adopt Blueprint practices and benefit from NIAID data resources."
        },
        {
          heading: "The Full Blueprint Picture",
          text: "All five areas are interdependent: metadata without PIDs lacks persistence; PIDs without APIs cannot be machine-harvested; APIs without citation guidance break the attribution chain; and all technical work fails without community adoption (outreach). The NIAID Data Ecosystem Discovery Portal aggregates resources from repositories that implement all five areas, creating a federated, searchable catalog of IID digital objects."
        }
      ],
      flashcards: [
        { front: "What is a Contact Point (CP) in Blueprint terms?", back: "A designated individual at a major NIAID repository responsible for outreach, training, stakeholder engagement, and supporting Blueprint implementation." },
        { front: "Can a group alias replace the individual CP designation?", back: "No — a group alias can supplement the CP but repositories must still designate one named individual as the primary Contact Point." },
        { front: "What is the NIAID Data Ecosystem Discovery Portal?", back: "A portal that aggregates and enhances metadata from NIAID-relevant data resources to support cross-repository search for infectious and immune-mediated disease datasets." }
      ],
      quiz: [
        {
          question: "Which statement best describes why the Blueprint includes outreach requirements alongside technical ones?",
          options: ["Regulatory compliance requires a named contact at each repository", "Many data sharing challenges are social-cultural, not just technical", "The Discovery Portal requires a human interface for each repository", "Training reduces the volume of API requests"],
          answer: 1,
          explanation: "The Blueprint explicitly states that many barriers to data integration are based on social-cultural factors. A human network of Contact Points addresses what technical specifications alone cannot."
        },
        {
          question: "A repository has excellent metadata and a working API, but no Contact Point and no citation guidance posted publicly. Under the Blueprint, this repository:",
          options: ["Fully meets Blueprint requirements", "Meets technical requirements but is incomplete — citation guidance and a CP are required", "Only needs to add a CP to be compliant", "Is compliant because the technical areas are the most important"],
          answer: 1,
          explanation: "The Blueprint requires all five areas. Missing citation guidance (Area 4) and a Contact Point (Area 5) means the repository is incomplete, even if its metadata, PIDs, and API are solid."
        }
      ],
      sources: [
        { label: "NIAID Data Ecosystem — How to Contribute", url: "https://data.niaid.nih.gov" },
        { label: "Contact: NIAID Data Ecosystem", url: "mailto:niaiddataecosystem@mail.nih.gov" },
        { label: "Contact: ODSET Data Science", url: "mailto:datascience@niaid.nih.gov" }
      ]
    }
  ]
};

// App state
let currentLesson = 0;
let flippedCards = {};
let quizAnswers = {};
let lessonProgress = {};
let finalQuizAnswers = {};

const FINAL_QUIZ = [
  {
    question: "Which schema does the Blueprint recommend as the primary basis for metadata elements?",
    options: ["Dublin Core", "Schema.org", "FHIR", "BioSchemas"],
    answer: 1,
    explanation: "Schema.org is the preferred standard. Alternatives like Bioschemas and FHIR are acceptable if interoperable with schema.org."
  },
  {
    question: "ORCID identifies which type of entity?",
    options: ["A funding organization", "A dataset", "A researcher or academic", "A repository"],
    answer: 2,
    explanation: "ORCID (Open Researcher and Contributor Identifier) identifies individual researchers. ROR identifies organizations."
  },
  {
    question: "A NIAID repository that cannot build a REST API can still meet Blueprint API requirements by:",
    options: ["Requesting an exemption from ODSET", "Embedding JSON-LD metadata in their HTML pages", "Providing CSV downloads of data files", "Using email-based data requests"],
    answer: 1,
    explanation: "HTML with embedded JSON-LD metadata is explicitly listed as a valid minimal implementation option for repositories without API infrastructure."
  },
  {
    question: "For the license metadata element, the Blueprint default is:",
    options: ["Creative Commons BY 4.0", "An SPDX License Identifier or URL to the license document", "A plain text description of access terms", "ODRL expression"],
    answer: 1,
    explanation: "SPDX License Identifiers are the default. If the license is not in SPDX, an IRI pointing to the license document is acceptable."
  },
  {
    question: "Which combination of PIDs is correct for a dataset record in Blueprint-aligned metadata?",
    options: [
      "identifier=ORCID, author=DOI, funder=RRID",
      "identifier=DOI, author=ORCID, funder=ROR",
      "identifier=ROR, author=ISNI, funder=ORCID",
      "identifier=URL, author=ROR, funder=DOI"
    ],
    answer: 1,
    explanation: "The correct defaults are: identifier uses DOI, author uses ORCID, and funder uses ROR. These are the three most commonly required PID mappings."
  }
];

function init() {
  renderSidebar();
  renderLesson(0);
  renderFinalQuiz();
  updateProgress();
}

function renderSidebar() {
  const sidebar = document.getElementById("lesson-sidebar");
  sidebar.innerHTML = COURSE.lessons.map((lesson, i) => `
    <button
      class="sidebar-btn ${i === currentLesson ? "active" : ""} ${lessonProgress[i] ? "completed" : ""}"
      onclick="goToLesson(${i})"
      id="sidebar-btn-${i}"
    >
      <span class="lesson-num">Lesson ${lesson.id}</span>
      <span class="lesson-label">${lesson.title}</span>
      ${lessonProgress[i] ? '<span class="check">&#10003;</span>' : ""}
    </button>
  `).join("") + `
    <button
      class="sidebar-btn ${currentLesson === "final" ? "active" : ""}"
      onclick="goToLesson('final')"
      id="sidebar-btn-final"
    >
      <span class="lesson-num">Review</span>
      <span class="lesson-label">Final Quiz</span>
    </button>
  `;
}

function goToLesson(index) {
  currentLesson = index;
  renderSidebar();
  if (index === "final") {
    document.getElementById("lesson-content").classList.add("hidden");
    document.getElementById("final-quiz-section").classList.remove("hidden");
    window.scrollTo(0, 0);
  } else {
    document.getElementById("final-quiz-section").classList.add("hidden");
    document.getElementById("lesson-content").classList.remove("hidden");
    renderLesson(index);
    window.scrollTo(0, 0);
  }
}

function renderLesson(index) {
  const lesson = COURSE.lessons[index];
  const el = document.getElementById("lesson-content");

  el.innerHTML = `
    <div class="lesson-header">
      <div class="lesson-tag">Lesson ${lesson.id} of ${COURSE.lessons.length}</div>
      <h2>${lesson.title}</h2>
      <p class="lesson-goal">${lesson.goal}</p>
    </div>

    <div class="objectives-block">
      <h3>Learning Objectives</h3>
      <ul>
        ${lesson.objectives.map(o => `<li>${o}</li>`).join("")}
      </ul>
    </div>

    <div class="content-sections">
      ${lesson.content.map(section => `
        <div class="content-section">
          <h4>${section.heading}</h4>
          <p>${section.text}</p>
        </div>
      `).join("")}
    </div>

    <div class="flashcard-section">
      <h3>Flashcards</h3>
      <div class="flashcard-grid">
        ${lesson.flashcards.map((card, ci) => `
          <div
            class="flashcard ${flippedCards[index + "-" + ci] ? "flipped" : ""}"
            onclick="flipCard(${index}, ${ci})"
            role="button"
            aria-label="Flashcard ${ci + 1}"
          >
            <div class="card-inner">
              <div class="card-front"><span class="card-hint">tap to flip</span><p>${card.front}</p></div>
              <div class="card-back"><p>${card.back}</p></div>
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <div class="quiz-section">
      <h3>Knowledge Check</h3>
      ${lesson.quiz.map((q, qi) => renderQuestion(q, qi, index, "lesson")).join("")}
    </div>

    <div class="source-section">
      <h3>Sources</h3>
      <div class="source-grid">
        ${lesson.sources.map(s => `
          <a href="${s.url}" target="_blank" rel="noopener" class="source-card">
            <span class="source-icon">&#128279;</span>
            <span>${s.label}</span>
          </a>
        `).join("")}
      </div>
    </div>

    <div class="lesson-nav">
      ${index > 0 ? `<button class="nav-btn secondary" onclick="goToLesson(${index - 1})">&#8592; Previous</button>` : "<span></span>"}
      ${index < COURSE.lessons.length - 1
        ? `<button class="nav-btn primary" onclick="completeAndNext(${index})">Next Lesson &#8594;</button>`
        : `<button class="nav-btn primary" onclick="completeAndNext(${index})">Final Review &#8594;</button>`}
    </div>
  `;
}

function renderQuestion(q, qi, lessonIndex, scope) {
  const key = scope === "lesson" ? `${lessonIndex}-${qi}` : `final-${qi}`;
  const answered = scope === "lesson" ? quizAnswers[key] : finalQuizAnswers[qi];

  return `
    <div class="quiz-question" id="q-${key}">
      <p class="q-text">${qi + 1}. ${q.question}</p>
      <div class="options">
        ${q.options.map((opt, oi) => {
          let cls = "option-btn";
          if (answered !== undefined) {
            if (oi === q.answer) cls += " correct";
            else if (oi === answered && oi !== q.answer) cls += " incorrect";
            else cls += " dim";
          }
          return `<button class="${cls}" onclick="answerQuestion('${key}', ${oi}, ${q.answer}, '${scope}')" ${answered !== undefined ? "disabled" : ""}>${opt}</button>`;
        }).join("")}
      </div>
      ${answered !== undefined ? `<div class="explanation">${q.explanation}</div>` : ""}
    </div>
  `;
}

function renderFinalQuiz() {
  const el = document.getElementById("final-quiz-section");
  el.innerHTML = `
    <div class="lesson-header">
      <div class="lesson-tag">Final Review</div>
      <h2>Cumulative Quiz</h2>
      <p class="lesson-goal">Test your mastery across all five Blueprint areas.</p>
    </div>
    <div class="quiz-section" id="final-quiz-questions">
      ${FINAL_QUIZ.map((q, qi) => renderFinalQuestion(q, qi)).join("")}
    </div>
    <div id="final-score" class="final-score hidden"></div>
    <div class="lesson-nav">
      <button class="nav-btn secondary" onclick="goToLesson(${COURSE.lessons.length - 1})">&#8592; Last Lesson</button>
      <button class="nav-btn primary" onclick="showFinalScore()">Show Score</button>
    </div>
  `;
}

function renderFinalQuestion(q, qi) {
  const answered = finalQuizAnswers[qi];
  return `
    <div class="quiz-question" id="fq-${qi}">
      <p class="q-text">${qi + 1}. ${q.question}</p>
      <div class="options">
        ${q.options.map((opt, oi) => {
          let cls = "option-btn";
          if (answered !== undefined) {
            if (oi === q.answer) cls += " correct";
            else if (oi === answered && oi !== q.answer) cls += " incorrect";
            else cls += " dim";
          }
          return `<button class="${cls}" onclick="answerFinalQuestion(${qi}, ${oi}, ${q.answer})" ${answered !== undefined ? "disabled" : ""}>${opt}</button>`;
        }).join("")}
      </div>
      ${answered !== undefined ? `<div class="explanation">${q.explanation}</div>` : ""}
    </div>
  `;
}

function flipCard(lessonIndex, cardIndex) {
  const key = `${lessonIndex}-${cardIndex}`;
  flippedCards[key] = !flippedCards[key];
  renderLesson(lessonIndex);
}

function answerQuestion(key, chosen, correct, scope) {
  if (scope === "lesson") {
    quizAnswers[key] = chosen;
  } else {
    finalQuizAnswers[parseInt(key.split("-")[1])] = chosen;
  }
  const parts = key.split("-");
  const lessonIndex = parseInt(parts[0]);
  renderLesson(lessonIndex);
  updateProgress();
}

function answerFinalQuestion(qi, chosen, correct) {
  finalQuizAnswers[qi] = chosen;
  const el = document.getElementById("fq-" + qi);
  const q = FINAL_QUIZ[qi];
  el.querySelector(".options").innerHTML = q.options.map((opt, oi) => {
    let cls = "option-btn";
    if (oi === correct) cls += " correct";
    else if (oi === chosen && oi !== correct) cls += " incorrect";
    else cls += " dim";
    return `<button class="${cls}" disabled>${opt}</button>`;
  }).join("");
  if (!el.querySelector(".explanation")) {
    const exp = document.createElement("div");
    exp.className = "explanation";
    exp.textContent = q.explanation;
    el.appendChild(exp);
  }
}

function showFinalScore() {
  const total = FINAL_QUIZ.length;
  const correct = FINAL_QUIZ.filter((q, i) => finalQuizAnswers[i] === q.answer).length;
  const pct = Math.round((correct / total) * 100);
  const el = document.getElementById("final-score");
  el.classList.remove("hidden");
  el.innerHTML = `
    <div class="score-card">
      <div class="score-number">${correct}/${total}</div>
      <div class="score-label">${pct}% — ${pct >= 80 ? "Blueprint Ready!" : pct >= 60 ? "Good Progress" : "Keep Reviewing"}</div>
      <div class="score-bar"><div class="score-fill" style="width:${pct}%"></div></div>
    </div>
  `;
  el.scrollIntoView({ behavior: "smooth" });
}

function completeAndNext(index) {
  lessonProgress[index] = true;
  updateProgress();
  if (index < COURSE.lessons.length - 1) {
    goToLesson(index + 1);
  } else {
    goToLesson("final");
  }
}

function updateProgress() {
  const done = Object.keys(lessonProgress).length;
  const total = COURSE.lessons.length;
  const pct = Math.round((done / total) * 100);
  const bar = document.getElementById("progress-bar");
  const label = document.getElementById("progress-label");
  if (bar) bar.style.width = pct + "%";
  if (label) label.textContent = `${done}/${total} lessons complete`;
}

document.addEventListener("DOMContentLoaded", init);
