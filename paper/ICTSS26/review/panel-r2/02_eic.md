# Reviewer Review (re-review, round 2)

**Reviewer profile:** eic (Editor-in-Chief / committee chair)
**Persona:** Editor of a leading SE venue; authority on architecture, refactoring, design patterns (Fowler-type lens)
**Target:** ICTSS 2026 submission (revised) — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** re-review (round 2)
**Frame:** ICTSS 2026 (Springer LNCS, software-testing venue, ≤15 pp + 2 ref, double-blind). Round-1 verdict: MAJOR REVISION.

---

## Summary judgment

The revision is a substantial, intelligent response and the paper has clearly moved up. The authors did the two hardest things round 1 demanded: they **softened the central claim from a proven adequacy gap to a cautiously-read test-adequacy *gap hypothesis*** (§5.2 ll.264–268), and they **restructured §5 to lead with the testing result** (§5.2 "Behavioral Gating and Test Adequacy" now precedes the inferential statistics, with an explicit signpost at l.263). The statistics catastrophe is fixed — the impossible W=473 is gone, replaced by an internally consistent and now-reproducible W=81, p=0.028, r̂=0.50, CI [0.29, 2.98], with an honest sensitivity collapse to p=0.083 (§5.3 ll.271–275). Behavioral gating is reconciled to the real dataset (28 repos / 208 steps; logs for 20 / 121 steps; real suite in 15; 0 regressions; coverage explicitly **not** measured — §5.2 l.264–266). A genuine §2.3 oracle/test-gen related-work subsection now exists (ll.74–75). Double-blind anonymization is applied (header ll.27–31; Data Availability l.436). This is a credible, venue-appropriate paper.

What still blocks ACCEPT is what blocked it in round 1, now correctly demoted but not eliminated: the headline contribution is **inferred from a null, not measured**. The authors chose the "reframe" path over the "positive control + coverage" path (roadmap fourth batch confirms this was a deliberate decision). That reframe is honest and legitimate, but it converts the paper's promised contribution from "we show existing suites are inadequate oracles for LLM architectural edits" into "we observed 0/121 regressions and *cannot tell* whether that means safe or untested." A testing-venue reviewer will note that the strong, citable result the title implies is still not delivered — and one cheap experiment (coverage.py on the diffed files) would deliver it. Combined with the unchanged file-splitting confound (no baseline), this lands the paper at the **top of MAJOR / borderline MINOR**.

**Provisional decision: MAJOR REVISION (borderline MINOR), improved from round 1.** The reframe lifts the central over-claim that the panel upheld as CRITICAL, so the strict checkpoint block is released; but the contribution remains diagnostic-without-instrumentation, and CRIT-2/CRIT-4 are still open. One coverage run would, in my judgment, move this to MINOR/ACCEPT.

## Movement vs. round 1

| Round-1 demand | Status | Evidence |
|---|---|---|
| Restructure §5 to lead with testing | ✅ Resolved | §5.2 testing precedes §5.3 stats; signpost l.263 |
| Fix the impossible Wilcoxon statistics | ✅ Resolved | §5.3 ll.271–272 W=81, p=0.028, r̂=0.50, CI [0.29,2.98] |
| Reconcile behavioral gating to dataset | ✅ Resolved | §5.2 ll.264–266 (28/208, 20/121, 15 real, 0 triggers) |
| Soften the central adequacy claim | ✅ Resolved | §5.2 ll.266–267 "does not establish… read cautiously" |
| Add test-oracle / LLM-test-gen related work | ✅ Resolved | §2.3 ll.74–75 (Barr, Chen, CodaMosa, Schäfer) |
| State classification tolerance, ITT | ✅ Resolved | §3.4 l.116 (ΔMI>0.01); ITT via 32.1% (§5.1 l.215, §5.3 l.277) |
| Double-blind anonymization | ✅ Resolved | header ll.27–31; Data Availability l.436 |
| Compact 26→17 pp | ✅ Resolved | LNCS, well within 15 pp |
| **Operationalize/measure adequacy (positive control + coverage)** | ❌ Open | Deliberately deferred (§6 l.408; future work l.424) |
| **File-splitting confound: random-split baseline** | ❌ Open | Named (§5.3 l.275; §5.10 l.400) but not controlled |
| Second annotator + κ | ❌ Open | §6 l.408 "single annotator (no inter-rater check)" |

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Problem framed as a testing problem | ✅ Present | Intro §1 ll.47–49 lands validation-not-generation cleanly. Strong fit. | — |
| S2 | RQs aligned to venue | ⚠️ Partial | RQ1 (§1 l.53) is still a co-equal maintainability question the paper later calls "a weak proxy" (§5.8 l.383; §5.10 l.400). Reads as legacy; consider demoting to a precondition. | SHOULD |
| S3 | Method for the gating mechanism | ✅ Present | §4.4 ll.202–203 concrete: baseline capture, snapshot/apply/re-run, rollback, two self-heal attempts. | — |
| S4 | Test-adequacy **measurement** | ❌ Missing | The central claim is suites are inadequate oracles, yet adequacy is never instrumented. No line/branch coverage on modified files. §5.2 l.265 says coverage "unmeasured" — honestly admitted, but it is precisely the missing evidence. A coverage.py run on the diffed files is cheap and is the single thing that would convert the null into a result. | MUST |
| S5 | Threats to validity | ✅ Present | §6 ll.408–414 honest across internal/external/construct/conclusion; oracle gap, single annotator, single model, outlier-driven significance all admitted. | — |
| S6 | Reproducibility | ✅ Present | §Data Availability l.436: model ID, params, anonymized package. Token leak from round 1 is gone. Gating prompt still "in the replication package" rather than an in-paper algorithm box — NICE, not blocking. | NICE |
| S7 | Anonymization | ✅ Present | Header anonymized (ll.27–29); self-citation `anon_archdetect_2026`; Data-Availability link de-tokenized. | — |
| S8 | Length / format | ✅ Present | LNCS, ~17 pp source, within bound. | — |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | The "0 regressions / test-adequacy gap" headline | ⚠️ Weak | Now honestly hedged (§5.2 ll.266–267), which removes the over-claim — but a hedge is not evidence. 0/121 is still consistent with (a) sparse tests, (b) genuinely safe edits, (c) no runnable suite. The paper leans to (a)+(c) but cannot exclude (b) without coverage. The strongest version *proves* the suites missed the edits. | MUST |
| P2 | Significance for a testing audience | ⚠️ Weak | The actionable take — "pair refactoring with LLM test generation" (§5.2 l.268; §7 l.424) — is now correctly labeled future work, which is the honest move. But the paper still diagnoses a gap it does not begin to close; even a 3-repo test-gen probe showing the gate *can* fire would lift this from "found a gap" to "contribution." | SHOULD |
| P3 | RQ1 / maintainability proportion | ⚠️ Weak | Despite the §5 reorder, §5.4–5.9 (Tables 2–6, case studies, size/tactic/style breakdowns) still consume the majority of the paper to argue a result the authors call noise (§5.10 l.400). The testing contribution is one subsection (§5.2). Compress further; reinvest in P1/P4. | SHOULD |
| P4 | Statistical honesty | ✅ Strong | Sensitivity collapse to p=0.083 (§5.3 l.275), ITT vs per-protocol split (§5.3 l.277), "26/42 within ±0.5 ≈ noise" — exemplary candor that makes the negative result credible. | — |
| P5 | Internal numeric consistency | ⚠️ Weak | **§5.10 Discussion l.400 still cites the *old, withdrawn* sensitivity p-value: "removing the two outliers erases statistical significance ($p = 0.156$)."** §5.3 l.275 and §7 l.422 correctly say p=0.083. This is a leftover from the pre-correction draft and directly contradicts the corrected statistic two pages earlier. Must reconcile to p=0.083. | MUST |
| P6 | Causal story for "0 triggers" | ⚠️ Weak | §5.2 l.264 gives 28/208, 20/121, "real suite in 15," but not the clean 4-way breakdown (no suite / suite-but-0-covering / covering-passed / covering-failed→rollback) that would make the claim airtight. Partial improvement over round 1. | SHOULD |

## Standing critical issue coverage

| ID | Issue | Status | Remaining action |
|---|---|---|---|
| **CRIT-1** | MI ≠ architecture-level maintainability; "architecture-aware" framing | ✅ Resolved | The pipeline is repeatedly and correctly scoped "code level, not architecture level" (§5.8 l.383; §7 l.422); Table 7 (fan-out/package/depth unchanged) furnishes the evidence. The residual "architecture-aware" phrase the round-1 EIC flagged in §3.1 is **gone** — §3.1 now says only "architectural code changes" / "tactic implementation." Construct claim and dependent variable are now aligned. |
| **CRIT-2** | File-splitting confound; no random-split baseline | ⚠️ Partial | Now thoroughly *named* (§5.3 l.275 "metric arithmetic"; §5.4 case studies l.285–288; §5.10 l.400; §6 l.408 "regression to the mean") and the construct caveat is strong — but still not *controlled*. No do-nothing/random-split baseline; deferred to future work (§6 l.408). Upgraded from ❌ to ⚠️ because the confound is now disclosed and bounded, but the baseline that would close it is absent. |
| **CRIT-3** | Single-annotator ground truth; no κ | ❌ Open | §6 l.408 still "single annotator (no inter-rater check)." Less central now that detection is offloaded to a separate dataset (§3.7 l.136), but the validated-label premise (§3.4) still rests on one annotator. |
| **CRIT-4** | No comparison condition | ❌ Open | Unchanged. For RQ1 the missing baseline (random split / static-only / human) caps the claim at absolute capability; for RQ2/RQ3 the missing comparison is the positive control proving the gate can fire (S4/P1). This is the issue that keeps the decision at MAJOR. |
| **CRIT-5** | Overgeneralization from niche | ✅ Resolved | The niche is now the finding: gains confined to tiny/script repos (Table 4 ll.306–309; §5.5; §5.10 l.400), practical advice scoped to "<30 files, ~32% success" (§5.10 l.404). |

## Defensibility vs. publishability

- **Sound conference paper?** Yes after MUST items. The reframe is honest and the negative result is real and venue-relevant. The two MUST items (P5 numeric inconsistency; S4/P1 the un-instrumented central claim) are the gate.
- **Publishable at ICTSS as-is?** No — but close. With (a) the §5.10 p-value fixed and (b) either a coverage measurement on the modified files **or** the claim further narrowed to "we did not observe regressions; adequacy is uninstrumented and out of scope," this is a credible ICTSS full paper. The topic maps directly onto the CFP's "Testing/validation of generative-AI outputs," "Regression testing," and "Test adequacy and coverage criteria" tracks. The negative-result framing is a fit, not a liability.

## Decisions required (MUST before next revision)

1. **Reconcile the contradicted statistic (P5):** §5.10 l.400 still reports the withdrawn p=0.156; correct it to the verified p=0.083 (§5.3 l.275). Non-negotiable — a corrected paper cannot contradict its own corrected number.
2. **Instrument adequacy or narrow the claim further (S4/P1):** Either run coverage.py over the modified files and report what fraction of edited code the suites exercised (turning the null into a measured gap), or explicitly scope the contribution to "0 observed regressions, adequacy uninstrumented." Alternative explanation (b) "edits were actually safe" otherwise stands unrefuted.
3. **(SHOULD) Probe the diagnosed gap (P2):** a 3–5 repo test-generation experiment showing the gate *can* fire would elevate diagnosis to contribution.
4. **(SHOULD) Demote RQ1 / compress §5.4–5.9 (S2/P3):** make the testing story the structural majority, not one subsection.

---

_Priority definitions:_
- **MUST:** blocks acceptance or leaves the central claim unsupported — fix before submission.
- **SHOULD:** significantly weakens credibility/quality — fix if feasible.
- **NICE:** strengthens the paper — optional polish.
- **DEFER:** out of scope for a conference paper — note as future work.
