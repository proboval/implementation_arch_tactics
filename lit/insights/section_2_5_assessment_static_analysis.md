## Topic: Assessment Methods & Static Analysis (Section 2.5)

**Papers:** 7 | **Updated:** 2026-02-16

### Summary

The static analysis landscape for software maintainability assessment is characterized by a proliferation of tools and metrics that, upon empirical scrutiny, reveal troubling levels of disagreement and imprecision. Lenarduzzi et al. (2023) provide the most comprehensive evidence to date: across six widely-used static analysis tools applied to 47 Java projects, inter-tool detection agreement falls below 0.4%, with the best pairwise overlap (FindBugs--PMD) reaching only 9.4% at class level. Precision varies dramatically, from 18% for SonarQube to 86% for CheckStyle, though the latter's high precision reflects its focus on syntactic/formatting rules rather than substantive design or maintainability issues. Cui et al. (2024) deepen this concern by revealing the root causes of false positives and false negatives: 35.7% of confirmed FN/FP issues stem from missing cases in rule implementations, 28.9% from unhandled language features, and SonarQube's symbolic execution engine has fundamental limitations in tracking runtime types across method boundaries. Together, these findings make clear that single-tool reliance introduces both coverage blind spots and noise from false positives that can distort before/after maintainability comparisons.

On the metrics side, Ardito et al. (2020) catalog 174 static maintainability metrics from 43 primary studies and distill a consensus set of 15 most-mentioned metrics, with CBO (18 mentions), RFC (17), LOC (15), and CC (14) leading the list. The Maintainability Index -- MI = 171 - 5.2*ln(avgV) - 0.23*avgCC - 16.2*ln(avgLOC) -- remains widely used despite controversy about its effectiveness (Ostberg & Wagner doubt it; Sarwar et al. find it efficient). Critically, 75% of all 174 cataloged metrics appear in only a single paper, underscoring that consensus is narrow. Visser's SIG framework (2016) offers an alternative: 10 actionable guidelines mapped to measurable metrics with empirically calibrated star ratings (1--5 stars) benchmarked against hundreds of industrial systems. The SIG approach bridges the gap between abstract quality models (ISO 25010) and concrete coding practices, with predictive power showing issue resolution is 2x faster in 4-star versus 2-star systems.

At the architecture level, Abdelmoez et al. (2006) demonstrate that code-level metrics alone are insufficient: their change propagation probability model shows that a highly coupled component can become the riskiest in a system even without direct modification, validating the need for architecture-level assessment alongside code metrics. Meanwhile, Nocera et al. (2025) provide evidence from 321 GitHub projects that in practice, 89% of SonarQube Cloud quality gates enforce maintainability rating on new code, confirming that maintainability is a practitioner priority -- but the SQALE model's estimation of technical debt in minutes remains opaque in its calibration. Moreu De Leon et al. (2012), while addressing hardware maintainability, reinforce the principle that maintainability should be decomposed into weighted sub-attributes assessed at multiple levels, paralleling the thesis's approach of mapping ISO 25010 sub-characteristics to measurable static metrics.

### Metrics Inventory

| Metric | Papers Using It | Level | Tool | Threshold |
|--------|----------------|-------|------|-----------|
| Maintainability Index (MI) | `ardito2020`, `visser2016` | Module/File | Radon, VS | >85 easy, 65--85 moderate, <65 difficult |
| Cyclomatic Complexity (CC) | `ardito2020`, `visser2016`, `lenarduzzi2023` | Method/Unit | Radon, SonarQube, PMD | SIG: <=5 per unit |
| LOC (Lines of Code) | `ardito2020`, `visser2016`, `abdelmoez2006` | File/Module | Radon, all tools | SIG: <=15 per unit |
| Halstead Volume (V) | `ardito2020` | Method/File | Radon | Used in MI formula |
| Halstead Effort (E) | `ardito2020` | Method/File | Radon | -- |
| Halstead Difficulty (D) | `ardito2020` | Method/File | Radon | -- |
| CBO (Coupling Between Objects) | `ardito2020` | Class | CKJM, Understand | Most-cited metric (18 mentions) |
| RFC (Response for Class) | `ardito2020` | Class | CKJM, Understand | 2nd most-cited (17 mentions) |
| WMC (Weighted Methods per Class) | `ardito2020`, `visser2016` | Class | CKJM, SonarQube | -- |
| DIT (Depth of Inheritance Tree) | `ardito2020` | Class | CKJM | -- |
| NOC (Number of Children) | `ardito2020` | Class | CKJM | -- |
| LCOM (Lack of Cohesion of Methods) | `ardito2020` | Class | CKJM | -- |
| LCOM2 | `ardito2020` | Class | No open-source tool | Coverage gap |
| MPC (Message Passing Coupling) | `ardito2020` | Class | No open-source tool | Coverage gap |
| NOM (Number of Methods) | `ardito2020` | Class | Various | -- |
| Code Duplication % | `visser2016`, `nocera2025` | System | SonarQube, SIG | SIG: low %; SQC: quality gate condition |
| Unit Interface Size (params) | `visser2016` | Method | SIG tools | <=4 parameters |
| Component Independence (hidden code %) | `visser2016` | Architecture | SIG tools | High % hidden |
| Component Balance (Gini) | `visser2016` | Architecture | SIG tools | 6--12 components, balanced |
| Test Coverage | `visser2016`, `nocera2025` | System | SonarQube, SIG | >=80% (SIG); quality gate condition (SQC) |
| Maintainability Rating (SQALE) | `nocera2025` | System | SonarQube Cloud | A--E rating; 89% of projects enforce on new code |
| Reliability Rating | `nocera2025` | System | SonarQube Cloud | A--E rating; 88.7% enforce |
| Security Rating | `nocera2025` | System | SonarQube Cloud | A--E rating; 90.9% enforce |
| Technical Debt (minutes) | `nocera2025` | System | SonarQube Cloud (SQALE) | Estimated remediation time |
| Change Propagation Probability | `abdelmoez2006` | Architecture | SACPT (custom) | Risk = P(change) x Impact |

### Static Analysis Tools Comparison

| Tool | Precision | Recall | Rules | Agreement (best) | Source |
|------|-----------|--------|-------|-------------------|--------|
| SonarQube | 18% | Not measured | 180/413 violated | 9.4% w/ FindBugs (class) | `lenarduzzi2023` |
| PMD | 52% | Not measured | -- | 9.4% w/ FindBugs (class) | `lenarduzzi2023` |
| FindBugs/SpotBugs | 57% | Not measured | 468 Java rules | 9.4% w/ PMD (class) | `lenarduzzi2023`, `cui2024` |
| Coverity Scan | 37% | Not measured | -- | -- | `lenarduzzi2023` |
| Better Code Hub | 29% | Not measured | -- | -- | `lenarduzzi2023` |
| CheckStyle | 86% | Not measured | -- | 0.144% w/ PMD (class) | `lenarduzzi2023` |
| Radon | N/A (metrics) | N/A | CC, MI, Halstead, LOC | N/A (Python only) | `ardito2020` |
| SIG/Better Code Hub | N/A (benchmark) | N/A | 10 guidelines | N/A | `visser2016` |
| SonarQube Cloud | N/A (SaaS) | N/A | 618 Java rules | N/A | `nocera2025`, `cui2024` |
| CKJM | N/A (metrics) | N/A | CK suite + CA + NPM | N/A | `ardito2020` |

### Validation Methods

| Method | Papers | Strengths | Weaknesses |
|--------|--------|-----------|------------|
| Manual precision validation (stratified sample) | `lenarduzzi2023` | Rigorous dual-inspector process (Krippendorff alpha=0.84); 95% CI, 5% margin | Only evaluates precision, not recall; labor-intensive |
| Historical FN/FP issue mining | `cui2024` | Studies actual developer-confirmed bugs in analyzers; Cohen's Kappa=1.0 | Biased toward FPs (users report FPs more than FNs); Java-only |
| SLR with Likert-scale scoring | `ardito2020` | Systematic, reproducible (Kitchenham guidelines); 801 papers screened | Manual evaluation subjectivity; 20-year scope may include outdated findings |
| MSR (mining software repositories) | `nocera2025` | Large-scale empirical (321 projects); API cross-validation | Only captures tool configuration, not actual quality outcomes |
| SIG benchmark (industry calibration) | `visser2016` | Empirical star ratings from hundreds of systems; yearly recalibration; predictive power validated | Proprietary benchmark data; limited transparency of thresholds |
| Change propagation modeling (UML) | `abdelmoez2006` | Architecture-level risk quantification; early lifecycle intervention | Requires detailed UML artifacts; single case study validation |
| Expert-based weighted assessment | `moreu2012` | Decomposes maintainability into measurable sub-attributes | Subjective (expert 0--4 scores); hardware domain, not software |

### Tool Agreement

| Tool A | Tool B | Agreement Level (Class) | Agreement Level (Line) | Source |
|--------|--------|-------------------------|------------------------|--------|
| FindBugs | PMD | 9.378% (best case) | -- | `lenarduzzi2023` |
| CheckStyle | PMD | 0.144% (worst case) | -- | `lenarduzzi2023` |
| All six tools combined | -- | < 0.4% overall | -- | `lenarduzzi2023` |
| Rules with 100% issue agreement | -- | 6 out of 66 rule pairs (all CheckStyle--PMD) | -- | `lenarduzzi2023` |

### Key Papers

| Paper | Contribution | Relevance |
|-------|--------------|-----------|
| `lenarduzzi2023critical` | Largest empirical SAT comparison: 6 tools, 47 projects, precision 18--86%, agreement <0.4% | HIGH -- directly informs multi-tool strategy |
| `cui2024empirical` | Root cause taxonomy of 350 FN/FP issues in PMD, SpotBugs, SonarQube | HIGH -- explains why tools fail, guides metric selection |
| `ardito2020maintainability` | SLR of 174 metrics, 15 most-mentioned, 19 tools cataloged, MI formula | HIGH -- authoritative metric catalog and tool-coverage map |
| `visser2016maintainable` | 10 SIG guidelines, star ratings, industry benchmark, ISO 25010 alignment | HIGH -- provides benchmarked thresholds and tactic mapping |
| `nocera2025sonarqube` | Mining study of 321 GitHub projects' SonarQube Cloud usage; 89% enforce maintainability | MEDIUM -- validates SonarQube as practitioner-relevant tool |
| `abdelmoez2006methodology` | Architecture-level risk via change propagation probabilities | MEDIUM -- validates architecture-level assessment beyond code metrics |
| `moreu2012practical` | Weighted sub-attribute decomposition of maintainability (hardware domain) | LOW -- conceptual parallel to ISO 25010 decomposition only |

### Consensus

| Finding | Papers | Confidence |
|---------|--------|------------|
| No single static analysis tool is sufficient for comprehensive quality assessment | `lenarduzzi2023`, `cui2024`, `ardito2020` | **High** -- empirically demonstrated across large datasets |
| CC, LOC, CBO, RFC are the most established maintainability metrics | `ardito2020`, `visser2016` | **High** -- convergent evidence from SLR (43 studies) and industry benchmark |
| MI is useful but controversial as a single aggregate measure | `ardito2020` | **Medium** -- mixed opinions (Ostberg vs. Sarwar); still widely tool-supported |
| SonarQube has broadest rule coverage but lowest precision among general tools | `lenarduzzi2023`, `cui2024` | **High** -- 18% precision confirmed; FP root causes identified |
| Maintainability is a top practitioner priority in CI/CD quality gates | `nocera2025`, `visser2016` | **High** -- 89% enforcement rate in 321 projects; SIG industry adoption |
| Architecture-level coupling assessment complements code-level metrics | `abdelmoez2006`, `visser2016` | **Medium** -- validated in case study and SIG guidelines 5--7 |
| Multi-level decomposition (sub-characteristics to metrics) is essential | `ardito2020`, `visser2016`, `moreu2012` | **High** -- consistent across software and hardware domains |

### Contradictions

| Issue | Position A | Position B | Thesis Choice |
|-------|------------|------------|---------------|
| MI effectiveness | `ardito2020` (citing Ostberg & Wagner): MI is unreliable as a single quality indicator | `ardito2020` (citing Sarwar et al.): MI is efficient for maintainability evaluation | **Use MI as one metric among several**, not as sole indicator; combine with CC, Halstead, LOC, and CK metrics |
| SonarQube reliability | `nocera2025`: Widely adopted (89% enforce maintainability); industry standard | `lenarduzzi2023`: 18% precision; `cui2024`: systematic FN/FP from missing cases and engine limitations | **Use SonarQube for trend detection and SQALE rating**, but cross-validate with Radon (Python) and do not rely on raw violation counts |
| CheckStyle value | `lenarduzzi2023`: Highest precision (86%) among all tools | `lenarduzzi2023`: Mostly syntactic/formatting, not design-level issues | **Exclude CheckStyle-style metrics** from maintainability assessment; focus on design and complexity metrics |
| Code-level vs. architecture-level assessment | `ardito2020`: Code metrics are sufficient (15 metrics cover maintainability) | `abdelmoez2006`: Architecture-level change propagation captures risks invisible at code level | **Combine both levels**: code-level metrics (Radon, SonarQube) + architecture-level indicators (coupling between components, module independence) |

### Gaps

| Gap | Impact on Thesis |
|-----|-----------------|
| No recall measurement for SATs (Lenarduzzi measured precision only) | Cannot quantify what issues tools *miss*; thesis must acknowledge this blind spot in evaluation methodology |
| Inter-tool agreement studied only for Java | Thesis targets Python projects; agreement levels may differ; must validate tool behavior on Python codebases |
| Open-source tool coverage gap for LCOM2 and MPC | Cannot compute these coupling/cohesion metrics with open-source tools for Python; need alternative proxies or custom implementation |
| No study links SonarQube quality gate configurations to actual maintainability outcomes | Nocera 2025 explicitly flags this as future work; thesis cannot assume quality gate pass = good maintainability |
| MI formula validated primarily on C/Fortran codebases (Oman 1992 origin) | Python-specific MI calibration is unverified; Radon implements the formula but thresholds may not transfer directly |
| SonarQube's SQALE technical debt estimation in minutes lacks transparent calibration | Cannot independently verify the time estimates; should use as relative trend indicator only |
| FN/FP root cause study covers pre-2022 analyzer versions only | Current versions of PMD, SpotBugs, SonarQube may have fixed some issues; findings are directionally valid but not version-specific |

### Measurement Framework Recommendations

**Adopt:**
- **Multi-metric approach** using CC, Halstead Volume, MI, and LOC (Radon) as primary code-level metrics -- supported by `ardito2020` consensus and `visser2016` SIG guidelines
- **Before/after delta measurement** rather than absolute thresholds -- mitigates tool precision issues (`lenarduzzi2023`) since systematic bias cancels in paired comparisons
- **SIG-style risk profiling** (categorize code into low/moderate/high/very-high risk buckets) from `visser2016` -- provides interpretable quality profiles beyond single-number aggregates
- **SonarQube maintainability rating** (SQALE) as a practitioner-aligned summary metric, validated by 89% adoption (`nocera2025`)
- **Statistical significance testing** on metric deltas -- required because tool noise (FPs/FNs) from `cui2024` could produce spurious improvements

**Adapt:**
- **Visser's 10 guidelines** to Python context: translate unit-length (<=15 LOC), CC (<=5), parameters (<=4) thresholds for Python idioms (e.g., Python functions tend to be shorter; decorators affect parameter counting)
- **MI formula** (3-metric variant from `ardito2020`): use Radon's implementation but interpret thresholds cautiously given C/Fortran origin; report as supplementary to component-level metrics
- **Architecture-level coupling indicators** inspired by `abdelmoez2006`: compute import-graph fan-in/fan-out and module dependency depth as proxies for change propagation risk, since full UML models are unavailable for open-source Python projects

**Avoid:**
- **Single-tool reliance** on any one SAT -- definitively shown to be unreliable (`lenarduzzi2023`: <0.4% agreement; `cui2024`: systematic blind spots)
- **Raw violation counts** as quality indicators -- SonarQube's 18% precision means ~82% of flagged issues may be false positives; use severity-weighted or rule-filtered counts instead
- **CheckStyle-equivalent (formatting) metrics** for maintainability assessment -- high precision (86%) but measures style, not design quality (`lenarduzzi2023`)
- **SQALE debt-in-minutes** as an absolute measure -- opaque calibration, useful only for relative comparison between project versions
- **Aggregate MI as sole metric** -- controversial effectiveness (`ardito2020`); always pair with decomposed metrics (CC, Halstead, LOC individually)

### Related Work Draft

> Software maintainability assessment relies on a combination of metrics and static analysis tools, yet empirical evidence reveals significant challenges with both. Ardito et al. \cite{ardito2020maintainability} catalog 174 static maintainability metrics from a systematic review of 43 primary studies, identifying Coupling Between Objects (CBO), Response for Class (RFC), Lines of Code (LOC), and Cyclomatic Complexity (CC) as the most frequently cited measures. The Maintainability Index, originally formulated by Oman and Hagemeister (1992) as $MI = 171 - 5.2 \ln(V) - 0.23 \cdot CC - 16.2 \ln(LOC)$, remains widely implemented in tools such as Radon and Visual Studio, though its effectiveness as a standalone indicator is debated. Visser \cite{visser2016maintainable} operationalizes maintainability through 10 actionable guidelines -- including unit length ($\leq 15$ LOC), cyclomatic complexity ($\leq 5$ per unit), and loose component coupling -- benchmarked against hundreds of industrial systems via the SIG quality model, demonstrating that systems rated 4 stars resolve issues twice as fast as 2-star systems.
>
> However, the reliability of static analysis tools themselves presents a critical methodological concern. Lenarduzzi et al. \cite{lenarduzzi2023critical} conduct the largest empirical comparison of six tools (SonarQube, PMD, FindBugs, CheckStyle, Coverity Scan, Better Code Hub) on 47 Java projects and find that inter-tool agreement falls below 0.4\%, with precision ranging from 18\% (SonarQube) to 86\% (CheckStyle, limited to formatting rules). Cui et al. \cite{cui2024empirical} further investigate the root causes of false positives and negatives through 350 developer-confirmed issues, revealing that missing rule cases (35.7\%) and unhandled language features (28.9\%) account for the majority of analyzer failures. Despite these limitations, SonarQube remains the most widely adopted tool in practice: Nocera et al. \cite{nocera2025sonarqube} report that 89\% of the 321 surveyed GitHub projects enforce maintainability ratings through SonarQube Cloud quality gates. These findings collectively motivate the multi-tool, multi-metric evaluation strategy adopted in this thesis, combining Radon-based code metrics (CC, MI, Halstead volume) with SonarQube trend analysis and architecture-level coupling indicators to mitigate the documented blind spots of any single tool.
