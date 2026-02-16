## A Critical Comparison on Six Static Analysis Tools: Detection, Agreement, and Precision

| Field | Value |
|-------|-------|
| **Key** | `lenarduzzi2023critical` |
| **Authors** | Lenarduzzi, Pecorelli, Saarimaki, Lujan, Palomba |
| **Venue** | Journal of Systems and Software (2023, preprint December 2022) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Developers use SATs to control for potential quality issues, but the growing number of available tools makes selection difficult. Existing knowledge on SAT capabilities is limited, particularly regarding inter-tool agreement on detected issues and the precision of their recommendations.
- **Gap:** Prior comparisons of SATs focused on specific aspects (security vulnerabilities, feature listings, or defect prediction) but did not investigate (1) detection agreement among a broad set of general-purpose SATs at line/class level, (2) precision of recommendations across multiple tools simultaneously, or (3) the overlap of quality issues detected by different tools on a large-scale Java benchmark.

### Contribution
This paper presents the largest empirical comparison to date of six widely-used static analysis tools (Better Code Hub, CheckStyle, Coverity Scan, FindBugs, PMD, and SonarQube) applied to 47 Java projects from the Qualitas Corpus dataset. It investigates three dimensions: (1) the types of source code quality issues each tool detects, (2) inter-tool detection agreement at class-level and line-level, and (3) the precision of each tool based on manual validation of statistically significant samples. The study reveals that tools have little to no agreement with each other and that most suffer from low precision, with values ranging from 18% (SonarQube) to 86% (CheckStyle).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 1  | 1  |   3   |  0  |   5    | 10/25 |

**Relevance:** MEDIUM

This paper is directly relevant to the thesis methodology for evaluating maintainability improvements via static analysis (Objectives O3, O4). It provides critical evidence that relying on a single static analysis tool introduces significant blind spots and false positive risks, which must be accounted for when measuring the impact of LLM-applied architectural tactics. The finding that SonarQube detects the broadest range of issues but has the lowest precision (18%) is especially important since SonarQube is the thesis's primary evaluation tool.

### Method & Validation
- **Type:** Large-scale empirical comparison study
- **Validation:** 47 Java projects from Qualitas Corpus; manual precision evaluation of stratified samples (~375-384 items per tool, 95% confidence level, 5% margin); dual-inspector process with Krippendorff's alpha = 0.84; replication package available

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** Six SATs compared: SonarQube LTS 6.7.7, Better Code Hub, Coverity Scan, FindBugs, PMD, CheckStyle
- **Languages:** Java

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Total rules detected across all tools | 936 unique rules, violated 13,554,762 times across 47 projects |
| SonarQube rules detected | 180 of 413 rules; 418,433 issue occurrences |
| CheckStyle issue volume | 9,686,813 occurrences (highest volume by far) |
| Tool agreement (best case, class-level) | FindBugs-PMD: 9.378% overlap |
| Tool agreement (worst case, class-level) | CheckStyle-PMD: 0.144% overlap |
| Overall detection agreement across all tools | Less than 0.4% |
| Rules with 100% agreement related to same issue | Only 6 out of 66 rule pairs (all between CheckStyle and PMD) |
| Precision -- SonarQube | 18% (69/384 true positives) |
| Precision -- Better Code Hub | 29% (109/375 true positives) |
| Precision -- Coverity Scan | 37% (136/367 true positives) |
| Precision -- PMD | 52% (199/380 true positives) |
| Precision -- FindBugs | 57% (217/379 true positives) |
| Precision -- CheckStyle | 86% (330/384 true positives), but mostly syntactic/formatting rules |
| SonarQube avg violations per class | 47.4 |
| Inter-rater agreement (precision validation) | Krippendorff's alpha = 0.84 |

### Dataset / Benchmark
Qualitas Corpus (Release 20130901), compiled version: 112 Java systems with 754 versions, 18+ million LOC, 16,000 packages, 200,000 classes. Of these, 47 projects were successfully analyzed by all six tools (some tools could not process all 112 systems). Projects span IDEs, databases, compilers, and various domains. Dataset is publicly available.

### Challenges & Limitations
- **Dataset age:** Qualitas Corpus data collected in 2013; may miss newer Java constructs (e.g., lambda expressions) and modern coding patterns.
- **Default tool configuration:** All tools run with default settings; project-specific custom configurations by developers could affect results. However, this was intentional to compare baseline capabilities.
- **Java-only:** Results limited to Java; cannot generalize to other programming languages.
- **Open-source only:** While open-source projects are shown to be comparable in quality to industrial code, further replication on closed-source projects is desirable.
- **No recall measurement:** Study evaluates precision only, not recall; future work planned to assess what issues tools miss entirely.
- **SonarQube duplicate issues:** Some SonarQube results contained duplicated issues in the same class, requiring manual exclusion.
- **CheckStyle precision caveat:** Highest precision (86%) but mostly detects syntactic/formatting issues, not functional defects or design problems.

### Key Quotes
> "The key results show little to no agreement among the tools and a low degree of precision." (Abstract)

> "There is no silver bullet that is able to guarantee source code quality assessment on its own." (Section 6, Discussion)

> "Most of the considered SATs suffer from a high number of false positive rules, and their precision ranges between 18% and 57%." (Finding 4)

### Key Takeaway
When using static analysis tools to evaluate LLM-driven architectural tactic implementations, the thesis must account for the fact that no single tool provides comprehensive or highly precise detection. SonarQube offers the broadest rule coverage and language support but has the lowest precision (18%), meaning the vast majority of its flagged issues may be false positives. The thesis evaluation methodology should either (a) combine multiple complementary tools to increase coverage, or (b) carefully select which SonarQube rules to track (focusing on high-precision rule categories) rather than relying on aggregate violation counts, especially when comparing before/after maintainability metrics.
