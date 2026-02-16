## A Study of Maintainability in Evolving Open-Source Software

| Field | Value |
|-------|-------|
| **Key** | `molnar2020study` |
| **Authors** | Arthur-Jozsef Molnar, Simona Motogna |
| **Venue** | Preprint / arXiv (2020); extends work published at ENASE 2020 |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** Maintenance effort is costly, especially for large-scale applications, yet maintainability is often only addressed late in the development lifecycle when technical debt has already accumulated. Existing research relating software metrics to maintainability is typically limited to single metrics and singular applications, lacking comprehensive cross-application longitudinal evaluations with multiple models.
- **Gap:** No prior study had compared multiple quantitative maintainability models (MI, ARiSA, SQALE) across the entire development history of multiple complex open-source applications, nor examined how these models behave at different granularity levels (system vs. package vs. class) over long-term evolution.

### Contribution
Longitudinal empirical study of maintainability across 111 releases of three Java open-source applications (FreeMind, jEdit, TuxGuitar), spanning 10+ years of development each. The study compares three quantitative maintainability models of varying complexity -- the Maintainability Index (MI), the ARiSA Compendium model, and the SQALE technical debt model (via SonarQube) -- evaluating their strengths, weaknesses, and agreement when applied to real evolving software. Provides evidence on what drives maintainability changes across versions and how maintenance effort distributes at the package level.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 2  |   5   |  0  |   4    | 12/25 |

**Relevance:** HIGH

This paper directly supports thesis Objectives O3 and O4 (evaluating and comparing maintainability before/after code changes). It provides empirical grounding for choosing maintainability measurement models and demonstrates how SQALE/SonarQube technical debt ratios behave in practice over long-term software evolution. The finding that SQALE is the most reliable system-level maintainability model, while MI is useful at method/class granularity, directly informs the thesis evaluation framework. The evidence that maintainability is not correlated with system size validates using metric-based comparison for before/after LLM transformation assessment.

### Method & Validation
- **Type:** Longitudinal empirical case study
- **Validation:** Cross-application comparison across 3 Java applications (111 releases total), manual source code examination to contextualize quantitative findings, Spearman rank correlation analysis, open-sourced replication data

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** SonarQube 8.2 (SQALE/technical debt), VizzMaintenance Eclipse plugin (ARiSA model, class-level OO metrics), Metrics Reloaded IntelliJ plugin (MI components: statement count, Halstead volume, cyclomatic complexity)
- **Languages:** Java

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Maintainability independence from size | MI and ARiSA are confounded by software size; SQALE (technical debt ratio) is not directly influenced by size-related metrics |
| Best system-level model | SQALE/SonarQube technical debt ratio is the most accurate and practical system-level maintainability measure among the three studied |
| MI utility at fine granularity | MI correlates with SQALE at class level (Spearman rho ~ -0.6), making it useful for quick method/class-level complexity screening |
| ARiSA model limitation | Class-level scores masked by aggregation; small low-complexity classes dilute system-level values, making cross-version/cross-application comparison unreliable |
| Mature versions stabilize | Mature application versions no longer introduce significant quality issues, explained by matured architecture and experienced contributors |
| Milestone versions cause spikes | Major feature additions (e.g., FreeMind 0.8.0, jEdit 4.0pre4) cause maintainability drops; deliberate refactoring (TuxGuitar 1.0rc1) can couple new features with debt reduction |
| Maintenance effort concentration | Most maintainability issues are concentrated in a small subset of packages (e.g., 6 packages in jEdit account for ~80% of maintenance effort) |
| SQALE rating thresholds | Most studied versions received an A rating (TDR < 5%); only FreeMind 0.8.0 and 0.8.1 earned a B rating |
| Generated code impact | In FreeMind, auto-generated code in a single package was the main driver of the severe maintainability decrease |

### Dataset / Benchmark
Three Java open-source GUI applications from public repositories: FreeMind (38 releases, mind-mapping tool), jEdit (45 releases, text editor), TuxGuitar (28 releases, tablature editor) -- 111 releases total spanning 10+ years each. Full metric data openly available on FigShare (doi:10.6084/m9.figshare.12901331.v1).

### Challenges & Limitations
- **External validity:** Limited to GUI-driven Java applications; conclusions may not generalize to other programming languages, mobile, or distributed systems.
- **ARiSA aggregation problem:** Class-level scores are masked by aggregation -- small low-complexity classes dilute system-level values, making cross-version and cross-application comparison unreliable.
- **MI limitations:** Defined for modular/procedural languages; does not account for OO features (inheritance, coupling, cohesion) that significantly affect maintainability.
- **Generated code confound:** Auto-generated code (e.g., FreeMind's generated.instance.impl package) can dominate maintainability measurements, requiring manual identification and contextualization.
- **Single-language study:** Java-only selection limits applicability to multi-language or Python-based projects.

### Key Quotes
> "We confirmed our initial findings regarding the independence of maintainability effort from software size." (Section 6, Conclusion)

> "Mature application versions no longer introduced significant quality issues. We believe this can be explained through an already matured application architecture, together with the existence of a core of experienced contributors." (Section 6, Conclusion)

> "We found the SQALE model, and its implementation in the form of technical debt to be the most accurate quantitative quality measure among those studied." (Section 5.4, RQ4)

### Key Takeaway
For the thesis evaluation framework, use SQALE/SonarQube technical debt ratio as the primary system-level maintainability metric (robust against size confounding), supplemented by MI at the method/class level for finer-grained complexity assessment. The finding that maintainability effort concentrates in a small number of packages suggests that LLM-driven tactic implementations should target identified "hotspot" packages for maximum measurable impact.
