# Methodology Examiner Review (R1)

**Reviewer:** Empirical-SE methods professor (controlled experiments, validity, statistics, reproducibility)
**Target:** diploma/v3 — emphasis on Ch.3 (Methodology), Ch.4 (Implementation), Ch.5 (Evaluation), Appendix
**Date:** 2026-06-17
**Mode:** post-draft
**Frame:** Innopolis MS defense (+ publishability flagged)

---

## Summary judgment

The statistical apparatus is now solid for an MS thesis and, in places, better than many published papers: a Shapiro-Wilk check motivates the non-parametric choice, the Wilcoxon test reports W/p/r, bootstrap BCa 95% CIs accompany the means, the sensitivity analysis honestly reports that significance is outlier-driven, and the multiple-comparison family-wise error is computed and bounded. Credit where due. My concerns are concentrated in the three areas the author flagged — **reproducibility**, **project selection**, and **methodological design** — and they are real but mostly addressable by writing and one or two computations, not by re-running everything.

The single most important methodological finding: **the thesis promises architecture-level metrics in §3.10.4 that the results chapter never reports** (R1-T4), and **the headline 18.2%→42.9% comparison is confounded by using different repository populations** (R1-M2). Those two are MUST. The reproducibility gaps (R1-R1..R5) are individually SHOULD but collectively determine whether anyone can replicate this.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Hypothesis, IV/DV defined | ✅ Present | §3.1: clean H₀, each repo its own control. Good design choice. | — |
| S2 | Statistical tests appropriate & justified | ✅ Present | Wilcoxon + rank-biserial + bootstrap CIs + Shapiro-Wilk. Appropriate throughout. | — |
| S3 | Sensitivity / robustness | ✅ Present (Study 1) | §5.2.2 is exemplary honesty. **But absent for Study 3**, which has the same +21.98 outlier (webapp-color) in its N=42 (R1-M3). | SHOULD |
| S4 | Reproducibility package | ⚠️ Partial | Raw LLM outputs preserved (good, §4.7). But prompts, model snapshots, tool versions, dataset manifests, and an artifact link are missing (R1-R1..R5). | MUST (collectively) |
| S5 | Dataset descriptive statistics | ❌ Missing | No size/age/domain distribution for the 162 or the 57. Sizes appear only as Study-3 bins (Table, §5.5). A reader cannot judge representativeness. | SHOULD |

## Persuasive effectiveness / technical soundness

| # | Issue | Status | Detail | Priority |
|---|-------|--------|--------|----------|
| **R1-T1** | **MI aggregation = unweighted file mean** | ❌ Weak | §3.6.1: "mean MI across all analyzed Python files." This is the mechanism behind the entire file-splitting artifact you diagnose in §5.6. Adding a trivial `config.py` (MI=100) raises the *mean* regardless of architecture. **A LOC-weighted MI is computable from the data you already have and would neutralize the artifact as a robustness check.** Reporting ΔMI both unweighted and LOC-weighted would convert §5.6 from "we admit the metric is confounded" into "we quantified the confound and show the effect under a weighting that removes it." This is the highest-value technical fix in the thesis. | MUST |
| **R1-T2** | **Architecture-level metrics promised, not delivered** | ❌ Missing | §3.10.4 explicitly promises cyclic-dependency ratio, inter-module coupling intensity, and package-tangle % computed before/after for the 42 Study-3 repos. §5.6 reports only file count, package count, directory depth, fan-out. The three promised metrics never appear. This is the exact remedy the prior review demanded for CRIT-1; the method says it was done but the results don't show it. Either report them or remove the promise. | MUST |
| **R1-T3** | **Failure taxonomy inconsistent between studies** | ⚠️ Weak | Study 1's 25.3% failures are *syntax/import* errors introduced by the LLM (§5.2.1). Study 3's "25.0%" are 14/56 *cloning* failures (§5.5.1) — an environmental problem unrelated to pipeline quality. Two different phenomena are reported as the same headline rate. Cloning failures should be reported separately (and ideally retried) so the LLM-induced failure rate is comparable across studies. Also: 57 labeled → "56 processable" drops one repo with no explanation. | SHOULD |
| **R1-T4** | **Test-suite coverage unreported** | ⚠️ Weak | The self-healing loop runs tests "where available" (§4.6.2, App). But the thesis never says *how many* repos had usable test suites. If few do, behavioral preservation is effectively absent for most of the dataset, which materially weakens every "improvement" claim. Report the fraction of repos with executable tests. | SHOULD |
| **R1-T5** | **Study 3 lacks a significance test** | ⚠️ Weak | Study 1 gets W/p/r; Study 3 (Table §5.5) reports only mean + CI [+0.26, +3.51]. The CI lower bound is near zero and the +21.98 outlier is present. Give Study 3 the same Wilcoxon + sensitivity treatment as Study 1, or state why not. | SHOULD |

## Reproducibility (focus area)

| # | Issue | Status | Detail | Priority |
|---|-------|--------|--------|----------|
| **R1-R1** | Prompts not included | ❌ Open | §3.7 and §4.4 describe prompt *structure* (allowed labels, JSON schema fields) but the verbatim prompts (system instruction, taxonomy definitions, tactic-selection and implementation prompts) are nowhere. These are the experiment. Put them in an appendix or the artifact repo and reference them. Without them, Study 2's evidence-type findings cannot be reproduced. | MUST |
| **R1-R2** | Model versions not pinned | ❌ Open | §3.8 / §4.4: `qwen3-coder-next:cloud` and the five Study-2 models (DeepSeek-v3.2, Gemini-3-flash-preview, Gemma4, MiniMax-M2.7) are named by moving cloud tags with no snapshot date or version hash. Cloud models behind a tag change silently; §4.7 acknowledges this and preserves raw outputs (good) but does not record *which* snapshot produced them. Record collection dates and any available version identifiers. | SHOULD |
| **R1-R3** | Tool versions not stated | ❌ Open | Radon version is not given (§3.6.1, §4.3). MI formula coefficients have changed across Radon releases; the absolute MI numbers are version-dependent. Pin Radon (and Python 3.12 patch, BM25 library) versions. | SHOULD |
| **R1-R4** | GitHub query not specified | ❌ Open | §3.3 / §4.2: "GitHub Search API … predefined search criteria." The exact query string, the collection date, the sort/ranking, how many results were screened, and how 162 (and 57) were arrived at from the raw hits are all absent. This is both a reproducibility and a selection-validity gap (see R1-S*). | MUST |
| **R1-R5** | Dataset not frozen/enumerated | ❌ Open | Shallow clone `--depth 1` (§3.4 step 1, App) captures whatever the default branch HEAD was *on the collection date*. Without per-repo commit SHAs, the exact inputs are unrecoverable even from the same URLs. Provide a manifest: repo URL + commit SHA + label for all 162 and all 57. | MUST |

## Choice of projects to analyse (focus area)

| # | Issue | Status | Detail | Priority |
|---|-------|--------|--------|----------|
| **R1-S1** | `requirements.txt` hard filter biases the sample | ⚠️ Acknowledged, under-analyzed | §6 Limitations correctly notes this excludes poetry/pipenv/pyproject projects and skews toward "older or less modern" repos. The deeper problem: older/unstructured repos are exactly where trivial decomposition gains are easiest, so **the selection criterion may manufacture the headline finding** ("script-based repos are the sweet spot"). At minimum, discuss this interaction explicitly; ideally, report the MI/size distribution of the included sample to show whether it is skewed low. | SHOULD |
| **R1-S2** | Relationship between the 162 and the 57 unstated | ❌ Open | Are the 57 manually-labeled repos a subset of the 162, or independently collected? §5.1 says "different datasets because they answer different questions" but never states whether they overlap. This is essential for R1-M2 (the 18.2%→42.9% comparison) and for judging whether Study 2's accuracy transfers to Study 1's population. | MUST |
| **R1-S3** | Tiny per-cell N | ⚠️ Weak | Several reported conclusions rest on single-digit counts: Study 1 Layered N=3 completed (flagged, good); Study 3 Script N=7, Reduced Coupling N=3, Layered N=9; Study 2 Script N=8, Layered N=16. Conclusions like "Layered shows the highest improvement rate (6 of 9)" and "Reduced Coupling is the worst tactic (3 repos)" must be stated as suggestive, not as findings. §5.13 (Conclusion validity) covers this generally but specific claims in §5.5 read stronger than N supports. | SHOULD |

## Methodological design

| # | Issue | Status | Detail | Priority |
|---|-------|--------|--------|----------|
| **R1-M1** | Single run per condition | ⚠️ Acknowledged | temperature 0.2 (not 0) leaves residual stochasticity; each prompt run once per model (§5.12.1). For at least the best model, run the detection N×3–5 and report variance — otherwise the 70.2% is a point estimate of unknown stability. | SHOULD |
| **R1-M2** | Confounded label-quality claim | ❌ Open | "Validated labels raise improvement 18.2%→42.9%" (§5.5, §6 Obj.4) compares Study 1 (162 repos, LLM labels) with Study 3 (57 repos, human labels). The populations differ, so the gain may be dataset composition, not label quality. Without a within-sample comparison (same repos, LLM-label vs human-label arm), this is correlational at best. Either run the within-sample comparison or restate as a hypothesis consistent with the data. | MUST |
| **R1-M3** | Study 3 sensitivity analysis missing | ⚠️ Weak | webapp-color (+21.98) sits in Study 3's N=42; without the same leave-out check as Study 1, the +1.484 mean and its CI are not shown to be robust. | SHOULD |

## Standing critical issue coverage
- **CRIT-1** ⚠️ — reframing done; **but R1-T2 (promised metrics missing) and R1-T1 (no LOC-weighted MI) leave the construct fix incomplete.**
- **CRIT-2/4** ❌ — no baseline. The LOC-weighted MI (R1-T1) is a partial, cheap substitute that directly tests the mechanical-splitting hypothesis; a random-split baseline is the full fix.
- **CRIT-3** ❌ — single annotator, κ not measured. For an MS defense, acknowledging is defensible; for publication, run a 20–30 repo second-annotator subset oversampling modular-monolith.
- **CRIT-5** ✅.

## Defensibility vs. publishability
- **Defensible?** Yes, once R1-T2 (deliver or withdraw the promised metrics) and R1-M2 (de-confound the label claim) are fixed in text, plus the reproducibility manifest (R1-R4/R5). These are writing/computation tasks, not new studies.
- **Publishable?** Needs R1-T1 (LOC-weighted robustness), the baseline (CRIT-2), and the second annotator (CRIT-3).

## Decisions required
1. **R1-T2:** Were the §3.10.4 architecture-level metrics actually computed? If yes, add the table; if no, remove the methodological promise. The panel cannot evaluate a method whose results are absent.
2. **R1-T1:** Will you add a LOC-weighted ΔMI as a robustness column? (Strongly recommended — cheap, decisive.)
3. **R1-S2/M2:** State the overlap between the 162 and the 57, and either de-confound or re-word the 18.2%→42.9% claim.
