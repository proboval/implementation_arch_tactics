## An Empirical Study on the Code Refactoring Capability of Large Language Models

| Field | Value |
|-------|-------|
| **Key** | `cordeiro2024llm` |
| **Authors** | Cordeiro, Noei, Zou |
| **Venue** | arXiv preprint / ACM submission (2024) |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** LLMs are increasingly used for code generation, but there is no systematic empirical study comparing LLM-generated refactorings against developer-performed refactorings in terms of code quality improvement (code smell reduction and code metrics).
- **Gap:** Prior work evaluated LLM refactoring in isolation or on synthetic benchmarks; this study fills the gap by comparing LLM vs. developer refactorings on the same code commits in real open-source projects, controlling for data leakage.

### Contribution
This paper conducts a large-scale empirical study comparing StarCoder2-15B refactoring capabilities against human developers across 30 open-source Java projects (5,194 commits, 39,309 files). It evaluates code smell reduction, code quality metrics (coupling, cohesion, complexity, modularity), unit test pass rates, and the impact of prompt engineering (zero-shot, one-shot, chain-of-thought) on refactoring quality. The study provides an evaluation framework and replication package for assessing LLM refactoring effectiveness.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 2  |   4   |  5  |   4    | 16/25 |

**Relevance:** HIGH

This paper directly informs the thesis by demonstrating that LLMs can reduce code smells and improve maintainability metrics (cohesion, complexity, modularity) more effectively than developers for systematic/repetitive issues, but struggle with architectural-level changes (modularization, encapsulation, cross-class refactorings). This distinction between implementation-level and design-level refactoring is critical for understanding where LLM-driven architectural tactic implementation will succeed vs. require human oversight.

### Method & Validation
- **Type:** Empirical study (controlled comparison experiment)
- **Validation:** Quantitative comparison using Mann-Whitney U-test, Cliff's delta effect sizes, Scott-Knott clustering; unit test pass rates via EvoSuite-generated tests; code smell detection via DesigniteJava; code metrics via Understand static analysis tool; refactoring detection via RMiner 3.0

### Models & Tools
- **LLM/AI models:** StarCoder2-15B-Instruct-v0.1 (open-source, training data known to avoid data leakage)
- **Tools:** DesigniteJava 2.5.2 (code smell detection, 46 smell types), Understand (static analysis, code metrics), RMiner 3.0 (refactoring detection, 102 types, 99.8% precision), EvoSuite (automated unit test generation)
- **Languages:** Java

### Dataset / Benchmark
20-MAD dataset (765 Apache projects); filtered to 30 Java projects not in StarCoder2 training set (The Stack v2); 5,194 pure-refactoring commits with 39,309 files; publicly available replication package at GitHub (SEAL Lab).

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| LLM code smell reduction rate | 44.36% (vs. 24.27% for developers); 20.1% higher |
| Unit test pass rate (Pass@1) | 28.36% (developers: 100%) |
| Unit test pass rate (Pass@5) | 57.15% (best of 5 generations) |
| LLM strengths (smell types) | Implementation smells: Long Statement, Magic Number, Empty Catch Clause, Long Parameter List, Long Identifier, Complex Conditional, Complex Method |
| Developer strengths (smell types) | Design smells: Broken Modularization, Deficient Encapsulation, Multifaceted Abstraction, Insufficient Modularization |
| LLM refactoring type strengths | Syntactic, rule-based: Rename Method, Extract Method, annotation changes, access modifier changes |
| Developer refactoring type strengths | Complex structural: Move Method, Extract Superclass, Pull Up Method, Move Source Folder |
| Avg code metrics improvement (LLM) | 19.32% across all metrics (vs. 17.46% for developers) |
| Complexity reduction (LLM) | AvgCyclomatic: 17.4%, SumCyclomatic: 18.6% (medium effect size, delta=0.47) |
| Coupling reduction (Developer) | CountClassCoupled: 24.1% (developers outperform LLM) |
| One-shot prompting improvement | Unit test pass rate: 34.51% (+6.15% over zero-shot); SRR: 42.97% (+3.52%) |
| Chain-of-thought prompting | Adds 7 new refactoring types (Extract Method, Rename Method, Extract Variable, Inline Method, Add Parameter, Extract Class, Parameterize Variable) |
| Multiple generations benefit | Pass@5 yields 28.8% higher unit test pass rate than Pass@1 |
| Statistical significance | p-value=0.003 for smell reduction difference (U-test) |

### Challenges & Limitations
- **Low functional correctness:** StarCoder2 achieves only 28.36% Pass@1 (57.15% Pass@5), meaning most single-attempt refactorings break functionality.
- **Architecture-level refactoring weakness:** LLMs fail at cross-class, dependency-aware refactorings (modularization, encapsulation) that require understanding of broader system architecture.
- **Hallucination risk:** LLM-generated code may appear correct but be logically/syntactically invalid.
- **Single-commit scope:** Study analyzes refactorings within individual commits; multi-commit refactoring campaigns are not captured.
- **Java only:** Results may not generalize to other languages.
- **Single LLM tested:** Only StarCoder2-15B; GPT-4, Claude, or other models may perform differently.
- **Quality metrics limitations:** Code smell reduction and metrics may not capture all quality dimensions (readability, performance).

### Key Quotes
> "StarCoder2 excels in reducing more types of code smells, such as Long Statement, Magic Number, Empty Catch Clause, and Long Identifier. Developers perform better in fixing complex issues, such as Broken Modularization, Deficient Encapsulation, and Multifaceted Abstraction." (Abstract)

> "Developers surpass in refactorings that require a deeper understanding of code context and architecture." (Abstract)

> "StarCoder2 outperforms developers across most evaluated code metrics, achieving an average reduction across all metrics of 19.32% compared to 17.46% for developers, demonstrating its strength in automating complex code quality improvements." (Section 3.1, RQ1 Summary)

### Key Takeaway
LLMs excel at systematic, pattern-based code improvements (implementation smells, complexity reduction, cohesion improvement) but fundamentally struggle with architecture-level changes requiring cross-class reasoning. For the thesis, this means LLM-driven architectural tactic implementation will likely need a hybrid approach: use LLMs for within-class transformations (simplifying methods, improving encapsulation patterns, reducing complexity) while providing explicit architectural context (e.g., via chain-of-thought or one-shot prompts with architectural examples) for cross-component changes like modularization tactics. Multiple generation attempts (Pass@5) with test validation significantly improve quality, suggesting the thesis pipeline should incorporate iterative generation with automated testing gates.
