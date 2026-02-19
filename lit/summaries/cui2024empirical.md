## An Empirical Study of False Negatives and Positives of Static Code Analyzers From the Perspective of Historical Issues

| Field | Value |
|-------|-------|
| **Key** | `cui2024empirical` |
| **Authors** | Han Cui, Menglei Xie, Ting Su, Chengyu Zhang, Shin Hwei Tan |
| **Venue** | Preprint / Under Review (August 2024), arXiv:2408.13558 |
| **Level** | L3-Thesis-Specific |

### Motivation & Gaps
- **Problem:** Static code analyzers suffer from false negatives (missing real bugs) and false positives (spurious warnings) that undermine their effectiveness and usability. Prior studies evaluate FN/FP rates by running analyzers against known faults, but do not examine the analyzers' own implementations and fixing patches to understand why FNs/FPs occur at the root level.
- **Gap:** No prior work had systematically studied the historical, developer-confirmed and -fixed FN/FP issues from the analyzers' own issue repositories. Existing studies (e.g., Thung et al. investigating 19 FNs, Wang et al. with 46 issues) examined limited samples without inspecting fixing patches or analyzer internals, providing only surface-level conclusions about FN/FP causes.

### Contribution
This paper presents the first systematic study of 350 historical, developer-confirmed and fixed false negative (FN) and false positive (FP) issues from three popular Java static code analyzers: PMD, SpotBugs, and SonarQube. The authors build taxonomies of 7 root causes and 10 input characteristics that trigger FNs/FPs, and demonstrate the usefulness of their findings through a metamorphic testing strategy that discovered 14 new FN/FP issues (11 confirmed, 9 fixed) plus 5 additional issues from manual investigation of analysis module weaknesses.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 0  | 1  |   2   |  0  |   5    | 8/25  |

**Relevance:** MEDIUM

This paper provides essential understanding of the reliability and limitations of static code analyzers (PMD, SpotBugs, SonarQube) that are used as evaluation instruments in the thesis. Since the thesis relies on static analysis to measure maintainability improvements before and after LLM-driven architectural tactic implementation, understanding the FN/FP characteristics of these tools is critical for interpreting results and selecting appropriate metrics. The findings inform which analyzer weaknesses to be aware of and how to mitigate measurement noise.

### Method & Validation
- **Type:** Empirical Study (open card sorting + metamorphic testing)
- **Validation:** Cross-validation by two independent co-authors with Cohen's Kappa reaching 1.0 after iterative consensus; metamorphic testing found 14 new issues (11 confirmed by tool developers); manual investigation revealed 5 additional confirmed issues

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** PMD (v6.x, 325 Java rules), SpotBugs (468 Java rules), SonarQube (618 Java rules) -- three popular open-source static code analyzers for Java
- **Languages:** Java (selected as one of the most popular languages targeted by existing static code analyzers)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Dataset size | 350 confirmed/fixed FN/FP issues: 80 FNs + 270 FPs across PMD (226), SpotBugs (21), SonarQube (103) |
| Most common root cause | Missing cases: 35.7% of all issues (125/350) -- missing whitelisted items, missing similarly-handled cases, missing specific cases |
| Second most common root cause | Unhandled language features or libraries: 28.9% (101/350) -- new Java features and libraries not supported by rules |
| Most common input characteristic | Annotations: 21.07% of input-related issues (59/280) -- analyzers fail to model annotation semantics |
| Analysis module errors | Type resolution is the most common analysis module error; PMD affected by scope analysis and type resolution limitations |
| SonarQube symbolic execution | SonarQube's symbolic execution engine has limitations in tracking runtime types and variable scopes outside method boundaries |
| PMD data-flow analysis | PMD's data-flow analysis is limited to reaching definition analysis only; cannot handle basic inter-procedural call flows |
| Metamorphic testing results | 14 new issues found (12 FNs, 2 FPs); lambda-to-anonymous-class conversion (mutation operator b) found the most issues (6) |
| FP vs FN reporting bias | Users more likely to report FPs than FNs; many FNs go unreported because no checking rules exist for those defect types |
| Best practice: modularity in rule design | PMD developers recommend using common utility classes to share logic between rules, reducing duplicated FN/FP fixes |

### Dataset / Benchmark
350 historical, developer-confirmed and fixed FN/FP issues collected from the issue repositories of PMD (226 issues: 155 FPs, 71 FNs), SpotBugs (21 issues: 15 FPs, 6 FNs), and SonarQube (103 issues: 100 FPs, 3 FNs). Issues collected before October 2022. All artifacts (datasets and tools) publicly available at Zenodo: https://zenodo.org/doi/10.5281/zenodo.11525129.

### Challenges & Limitations
- **FP/FN imbalance:** 270 FPs vs. 80 FNs in the dataset, reflecting reporting bias (users more likely to report FPs than FNs) rather than actual severity balance.
- **Java-only scope:** Findings may be specific to Java and may not generalize to other programming languages supported by these analyzers.
- **Three analyzers only:** Conclusions may not generalize beyond PMD, SpotBugs, and SonarQube, though these are representative and implement different forms of static analysis.
- **Manual analysis subjectivity:** Root cause and input characteristic categorization required six person-months of manual effort; mitigated by independent cross-validation with Cohen's Kappa reaching 1.0.
- **Unexplored dimensions:** Severity, affected versions, latency, and fixability of FN/FP issues were not analyzed because these dimensions are difficult to measure objectively.

### Key Quotes
> "We conduct the first systematic study to investigate FNs and FPs of static code analyzers from the new perspective of the historical issues. We construct a dataset of 350 historical issues of FNs and FPs from the studied analyzers to serve as the basis of our study and future research in this field." (p. 3)

> "Unfortunately, this rule is (implemented as) AST-based, and it brings some limitations. So to eliminate these false positives the rule should rely on the data flow." (SonarQube developer comment, p. 20)

> "We are working on a new bug-detection engine, that should be, at some point, able to handle such cases and would allow us to replace this rule with a more performant version of it (this new engine is already running on SonarCloud and some versions of SonarQube)." (SonarQube developer comment, p. 18)

### Key Takeaway
Static code analyzers like PMD, SpotBugs, and SonarQube have systematic FN/FP weaknesses rooted in missing cases (35.7%), unhandled language features (28.9%), and analysis module limitations. For the thesis, this means that maintainability metrics from these tools should be interpreted with awareness of their blind spots -- particularly around annotations, complex expressions, and inter-procedural analysis. When comparing before/after metrics for LLM-driven tactic implementations, multiple analyzers should be used in combination to cross-validate results, and metric changes should be evaluated for statistical significance rather than taken at face value.
