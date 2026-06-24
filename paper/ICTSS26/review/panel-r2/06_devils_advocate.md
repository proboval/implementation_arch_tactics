# Reviewer Review (post-draft mode) — ROUND 2 RE-REVIEW

**Reviewer profile:** devils-advocate
**Persona:** Rigorous critical empiricist (Briand-style inference dismantler)
**Target:** ICTSS 2026 submission — "Can Regression Tests Catch Unsafe LLM Refactorings?" (`paper/ICTSS26/main.tex`, revised)
**Date:** 2026-06-23
**Mode:** post-draft, round-2 re-review
**Frame:** Conference paper, ICTSS 2026 (Springer LNCS, software *testing* venue, double-blind, ≤15pp).

---

## Verdict up front

**Do any of my round-1 CRITICALs still stand as CRITICALs? NO.** Both C-1 and C-2 are downgraded to MAJOR. The revision did the one thing that can legitimately defuse an over-read-of-a-null objection: it stopped over-reading. The paper now (a) states outright that coverage of edited code was not measured, (b) states that a clean run "cannot distinguish a behavior-preserving edit from one the suite simply never exercises," (c) reads the null as *evidence of* (not *proof of*) a test-adequacy gap, and (d) parks the positive control as future work. A claim that openly concedes its own key limitation is no longer an over-claim — it is a bounded, honest observation. **No CRITICAL blocks ACCEPT under the checkpoint rule.**

That said, the *body* (§5.2, §6, §7-Threats) has been disciplined while the *abstract and conclusion still carry the round-1 strong framing*. That residual gap is now the main lever — but it is a MAJOR (re-scope the abstract), not a CRITICAL, because the body itself no longer supports the over-read and a careful reader is correctly warned.

## Standing critical issue coverage (round-2)

| ID | Round-1 | Round-2 | Evidence |
|---|---|---|---|
| CRIT-1 (MI ≠ architecture-level) | ✅ largely | ✅ Resolved | §5.9, §5.10 ("operates at the code level, not the architecture level"), Threats-construct; "architecture-aware" phrase is gone from §3.1 |
| CRIT-2 (file-splitting confound / no baseline) | ⚠️ partial | ⚠️ Partial | Confound named (§5.3 sensitivity, §5.10) and a do-nothing/random-split control explicitly promised as future work (Threats-internal); still no control run |
| CRIT-3 (single annotator) | ❌ open | ⚠️ Acknowledged | Threats-internal concedes "single annotator (no inter-rater check)"; bounded |
| CRIT-4 (no oracle-quality baseline) | ❌ open / central | ⚠️ Partial | Adequacy still not *measured*, but the paper no longer claims it was; positive control deferred (Threats, §5.2). Demoted from central gap to honest open item |
| CRIT-5 (overgeneralization) | ⚠️ partial | ⚠️ Partial | §5.2 now scopes the null to "20 ... 15 repositories"; but abstract/§7 still generalize to "the chief obstacle to trusting AI-driven code changes" field-wide |

---

## 1. Strongest counter-argument (round-2) — and why it no longer reaches CRITICAL

My round-1 attack was: *the headline is a positive interpretation of a null the design cannot support.* That attack required the paper to be asserting the adequacy-gap explanation **over** the rival safe-edit and no-measurement explanations. The revised §5.2 no longer does this. It now states the null "does not establish that the edits were behavior-preserving," that coverage was unmeasured, and that the result is read "cautiously — as evidence of a test-adequacy gap ... rather than as proof of safe transformation." That is precisely the epistemic hedge whose absence made it a CRITICAL. The safe-edit rival is also now implicitly conceded everywhere the paper insists the edits were trivial (MI=100 extractions, §5.5; structure unchanged, §5.10) — the authors are not hiding the alternative, they are foregrounding it. **When a paper concedes that its null is consistent with both "untested" and "safe-but-trivial," the over-claim is gone.** What remains is a defensible, modest claim: *a green run of a sparse OSS suite is weak evidence of safety, and in our sample the suites rarely reached the edits.* That is true, bounded, and the right message for a testing audience.

**The strongest *remaining* attack is therefore not about validity but about contribution weight and framing consistency:**

1. **The body and the abstract now disagree.** §5.2/§7-Threats say "we cannot distinguish untested from safe." The abstract says "for a troubling reason: the projects' existing tests rarely exercised the AI's changes" and "Our main finding is that the chief obstacle ... is not the AI itself but the shortage of tests." The conclusion says "More importantly, the regression gate could not actually validate the changes." The qualified body sentence and the unqualified abstract sentence are in tension: the abstract still selects the adequacy-gap world as *the* explanation. This is a framing-honesty MAJOR (§7, Abstract vs. §5.2), cheaply fixed by importing the §5.2 hedge into the abstract/conclusion.

2. **Selective-reporting check on 20/121 vs 28/208 (NEW — does the restriction bias the result?).** I specifically examined whether restricting the testing analysis to the 20 repos / 121 logged steps, when 28 repos / 208 steps actually received changes, manufactures the null. It does **not** make the null worse for the authors — it makes it *weaker for the authors*, which is the honest direction: the 8 unlogged repos / 87 unlogged steps are dropped from the "gate never fired" count, so the claim is made on *less* data, not cherry-picked data. Crucially the direction of the headline (0 regressions) cannot be inflated by excluding steps — excluding steps can only *reduce* the evidentiary base, and the paper says so ("15 repositories ... the rest either lacked a runnable suite or exposed no tests touching the modified code"). So this is not a selective-reporting *validity* problem. **But** it does sharpen the contribution-weight problem: the field-level claim now rests on an even smaller informative base (15 repos with real execution), which is a MAJOR on external validity / generalization, not a CRITICAL.

3. **Is the softened claim now too weak to be a contribution? (The genuine round-2 risk.)** This is the real danger of the revision and I press it: if the headline reduces to "a passing run of a sparse test suite is weak evidence of safety," that is *prior knowledge* (the oracle problem; decades of coverage studies; the paper's own §2.3). The paper survives this only on the narrow, novel sliver: it is — to my knowledge from §2.3 — the first to *integrate* a regression gate into an LLM architectural-tactic pipeline and to *empirically show the gate is starved of signal for cross-module edits on real repos*. That is a thin but real contribution for a testing venue, and the honest negative framing is appropriate. It is, however, feasibility-grade, not a definitive finding — and the paper now says exactly that (Threats-conclusion: "early feasibility evidence, not definitive performance claims"). So the contribution is *thin but honest*, which is acceptable for a workshop/conference negative-result slot. MAJOR-bordering-MINOR: the abstract oversells thinness as "main finding."

## 2. Issue list (round-2, severity-ranked)

| # | Severity | Issue | Location | One-line |
|---|----------|-------|----------|----------|
| R2-1 | ~~CRITICAL~~ → **MAJOR** | Null still framed as *the* adequacy gap in abstract/conclusion, though §5.2 hedges it | Abstract, §7, §5.2 | Import the §5.2 "cannot distinguish untested from safe" hedge into the abstract and conclusion so framing matches the body. |
| R2-2 | ~~CRITICAL~~ → **MAJOR** | Adequacy still asserted, never *measured* (no coverage-of-modified-lines, no mutation, no positive control) | §5.2, §4-Phase4, Threats | Deferred honestly, but for a *testing* venue the obvious instrument is still absent; coverage of modified lines is cheap and would convert "untested" into a measured quantity. |
| R2-3 | **MAJOR** | Field-level generalization from 15 repos with real test execution | Abstract, §7, §5.2 | "Chief obstacle to trusting AI-driven code changes" generalizes from a single-model, single-language, ~15-repo informative base. Re-scope to the sample. |
| R2-4 | **MAJOR** | Thin/known core claim; novelty rests only on the integration + cross-module signal-starvation sliver | §2.3, §5.2 | Make explicit what is *new* vs. the long-known under-testing of small OSS; isolate the cross-module-edit-specific contribution. |
| R2-5 | **MAJOR** | File-splitting / regression-to-the-mean confound still has no control run | §5.3, §5.10, Threats | Do-nothing/random-split baseline promised but not run; significance already vanishes on outlier removal (p=0.083), so the MI result is fragile feasibility evidence. |
| R2-6 | MINOR | Self-healing deflation of the 0/121 still undiscussed | §4-Phase4 | Up to two self-healing retries can silently repair a caught regression before a step terminates; the 0 is partly a loop artifact, not only test sparsity. Note it. |
| R2-7 | MINOR | Number consistency: abstract "56 projects" vs dataset "57 labeled (one unavailable → 56)" | Abstract, §3.3 | Now internally reconcilable but still reads as two figures; state once. |
| R2-8 | MINOR | Stat correction is right but unflagged | §5.3 vs prior version | W=81, p=0.028 is now plausible (round-1 W=473 was impossible for N≈42); good, but confirm the rank-biserial r̂=0.50 and the bootstrap CI [0.29, 2.98] are recomputed from the same corrected ranks, not carried over. |

> Per the checkpoint rule: **no CRITICAL remains; nothing blocks ACCEPT on my lens.** The decision is now an editorial weighing of a thin-but-honest contribution against ICTSS's bar — not a validity veto.

## 3. Ignored alternative explanations (status)

The safe-edit, edits-missed-tested-code, and no-measurement rivals are now **acknowledged** in §5.2 ("cannot distinguish a behavior-preserving edit from one the suite simply never exercises"). Still unaddressed: **self-healing deflation** (R2-6) and **selection toward under-tested hobby repos** (the 10-star/5-file filter, §3.3) — the latter means the adequacy gap may partly reflect dataset selection rather than OSS suites broadly; the abstract's field-level claim should concede this.

## 4. Missing stakeholder perspectives

Largely the same asks, but they are now *future-work requests* rather than *acceptance blockers*: the testing researcher and mutation-testing community still want a positive control + adequacy metric; the paper now correctly points them there. Large-repo maintainers remain out of scope (§ Threats-external, scope to <30 files).

## 5. Observations (genuine strengths)

- The revision is a model of how to defuse a null-result over-read: it removed the inflation rather than adding spin. §5.2's "evidence of, not proof of" is exactly right.
- Restricting the testing claim to the *logged* 20/121 subset is the honest direction (reduces, not inflates, the base) and pre-empts a selective-reporting charge.
- The statistical correction (W=81, p=0.028; outlier-removal p=0.083) and the consistent ITT-vs-per-protocol reporting remain exemplary.
- The supplementary architecture-metric table (unchanged package count/depth) continues to be the paper's most trust-building element — it self-refutes any architecture-level over-claim.

## Defensibility vs. publishability

- **As a testing-venue contribution now?** Borderline-acceptable as honest feasibility / negative-result work, contingent on R2-1 and R2-3 (align abstract/conclusion with the hedged body and re-scope the generalization). No validity CRITICAL remains.
- **What would lift it from borderline to clear accept:** coverage-of-modified-lines per step (R2-2) and a do-nothing baseline (R2-5) — both already named as future work; doing even one in-paper would convert the thin claim into a measured one.

## Decisions required (editorial)

1. **R2-1 (framing):** Will the authors propagate the §5.2 hedge ("cannot distinguish untested from safe") into the abstract and conclusion so the headline stops asserting the adequacy gap as *the* explanation?
2. **R2-3 (scope):** Will the abstract's "chief obstacle to trusting AI-driven code changes" be re-scoped to the ~15-repo, single-model sample?

---

_I do not issue a decision. Per the checkpoint rule, **no CRITICAL stands after round 2** — C-1 and C-2 are downgraded to MAJOR. ACCEPT is no longer blocked on my lens; the remaining issues are framing/scope MAJORs the editorial phase should weigh against the venue bar._
