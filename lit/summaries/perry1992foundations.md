## Foundations for the Study of Software Architecture

| Field | Value |
|-------|-------|
| **Key** | `perry1992foundations` |
| **Authors** | Dewayne E. Perry, Alexander L. Wolf |
| **Venue** | ACM SIGSOFT Software Engineering Notes, vol. 17, no. 4 (1992) |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** Software design research in the 1970s-80s focused on implementation-level techniques, but lacked a formal model for software architecture as a distinct discipline. The blurring of design and implementation led to systems suffering from increasing brittleness during evolution.
- **Gap:** No formal model existed that defined software architecture in terms of its constituent parts (elements, form, rationale), and the phenomena of architectural erosion and drift had not been formally conceptualized or named.

### Contribution
Perry and Wolf propose the first formal model of software architecture, defining it as a triple of **elements** (processing, data, connecting), **form** (weighted properties and relationships that constrain elements), and **rationale** (system constraints motivating architectural choices). The paper establishes the vocabulary and conceptual framework that all subsequent software architecture research builds upon, drawing analogies from hardware, network, and building architecture to develop an intuition for the discipline. It also introduces the concepts of **architectural style** as an abstraction over specific architectures, **architectural erosion** (violations of architecture leading to brittleness), and **architectural drift** (insensitivity to architecture leading to inadaptability).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 3  | 5  |   3   |  0  |   0    | 11/25 |

**Relevance:** HIGH

This paper provides the foundational vocabulary (elements, form, rationale, style, erosion, drift) that underpins the thesis's treatment of software architecture in Section 2.1. The concepts of architectural erosion and drift are directly relevant to the thesis objective of improving maintainability through automated tactic implementation: LLM-driven changes must preserve architectural integrity rather than contributing to erosion. The elements-form-rationale model also frames how architectural tactics (as constrained design decisions) fit within a broader architecture.

### Method & Validation
- **Type:** Framework / Conceptual Model
- **Validation:** Illustrative examples (multi-phase compiler architectures: sequential and parallel process with shared data structure), analogy to building/hardware/network architecture disciplines

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** N/A (conceptual framework paper); references Inscape environment for managing interdependencies between interface specifications and implementations
- **Languages:** N/A (language-independent; compiler architecture examples used for illustration)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Architecture model | Software Architecture = {Elements, Form, Rationale} |
| Three element classes | Processing elements, data elements, connecting elements |
| Form definition | Weighted properties (constraining element choice) + relationships (constraining element placement/interaction) |
| Architectural style | Abstraction over specific architectures; constrains elements and formal arrangements; no hard boundary between style and architecture |
| Architectural erosion | Violations of architecture leading to increased brittleness and system problems |
| Architectural drift | Insensitivity to architecture leading to inadaptability and loss of coherence |
| Connecting elements | Often overlooked but have a "profound impact" on resulting architecture; distinguishing factor between architectures of the same style |
| Multiple views needed | Processing view, data view, and connector view are interdependent and all necessary at the architectural level |
| Property-based over type-based | Property-based schemes (application-oriented properties) capture architectural constraints more expressively than type-based schemes |
| Reuse at architecture level | Greatest reuse opportunities exist at the architectural level where specifications are least constrained |
| Rationale captures non-functional concerns | Rationale explicates satisfaction of system constraints including economics, performance, and reliability |

### Dataset / Benchmark
No formal dataset or benchmark. The paper uses illustrative examples of multi-phase compiler architectures (sequential and parallel process with shared data structure) to demonstrate the elements-form-rationale model and the utility of application-oriented properties.

### Challenges & Limitations
- The model is conceptual and philosophical; no formal specification language or tool support is provided for expressing or verifying architectural specifications.
- Type-based schemes for characterizing elements are identified as insufficient at the architectural level, but the proposed property-based alternative is not fully formalized.
- The concepts of architectural erosion and drift are introduced but not operationalized with detection methods or metrics.
- The paper acknowledges that software architecture is still in a pre-paradigmatic state, lacking the standard set of named architectural styles found in building architecture.

### Key Quotes
> "Architectural erosion is due to violations of the architecture. These violations often lead to an increase in problems in the system and contribute to the increasing brittleness of a system." (p. 43)

> "Architectural drift is due to insensitivity about the architecture. This insensitivity leads more to inadaptability than to disasters and results in a lack of coherence and clarity of form." (p. 43)

> "The important lesson in reusing components is that the possibilities for reuse are the greatest where specifications for the components are constrained the least -- at the architectural level." (p. 51)

### Key Takeaway
The elements-form-rationale model provides the theoretical basis for defining what an "architectural tactic" modifies: tactics act on architectural **elements** and their **form** (properties and relationships) to satisfy quality-attribute requirements captured in the **rationale**. When the thesis evaluates LLM-generated architectural changes, it should verify that modifications respect the existing form constraints to avoid contributing to architectural erosion or drift.
