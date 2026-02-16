## Ensuring Software Maintainability at Software Architecture Level Using Architectural Patterns

| Field | Value |
|-------|-------|
| **Key** | `rahmati2021ensuring` |
| **Authors** | Zahed Rahmati, Mohammad Tanhaei |
| **Venue** | AUT Journal of Mathematics and Computing, 2(1), 81-102 (2021) |
| **Tier** | Q2 (university journal, peer-reviewed) |
| **Citations** | ~15 (estimated) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** The maintenance phase of software development is extremely costly, yet there is no systematic framework linking standard architectural patterns to specific maintainability sub-attributes to guide architecture-level refactoring decisions.
- **Motivation:** Maintainability can be addressed at code, design, or architecture levels. Architecture-level improvements have the broadest impact (coarse-grained, affecting many components) and can be performed without system implementation, reducing project risk. However, existing quality models do not provide actionable mappings between architectural patterns and measurable maintainability factors.
- **Gap:** Prior work lacked a unified quality model decomposing maintainability into measurable sub-attributes (analyzability, changeability, stability, testability, understandability, portability) with concrete factors, and no study had systematically evaluated standard architectural patterns against these sub-attributes using a visual comparison framework (radar diagrams) validated with real-world refactoring case studies.

### Contribution
The paper develops a hierarchical quality model for maintainability at the software architecture level, decomposing maintainability into six sub-attributes (analyzability, changeability, stability, testability, understandability, portability) and defining measurable factors for each. Using this model, the authors evaluate seven standard architectural patterns (Multi-Layered, Pipe & Filter, Batch Sequential, Blackboard, Object-Oriented, Interpreter, Virtual Machine, Broker, MVC) via "maintainability hexagon radar" diagrams that score each pattern on a 0-4 scale per sub-attribute. Two real-world architecture-level refactoring case studies (one successful, one unsuccessful) validate the model and demonstrate that appropriate pattern selection can yield 50-64% maintenance effort reduction, while inappropriate refactoring can worsen maintainability.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 4  | 5  |   5   |  0  |   1    | 15/25 |

**Relevance:** HIGH

This paper provides a structured mapping between architectural patterns and maintainability sub-attributes that directly supports thesis Objectives O1 (identifying tactics that influence maintainability) and O3/O4 (evaluating maintainability impact of architectural changes). The maintainability quality model and radar diagrams can inform tactic selection logic in the LLM-driven pipeline. The case studies provide empirical evidence that architecture-level refactoring improves maintainability -- but also that pattern adoption alone is insufficient without proper implementation at lower levels.

### Method & Validation
- **Type:** Framework + Case Study
- **Validation:** Two real-world case studies with before/after man-hour comparison across multiple maintenance scenarios
- **Evidence:** Quantitative comparison of person-hours needed for maintenance scenarios in old vs. new architectures. First case study (Proxy to MVC refactoring) showed 50-64% average improvement. Second case study (unstructured PHP to MVC) showed 10% degradation on average, demonstrating that pattern adoption does not guarantee improvement.

### Models & Tools
- **LLM/AI models:** N/A
- **Tools/frameworks:** Yii Framework (PHP MVC framework, used in Case Study 2 for architecture refactoring); maintainability hexagon radar diagrams (custom visual assessment tool); quality models compared include McCall, Boehm, ISO/IEC 9126
- **Languages:** Visual Basic (Case Study 1: rms.ilam.ac.ir), PHP (Case Study 2: chavir.ir with Yii Framework)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Maintainability sub-attributes | Six: analyzability, changeability, stability, testability, understandability, portability |
| Factors per sub-attribute | Testability: 5 factors (operability, controllability, decomposability, simplicity, self-descriptiveness); Changeability: 3 (localized modification, reduced coupling, deferred binding time); Analyzability: 5 (simplicity, self-descriptiveness, decomposability, formality, traceability); Stability: 2 (feature-based decomposition, architectural runway); Understandability: 3 (standardization, documentation, self-descriptiveness); Portability: 2 (machine independence, software system independence) |
| Best pattern for maintainability | Multi-Layered and Broker patterns score highest overall across maintainability sub-attributes |
| Worst pattern for maintainability | Blackboard pattern scores lowest (high changeability but very low testability, understandability, analyzability) |
| MVC refactoring benefit | 50-64% average effort reduction across maintenance scenarios (Case Study 1: Proxy -> MVC) |
| MVC refactoring failure | ~10% effort increase when applied to already-simple system (Case Study 2: flat PHP -> MVC) |
| Architecture as preventive, not preserving | Patterns prevent maintainability problems at the architecture level but cannot guarantee maintainability is not violated at lower levels |
| Hexagon radar scale | 0 = large reduction, 1 = relative reduction, 2 = neutral, 3 = relative increase, 4 = large increase |
| Multi-Layered radar scores | Testability: 4, Changeability: 4, Understandability: 2, Portability: 4, Stability: 3, Analyzability: 3 |
| Pipe & Filter radar scores | Testability: 1, Changeability: 4, Understandability: 0, Portability: 3, Stability: 2, Analyzability: 0 |
| Broker radar scores | Testability: 4, Changeability: 4, Understandability: 2, Portability: 3, Stability: 2, Analyzability: 4 |
| MVC radar scores | Testability: 4, Changeability: 4, Understandability: 3, Portability: 4, Stability: 2, Analyzability: 3 |

### Key Quotes
> "Although the use of a particular architectural pattern cannot have a preserving effect on software maintainability, the mere conformance of a system to any architecture cannot guarantee the system's high maintainability." (p. 81)

> "Architecturally sensitive maintainability patterns refer to a series of patterns, which need changes at the architecture level for their implementation. In other words, implementing these kinds of patterns is difficult or even impossible without modifying software architecture." (p. 87)

> "It should be noted that architecture patterns are preventing rather than preserving in maintainability aspects." (p. 87)

> "Maintainability patterns together with correct decisions at lower levels may lead to a maintainable software." (p. 99)

> "The average improvement achieved during performing is at least 50 percent. This improvement has increased by 12 and 14 percent, respectively, in the next months owing to the reduction of time needed for understanding and changing the code." (p. 97)

### Challenges & Limitations
- **Subjective scoring:** The radar diagram values are based on qualitative expert assessment, not empirical measurement; the authors acknowledge "the value for some of the factors is fuzzy and subjective" (p. 86).
- **Uncontrolled experiments:** The case studies are real-world experiences, not controlled experiments. The authors acknowledge "perhaps some other factors have affected results as well" (p. 97).
- **Limited case studies:** Only two case studies are presented, both involving migration to MVC, limiting generalizability to other pattern transitions.
- **No formal metrics:** The quality model defines factors but does not provide concrete measurement procedures or tool-based metric computation.
- **No cost estimation model:** The authors identify estimating refactoring cost as open future work -- there is no guidance on when architecture-level refactoring is economically justified.
- **Architecture detection assumed:** The refactoring framework assumes the current architectural pattern is known, but the paper does not address automated architecture detection.

### Dataset / Benchmark
- **Name:** Two real-world case studies (rms.ilam.ac.ir and chavir.ir)
- **Size:** Case Study 1: university research management system (~15 years old, Visual Basic, Proxy-to-MVC refactoring, 3 maintenance scenarios); Case Study 2: commercial CMS (PHP, 17 files refactored into 17 controllers + 76 views + 40 models, 4 maintenance scenarios)
- **Domain:** University research management (Case Study 1); commercial content management (Case Study 2)
- **Availability:** Not publicly available (proprietary systems); no static analysis metrics used, only manual person-hour effort tracking

### Key Takeaway
The maintainability hexagon radar model and pattern-to-sub-attribute mapping provide a structured decision framework for selecting which architectural pattern to refactor toward. For the thesis pipeline, this model can inform the tactic selection agent: when the LLM detects a current architecture pattern, it can consult radar diagrams to predict which refactoring target pattern will most improve the specific maintainability sub-attributes that are deficient. Critically, the failed case study warns that architecture-level refactoring is not universally beneficial -- it must be matched to the system's complexity and the team's familiarity with the target pattern.

### Snowball References
**Backward:** `bass2003software` (Bass, Clements, Kazman -- Software Architecture in Practice, foundational reference for architecture-quality linkage), `bengtsson2004alma` (Architecture-Level Modifiability Analysis -- ALMA method), `hegedus2012myth` (effect of design patterns on maintainability), `heitlager2007practical` (practical model for measuring maintainability -- ISO 9126 metrics at code level), `hoffman2001architectural` (architectural patterns and maintainability case study), `prechelt2001controlled` (controlled experiment: design patterns vs. simpler solutions for maintenance), `liu2013maintainability` (maintainability metrics based on symbol connectors at architecture level), `bachmann2012tactics` (architectural tactics to support rapid and agile stability)
**Forward:** Check Google Scholar for papers citing this (DOI: 10.22060/ajmc.2021.19232.1044)
