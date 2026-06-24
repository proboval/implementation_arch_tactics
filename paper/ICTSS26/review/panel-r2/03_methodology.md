# Reviewer Review (post-draft mode) — ROUND 2

**Reviewer profile:** methodology-examiner (R2 re-review)
**Persona:** Professor of Empirical Software Engineering; authority on controlled experiments, validity threats, and statistical reporting
**Target:** ICTSS 2026 conference paper — `paper/ICTSS26/main.tex` ("Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation")
**Date:** 2026-06-23
**Mode:** post-draft re-review
**Frame:** ICTSS 2026 (Springer LNCS, software-testing venue, double-blind, full paper ≤15pp)
**Prior decision (R1):** MAJOR REVISION

---

## Summary judgment

This is a substantially improved and, importantly, a **statistically trustworthy** revision. I re-derived every headline number directly from the released dataset (`paper/tactic_implementation/artifacts/improvement_maintainability_dataset.csv`, 56 data rows) and from the per-step test logs (`.../tactic_application/`, 20 repos / 121 steps). The recomputed inferential statistics are now **exactly** what the paper reports: Wilcoxon $W=81$, $p=0.0283$, matched-pairs rank-biserial $\hat r=0.502$, with the outlier-drop sensitivity falling to $p=0.083$ and the within-$\pm0.5$ share at 61.9% (26/42). The impossible/duplicated $W=473$ from R1 is gone and the zero-handling convention is now stated ("$\pm0.01$ tolerance treated as ties," §5.3 line 272). Every subgroup table (size, tactic, style) reproduces from the CSV cell-for-cell. The behavioral-gating denominators (28 applied / 208 steps; 20 logged / 121 steps; 0 regressions) reconcile against the artifacts. The test-adequacy claim has been correctly **demoted from a proven adequacy gap to a cautious null read** ("coverage unmeasured … a clean run cannot distinguish a behavior-preserving edit from one the suite simply never exercises," §5.3 line 266). This directly answers four of my five R1 MUSTs.

The remaining gap is the one the authors chose to defer: there is still **no positive control** proving the gate *can* fire. They now handle this honestly by not claiming the suites are inadequate as fact — they read 0/121 as *consistent with* a test-adequacy gap and explicitly flag coverage as unmeasured. That is a legitimate, venue-appropriate framing for a feasibility paper, and it converts the former fatal inference flaw into a candid, well-scoped limitation. It is no longer a blocking over-claim, though it does cap the strength of the testing contribution. I am moving this to **ACCEPT WITH MINOR REVISION**.

## Verification log (what I reproduced from the data)

| Paper claim (§/line) | Reported | Recomputed from dataset | Verdict |
|---|---|---|---|
| Wilcoxon on 42 pairs, ±0.01 ties (§5.3 l.272) | $W=81$, $p=0.028$, $\hat r=0.50$ | $W=81$, $p=0.0283$, $\hat r=0.502$ | ✅ exact |
| Bootstrap 95% CI mean ΔMI (§5.3 l.272) | [0.29, 2.98] | mean ΔMI = +1.484 (CI plausible; not re-bootstrapped without scipy) | ✅ consistent |
| Sensitivity, drop 2 outliers (§5.4 l.275) | mean +0.56, $p=0.083$ | mean +0.555, $p=0.083$ | ✅ exact |
| Within ±0.5 (§5.4 l.275) | 26/42 = 61.9% | 26/42 = 61.9% | ✅ exact |
| Classification, ±0.01 tol (Tab.1) | 18 / 17 / 7 | 18 / 17 / 7 (strict-0 would give 19/16/7) | ✅ tolerance drives the table, as stated |
| Mean ΔMI all / improved / worsened (Tab.2) | +1.484 / +3.716 / −0.653 | +1.484 / +3.716 / −0.653 | ✅ exact |
| Gating: applied / steps (§5.2 l.264) | 28 / 208 | 28 / 208 | ✅ exact |
| Gating: logged repos / steps / regressions (§5.2 l.264) | 20 / 121 / 0 | 20 / 121 / 0 | ✅ exact |
| Size/tactic/style subtables (Tab.4/5/6) | see tables | reproduced cell-for-cell | ✅ exact |
| ITT 18/56 (§5.1, §5.3 l.277) | 32.1% | 32.1% | ✅ exact |

The only number I could not independently re-derive without `scipy` is the bootstrap CI endpoint values, but the point estimate and resampling design are consistent and the rest of the suite checks out exactly; I have no reason to doubt the CI.

## Standing critical issue coverage

| ID | Issue | Status R1 → R2 | Evidence |
|---|---|---|---|
| **CRIT-1** | MI ≠ architecture-level maintainability; "architecture-aware" overclaim | ⚠️ → ✅ **Resolved** | The residual "architecture-aware pipeline" phrasing I flagged at §3.1 in R1 is **removed**. §5.7 (Table 7) shows package count and depth unchanged across all 42 repos, fan-out −0.17; §5.9 + §5.12 conclude "the pipeline operates at the code level, not the architecture level"; §6 construct validity states MI "cannot in principle capture … Reduced Coupling." Claim now matches evidence. |
| **CRIT-2** | File-splitting confound; no random-split baseline | ⚠️ **Partial (unchanged)** | Named and quantified honestly (§5.4 sensitivity erases significance; §5.5 size as dominant moderator; §5.6 "12 of 18 improvements extracted a new MI=100 module"; §6.1 proposes do-nothing/random-split control as future work). Confound is no longer hidden but is still not ruled out empirically. Acceptable for a feasibility paper that says so. |
| **CRIT-3** | Single-annotator ground truth; no κ | ❌ **Open (disclosed)** | §6.1 line 408: "Labels came from a single annotator (no inter-rater check)." Not fixed. Lower impact here since labels only feed the §5.8 subgroup split, but those style conclusions inherit unquantified label noise. |
| **CRIT-4** | No comparison/baseline condition | ❌ **Open (disclosed)** | No random-split, static-only, or human baseline; the prior LLM-inferred-label run (18.2%/+0.48) is used as a quasi-baseline but explicitly disclaimed ("not proof … datasets also differ," §3.7 l.136, §5.1 l.259). For the *testing* claim this baseline is the missing **positive control** (below). |
| **CRIT-5** | Overgeneralization from niche script repos | ✅ **Resolved (unchanged)** | Paper leads with the caveat: §5.5/§5.9 gains only on small repos; §5.10 "apply only to small repositories (<30 files)"; §6.2 scopes to Python backends. |

## R1 MUST items — disposition

| R1 MUST | R2 status |
|---|---|
| (P2) Impossible/duplicated Wilcoxon $W=473$ | ✅ **Fixed** — now $W=81$, reproduced exactly; zero-handling convention stated. |
| (P6) No-intervention zeros folded into the 42 | ✅ **Resolved adequately** — Wilcoxon drops ties so the 14/10 zeros do not enter the inferential test (verified: dropping changes nothing); §5.1 l.239 reports the treated-only rate (18/32 = 56.2%) and §5.3 l.277 reports ITT (18/56). The descriptive "42" is retained but now disambiguated. |
| (S3/S4) Test adequacy never measured; coverage absent | ⚠️ → ✅ **Claim now defensible** — paper explicitly states coverage of edited code was NOT measured (§5.3 l.266) and reads the null cautiously; no longer asserts a *proven* adequacy gap. |
| (S9) Non-determinism unreported | ⚠️ **Partial** — §6.1 now adds "A single model was used," and temp/top-p are given (§3.6), but the number of pipeline runs per repo and run-to-run ΔMI variance are still not stated. Each reported ΔMI remains a single stochastic draw at temperature 0.2. |
| (S2/P1) No positive control the gate can fire | ❌ **Open, now honestly scoped** — left to future work; the inference is correspondingly softened so it no longer over-claims. No longer a blocker, but it caps the testing contribution. |

## Persuasive effectiveness (delta from R1)

| # | Dimension | R2 status | Note |
|---|---|---|---|
| P1 | "0 regressions ⇒ test-adequacy gap" | ⚠️ → ✅ Adequate | The inference is now *cautious and falsifiable-in-principle*: the paper concedes it cannot distinguish behavior-preserving from never-exercised, and frames the gap as a hypothesis pointing to test generation. Honest. |
| P2 | Wilcoxon statistic | ❌ → ✅ Strong | $W=81$, $p=0.028$ reproduced exactly; tolerance/tie convention stated. |
| P3 | Effect size + CI | ✅ Strong (retained) | $\hat r=0.50$ + bootstrap CI + sensitivity + ITT. Exemplary candor. |
| P4 | Construct validity of "safe refactoring" | ⚠️ Honest | Title's question is, strictly, answered "we could not tell." §6.3 says so. Acceptable but the title slightly oversells; consider it a presentation point. |
| P5 | Denominator consistency (57/56/42/32) | ⚠️ Improved | §3.3 l.106 now states "57 … one unavailable, leaving 56, of which 42 produced paired measurements." Still four N's in play (57, 56, 42, 32); a reader must track them, but each is now defined where it appears. |
| P6 | "Stable" double-counts non-interventions | ✅ Resolved | §5.1 l.239 explicitly separates 7 genuine no-ops from 7 planner failures + 3 syntax errors and reports 18/32. |

## Defensibility vs. publishability

- **Defensible as the empirical core of an MS thesis?** **Yes.** The statistics are now reproducible from the released data, the threats section states the killer limitations first, and the central claims are proportionate to evidence. This clears the MS bar comfortably.
- **Publishable at ICTSS?** **Yes, after minor revision.** The four correctness/over-claim MUSTs from R1 are fixed. The remaining items (positive control, non-determinism, multiple-comparison note) are SHOULD-level for a feasibility paper that openly frames the null as a hypothesis rather than a finding. The contribution — a candid null result reframed as a test-adequacy hypothesis with a reproducible package — is a legitimate LNCS short/full paper. The one substantive caveat I would press at a testing venue is that the headline question ("Can regression tests catch unsafe refactorings?") is answered "we couldn't tell," and a single positive-control mutant on the 4–15 runnable-test repos would have turned "couldn't tell" into "demonstrably not on these suites." Strongly recommended, not required.

## Decisions required (R2)

1. **Positive control (SHOULD, was MUST):** Inject ≥1 known behavior-altering change into the repos with runnable suites to show the gate *fires*. Without it the title's question stays at "could not tell." Now optional because the paper no longer over-claims, but it is the single highest-value addition.
2. **Determinism (SHOULD):** State runs-per-repo (apparently one) and bound run-to-run ΔMI variance on a handful of repos; every reported figure is otherwise one draw at temp 0.2.
3. **Multiple comparisons (SHOULD):** Tables 4/5/6 plus the global test are many comparisons; add one sentence on family-wise risk / why no correction (small N, exploratory).
4. **Gating denominator "15" (MINOR):** §5.3 says a non-trivial suite "actually executed in only 15 repositories," but the per-step logs cover 20 repos and only ~4 show explicit pass/fail counts in stdout. Define operationally what "executed meaningfully in 15" counts (infra detected and ran without infra_error/timeout, presumably) so the three denominators (20 logged / 15 executed / 4 with visible counts) are not confusable.
5. **Title vs. construct (NICE):** Consider softening the title or adding a one-line scope note, since behavior preservation was never measured on any repo.

---

_Priority definitions:_
- **MUST:** blocks publication / central claim unsupported.
- **SHOULD:** significantly strengthens credibility; fix if feasible.
- **NICE / MINOR:** polish.
- **DEFER:** legitimately future work.
