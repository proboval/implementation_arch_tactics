# Reviewer Review (post-draft mode)

**Reviewer profile:** methodology-examiner (R1)
**Persona:** Professor of Empirical Software Engineering; authority on controlled experiments, validity threats, and statistical reporting
**Target:** ICTSS 2026 conference paper — `paper/ICTSS26/main.tex` ("Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation")
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** ICTSS 2026 (Springer LNCS, software-testing venue, double-blind, full paper ≤15pp+2ref). Reframed toward testing/behavioral validation.

---

## Summary judgment

The reframe is the right move and, methodologically, the most honest version of this work I have seen: the paper now leads with a **null result** (the regression gate caught 0 regressions across 121 steps) and interprets it as a *test-adequacy gap* rather than as a safety guarantee. That inversion — "a green gate means *untested*, not *safe*" — is a genuine, well-motivated, venue-appropriate contribution, and the statistical reporting around the MI result (Wilcoxon + bootstrap CI + outlier sensitivity + intention-to-treat) is markedly more rigorous and more candid than the thesis it derives from. The honesty is exemplary.

The blocking problem is that the paper's **headline claim (RQ2/RQ3, the test-adequacy gap) rests on a near-absence of measurement**, not on a measurement. Zero regressions were observed because tests "executed meaningfully" in only 15 repos and only 21 of 121 steps recorded *any* passing execution (§5.3, lines 272–274). The study therefore cannot distinguish "the gate works and the edits were safe" from "the gate had nothing to bite on" from "the gate was mis-wired" — and the design includes **no positive control** (no seeded/mutated regression to confirm the gate *can* fire). For a testing venue, demonstrating that your oracle detects a *known* fault is close to mandatory. With that one addition the central claim would be defensible. Without it, the inference from "0 detections" to "test suites are inadequate oracles" is confounded by the untested possibility that the gate itself never fires. **MAJOR REVISION.**

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Research design stated (pre/post, repo-as-own-control, H0, α) | ✅ Present | §3.1 lines 88–92 cleanly define IV, DV, H0, test, α, effect size, CI. Good. | — |
| S2 | Positive control that the regression gate *can* detect a regression | ❌ Missing | The central RQ2/RQ3 claim hinges on a 0-detection result, but nothing shows the gate fires on a *known* break (e.g., injecting a mutant or a deliberately behavior-altering edit on the 15 repos with runnable tests). Without it, "0 detections" is uninterpretable. | **MUST** |
| S3 | Operational definition + reliability of "tests executed meaningfully" / "no tests touching modified code" | ⚠️ Partial | §5.3 distinguishes "ran on 121 steps," "executed meaningfully in 15 repos," "21 steps recorded a passing execution" — three different denominators, none operationally defined. How is "touching the modified code" determined — coverage instrumentation, or inferred? If not measured by coverage, the test-adequacy claim is asserted, not demonstrated. | **MUST** |
| S4 | Coverage measurement of modified code paths | ❌ Missing | The test-adequacy gap is fundamentally a *coverage* claim ("suites were too sparse to exercise the modified code paths," line 274). Coverage of the edited lines/functions is the direct evidence for this and is never reported. This is the single measurement that would convert the claim from plausible to demonstrated. | **MUST** |
| S5 | Multiple-comparison control for subgroup analyses | ⚠️ Partial | Tables 4/5/6 (tactic, size, style) plus the global Wilcoxon constitute many comparisons; no Bonferroni–Holm or family-wise discussion. §6 acknowledges low power for N=3 subgroups but not the inflated Type-I risk of reporting the most extreme subgroup. | SHOULD |
| S6 | Reproducibility (model ID, params, prompts, parameters) | ✅ Present | §3.6 + Data Availability give exact model id, temp 0.2, top-p 0.9, rep penalty 1.1, 256k ctx, BM25 k1=1.5/b=0.75, iteration limits, 300 s timeout, replication package on Zenodo. Strong. | — |
| S7 | Attrition / selection-bias handling | ✅ Present | §5.11 lines 392–393 compares failed vs. completed on file count, architecture, baseline MI; honestly notes "too small for a formal test." Appropriate for the N. | — |
| S8 | Threats to validity, structured (internal/external/construct/conclusion) | ✅ Present | §6 covers all four buckets and states the killer limitations first (single annotator, MI≠coupling, significance vanishes without outliers, N=3 subgroup powerlessness). | — |
| S9 | LLM non-determinism bounded | ❌ Missing | temp=0.2 ≠ deterministic. No repeated-run variance, no statement of how many pipeline runs underlie each ΔMI. A single stochastic run per repo means every reported number is one draw from an unquantified distribution. | SHOULD |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | "0 regressions ⇒ test-adequacy gap" inference | ⚠️ Weak | The interpretation is plausible and honestly hedged ("does not establish edits were behavior-preserving," line 273), but the data underdetermine it. **Alternative explanations not ruled out:** (a) the gate never fires by construction (no positive control — S2); (b) the LLM edits genuinely *were* behavior-preserving on covered paths (the paper cannot exclude this and arguably should not want to); (c) baseline-failure subtraction logic masks regressions when baseline already had failures. Each is a competing cause of "0." | **MUST** |
| P2 | W=473 identical for N=42 and N=56 Wilcoxon | ❌ Unconvincing | Line 262 reports W=473, p=0.023 for the 42-pair test; line 267 reports W=473, p=0.087 for the 56-pair intention-to-treat test. The Wilcoxon statistic being **numerically identical** after adding 14 zero-difference pairs is a red flag. Standard Wilcoxon drops zeros, so adding 14 zeros *can* leave W unchanged — but then the p-value change comes only from the n used in the normal approximation, which should be stated. As written it reads like a copy-paste error or an undocumented variant. Must be verified and the zero-handling convention named. | **MUST** |
| P3 | Effect-size + CI reporting on the primary result | ✅ Strong | §5.2: rank-biserial r̂=0.35 with bootstrap 95% CI [0.21, 3.04] for mean ΔMI, plus the outlier-removal sensitivity (p=0.156, r̂=0.17) and ITT (p=0.087). This is exactly the candor an examiner wants — the result is reported *with* its fragility. | — |
| P4 | Construct validity of the safety claim | ⚠️ Weak | The paper claims to study "behavioral gating," but behavior preservation is never *measured* on any repo — the gate's verdict was vacuous on ≥106/121 steps. The construct "safe refactoring" is operationalized only as "no new test failure," and the paper itself concedes that operationalization failed. This is honestly stated (§6 construct validity, line 411) but means the title's question is, strictly, answered "we could not tell" rather than "no." | SHOULD |
| P5 | Numeric/denominator consistency across abstract, methodology, results | ⚠️ Weak | Abstract says "56 projects" (line 39); §3.3 says dataset is 57 labeled repos, one unavailable → 56 (lines 100–105). Consistent once read carefully, but the abstract/intro "56" vs. methodology "57→56" should be reconciled in one sentence up front. Also §3.1 line 92 says "two-sided paired Wilcoxon on the **42** before/after MI pairs" while §3.3 describes the 56/57 framing — fine, but a reader meets three N's (57, 56, 42) before the outcome table explains them. | SHOULD |
| P6 | "Stable" category double-counts planner failures | ⚠️ Weak | Table 1 lists "Planner failure 7" and "Syntax error 3" *under* "Stable / completed" (lines 227–229), and the text treats all 42 as having "paired before/after measurements" (line 214). A planner failure that produced no edit trivially has ΔMI=0, so including it as a "completed pair" inflates the denominator of the Wilcoxon with 10 structural zeros that are not "no-change outcomes" but "no-intervention" outcomes. This materially affects the test (those 10 zeros are dropped by Wilcoxon but counted in the descriptive "42"). The improvement rate is honestly re-stated as 18/32 (line 238); the *inferential* test should likewise be reported on the 32 genuinely-treated repos, or the inclusion of non-treated zeros justified. | **MUST** |

## Standing critical issue coverage

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| **CRIT-1** | MI ≠ architecture-level maintainability, yet framed as "architecture-aware" | ⚠️ Partial | Largely **defused by reframing**: §5.7 adds fan-out/package-count/depth (Table 7) and §5.9 explicitly concludes "the pipeline operates at the code level, not the architecture level"; §6 construct-validity para states MI "cannot in principle capture Reduced Coupling." This is the right fix. **But** §3.1 line 88 still calls it "the architecture-aware maintainability improvement pipeline" — residual overclaim; reconcile with the §5.9 conclusion. |
| **CRIT-2** | File-splitting confound; no random-split baseline | ⚠️ Partial | Now **named and quantified honestly**: §5.5 (Table 5, size as dominant moderator), §5.5 case studies (webapp-color "artifact of small size," line 284), §5.9 "largely metric arithmetic." §6 internal validity proposes a "do-nothing/random-split control" — but as **future work**, not done. The confound is no longer hidden, yet still not ruled out empirically. |
| **CRIT-3** | Single-annotator ground truth; no inter-rater reliability | ❌ Open | §6 internal validity line 407: "Labels came from a single annotator (no inter-rater check)." Honestly disclosed, **not fixed**. No Cohen's κ. For this paper the labels enter only as Phase-2 input (architecture style → subgroup analysis in Table 6), so the impact is lower than in the thesis, but the script/layered/modular-monolith subgroup conclusions (§5.8) inherit unquantified label noise. |
| **CRIT-4** | No comparison/baseline condition | ❌ Open | No random-split, static-only, or human-developer baseline. §3.7/§5.1 use the *prior LLM-inferred-label run* (18.2%, +0.48) as a quasi-baseline, but explicitly disclaim it ("not proof… since the datasets also differ," lines 135, 258). So results show absolute capability, not relative effectiveness. For the **testing** claim, the missing baseline is the **positive control** (S2) — the most damaging absence. |
| **CRIT-5** | Overgeneralization from niche script repos | ✅ Resolved | The paper now *leads* with this caveat: §5.4–5.6 show gains concentrate in tiny/script repos, §5.9 "measurable gains only on small repos," §5.10 practice implication "apply only to small repositories (<30 files)," §6 external validity scopes to Python backends. Generalization is appropriately narrowed. |

## Defensibility vs. publishability

- **Defensible (as the empirical core of an MS thesis)?** Yes after MUST items. The honesty, the structured threats section, and the candid statistics clear the MS bar; the construct-validity reframe (CRIT-1/5) is the standout improvement. The open items are about *strengthening an inference*, not rescuing a collapsed claim.
- **Publishable at ICTSS as-is?** No — after major work. For a *testing* venue the central testing claim must be backed by (a) a positive control proving the gate fires (S2/P1), and (b) coverage evidence for the "suites too sparse" claim (S4). The W=473 anomaly (P2) and the planner-failure denominator issue (P6) are correctness bugs in the stats that a methods referee will catch immediately. Fix those four and this is a credible LNCS short/full paper: the null result is interesting and the framing is sound. The contribution is real; the evidentiary chain to it is currently one link short.

## Decisions required

1. **Positive control (gate validity):** Will you inject ≥1 known behavior-altering change (or a small mutation set) into the 15 repos with runnable tests to demonstrate the regression gate *can* fire? Without this, "0 regressions" cannot be distinguished from "gate never fires," and the headline claim is unfalsifiable. (MUST)
2. **Coverage evidence:** Will you report coverage (line/branch) of the LLM-modified code paths under each repo's existing suite? This is the direct measurement of the "test-adequacy gap" you currently infer. (MUST)
3. **Wilcoxon W=473 twice:** Verify and explain why the test statistic is identical for N=42 (p=0.023) and N=56 (p=0.087); state the zero-handling convention (drop vs. Pratt). If it is an error, correct it. (MUST)
4. **Inferential denominator:** State whether the Wilcoxon is computed over all 42 "completed" pairs (including 10 planner-failure/syntax zeros that received no real intervention) or over the 32 genuinely-treated repos; justify the choice and report the test on the treated set. (MUST)
5. **Determinism:** With temperature 0.2, how many pipeline runs per repo underlie each ΔMI? If one, add a statement bounding run-to-run variance (even on a handful of repos), since every reported figure is otherwise a single stochastic draw. (SHOULD)

---

_Priority definitions:_
- **MUST:** blocks the defense or makes a central claim unsupported — fix before defending/publishing.
- **SHOULD:** significantly weakens credibility/quality — fix if feasible.
- **NICE:** strengthens the paper — optional polish.
- **DEFER:** legitimately out of scope — note as future work.
