# Methodology Review Report — Peer Reviewer 1

**Reviewer:** Dr. Davide Falessi — University of Rome Tor Vergata
**Paper:** "Can LLMs Implement Architectural Tactics? Early Results" — EASE 2026
**Review focus:** Research design rigor, sampling/representativeness, measurement validity, statistical analysis, reproducibility, handling of attrition, threats to validity
**Overall score:** 60 / 100

---

## Summary Assessment

This paper presents a pre-test/post-test experiment evaluating whether an LLM (Qwen3-Coder-34B) can improve software maintainability by implementing architectural tactics in 56 Python repositories. The topic is timely and the pipeline is thoughtfully engineered. However, the methodological contribution is weakened by the absence of inferential statistics, over-reliance on a single metric with acknowledged limitations, and insufficient treatment of a 25% attrition rate. The paper reads as an engineering feasibility demonstration rather than a rigorous empirical study, which limits its contribution to the evaluation and assessment community.

---

## 1. Research Design Rigor (§3.1, pp. 3–4)

**Verdict: Adequate but incomplete.**

The within-subjects pre-test/post-test design (each repo as its own control) is appropriate for this research question. It controls for between-repository variance (size, domain, coding style) and enables paired comparison, which is the correct choice given the heterogeneous dataset. The paper states a null hypothesis (§3.1): "tactic implementation does not produce a statistically significant change in the Maintainability Index."

**Critical gap:** The null hypothesis is stated but **never tested**. Section 5 reports only descriptive statistics (mean ΔMI = +1.484, improvement rate = 42.9%). No p-value, test statistic, confidence interval, or effect size is reported for the primary research question (RQ2). This is a fundamental omission for any study claiming to evaluate a causal intervention. The descriptive statistics alone cannot support conclusions about whether the observed ΔMI is likely to reflect a real effect or random variation. For EASE, where empirical rigor is the central criterion, this is a major weakness.

**Recommendation:** Report a paired Wilcoxon signed-rank test (the non-parametric choice is appropriate given the small N = 42 and likely non-normal distribution of ΔMI). Include the W statistic, exact p-value, and a standardized effect size (e.g., matched-pairs rank-biserial correlation or Cliff's delta). Report 95% confidence intervals for mean ΔMI.

---

## 2. Sampling Strategy and Dataset Representativeness (§3.3, p. 4)

**Verdict: Moderate. Adequately described but limited scope.**

The dataset of 57 Python backend repositories is relatively small by SE empirical standards but defensible for an early-stage study. The repositories were "collected and filtered from GitHub" (Abstract) — however, the inclusion/exclusion criteria are **not specified** in §3.3. The paper should describe: (a) the search strategy used, (b) the filtering criteria, (c) the initial pool size before filtering, and (d) how representativeness was assessed. Without this information, the reader cannot assess selection bias or generalizability.

Three architectural styles (script-based, layered, modular monolith) are covered, but all repositories are Python backend projects. This limits external validity to a single language and domain. The paper acknowledges this in §6 (Threats to Validity), which is appropriate, but the limitation should be more prominent in the interpretation of results.

The use of validated (manually labeled) architecture labels is a strength — it isolates tactic selection/implementation from detection error. However, the labels were assigned by a single annotator (acknowledged in §6), which introduces potential bias without inter-annotator reliability assessment.

**Recommendation:** Document the complete sampling frame, inclusion/exclusion criteria, and selection process. Add a characterization table comparing the sample to the broader population of Python backend repositories (e.g., size distribution, domain categories, Star count).

---

## 3. Measurement Validity: Maintainability Index (§3.4, p. 4)

**Verdict: Problematic. MI limitations are acknowledged but the study design does not mitigate them.**

The Maintainability Index (MI) is used as the sole primary outcome measure. The paper cites Lenarduzzi et al. (2023) finding <0.4% agreement among static analysis tools, and acknowledges in §6 that MI "captures file-level complexity but is insensitive to module boundary quality, inter-module coupling changes, and semantic correctness." Despite these caveats, MI remains the only quantified dependent variable — fan-out and docstring coverage are mentioned as "collected" but **never reported** in the results.

This creates a construct validity problem: the paper claims to measure "maintainability improvement" but actually measures a specific arithmetic composite of Halstead Volume, Cyclomatic Complexity, and LOC. As the paper itself notes (§5.5), 12 of 18 improvements involved adding a new file with MI = 100 — a pattern consistent with metric gaming (adding trivial, simple files inflates the average). The paper mentions this but does not present any analysis to disentangle genuine architectural improvement from metric-arithmetic effects.

**Recommendation:** At minimum, (1) report the supplementary metrics (fan-out, docstring coverage, package count) that were collected, and (2) conduct a per-file analysis distinguishing repositories where improvement reflects genuine restructuring from those where it reflects trivial module addition. A trivial baseline — e.g., what ΔMI results from adding a single empty `__init__.py` or a simple utility file — would help calibrate the magnitude of observed effects.

---

## 4. Statistical Analysis (§5, pp. 6–12)

**Verdict: Insufficient. Descriptive statistics only — no inferential testing.**

This is the most significant methodological weakness. The paper includes:

| What is present | What is missing |
|----------------|-----------------|
| Means and counts (§5.1) | Statistical significance test (RQ2 null hypothesis) |
| Breakdown by size (§5.3) | Confidence intervals for ΔMI |
| Breakdown by tactic (§5.4) | Effect sizes with uncertainty estimates |
| Breakdown by architecture (§5.5) | Multiple comparison correction (RQ3 tests across 3 tactics × 3 architectures) |
| Failure categorization (§5.6) | Power analysis or sensitivity analysis |

The comparison between the "initial pipeline experiment" (§3.8) and the current experiment (§5.1) — mean ΔMI +0.48 vs. +1.484 — is presented as evidence that validated labels improve outcomes. However, the paper correctly cautions that "the datasets differ and direct comparison must be made cautiously" (§5.8). A statistical comparison (e.g., independent-samples test) would be needed to substantiate this claim.

When testing RQ3 (tactic and architecture effects), the paper conducts implicit multiple comparisons across groups without any correction. With 3 tactics and 3 architectures, the family of comparisons increases the risk of false positives.

The sub-group analysis by repository size (§5.3, Table 3) is informative but uses absolute |ΔMI| rather than signed ΔMI, which conflates improvement and degradation.

**Recommendation:** Add a complete inferential statistics subsection:
- Paired Wilcoxon test for RQ2 (primary hypothesis), with exact p-value and effect size
- Bootstrap 95% CIs for mean ΔMI overall, per tactic, and per architecture
- Explicit statement that RQ3 analyses are exploratory (no correction needed if framed as such)
- Sensitivity analysis: re-compute mean ΔMI excluding the top-2 outlier cases (webapp-color, Paper2Rebuttal) to assess whether the overall result is driven by extreme values

---

## 5. Handling of Failures and Attrition (§3.3, §4.6, §5.6)

**Verdict: Transparent reporting but insufficient analysis.**

The 25% failure rate (14/56 repos) is explicitly reported and retained in the dataset — this is methodologically honest and commendable. However, several issues remain:

1. **Numerical inconsistency:** Section 3.3 reports 14 failures during cloning; §5.6 then states "10 repositories failed during the cloning stage" and "5 repositories... could not produce after-analysis measurements." This sums to 15, not 14. The paper needs to reconcile these numbers.

2. **No failure analysis by repository characteristics:** Are failures correlated with size, architecture type, or other covariates? If failures cluster in specific subpopulations, the complete-case analysis (N = 42) may be biased. For example, if larger repositories fail more often due to rate limiting or context window limits, the effective sample over-represents small repos — which happen to show the largest effects.

3. **Infrastructure vs. algorithmic failures:** Rate limiting (HTTP 429) is an infrastructure issue, not a pipeline limitation. These should be separated from algorithmic failures (planner parse failures, stuck loops) in the failure taxonomy. This distinction affects the interpretation of the pipeline's robustness.

**Recommendation:** (a) Reconcile the failure counts. (b) Compare characteristics of failed vs. completed repos on available covariates (size, architecture label, domain). (c) Report results under a "worst-case" scenario (treating all failures as non-improvements, i.e., 18/56 = 32.1%) alongside the complete-case analysis (18/42 = 42.9%). (d) Separate infrastructure and algorithmic failure categories.

---

## 6. Reproducibility and Data Transparency (§7, Data Availability)

**Verdict: Partially adequate.**

The paper provides a Zenodo replication package with static analysis artifacts. This is commendable. However, several reproducibility concerns remain:

1. **Model specificity:** The model is identified as "Qwen3-Coder-34B" but the paper does not specify the exact model variant, checkpoint, or release version. LLM behavior can vary significantly across versions. A specific Hugging Face model ID or quantized variant should be cited.

2. **Temperature and parameters:** Temperature = 0.2 is reported, but other decoding parameters (top-p, top-k, repetition penalty) are not. For exact reproducibility, all non-default generation parameters should be documented.

3. **Prompt templates:** The two prompt templates (file selection, patch generation) are described in §4.4 but not reproduced verbatim. For a study whose primary intervention is prompt-based, the exact prompts are essential for reproducibility. They should be included in the replication package or an appendix.

4. **Source code:** The pipeline is implemented in Python (767 lines). The Zenodo archive should include the full source code, not just artifacts.

**Recommendation:** Provide the full pipeline source code, exact prompt templates, model version identifier, and all generation parameters in the replication package. Add a Dockerfile or environment specification for full computational reproducibility.

---

## 7. Threats to Validity (§6, p. 12)

**Verdict: Adequately identified but insufficiently addressed.**

The paper's threats section is structured by Campbellian validity types, which is appropriate. The threats are correctly identified, but several require further discussion:

**Internal validity:**
- The paper notes that "MI changes may be influenced by factors beyond the intended tactic." This is a maturation threat (repositories may have changed in ways unrelated to the tactic). A control condition — e.g., re-running the pipeline with a "do nothing" prompt or random file extraction — would quantify the background rate of MI change from any LLM interaction.
- Regression to the mean: Repos with MI = 0 (extreme low values) are most likely to improve under any intervention. The paper's largest gains come from precisely these cases (MI = 0 files). This should be discussed.

**External validity (§6.2):**
- The single-model, single-language design is noted. The paper should also note that all repositories are open-source Python projects, which may differ systematically from industrial or closed-source codebases in structure, documentation, and modularity.

**Construct validity (§6.3):**
- The MI limitation is correctly identified. However, the paper should also discuss whether MI and its sub-metrics capture the same construct as the intended architectural tactics. For example, "Reduced Coupling" is a tactic targeting inter-module dependency — but MI measures intra-file complexity and is largely insensitive to coupling changes. This means the primary metric may be incapable of detecting the effect of one of the three tactics studied.

**Conclusion validity (§6.4):**
- The small sample is noted. The paper should also discuss the risk of Type II error (failing to detect a real effect due to insufficient power, especially in medium/large repository subgroups where N is small and effect sizes are near zero).

**Recommendation:** Add regression-to-the-mean discussion, a control/baseline condition, and an explicit mapping of each tactic to whether MI is theoretically capable of detecting its effect.

---

## 8. Specific Issues Requiring Correction

| # | Location | Issue | Severity |
|---|----------|-------|----------|
| 1 | §3.1 | Null hypothesis stated but no statistical test performed | **Critical** |
| 2 | §5.1 | Descriptive statistics only — no confidence intervals or p-values | **Critical** |
| 3 | §5.6 vs. §3.3 | Failure count inconsistency: 14 vs. 15 | **Major** |
| 4 | §3.3 | Dataset inclusion/exclusion criteria not specified | **Major** |
| 5 | §3.4, §5.5 | MI gaming confound (12/18 improvements = new MI=100 files) not quantitatively addressed | **Major** |
| 6 | §4.4 | Exact prompts not provided in paper or supplement | **Major** |
| 7 | §4.1 | Model version not fully specified (no Hugging Face ID, no checkpoint) | **Major** |
| 8 | §5.4 | Three-group tactic comparison without multiple comparison correction | **Minor** |
| 9 | §5.7 | Failure analysis does not compare failed vs. completed repos on covariates | **Minor** |
| 10 | §6 | No discussion of regression to the mean for MI=0 cases | **Minor** |

---

## 9. Suggestions for Strengthening the Paper

1. **Add inferential statistics.** Run a paired Wilcoxon signed-rank test on the 42 before/after MI pairs. Report W, p, and a standardized effect size. This is the minimum requirement for any paper claiming to evaluate a causal intervention.

2. **Report the end-to-end success rate explicitly.** The paper reports 42.9% (18/42 of completed), but the actual deployment success rate is 18/56 = 32.1%. Both figures should be presented, with the denominator clearly explained.

3. **Disaggregate the "stable" category.** Of 17 stable cases, 7 were planner failures (no code generated) and 3 had syntax errors. These are not "stable" — they are failures. Only the no-op modifications (7 cases) are true stable outcomes where code was changed but MI was unaffected. Reframe accordingly.

4. **Include a trivial baseline.** What ΔMI results from adding a single empty file, or from asking the LLM to "add one simple function" without any tactic guidance? This would calibrate the metric-arithmetic effect.

5. **Report file-level alongside repository-level MI.** The repository-level average dilutes effects in larger repos. File-level ΔMI for the specific files the LLM modified would be a more sensitive and interpretable measure.

6. **Compare failed vs. completed repositories.** A simple table comparing size, architecture type, and baseline MI between the 14 failed and 42 completed repos would assess whether attrition introduces bias.

---

## 10. Conclusion

The paper addresses an interesting and timely question — whether LLMs can implement architectural tactics — and presents a non-trivial, reproducible pipeline. The topic is relevant to EASE's evaluation and assessment focus. However, in its current form, the methodology falls short of the empirical standards expected at a conference like EASE:

- **No statistical inference** is performed on the primary research question.
- **Single metric (MI)** with acknowledged limitations is used without triangulation using the supplementary metrics that were collected.
- **25% attrition** is transparently reported but not rigorously analyzed for bias.
- **Single model, single language** design limits generalizability.
- **Metric-arithmetic confound** (adding MI=100 files inflates averages) is identified but not addressed quantitatively.

The paper would be significantly strengthened by adding inferential statistics, confidence intervals, a sensitivity analysis, and a more careful treatment of the MI gaming issue. With these additions, the paper could make a solid contribution as an early feasibility study. Without them, the empirical foundation is too weak to support the claims being made.

**Score: 60 / 100**

*Recommendation: Major Revision — the core idea and pipeline have merit, but the empirical methodology requires substantial strengthening before the paper meets EASE standards for evaluation research.*
