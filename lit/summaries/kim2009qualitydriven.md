## Quality-Driven Architecture Development Using Architectural Tactics

| Field | Value |
|-------|-------|
| **Key** | `kim2009qualitydriven` |
| **Authors** | Suntae Kim, Dae-Kyoo Kim, Lunjin Lu, Sooyong Park |
| **Venue** | The Journal of Systems and Software (2009) |
| **Tier** | Q1 (JSS, Elsevier) |
| **Citations** | ~200+ (highly cited in architectural tactics literature) |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** Non-functional requirements (NFRs) are often deferred until late development phases, making it difficult to satisfy them and necessitating costly changes to early artifacts such as architecture and design.
- **Motivation:** Existing approaches either specify NFRs as architectural constraints (checking satisfaction but not providing solutions) or use domain-specific, coarse-grained building blocks (one per quality attribute) that require significant tailoring. There is a lack of systematic techniques for embodying NFRs in the early development phase.
- **Gap:** No prior work provided fine-grained, reusable, formally specified architectural tactics with explicit variability relationships (mandatory, optional, requires, suggested, mutually exclusive) and precise structural/behavioral semantics enabling systematic selection, composition, and automated architecture instantiation.

### Contribution

This paper presents a systematic, quality-driven approach to embodying non-functional requirements (NFRs) into software architecture using architectural tactics. Tactics are represented as feature models to capture their variability and relationships (mandatory, optional, requires, suggested, mutually exclusive), and their structural and behavioral semantics are formally defined using the Role-Based Metamodeling Language (RBML), a UML-based pattern specification notation. The paper provides detailed feature models and RBML specifications for availability, performance, and security tactics, demonstrates tactic composition via binding and composition rules, and validates the approach through a stock trading system case study with tool support (RBML-PI, an IBM Rational Rose add-in) for automatic architecture instantiation.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 5  |   2   |  0  |   0    | 12/25 |

**Relevance:** HIGH

This is a foundational paper for the thesis because it provides the most rigorous formalization of architectural tactics as reusable building blocks with precise semantics. The feature-model-based tactic catalog (with relationships such as requires, suggested, mutually exclusive) directly informs Objective O1 (identifying tactics influencing maintainability). The systematic tactic selection and composition mechanism offers a blueprint that the thesis can adapt for LLM-driven tactic implementation: if an LLM is to implement tactics, it needs to understand what each tactic structurally entails, which is exactly what the RBML specifications provide. While the paper focuses on availability, performance, and security (not maintainability directly), its methodology is transferable to modifiability/maintainability tactics.

### Method & Validation
- **Type:** Framework + Case Study + Tool
- **Validation:** Prototype tool (RBML-PI) + Case study (stock trading system)
- **Evidence:** Two architecture instantiations of a stock trading system generated from composed tactics using the RBML-PI tool, demonstrating that the approach produces valid, NFR-embodying architectures. Composition rules are formally defined for all pairwise tactic combinations across availability, performance, and security.

### Models & Tools
- **LLM/AI models:** N/A
- **Tools/frameworks:** RBML-PI (Role-Based Metamodeling Language Pattern Instantiator), an IBM Rational Rose add-in for automatic architecture instantiation from composed tactic specifications
- **Languages:** UML (modeling); the approach is language-independent at the architecture level, demonstrated via UML class and sequence diagrams

### Key Findings

| Finding | Value/Detail |
|---------|-------------|
| Tactic formalization | Architectural tactics can be rigorously specified using feature models (for variability/relationships) + RBML (for structural/behavioral semantics) |
| Tactic composition | Tactics are composed via explicit binding rules (mapping corresponding roles) and composition rules (merging, packaging, IPS sequencing) |
| Feature model relationships | Tactics exhibit mandatory, optional, requires, suggested, and mutually exclusive relationships; feature models make these explicit for architects |
| Cross-quality-attribute tradeoffs | Security tactics (encryption) can decrease performance; the feature model's cross-attribute relationships capture these tradeoffs |
| Tactic reusability via RBML | Realization multiplicity in RBML roles enables the same tactic to be instantiated in different configurations (e.g., 1 vs. 3 FIFO queues) without redefining the tactic |
| Not all tactics formalizable | Resource demand tactics (Bass et al., 2003) are too abstract to formalize in RBML; manual realization by the architect is still needed |
| Automated tactic selection | Authors note future work on automating tactic selection using metrics and inference systems (e.g., Prolog) to find valid feature configurations satisfying quantified NFRs |
| Availability tactics | Fault Detection (Ping/Echo, Heartbeat, Exception), Recovery Reintroduction (Checkpoint/Rollback, State Resynchronization), Recovery Preparation and Repair (Voting, Active Redundancy, Passive Redundancy) |
| Performance tactics | Resource Arbitration (FIFO, Fixed Priority Scheduling, Dynamic Priority Scheduling), Resource Management (Introduce Concurrency, Maintain Multiple Copies/Cache) |
| Security tactics | Resisting Attacks (Authenticate Users: ID/Password, Onetime Password; Authorize Users; Maintain Data Confidentiality), Recovering from Attacks (Restoration) |

### Key Quotes

> "An architectural tactic is a fine-grained reusable architectural building block that provides an architectural solution built from experience to help to achieve a quality attribute." (p. 2)

> "A tactic is a design decision that influences the concerned quality, and a collection of tactics forms an architectural strategy." (p. 2)

> "Architectural tactics may be viewed as foundational building blocks from which architectural patterns and styles are created." (p. 2)

> "While we assumed in this paper that tactic selection is made by the architect, it is possible to automate tactic selection. One approach which we are currently investigating is using metrics and inference systems." (p. 20)

> "It should be noted that not all tactics can be specified in the RBML. For instance, the resource demand tactics, which are concerned with managing resource demand, are difficult to formalize in the RBML due to the abstract nature of their solutions." (p. 20)

### Challenges & Limitations

1. **Limited quality attribute coverage:** The paper only covers availability, performance, and security tactics. Modifiability, testability, and maintainability tactics are not formalized, which are the most relevant for this thesis.
2. **Manual tactic selection:** Tactic selection is assumed to be performed by the architect based on experience; no automated selection mechanism is provided (only mentioned as future work).
3. **Not all tactics formalizable:** Resource demand tactics and other abstract tactics cannot be specified in RBML, requiring manual realization.
4. **Single case study:** Validation is limited to one case study (stock trading system); no empirical evaluation of architecture quality improvement or metrics-based assessment.
5. **Tool dependency:** RBML-PI is built as an IBM Rational Rose add-in, a now largely discontinued tool, limiting practical reproducibility.
6. **No maintainability focus:** The paper does not address maintainability or modifiability as quality attributes, which are the primary focus of this thesis.
7. **Composition scalability:** Composition rules are defined pairwise; the paper does not discuss scalability of composition when many tactics from multiple quality attributes must be combined simultaneously.

### Dataset / Benchmark
- **Name:** Stock Trading System (STS) case study
- **Size:** 1 hypothetical system with 4 NFRs; 2 architecture instantiations generated
- **Domain:** Financial trading (stock trading system with availability, performance, and security requirements)
- **Availability:** Not publicly available (illustrative case study only)

### Key Takeaway

The feature-model representation of tactic relationships (requires, suggested, mutually exclusive) is directly adoptable for structuring the LLM's tactic selection knowledge base. When building an LLM-driven pipeline to implement architectural tactics, the structured tactic catalog from this paper (extended to maintainability tactics) can serve as the "menu" from which the LLM selects and composes tactics. The RBML structural specifications provide concrete role-based blueprints that can be translated into prompt templates guiding the LLM on what components, interfaces, and interactions each tactic requires.

### Snowball References

**Backward:**
- `bass2003sap` — Bass, Clements, Kazman. *Software Architecture in Practice* (2nd ed., 2003). The definitive source for architectural tactics taxonomy.
- `bachmann2002illuminating` — Bachmann, Bass, Klein. *Illuminating the Fundamental Contributors to Software Architecture Quality* (CMU/SEI-2002-TR-025). SEI technical report foundational to tactic definitions.
- `france2004uml` — France, Kim, Ghosh, Song. *A UML-based pattern specification technique* (IEEE TSE, 2004). Foundational work on the RBML used in this paper.
- `chung1999nfr` — Chung, Nixon, Yu, Mylopoulos. *Non-Functional Requirements in Software Engineering* (Springer, 1999). NFR framework that this paper builds upon.
- `bruin2001scenario` — Bruin, Vliet. *Scenario-based generation and evaluation of software architectures* (2001). Alternative approach using feature-solution graphs and UCMs.

**Forward:** Check Google Scholar for papers citing this, particularly:
- Harrison & Avgeriou (2010) — *How Do Architecture Patterns and Tactics Interact?* (already in inventory as `harrison2010how`)
- Papers extending Kim's tactic formalization to modifiability/maintainability
- Recent (2023-2026) works on automated tactic selection or LLM-based architecture design
