## ArchTacRV: Detecting and Runtime Verifying Architectural Tactics in Code

| Field | Value |
|-------|-------|
| **Key** | `ge2022archtacrv` |
| **Authors** | Ning Ge, Zewu Wang, Li Zhang, Jiuang Zhao, Yufei Zhou, Zewei Liu |
| **Venue** | SANER 2022 (IEEE) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Architectural tactics degrade over time as code evolves, but existing systems provide limited support for checking consistency between a tactic specification and its implementation.
- **Gap:** No automated method existed to both detect tactic behavioral methods in code and verify their runtime behavioral consistency against RBML specifications.

### Contribution
Presents a two-phase approach: (1) a machine learning-based method to detect behavioral methods of tactic structures in code, and (2) a runtime verification (RV) method for checking behavioral consistency between RBML tactic specifications and implementations. Implements the ArchTacRV prototype tool.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 4  |   2   |  0  |   3    | 14/25 |

**Relevance:** HIGH

This is the closest work to the thesis in terms of automated tactic detection. It detects tactics but does not implement them — the thesis fills the gap of automated tactic *implementation* using LLMs.

### Method & Validation
- **Type:** Tool + Experiment
- **Validation:** ML model comparison + case studies on open-source projects

### Models & Tools
- **LLM/AI models:** 5 ML models compared for tactic behavioral method detection (not LLMs)
- **Tools:** ArchTacRV prototype tool, RBML specifications (Kim et al.'s formalization)
- **Languages:** Java (open-source projects)

### Dataset / Benchmark
- **Name:** Custom dataset from open-source projects
- **Size:** 74 open-source projects, 10 types of architectural tactics
- **Domain:** Open-source Java projects
- **Availability:** Not specified

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| ML models compared | 5 models for behavioral method detection |
| Tactics covered | 10 types across 74 projects |
| Validation approach | Per-tactic case study on selected projects |
| Tool | ArchTacRV prototype for detection + RV |

### Challenges & Limitations
- IEEE paywalled — full paper not accessible for detailed analysis
- Based on abstract: approach is detection/verification only, not generation/implementation
- Relies on RBML structural specifications which require manual authoring
- Runtime verification requires instrumented execution

### Key Quotes
> "With the evolution of code, the designed architectural tactics might be degraded over time." (Abstract)

### Key Takeaway
ArchTacRV's tactic detection pipeline (ML on code structure → RBML matching) could serve as the *verification* component in the thesis pipeline — after LLM implements a tactic, ArchTacRV-style verification could confirm correct implementation.

### Snowball References
**Backward:** `kim2009qualitydriven` (RBML tactic specifications)
**Forward:** Limited citations; primarily extended by same research group
