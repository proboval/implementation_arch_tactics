## MANTRA: Enhancing Automated Method-Level Refactoring with Contextual RAG and Multi-Agent LLM Collaboration

| Field | Value |
|-------|-------|
| **Key** | `xu2025mantra` |
| **Authors** | Yisen Xu, Feng Lin, Jinqiu Yang, Tse-Hsun (Peter) Chen, Nikolaos Tsantalis |
| **Venue** | ACM Conference (2025) — preprint arXiv:2503.13400 |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Code refactoring remains labor-intensive, requiring developers to carefully analyze existing codebases and prevent the introduction of new defects. Existing LLM-based refactoring solutions are constrained in scope, focus on limited refactoring types, and lack mechanisms to guarantee code compilability and successful test execution.
- **Gap:** Prior LLM refactoring techniques primarily rely on simple prompt-based generation, neglect compound or repository-level transformations, and fail to ensure that the refactored code compiles and passes all tests. They have not fully utilized the self-reflection and self-improvement capabilities of LLMs, resulting in limited effectiveness that has yet to match human-level proficiency.

### Contribution
MANTRA is a multi-agent LLM framework for automated method-level code refactoring that integrates Context-Aware RAG, coordinated Developer/Reviewer/Repair agents, and Verbal Reinforcement Learning (Reflexion). It achieves an 82.8% success rate (582/703) in generating compilable, test-passing refactored Java code across six refactoring types, vastly outperforming a baseline single-prompt LLM (8.7%) and IntelliJ's EM-Assist by 50% on Extract Method. A user study with 37 developers found MANTRA-generated code comparable to human-written code in readability and reusability.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 2  | 2  |   4   |  5  |   3    | 16/25 |

**Relevance:** HIGH

MANTRA directly validates the feasibility of multi-agent LLM pipelines for automated code transformation with quality verification -- the same paradigm the thesis uses. Its three-agent architecture (Developer, Reviewer, Repair) with compilation/test feedback loops provides a reusable blueprint. The ablation study quantifies the contribution of each component (RAG, Reviewer, Repair Agent), offering design guidance for the thesis pipeline. However, MANTRA focuses on method-level refactoring (Extract/Move/Inline Method) rather than architectural tactics, so relevance to AT and SA is moderate.

### Method & Validation
- **Type:** Framework / Tool / Experiment
- **Validation:** Empirical evaluation on 703 pure refactorings from 10 open-source Java projects, comparison against RawGPT baseline and EM-Assist (IntelliJ), user study with 37 developers, ablation study
- **LLM used:** GPT-4o-mini (primary), GPT-3.5-turbo (for EM-Assist comparison)
- **Framework:** LangGraph 0.2.22, RefactoringMiner, CheckStyle, Eclipse JDT

### Models & Tools
- **LLM/AI models:** GPT-4o-mini (primary model for all experiments), GPT-3.5-turbo (for EM-Assist comparison); all-MiniLM-L6-v2 (embedding model for RAG dense retrieval)
- **Tools:** LangGraph 0.2.22 (multi-agent orchestration), RefactoringMiner (refactoring detection/verification, 99% precision/94% recall), PurityChecker (pure refactoring filtering, 95% precision/88% recall), CheckStyle (code style verification), Eclipse JDT (static analysis), Jacoco (code coverage), BM25 (sparse retrieval), Reciprocal Rank Fusion (RRF, result merging)
- **Languages:** Java

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| MANTRA success rate (compile + test + RM verified) | 82.8% (582/703) vs. RawGPT 8.7% (61/703) |
| MANTRA vs. EM-Assist on Extract Method | 77.1% (277/359) vs. 51.5% (185/359) -- 50% improvement |
| CodeBLEU similarity to human code | MANTRA 0.640 vs. RawGPT 0.517 |
| AST Diff Precision / Recall | MANTRA 0.781/0.635 vs. RawGPT 0.773/0.574 |
| Identical to developer refactoring | MANTRA 18% (105/582) vs. RawGPT 13.1% (8/61) |
| User study: readability (MANTRA vs. human) | 4.15 vs. 4.02 (no statistically significant difference) |
| User study: reusability (MANTRA vs. human) | 4.13 vs. 3.97 (no statistically significant difference) |
| Ablation: removing Reviewer Agent | Largest drop -- success from 582 to 222 (61.9% decrease) |
| Ablation: removing Repair Agent | Success from 582 to 287 (50.7% decrease) |
| Ablation: removing RAG | Success from 582 to 345 (40.7% decrease) |
| Cost per refactoring | < $0.10, < 1 minute per generation |
| Refactoring types covered | Extract Method, Move Method, Inline Method + 3 compound types |

### Dataset / Benchmark
703 pure refactoring instances from 10 open-source Java projects (checkstyle, pmd, commons-lang, hibernate-search, junit4, commons-io, javaparser, junit5, hibernate-orm, mockito; 59,615 total GitHub stars, 121,282 total commits). Derived from the Refactoring Oracle Dataset (12,526 refactorings from 547 commits across 188 projects, 2011-2021), filtered via PurityChecker to retain only pure refactoring commits with test coverage. Six refactoring types: Extract Method, Move Method, Inline Method, and three compound types. Data and code publicly available.

### Challenges & Limitations
- **Method-level only:** MANTRA focuses on method-level refactorings; class-level or architectural refactorings are not supported.
- **Java only:** Results may not generalize to other programming languages.
- **LLM dependency:** Only GPT-4o-mini and GPT-3.5-turbo were tested; performance with other LLMs (Claude, open-source models) is unknown.
- **Generative variability:** Due to the generative nature of LLMs, responses may vary across runs and model versions (temperature set to 0 to reduce variability).
- **Move to new classes:** Cannot predict newly created classes during Move Method, limiting applicability when methods are moved to classes that do not yet exist.
- **Human evaluation scale:** User study limited to 37 participants and 12 refactoring samples.

### Key Quotes
> "Among the three components, removing the Reviewer Agent has the most impact on the number of generated refactored that pass compilation/test (decrease from 636 to 359) and the number of successful refactoring (decrease from 582 to 222)." (Section 4, RQ4)

> "Our finding also shows a promising direction in combining traditional software engineering tools to guide LLMs in producing better results." (Section 4, RQ4)

### Key Takeaway
The Reviewer Agent -- which leverages traditional SE tools (RefactoringMiner, CheckStyle) to provide structured feedback to the LLM -- is the most critical component (61.9% drop without it). This strongly supports the thesis design of integrating static analysis verification into the LLM pipeline as a feedback loop rather than relying on the LLM alone. The thesis should adopt a similar multi-agent pattern with a dedicated verification agent that uses external tools (e.g., Radon, architectural constraint checkers) to validate LLM-generated architectural tactic implementations.
