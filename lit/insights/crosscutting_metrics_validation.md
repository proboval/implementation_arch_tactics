# Cross-Cutting Synthesis: Metrics & Validation Approaches (O3, O4)

## Topic: Metrics & Validation Approaches (Cross-Cutting: O3, O4)

**Papers:** 11 | **Updated:** 2026-02-16

---

### Summary

The literature reveals a multi-layered measurement landscape for evaluating automated code transformations, spanning functional correctness, structural similarity, code quality impact, and statistical rigor. At the **functional correctness** layer, Pass@K (K=1,3,5) and compilation rate are the dominant metrics for verifying that LLM-generated code is syntactically valid and semantically preserved (`liu2025`, `xu2025`, `piao2025`, `goncalves2025`). MANTRA's strict three-gate pipeline -- compile, test-pass, RefactoringMiner-verified -- achieves 82.8% success and represents the current gold standard for automated refactoring validation (`xu2025`). At the **structural/semantic similarity** layer, CodeBLEU (incorporating AST and data-flow matching) and AST Diff precision/recall quantify how closely LLM output matches human-written ground truth (`xu2025`, `piao2025`), while IPSynth's Dice coefficient and HR@K/MRR metrics measure inter-procedural code placement accuracy for architectural tactic synthesis (`shokri2024`). These similarity metrics are essential for understanding *how* the LLM transforms code, not just whether the result compiles.

At the **quality impact** layer, the field bifurcates between lightweight code-level metrics (Maintainability Index, Cyclomatic Complexity, Halstead Volume via Radon) and project-level technical debt models (SQALE/SonarQube Technical Debt Ratio). Molnar et al. demonstrate that SQALE is the most reliable system-level maintainability measure -- independent of software size -- while MI is useful at method/class granularity (`molnar2020`). Ardito et al.'s SLR of 174 metrics across 43 primary studies confirms that CC, LOC, CBO, RFC, and MI are the most frequently cited maintainability metrics, supported by 13-14 out of 19 cataloged tools (`ardito2020`). However, Lenarduzzi et al.'s critical finding that six static analysis tools agree on less than 0.4% of detected issues, with precision ranging from 18% (SonarQube) to 86% (CheckStyle), means that **no single tool can be trusted in isolation** (`lenarduzzi2023`). Goncalves et al.'s iterative SonarQube-LLM pipeline further shows that issue reduction does not proportionally translate to technical debt reduction (ratio as low as 0.71), warning against naive issue-counting as a proxy for maintainability improvement (`goncalves2025`).

For **statistical validation**, the literature converges on non-parametric methods appropriate for non-normally distributed software metrics: Cliff's Delta for effect size (negligible <= 0.147, small <= 0.33, medium <= 0.474, large > 0.474), Wilcoxon signed-rank test for paired before/after comparisons, Mann-Whitney U for independent group comparisons, and Scott-Knott test for partitioning multiple techniques into statistically distinct groups (`piao2025`, `liu2025`, `horikawa2025`). The thesis measurement framework should adopt a **triangulated approach**: functional correctness gates (compile + test), multi-tool quality metrics (Radon + SonarQube + at least one additional tool), architecture-level indicators (coupling, cohesion, modularity), and rigorous statistical testing with effect sizes reported alongside p-values.

---

### Metrics Inventory

| Metric | Papers Using It | Level | Tool | Threshold/Notes |
|--------|----------------|-------|------|-----------------|
| Pass@K (K=1,3,5) | `liu2025`, `xu2025` | Functional | Test suite | Higher is better; MANTRA reports at K=1 |
| Compilation Rate | `xu2025`, `piao2025`, `goncalves2025`, `shokri2024` | Functional | Compiler (javac, gcc) | 100% target; MANTRA 90.5%, Piao 38-51% real scenarios |
| Test Pass Rate | `xu2025`, `horikawa2025`, `goncalves2025` | Functional | JUnit, pytest | Must verify behavior preservation post-transformation |
| RefactoringMiner Verification | `xu2025`, `liu2025`, `piao2025` | Structural | RefactoringMiner 2.0/3.0 | F-score 99.5%; confirms intended refactoring type occurred |
| Maintainability Index (MI) | `ardito2020`, `molnar2020`, `visser2016` | Code (method/class) | Radon, Metrics Reloaded | >85 easy, 65-85 moderate, <65 difficult; 3-metric formula: 171 - 5.2ln(avgV) - 0.23avgCC - 16.2ln(avgLOC) |
| Cyclomatic Complexity (CC) | `ardito2020`, `piao2025`, `visser2016`, `molnar2020`, `horikawa2025` | Method | Radon, pyccmetrics | Visser: <=5 ideal; lower is better; most-cited after CBO/RFC |
| Lines of Code (LOC) | `ardito2020`, `horikawa2025`, `piao2025`, `visser2016` | Code | Any | <=15 per unit (Visser); ambiguity in definition noted by Ardito |
| Halstead Volume (V) | `ardito2020`, `molnar2020` | Code | Radon, Metrics Reloaded | Component of MI formula; operator/operand complexity |
| Technical Debt Ratio (TDR) | `goncalves2025`, `molnar2020` | Project | SonarQube SQALE | <5% = A rating; most reliable system-level metric (Molnar) |
| SonarQube Issue Count | `goncalves2025`, `lenarduzzi2023` | Project | SonarQube | Severity-weighted; >58% average reduction achievable with LLM loop |
| Technical Debt (minutes) | `goncalves2025`, `molnar2020` | Project | SonarQube SQALE | Debt reduction not proportional to issue reduction (ratio ~0.71) |
| Coupling Between Objects (CBO) | `ardito2020` | Class (OO) | CKJM, SonarQube | Most-cited single metric (18 mentions in SLR); lower is better |
| Response for Class (RFC) | `ardito2020` | Class (OO) | CKJM | Second most-cited (17 mentions); lower is better |
| Weighted Methods per Class (WMC) | `ardito2020`, `horikawa2025` | Class (OO) | DesigniteJava, CKJM | Median delta -2.07 for medium-level agent refactorings |
| Fan-in / Fan-out (FOUT) | `horikawa2025`, `piao2025` | Method/Class | DesigniteJava | Incoming/outgoing dependencies; lower FOUT is better |
| Design Smell Count | `horikawa2025` | Class/Package | DesigniteJava (27 types) | Median delta = 0.00 for agent refactoring (negligible effect) |
| Implementation Smell Count | `horikawa2025` | Method/Class | DesigniteJava | Median delta = 0.00 for agent refactoring (negligible effect) |
| CodeBLEU | `xu2025`, `piao2025` | Semantic | codebleu Python library | Includes AST + data flow matching; MANTRA 0.640 vs. RawGPT 0.517 |
| AST Diff Precision/Recall | `xu2025` | Structural | Custom (GumTree-based) | MANTRA P=0.781, R=0.635; measures tree edit distance |
| Dice Coefficient | `shokri2024` | Structural | Custom | >=0.5 threshold; measures overlap of API usage with specification |
| HR@K / MRR | `shokri2024` | Location Accuracy | Custom | HR@1=85%, MRR=0.88 for code annotation (tactic placement) |
| ArCode Plugin Score | `shokri2024` | Tactic Correctness | ArCode Plugin | Avg 0.95/1.0; verifies tactic API usage patterns |
| Cliff's Delta (d) | `liu2025`, `piao2025`, `horikawa2025` | Statistical | R / Python scipy | Negligible <=0.147, Small <=0.33, Medium <=0.474, Large >0.474 |
| Scott-Knott Test | `piao2025` | Statistical | R (ScottKnottESD) | Partitions techniques into statistically distinct groups |
| Wilcoxon Signed-Rank | `liu2025`, `horikawa2025` | Statistical | R / Python scipy | Paired before/after comparison; non-parametric |
| Mann-Whitney U | `horikawa2025`, `piao2025` | Statistical | R / Python scipy | Independent group comparison; non-parametric |
| Kruskal-Wallis | `horikawa2025` | Statistical | R / Python scipy | Multi-group comparison (>2 groups) |
| PMD Violation Count | `depalma2024`, `lenarduzzi2023` | Code | PMD | 8 categories; 52% precision (Lenarduzzi); used for quality-attribute-specific analysis |
| Code Duplication % | `visser2016` | Codebase | SonarQube, CPD | Low % target; SIG benchmark thresholds |
| Parameter Count per Unit | `visser2016` | Method | Custom / IDE | <=4 parameters (Visser) |
| Component Independence | `visser2016` | Architecture | Custom | % of hidden (non-public) code; higher is better |
| Component Balance (Gini) | `visser2016` | Architecture | Custom | 6-12 components, balanced distribution |
| Expert Quality Rating | `liu2025`, `depalma2024` | Human | Survey / Likert | 5-point (Liu) or 7-point (DePalma) scale; Fleiss' kappa 0.82 (Liu) |

---

### Validation Methods

| Method | Papers | Strengths | Weaknesses |
|--------|--------|-----------|------------|
| **Compile + Test + RM Gate** | `xu2025` | Triple verification: syntactic, semantic, structural correctness; 82.8% success rate | Requires existing test suite with adequate coverage; RM only supports known refactoring types |
| **Before/After Metric Comparison** | `goncalves2025`, `molnar2020`, `horikawa2025` | Simple, direct measurement; reproducible with standard tools | No control group; confounders (e.g., generated code, tangled commits); issue count != debt reduction |
| **Unit Test Pass Rate** | `xu2025`, `liu2025`, `horikawa2025`, `piao2025` | Functional correctness proof; automatable | Only covers existing tests; projects rarely have sufficient regression tests (Liu) |
| **RefactoringMiner Verification** | `xu2025`, `liu2025`, `piao2025` | Verifies intended refactoring type occurred; F-score 99.5% | Only supports 103 known refactoring types; cannot verify novel architectural transformations |
| **Expert/Manual Review** | `depalma2024`, `liu2025`, `xu2025` | Catches subtle issues (design quality, readability); high validity | Not scalable; subjective; expensive (Liu: 42 man-days for 180 instances) |
| **Multi-tool Cross-validation** | `lenarduzzi2023` | Reduces single-tool bias; increases coverage | Complex setup; tools disagree on >99.6% of findings; choosing which tool to trust is non-trivial |
| **User Study / Survey** | `xu2025`, `depalma2024` | Real developer perception; readability/reusability ratings | Small samples (37 for MANTRA, 15 for DePalma); cannot scale; potential bias |
| **SonarQube Iterative Feedback** | `goncalves2025` | Automated loop; measures convergence; configurable iterations | SonarQube precision only 18% (Lenarduzzi); may optimize for false positives; no test integration |
| **ArCode Plugin Verification** | `shokri2024` | Domain-specific tactic correctness; formal specification matching | Only for JAAS security tactics; requires pre-trained API usage model |
| **Statistical Hypothesis Testing** | `liu2025`, `piao2025`, `horikawa2025` | Rigorous; controls for chance; effect sizes quantify practical significance | Requires sufficient sample size; multiple comparisons need FDR correction |
| **Ablation Study** | `xu2025` | Quantifies contribution of each pipeline component | Expensive (requires re-running full pipeline per ablation) |
| **Longitudinal Analysis** | `molnar2020` | Tracks maintainability evolution over 10+ years; controls for maturity effects | Retrospective only; cannot isolate specific intervention effects |
| **Fractional Factorial Design** | `goncalves2025` | Systematic parameter exploration with reduced experiment count | Assumes no higher-order interactions; may miss configuration synergies |

---

### Datasets & Benchmarks

| Dataset | Size | Language | Scope | Availability | Used By |
|---------|------|----------|-------|-------------|---------|
| **IPSynth Tactic Dataset** | 20 programs (4-21 methods, 1-15 classes) | Java (JAAS) | Inter-procedural tactic synthesis | anonymous.4open.science/r/Anonymous-82DE | `shokri2024` |
| **Refactoring Oracle (MANTRA)** | 703 pure refactorings from 10 projects (12,526 total, filtered) | Java | Method-level refactoring (6 types) | GitHub (public) | `xu2025` |
| **Fowler Benchmark** | 61 refactoring types + 53 real scenarios | Java/JS | Full Fowler catalog coverage | GitHub (replication package) | `piao2025` |
| **LLM4Refactoring** | 180 refactorings from 20 projects + 20 negatives + 102 tests | Java | 9 within-document refactoring types | github.com/bitselab/LLM4Refactoring | `liu2025` |
| **AIDev Agent Dataset** | 15,451 refactoring instances from 14,998 commits | Java | Agentic coding tool outputs (Codex, Devin, Cursor, Claude Code) | GitHub (Mont9165/Agent_Refactoring_Analysis) | `horikawa2025` |
| **SonarQube Pipeline Dataset** | 3 repos: Commons Lang, Commons IO, Guava | Java | Iterative LLM-SonarQube improvement | Not explicitly public | `goncalves2025` |
| **DePalma Refactoring Dataset** | 40 Java files x 8 quality attributes = 320 trials | Java | Quality-attribute-specific refactoring | sites.google.com/stevens.edu/chatgptdataanalysis | `depalma2024` |
| **Qualitas Corpus** | 47 Java systems (112 total, 18M+ LOC) | Java | Static analysis tool comparison | Public (Release 20130901) | `lenarduzzi2023` |
| **Molnar Longitudinal Dataset** | 111 releases of 3 apps (FreeMind, jEdit, TuxGuitar) | Java | Maintainability evolution over 10+ years | FigShare (doi:10.6084/m9.figshare.12901331.v1) | `molnar2020` |
| **Ardito SLR Corpus** | 43 primary studies (from 801 screened) | Multi-language | Maintainability metric catalog (174 metrics) | FigShare (supplementary) | `ardito2020` |
| **SIG Benchmark** | Hundreds of real systems | Multi-language | Industrial maintainability benchmark (star ratings) | Proprietary (SIG/Visser) | `visser2016` |

---

### Tool Agreement

| Tool A | Tool B | Agreement Level (Class) | Agreement Level (Line) | Source |
|--------|--------|------------------------|----------------------|--------|
| FindBugs | PMD | 9.378% (best) | Not reported | `lenarduzzi2023` |
| CheckStyle | PMD | 0.144% (worst) | Not reported | `lenarduzzi2023` |
| SonarQube | FindBugs | <5% | Not reported | `lenarduzzi2023` |
| SonarQube | PMD | <5% | Not reported | `lenarduzzi2023` |
| SonarQube | CheckStyle | <5% | Not reported | `lenarduzzi2023` |
| **All 6 tools combined** | — | **<0.4%** | Not reported | `lenarduzzi2023` |

**Tool Precision (Manual Validation):**

| Tool | Precision | True Positives / Sample | Notes |
|------|-----------|------------------------|-------|
| CheckStyle | 86% | 330/384 | Mostly syntactic/formatting rules |
| FindBugs | 57% | 217/379 | Bug pattern detection |
| PMD | 52% | 199/380 | Code style + error patterns |
| Coverity Scan | 37% | 136/367 | Commercial, security-focused |
| Better Code Hub | 29% | 109/375 | SIG model-based |
| SonarQube | 18% | 69/384 | Broadest coverage but lowest precision |

**Implication for thesis:** SonarQube detects the widest range of issues but 82% of its findings are false positives (with default configuration). The thesis must either (a) use curated rule subsets with known high precision, (b) cross-validate with at least one additional tool, or (c) focus on relative change (delta) rather than absolute counts, since systematic bias cancels out in before/after comparisons.

---

### Key Papers

| Paper | Contribution to Metrics/Validation | Relevance |
|-------|-----------------------------------|-----------|
| `lenarduzzi2023` | Definitive evidence that SATs agree on <0.4% of issues; precision 18-86%; mandates multi-tool approach | CRITICAL |
| `ardito2020` | SLR of 174 metrics, identifies top 15 most-cited, maps to 19 tools; evidence-based metric selection | CRITICAL |
| `molnar2020` | Longitudinal comparison of MI, ARiSA, SQALE across 111 releases; SQALE best at system level, MI at class level | HIGH |
| `xu2025` | Gold-standard validation pipeline: compile + test + RefactoringMiner + CodeBLEU + ablation + user study | HIGH |
| `goncalves2025` | Iterative SonarQube-LLM feedback loop; demonstrates issue count != debt reduction (ratio 0.71) | HIGH |
| `horikawa2025` | Large-scale empirical metrics on agent refactoring: LOC delta, WMC delta, smell counts, fan-in/fan-out | HIGH |
| `piao2025` | CC and LOC as primary quality metrics; Scott-Knott for technique comparison; CodeBLEU for similarity | HIGH |
| `visser2016` | Practitioner-oriented 10 guidelines with SIG benchmark thresholds; maps to ISO 25010 | HIGH |
| `shokri2024` | Dice coefficient and HR@K/MRR for inter-procedural tactic placement accuracy; ArCode verification | MEDIUM |
| `liu2025` | Expert quality rating (Fleiss' kappa 0.82); quantifies 7.4% unsafe rate; Wilcoxon + Cliff's Delta | MEDIUM |
| `depalma2024` | PMD-based validation across 8 quality attributes; reveals LLM defaults to readability regardless of prompt | MEDIUM |

---

### Consensus

| Finding | Papers | Confidence |
|---------|--------|------------|
| **Compilation + test pass is the minimum verification gate** | `xu2025`, `liu2025`, `piao2025`, `goncalves2025`, `shokri2024` | **High** (5 papers) |
| **CC and LOC are the most widely used code-level quality metrics** | `ardito2020`, `piao2025`, `horikawa2025`, `visser2016`, `molnar2020` | **High** (5 papers) |
| **No single static analysis tool is sufficient** | `lenarduzzi2023`, `goncalves2025`, `molnar2020` | **High** (3 papers, with Lenarduzzi providing definitive evidence) |
| **SQALE/TDR is the best system-level maintainability metric** | `molnar2020`, `goncalves2025` | **High** (2 papers, Molnar with longitudinal validation) |
| **MI is useful at method/class granularity** | `molnar2020`, `ardito2020`, `visser2016` | **High** (3 papers) |
| **Issue reduction != debt reduction** | `goncalves2025` | **Medium** (1 paper, but ratio 0.71 is well-documented) |
| **Non-parametric statistics required for software metrics** | `liu2025`, `piao2025`, `horikawa2025` | **High** (3 papers, all use Wilcoxon/Mann-Whitney) |
| **Effect sizes must accompany p-values** | `liu2025`, `horikawa2025` | **High** (2 papers, both use Cliff's Delta) |
| **LLM-generated code requires behavior preservation testing** | `liu2025`, `xu2025`, `piao2025`, `depalma2024`, `goncalves2025` | **High** (5 papers) |
| **Agent refactoring improves LOC/WMC but not smell counts** | `horikawa2025` | **Medium** (1 paper, but N=15,451 instances) |
| **Expert review is gold standard but not scalable** | `liu2025`, `depalma2024`, `xu2025` | **High** (3 papers) |
| **CBO and RFC are most-cited OO coupling metrics** | `ardito2020` | **High** (SLR of 43 studies, 18 and 17 mentions respectively) |

---

### Gaps

| Gap | Impact on Thesis |
|-----|-----------------|
| **No Python-specific metric benchmarks:** All 11 papers evaluate Java projects; Python metric thresholds and tool coverage are under-studied | Thesis uses Python backends -- must establish Python-specific baselines using Radon; cannot directly reuse Java thresholds from Visser/SIG |
| **No architectural tactic-specific metrics:** Existing metrics (MI, CC, TDR) measure code quality, not whether an architectural tactic was correctly implemented | Thesis needs custom tactic verification metrics (e.g., did Encapsulation actually reduce coupling? Did Abstract Common Services create reusable modules?) |
| **LCOM2 and MPC not available in open-source tools:** Ardito SLR confirms coupling metrics gap in open-source tooling | Thesis may need custom LCOM2 computation for Python or use proxy metrics (e.g., afferent/efferent coupling from SonarQube) |
| **No standardized before/after comparison protocol:** Each paper uses ad hoc comparison methods; no established protocol for measuring architectural transformation impact | Thesis must define and justify a reproducible comparison protocol |
| **Small dataset sizes for tactic synthesis:** IPSynth has only 20 tasks; no large-scale benchmark for architectural tactic implementation exists | Thesis results will have limited statistical power; should target at least 30+ projects for meaningful effect size detection |
| **Test suite quality not controlled:** Papers assume existing tests are adequate, but Liu notes "projects rarely have sufficient regression unit tests" | Thesis must assess test coverage before/after and possibly augment test suites |
| **SonarQube precision problem:** 18% precision with default config means 82% of flagged issues are false positives | Using SonarQube for before/after comparison requires curated rule sets or delta-based analysis |
| **No cross-language validation:** All empirical validation is Java-only | Thesis Python results cannot claim generalizability; should explicitly position as Python-specific |
| **Smell detection unreliable for measuring improvement:** Horikawa shows median smell delta = 0.00 even with explicit refactoring | Thesis should not rely solely on smell counts; use structural metrics (CC, MI, coupling) instead |

---

### Measurement Framework Recommendations

**Adopt:**
- Compile + test pass gate from MANTRA (`xu2025`) -- mandatory first verification step
- Cliff's Delta + Wilcoxon signed-rank from `liu2025`, `horikawa2025` -- standard statistical protocol for before/after comparison
- SQALE/TDR from SonarQube as primary system-level metric (`molnar2020`) -- robust against size confounding
- MI via Radon at method/class level (`ardito2020`, `molnar2020`) -- well-established, Python-supported
- CC and LOC as core code-level metrics (`ardito2020`, `visser2016`) -- most-cited, universally supported

**Adapt:**
- MANTRA's triple-gate (compile + test + RefactoringMiner) (`xu2025`) -- replace RefactoringMiner with custom architectural constraint checker since tactics are not standard refactoring types
- SonarQube iterative feedback loop (`goncalves2025`) -- extend from code-smell level to architecture level; use curated rule subsets (not full default ruleset) to mitigate 18% precision problem
- Visser/SIG thresholds (`visser2016`) -- calibrate for Python (thresholds derived from Java/C# benchmarks); use as directional targets, not absolute gates
- CodeBLEU from `xu2025`, `piao2025` -- adapt for measuring similarity between LLM-generated tactic code and reference implementations (if reference implementations are available)
- Multi-tool cross-validation (`lenarduzzi2023`) -- use Radon + SonarQube + Pylint for Python (three-tool minimum); focus on metrics where tools agree

**Avoid:**
- Relying on SonarQube issue count alone as quality metric (`lenarduzzi2023`, `goncalves2025`) -- 18% precision + issue/debt ratio gap makes raw counts misleading
- Using smell counts as primary improvement metric (`horikawa2025`) -- median delta = 0.00 even with real refactoring; not sensitive enough
- LLM self-evaluation for behavior preservation (`depalma2024`) -- introduces bias; always use automated tests
- Single-tool evaluation (`lenarduzzi2023`) -- <0.4% inter-tool agreement makes single-tool results unreliable
- Absolute metric thresholds without context (`ardito2020`) -- thresholds are language- and domain-specific; always report deltas alongside absolute values
- Generic "quality" prompts without specifying attributes (`depalma2024`) -- LLM defaults to readability/naming changes regardless of stated goal

---

### Recommended Thesis Measurement Framework

| Layer | Metrics | Tools | Justification |
|-------|---------|-------|---------------|
| **L1: Functional Correctness** | Compilation rate, Test pass rate (Pass@1) | Python compiler, pytest | Mandatory gate: LLM output must compile and preserve behavior. Consensus across 5 papers (`xu2025`, `liu2025`, `piao2025`, `goncalves2025`, `shokri2024`). |
| **L2: Code Quality** | Maintainability Index (MI), Cyclomatic Complexity (CC), LOC, Halstead Volume | Radon | Standard, reproducible, Python-native. MI most validated at method/class level (`molnar2020`, `ardito2020`). CC and LOC are top-2 most-cited metrics (`ardito2020`). Thresholds: MI >85 good, CC <=5 ideal (Visser). |
| **L3: Technical Debt** | Technical Debt Ratio (TDR), Issue count (by severity), Debt in minutes | SonarQube (curated ruleset) + Pylint | SQALE TDR is best system-level metric (`molnar2020`); SonarQube provides SQALE model. Use curated rules to mitigate 18% default precision (`lenarduzzi2023`). Cross-validate with Pylint for Python-specific issues. |
| **L4: Architecture Quality** | Coupling (afferent/efferent), Cohesion (LCOM proxy), Modularity index, Module dependency count | SonarQube + custom Python scripts (import graph analysis) | Maps to ISO 25010 modularity/modifiability sub-characteristics. CBO is most-cited OO metric (`ardito2020`). Visser guidelines 5-7 (coupling, component independence, balance) provide targets. |
| **L5: Tactic Verification** | Tactic-specific structural checks (e.g., interface extraction confirmed, dependency inversion validated) | Custom AST-based checkers (Python `ast` module) | No existing tool verifies architectural tactic implementation. Inspired by IPSynth's specification-driven verification (`shokri2024`) and MANTRA's RefactoringMiner gate (`xu2025`). |
| **L6: Statistical Comparison** | Cliff's Delta (effect size), Wilcoxon signed-rank test (paired), Benjamini-Hochberg FDR correction | Python scipy, cliffs_delta package | Non-parametric methods appropriate for software metrics (`liu2025`, `horikawa2025`). Report both p-value and effect size. Cliff's Delta thresholds: negligible <=0.147, small <=0.33, medium <=0.474, large >0.474. |

**Execution Protocol:**
1. **Baseline measurement** (pre-transformation): Run L1-L4 metrics on original codebase. Record all values.
2. **Apply architectural tactic** via LLM pipeline.
3. **L1 gate**: If compilation fails or tests fail, reject transformation. Do not proceed to L2-L4.
4. **L5 verification**: Run tactic-specific structural checks. Confirm the intended tactic was actually applied.
5. **Post-measurement**: Run L2-L4 metrics on transformed codebase.
6. **Delta computation**: Calculate metric deltas (post - pre) for each metric.
7. **L6 statistical analysis**: Across all projects/tactics, compute Cliff's Delta and Wilcoxon signed-rank for each metric. Apply FDR correction for multiple comparisons.
8. **Report**: Present both absolute values (pre/post) and deltas. Include effect sizes with confidence intervals.

---

### Related Work Draft

> The evaluation of automated code transformations requires a multi-layered measurement approach spanning functional correctness, code quality, technical debt, and statistical rigor. For functional correctness, we adopt the compilation-plus-test-pass gate established as the gold standard by Xu et al. (2025), whose MANTRA framework achieves 82.8% success rate through a triple verification pipeline combining compilation, test execution, and RefactoringMiner structural validation. At the code quality layer, we measure Maintainability Index (MI), Cyclomatic Complexity (CC), and Lines of Code (LOC) using Radon, following Ardito et al.'s (2020) systematic literature review identifying these as the most frequently cited maintainability metrics across 43 primary studies. For system-level maintainability assessment, we employ the SQALE technical debt model via SonarQube, which Molnar and Motogna (2020) demonstrate to be the most reliable system-level maintainability measure in a longitudinal study of 111 software releases -- notably independent of software size, unlike the Maintainability Index which is confounded by code volume at system scale. Critically, our multi-tool evaluation approach is motivated by Lenarduzzi et al.'s (2023) finding that six widely-used static analysis tools agree on less than 0.4% of detected issues, with precision ranging from 18% (SonarQube) to 86% (CheckStyle), establishing that no single tool can reliably serve as the sole quality arbiter. To address this, we cross-validate findings using Radon (code-level metrics), SonarQube (technical debt and architectural rules), and Pylint (Python-specific quality assessment), focusing on metric deltas rather than absolute values to mitigate systematic tool bias. For statistical validation, we follow the non-parametric protocol established across recent LLM refactoring studies (Liu et al. 2025; Horikawa et al. 2025; Piao et al. 2025): Wilcoxon signed-rank tests for paired before/after comparisons with Cliff's Delta effect sizes, applying Benjamini-Hochberg correction for multiple comparisons. We interpret effect sizes using standard thresholds (negligible <= 0.147, small <= 0.33, medium <= 0.474, large > 0.474) and report both statistical significance and practical significance to avoid the common pitfall of reporting p-values without effect magnitudes.
