## An Introduction to Software Architecture

| Field | Value |
|-------|-------|
| **Key** | `garlan1993introduction` |
| **Authors** | David Garlan, Mary Shaw |
| **Venue** | Advances in Software Engineering and Knowledge Engineering, Vol. I, World Scientific (1993); also CMU-CS-94-166 and CMU/SEI-94-TR-21 |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** As software systems grow in size and complexity, design decisions at the architectural level become critical, yet in the early 1990s there was no systematic vocabulary or framework for reasoning about software architecture as a distinct design level above algorithms and data structures.
- **Gap:** No comprehensive taxonomy of architectural styles existed that systematically characterized each style in terms of components, connectors, and constraints, nor demonstrated how style choice directly impacts quality attributes like modifiability, reusability, and performance.

### Contribution
Garlan and Shaw provide the first comprehensive taxonomy of common software architectural styles, defining each in terms of **components**, **connectors**, and **constraints**. They catalog seven major styles -- Pipes and Filters, Data Abstraction / Object-Oriented, Event-based Implicit Invocation, Layered Systems, Repositories / Blackboard, Table-Driven Interpreters, and Heterogeneous Architectures -- and systematically characterize the properties, advantages, and disadvantages of each. Through six detailed case studies (KWIC, oscilloscope instrumentation, compilers, PROVOX process control, rule-based systems, and Hearsay-II), they demonstrate how the choice of architectural style directly impacts modifiability, reusability, performance, and functional extensibility, and how real systems often combine multiple styles in heterogeneous designs.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 5  |   3   |  0  |   0    | 10/25 |

**Relevance:** HIGH

This paper establishes the canonical vocabulary of architectural styles that the thesis relies upon in Section 2.1 (Software Architecture Foundations). The Pipes-and-Filters style described here is directly relevant to the thesis pipeline implementation. More importantly, the KWIC case study provides an early demonstration that architectural style choice determines a system's modifiability and maintainability -- the same quality attributes the thesis seeks to improve via automated tactic implementation. The component-connector-constraint framework also provides the structural vocabulary needed to describe where architectural tactics operate.

### Method & Validation
- **Type:** Survey / Taxonomy with illustrative case studies
- **Validation:** Six detailed case studies comparing architectural decompositions; KWIC comparison table evaluating styles across five design dimensions (algorithm change, data representation change, functional enhancement, performance, reuse)

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** N/A (conceptual taxonomy with manual case study analysis)
- **Languages:** N/A (language-independent architectural analysis; examples include KWIC index system, oscilloscope instrumentation, compilers)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Architecture definition | A collection of computational **components** together with **connectors** describing their interactions, composed into a graph with topological **constraints** |
| Seven canonical styles | Pipes & Filters, Data Abstraction/OO, Event-based Implicit Invocation, Layered, Repository/Blackboard, Interpreter, and heterogeneous combinations |
| Pipes & Filters properties | Independent filters, no shared state, incremental processing; supports reuse, maintainability (new filters added, old replaced), concurrent execution; poor for interactive systems |
| Layered systems properties | Support design by abstraction levels, enhancement (changes affect at most two layers), and reuse via standard interfaces; not all systems naturally layer; performance may require violating layer boundaries |
| Implicit invocation properties | Strong reuse support (register for events), eases evolution (components replaced without interface changes); loss of control over processing order, difficulties with data exchange and correctness reasoning |
| KWIC comparison | Pipe & Filter best for algorithm change, functional enhancement, and reuse; ADT best for data representation change and performance; no single style dominates all dimensions |
| Heterogeneous architectures | Real systems combine styles via hierarchy (components use different internal styles), mixed connectors, or multi-level elaboration |
| Style choice impacts quality | Different architectural styles yield different strengths for modifiability, reusability, performance, and extensibility -- choice must be driven by quality requirements |
| Architecture as design level | Software architecture is a distinct design level above algorithms and data structures, emerging as systems grow in size and complexity |
| Future research directions | Better taxonomies, formal models, notations, tools for architectural design, techniques for extracting architecture from code, and understanding architecture's role in the lifecycle |

### Dataset / Benchmark
No formal dataset or benchmark. The paper uses six illustrative case studies (KWIC index system, oscilloscope instrumentation, compilers, PROVOX process control, rule-based systems, and Hearsay-II speech understanding) drawn from the existing literature and teaching practice to compare architectural styles.

### Challenges & Limitations
- The taxonomy is descriptive rather than prescriptive -- it does not provide formal methods for selecting the optimal style for a given quality requirement.
- The KWIC comparison, while influential, evaluates styles across only five dimensions and does not quantify trade-offs.
- Real systems are heterogeneous combinations of styles, but the paper provides limited guidance on how to reason about quality attributes in mixed-style architectures.
- No formal notation for architectural description is proposed; the authors identify this as a key area for future research.
- The paper acknowledges that better taxonomies, formal models, notations, and tools for architectural design remain open problems.

### Key Quotes
> "As the size of software systems increases, the algorithms and data structures of the computation no longer constitute the major design problems. When systems are constructed from many components, the organization of the overall system -- the software architecture -- presents a new set of design problems." (p. 1)

> "Different architectural styles yield different strengths for modifiability, reusability, performance, and extensibility -- choice must be driven by quality requirements." (p. 15, KWIC case study discussion)

### Key Takeaway
The systematic comparison of architectural styles against quality-attribute dimensions (modifiability, reusability, performance, extensibility) in the KWIC case study is an early precursor to quality-driven architecture design. For the thesis, this reinforces that architectural decisions are the primary determinants of maintainability, and that automated tactic implementation must reason about the target system's architectural style to select appropriate transformations -- a Pipes-and-Filters system and a Layered system require fundamentally different tactics to achieve the same quality improvement.
