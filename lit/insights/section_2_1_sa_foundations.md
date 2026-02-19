## Topic: Software Architecture Foundations (Section 2.1)

**Papers:** 3 | **Updated:** 2026-02-16

### Summary

The discipline of software architecture emerged in the early 1990s as a response to the growing complexity of software systems, which could no longer be adequately described by algorithms and data structures alone. Perry and Wolf (1992) provided the first formal model, defining software architecture as a triple of **elements** (processing, data, and connecting), **form** (weighted properties and relationships constraining those elements), and **rationale** (the system constraints motivating architectural choices). This model is significant because it established that architecture is not merely a structural description but an intentional design artifact that captures the *why* behind decisions -- rationale explicates satisfaction of non-functional concerns such as economics, performance, and reliability. Perry and Wolf also introduced the concepts of **architectural erosion** (violations of architecture leading to brittleness) and **architectural drift** (insensitivity to architecture leading to inadaptability), both of which remain central to understanding how systems degrade over time.

Garlan and Shaw (1993) complemented this formal model with a practitioner-oriented contribution: the first comprehensive taxonomy of architectural styles. Working within a component-connector-constraint framework, they cataloged seven major styles -- Pipes and Filters, Data Abstraction/Object-Oriented, Event-based Implicit Invocation, Layered Systems, Repositories/Blackboard, Table-Driven Interpreters, and Heterogeneous Architectures -- and systematically characterized their properties, advantages, and disadvantages. Their KWIC case study was particularly influential: by comparing multiple architectural decompositions of the same system across five quality dimensions (algorithm change, data representation change, functional enhancement, performance, reuse), they demonstrated empirically that architectural style choice is the primary determinant of a system's modifiability and maintainability. Crucially, no single style dominated all dimensions, establishing the fundamental trade-off reasoning that pervades architecture design.

Garlan and Perry (1995), writing jointly in an editorial for the IEEE TSE special issue on software architecture, consolidated the field's identity by articulating four key distinctions (focus of concern, nature of representation, instance vs. style, design methods vs. architectures) and five areas of architectural impact (understanding, reuse, evolution, analysis, management). Their "load-bearing walls" metaphor -- that making architectural decisions explicit helps maintainers understand ramifications of changes and estimate modification costs -- directly bridges these foundations to the thesis concern of maintainability improvement. Collectively, these three works established software architecture as a principled discipline with formal vocabulary, taxonomic structure, and clear connections to quality attributes, providing the conceptual substrate on which architectural tactics, quality-driven design, and the thesis itself are built.

### Key Papers

| Paper | Contribution | Relevance |
|-------|--------------|-----------|
| `perry1992foundations` | First formal model of SA: elements, form, rationale; introduced erosion and drift concepts | HIGH -- provides the theoretical basis for defining what architectural tactics modify (elements and form) to satisfy quality requirements (rationale) |
| `garlan1993introduction` | First comprehensive taxonomy of architectural styles with component-connector-constraint framework; KWIC case study demonstrating style-quality trade-offs | HIGH -- establishes canonical vocabulary of styles; KWIC demonstrates that style choice determines maintainability; Pipes-and-Filters style directly relevant to thesis pipeline |
| `garlan1995editorial` | Framed SA as a discipline; four key distinctions, five areas of impact; "load-bearing walls" metaphor | MEDIUM -- consolidates the field's identity; metaphor supports thesis argument that architectural decisions are the primary lever for maintainability improvement |

### Consensus

| Finding | Papers | Confidence |
|---------|--------|------------|
| SA is a distinct design level above algorithms and data structures, requiring its own vocabulary and methods | `perry1992foundations`, `garlan1993introduction`, `garlan1995editorial` | High |
| Architecture is defined in terms of components, connectors, and their relationships/constraints | `perry1992foundations`, `garlan1993introduction` | High |
| Architectural style choice directly impacts quality attributes (modifiability, reusability, performance) | `garlan1993introduction`, `garlan1995editorial` | High |
| Architecture encompasses design intent and rationale, not just structural description | `perry1992foundations`, `garlan1995editorial` | High |
| Real systems are heterogeneous combinations of styles, not pure single-style implementations | `garlan1993introduction`, `perry1992foundations` | High |
| Making architectural decisions explicit supports understanding, evolution, and maintainability | `garlan1995editorial`, `perry1992foundations` | High |
| Connecting elements (connectors) are often overlooked but have profound impact on architecture | `perry1992foundations`, `garlan1993introduction` | Medium |

### Contradictions

| Issue | Position A | Position B | Thesis Choice |
|-------|------------|------------|---------------|
| Formality of SA definition | `perry1992foundations`: Formal triple model (elements, form, rationale) with emphasis on mathematical-style properties and constraints | `garlan1993introduction`: Informal taxonomic approach based on component-connector graphs, characterized through case studies rather than formalization | Adopt both perspectives: use Perry & Wolf's formal model to reason about what tactics modify (elements, form) and why (rationale), while using Garlan & Shaw's style taxonomy to characterize target systems and select appropriate tactics |
| Scope of "architecture" | `perry1992foundations`: Architecture includes rationale (the "why") as a first-class constituent, making it broader than structural description | `garlan1993introduction`: Focuses primarily on structural organization (components, connectors, constraints) with quality trade-offs discussed through empirical comparison | Include rationale as essential: LLM-driven tactic implementation must capture architectural intent, not just perform structural transformations |

### Gaps

| Gap | Impact on Thesis |
|-----|-----------------|
| No formal method for selecting the optimal style for a given quality requirement (Garlan & Shaw acknowledged this) | Thesis pipeline must include a style-aware tactic selection step; the LLM agent must reason about architectural style before choosing tactics |
| Erosion and drift are conceptualized but not operationalized with detection methods or metrics (Perry & Wolf) | Thesis must adopt later operationalizations (Li 2021, Rosik 2011) and define concrete metrics to detect whether LLM changes contribute to erosion |
| No formal notation for architectural description proposed by these foundational works | Thesis relies on informal architectural descriptions (code-level structure) rather than ADLs; the LLM must work with source code representations, not formal architecture models |
| Limited guidance on reasoning about quality attributes in mixed-style (heterogeneous) architectures | Thesis targets real-world systems that combine styles; tactic selection logic must handle heterogeneous architectures, not assume pure single-style systems |
| Rationale is identified as critical but no mechanism exists for extracting rationale from existing codebases | The LLM must infer architectural rationale from code structure and documentation, which introduces uncertainty; thesis should acknowledge this limitation |

### Recommendations

**Adopt:** Perry & Wolf's elements-form-rationale model as the conceptual frame for defining what architectural tactics are: they are constrained design decisions that modify architectural **elements** and their **form** (properties and relationships) to satisfy quality-attribute requirements captured in the **rationale**. This model directly structures the thesis's definition of tactic implementation.

**Adopt:** Garlan & Shaw's component-connector-constraint vocabulary and style taxonomy as the basis for characterizing target systems in the thesis pipeline. The architecture detection filter should identify the dominant style(s) to constrain tactic selection.

**Adapt:** The KWIC-style quality trade-off analysis from Garlan & Shaw, applying it not to style selection but to tactic selection -- different tactics yield different strengths for different maintainability sub-characteristics, and no single tactic dominates all dimensions. The thesis evaluation framework should compare tactic impact across multiple maintainability sub-characteristics (modularity, analysability, modifiability, testability per ISO 25010).

**Adapt:** The erosion/drift concepts from Perry & Wolf into operationalized checks within the thesis pipeline. After LLM-driven tactic implementation, the pipeline should verify that changes do not introduce architectural violations (erosion) or drift from the intended architecture.

**Avoid:** Treating these foundational works as providing prescriptive guidance for tool implementation -- they are conceptual frameworks, not engineering methodologies. The thesis must bridge from these conceptual foundations to concrete, automated transformation through the later works on quality-driven design (Kim 2009), tactic catalogs (Harrison 2010, Bi 2021), and LLM-based refactoring (DePalma 2024, Liu 2025).

### Related Work Draft

> Software architecture emerged as a distinct discipline in the early 1990s when researchers recognized that the growing size and complexity of software systems demanded a level of design reasoning above algorithms and data structures. Perry and Wolf \cite{perry1992foundations} proposed the first formal model, defining software architecture as a combination of **elements** (processing, data, and connecting), their **form** (weighted properties and relationships constraining element choice and placement), and **rationale** (the system constraints motivating architectural decisions). This tripartite model is significant because it established architecture as an intentional design artifact that captures not only structural organization but also the reasoning behind design choices. Perry and Wolf further introduced the concepts of **architectural erosion** -- violations of architecture leading to increased brittleness -- and **architectural drift** -- insensitivity to architecture leading to inadaptability -- providing a vocabulary for reasoning about how systems degrade over time. Garlan and Shaw \cite{garlan1993introduction} complemented this formal model with the first comprehensive taxonomy of architectural styles, defining each in terms of components, connectors, and constraints. Through detailed case studies -- most notably the KWIC comparison, which evaluated multiple architectural decompositions across five quality dimensions -- they demonstrated that the choice of architectural style directly determines a system's modifiability, reusability, and performance characteristics. No single style dominated all dimensions, establishing the fundamental trade-off reasoning that underpins quality-driven architecture design. Garlan and Perry \cite{garlan1995editorial} subsequently consolidated the field by articulating key distinctions and identifying five areas where architecture impacts software development: understanding, reuse, evolution, analysis, and management. Their observation that making architectural decisions explicit reveals the "load-bearing walls" of a system -- enabling maintainers to understand ramifications of changes and estimate modification costs -- directly motivates the thesis's focus on architectural tactics as the primary mechanism through which architecture influences maintainability. Together, these foundational works provide the conceptual vocabulary (elements, form, rationale, style, erosion, drift) and the quality-attribute reasoning framework that the thesis builds upon when defining, selecting, and evaluating architectural tactics for automated maintainability improvement.
