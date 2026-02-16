## A Tool-Based Perspective on Software Code Maintainability Metrics: A Systematic Literature Review

| Field | Value |
|-------|-------|
| **Key** | `ardito2020maintainability` |
| **Authors** | Luca Ardito, Riccardo Coppola, Luca Barbato, Diego Verga |
| **Venue** | Scientific Programming, Hindawi (2020) |
| **DOI** | 10.1155/2020/8840389 |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** Software maintainability is a crucial property, yet there is no common accordance in industry and academia about a universal set of metrics to adopt for evaluating it. The available models are very language- and domain-specific, and comprehensive tooling to apply analysis strategies across different languages is lacking.
- **Gap:** Prior secondary studies either analyzed tools and described metrics based on tool features (tool-first approach), covered limited time windows, or mixed static/dynamic/change metrics without focusing specifically on static maintainability metrics with tool coverage mapping. No existing SLR provided a metric-first perspective mapping the most popular static maintainability metrics to available tools across multiple programming languages over a 20-year period.

### Contribution

This SLR (following Kitchenham's guidelines) identifies and catalogs 174 static maintainability metrics from 43 primary studies (2000--2019) across four digital libraries (ACM, IEEE Xplore, Scopus, Web of Science). The authors distill a set of 15 most frequently mentioned metrics, catalog 19 available computation tools (6 closed-source, 13 open-source), and determine optimal tool sets (at most 5 tools) to cover all top metrics for the five most-supported programming languages (Java, C, C++, C#, JavaScript).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 0  | 1  |   5   |  0  |   5    | 11/25 |

**Relevance:** HIGH

This paper is the authoritative catalog of which maintainability metrics matter most in the literature and which tools compute them. It directly supports thesis Objectives O3 and O4 (evaluating maintainability before/after LLM-driven transformations) by providing evidence-based metric selection and tool-coverage mappings. The 15 most-popular metrics and the MI formula documented here justify the metric choices used in the thesis pipeline (Radon for CC, Halstead, MI, LOC).

### Method & Validation
- **Type:** Systematic Literature Review (Kitchenham guidelines)
- **Validation:** 801 unique papers screened; 43 primary studies selected via Likert-scale scoring with independent reviewer agreement; snowballing applied (no additional papers found)

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** 19 available tools cataloged (6 closed-source, 13 open-source), including CKJM (most cited, Java-only), Understand, CAST AIP, CCFinderX, CMT++, JHawk, Eclipse Metrics, Radon, and others. Tool data available on FigShare.
- **Languages:** Java (13 tools), C/C++ (12 tools), JavaScript (10 tools), C# (9 tools); 34 languages total covered across all tools

### Key Findings

| Finding | Value/Detail |
|---------|-------------|
| Total metrics cataloged | 174 metrics in 10 metric suites |
| Most-mentioned metrics (above-median score) | 15: CC, CE, CHANGE, C&K suite (6 metrics: WMC, DIT, NOC, CBO, RFC, LCOM), CLOC, Halstead suite (6 metrics), JLOC, LOC, LCOM2, MI, MPC, NOM, NPM, STAT, WMC |
| Most-cited single metric | CBO (Coupling Between Objects) -- 18 mentions |
| Second most-cited metric | RFC (Response for Class) -- 17 mentions |
| LOC mentions | 15 (but has 2 negative opinions; ambiguity in definition) |
| CC (Cyclomatic Complexity) mentions | 14; supported by 13/19 tools |
| LOC tool support | 14/19 tools |
| MI formula (3-metric) | MI = 171 - 5.2 ln(avgV) - 0.23 avgCC - 16.2 ln(avgLOC) |
| MI formula (4-metric, with comments) | Adds + 50 sin(sqrt(2.4 * perCM)) |
| MI thresholds | >85 easily maintainable; 65--85 moderately; <65 difficult |
| Total tools found | 38 (19 not retrievable, 6 closed-source, 13 open-source) |
| Most-cited tool | CKJM (5 papers; Java-only, C&K + CA + NPM) |
| Optimal tool set (closed+open, C/C++/C#) | 4 tools: CAST's AIP, Understand, CCFinderX, CMT++ -- covers 14/14 metrics |
| Optimal tool set (closed+open, Java) | 5 tools -- covers 15/15 metrics |
| Open-source only coverage gap | LCOM2 and MPC not explicitly supported by any open-source tool |
| Best-supported languages | Java (13 tools), C/C++ (12), JavaScript (10), C# (9) |
| 75% of all 174 metrics | Mentioned by only a single paper |
| Negative opinions on metrics | Very rare; no metric received many negative scores |
| MI controversy | Ostberg & Wagner doubt MI effectiveness; Sarwar et al. find it efficient |

### Dataset / Benchmark
SLR corpus of 801 unique papers (from ACM Digital Library, IEEE Xplore, Scopus, Web of Science), published 2000--2019, refined to 43 primary studies. All extracted metric data, tool information, and scoring tables available on FigShare as supplementary material.

### Challenges & Limitations
- **Construct validity:** Search strategy may not cover all possible studies; mitigated by thorough search string definition with synonyms and four major digital libraries.
- **Internal validity:** Manual paper evaluation and opinion assignment may suffer from misinterpretation; mitigated by independent evaluation and discussion of disagreements.
- **Open-source tool coverage gap:** LCOM2 and MPC metrics are not explicitly supported by any open-source tool, limiting fully open-source metric computation for coupling-level OO metrics.
- **Language coverage imbalance:** Newer or less popular languages (e.g., Rust, Go, Kotlin) have minimal or no tool support for computing the most popular maintainability metrics.
- **75% of metrics are single-mention:** The vast majority of the 174 cataloged metrics appear in only one paper, making it difficult to establish broad consensus beyond the top 15.
- **No metric received many negative scores:** This limits the ability to identify genuinely poor metrics versus simply unknown ones.

### Key Quotes
> "There is still no accordance in the industry and academia about a universal set of metrics to adopt to evaluate software maintainability." (Section 1, Introduction)

> "More than 75% of the metrics are mentioned by just a single paper." (Section 3.1, RQ1.1)

> "By using open-source tools only, it is not possible to obtain full coverage of the most mentioned metrics. The LCOM2 and MPC metrics were not explicitly supported by any of the considered open-source tools." (Section 3.3)

### Key Takeaway

When selecting maintainability metrics for the thesis evaluation pipeline, use the 15 most-mentioned metrics from this SLR as the evidence-based justification. The thesis already uses Radon (CC, Halstead, MI, LOC) -- this paper confirms these are among the most popular and tool-supported metrics. For Python projects specifically, the open-source tool coverage gap (LCOM2, MPC not available in open-source tools) means coupling-level OO metrics may need custom implementation or alternative proxies. The MI formula and thresholds documented here provide the normative basis for before/after maintainability comparisons in Objectives O3--O4.
