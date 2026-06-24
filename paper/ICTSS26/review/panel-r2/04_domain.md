# Reviewer Review (post-draft mode) — Round 2

**Reviewer profile:** domain-examiner
**Persona:** Software-architecture & software-testing specialist (architectural tactics, technical debt, behavioral validation / test oracles)
**Target:** ICTSS 2026 conference paper — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft — RE-REVIEW (round 2)
**Frame:** ICTSS 2026 (Springer LNCS, software-testing venue, ≤15pp+2ref, double-blind)

---

## Summary judgment

The round-1 MUSTs that blocked acceptance at a testing venue have been substantively addressed, and the paper has moved from MAJOR REVISION to a clear MINOR. The new §2.3 "Test Oracles and Behavioral Validation" (lines 74–75) now grounds the central object — regression tests as a *de facto* behavioral oracle — in the field that owns it: Barr et al.'s oracle-problem survey, metamorphic testing (Chen et al.), and two LLM-test-generation works (CodaMosa, Schäfer et al.) are cited and, importantly, used correctly rather than name-dropped. The single most important fix is the honest reframing in §5.2 (line 266): the paper now states explicitly that coverage was *not* measured, that a clean gate "cannot distinguish a behavior-preserving edit from one the suite simply never exercises," and reads the null result "cautiously … as evidence of a *test-adequacy gap* … rather than as proof of safe transformation." That sentence resolves both the round-1 "adequacy asserted not measured" and the "untested ≠ safe doesn't rule out behavior-preserving edits" objections — the alternative interpretation is now named in the body, not just conceded in threats. The test-generation prescription (§5.2 line 268; §7 line 424) now rests on Schäfer + CodaMosa + Cordeiro and is labeled future work, fixing the one-cite problem.

Is this a *testing* contribution now, or a maintainability study with a testing veneer? It is now genuinely the former. RQ2/RQ3 are foregrounded (results §5.2 is presented *before* the MI statistics, line 264), the maintainability claim is correctly demoted to "real but fragile" (§7 line 422), and the headline — that the binding constraint on trustworthy LLM refactoring is oracle adequacy, not generation — is a finding a testing audience should hear. The remaining gaps are now SHOULD/NICE, not blockers: adequacy is still *inferred* from a pass/fail proxy rather than *measured* with a coverage delta, and the "32 tactics" figure (lines 67, 195) still contradicts the "3 applied" (line 120) and the source's "over 40." Neither sinks the paper.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Test-oracle literature | ✅ Present | §2.3 now cites Barr et al. (oracle problem) and frames the regression suite as a *de facto* oracle whose reliability "depends entirely on how thoroughly the suite exercises the affected code" (line 75). The §2.4 "Validation/Oracle Void" gap is now anchored in the testing field, not only refactoring papers. Round-1 MUST resolved. | — |
| S2 | Test-adequacy / coverage literature | ⚠️ Partial | The adequacy claim is now correctly softened: §5.2 admits "the pipeline recorded test pass/fail but *not* whether the executed tests cover the modified code" (line 266). This converts the round-1 MUST from an unsupported assertion to an honestly-bounded inference. Still: no adequacy *criterion* is named (statement/branch/mutation) and no coverage delta is run. The fix is now optional rather than blocking, but a single line/branch coverage number on the modified files would convert the headline from inference to measurement. | SHOULD |
| S3 | LLM-based test generation | ✅ Present | The prescription now cites Schäfer et al. and CodaMosa alongside Cordeiro (§5.2 line 268; §7 line 424), and is explicitly future work. CodaMosa is correctly invoked as the coverage-driven route; Schäfer for LLM unit-test generation with its honest correctness caveat. Round-1 MUST resolved. | — |
| S4 | Architectural-tactics grounding | ✅ Present | Tactics-vs-patterns distinction correct (§2.1 line 63); Bass/Clements + Márquez cited; ISO/IEC 25010 sub-characteristics named (line 65). | — |
| S5 | Regression-testing positioning | ⚠️ Partial | Still no regression-test-selection/prioritization or safe-refactoring-testing citation; the gate is positioned against the oracle literature now (good) but not against RT research specifically. Lower priority given the venue will read the oracle framing as sufficient. | NICE |
| S6 | Threats to validity | ✅ Present | §6 honest; construct section concedes MI cannot capture Reduced Coupling and behavior preservation unconfirmed (line 412). | — |
| S7 | Architecture-level metric | ✅ Present | §5.9 + Table 7 report fan-out/package/depth and make the code-level-not-architecture-level point (line 383). | — |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Soundness of the oracle/adequacy argument | ✅ Strong | The round-1 inferential leap is fixed at the source: §5.2 (line 266) explicitly states the null result "does not establish that the edits were behavior-preserving" and names the competing interpretation ("a clean run cannot distinguish a behavior-preserving edit from one the suite simply never exercises"). The conclusion is now "weak behavioral oracle," not "inadequate oracle proven." This is exactly the softening requested. Residual: it is still a *proxy* argument (15/20 repos ran a non-trivial suite; gate never fired), so a coverage number would make it airtight — but the claim no longer outruns the evidence. | — |
| P2 | Correctness of tactic-catalog claim | ⚠️ Weak | Unchanged from round 1. §2.1 (line 67) and §4.3 (line 195) still assert "32 tactics" with no listing, contradicting both the Márquez "over 40" and the paper's own "Three … tactics were applied" (line 120). A domain reader will still ask where the 29 unused tactics are. List them in the replication package and say so, or scope the catalog to the 3 used. | SHOULD |
| P3 | Faithfulness of intervention to tactic | ✅ Strong | §5.5 still contrasts genuine separation (Paper2Rebuttal, line 288) vs. mechanical splitting (webapp-color, line 285) and concedes MI cannot tell them apart. | — |
| P4 | Reduced Coupling result interpretation | ⚠️ Weak | Partially addressed. Table 5 (line 334) still reports Reduced Coupling by MI (N=3, mean −0.16, never improved) while §6 (line 412) states MI "cannot in principle capture the effect of Reduced Coupling." The internal tension persists: a metric the paper says cannot measure the tactic is used to report the tactic failing. The §6 caveat blunts the worst reading, but the cleanest fix — evaluate Reduced Coupling on fan-out (already in Table 7) — is not taken. | SHOULD |
| P5 | Readability for an architecture/testing reader | ✅ Strong | RQ1→RQ2→RQ3 maps onto §5; testing results foregrounded (§5.2 before §5.3). Accessible abstract. | — |
| P6 | Currency of LLM-for-SE coverage | ✅ Strong | Refactoring side current (MANTRA, agentic, Liu, Martinez, Piao, IPSynth); testing side now current too (CodaMosa 2023, Schäfer 2024, Chen 2018, Barr 2015). The round-1 asymmetry is closed. | — |
| P7 | Headline vs. evidence proportionality | ✅ Strong | Maintainability demoted ("real but fragile," significance vanishes without 2 outliers, §5.3/§5.10); testing claim foregrounded; no architecture-side overclaim. | — |

## Standing critical issue coverage

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability | ✅ Resolved | §5.9 + Table 7 + §6 construct para state the pipeline operates at the code level, not the architecture level. |
| CRIT-2 | File-splitting confound; no baseline | ⚠️ Partial | Artifact named openly (§5.4, §5.5, §5.10); removing 2 outliers erases significance. Confound acknowledged, random-split control still future work (§6 line 408). |
| CRIT-3 | Single-annotator ground truth | ⚠️ Partial | §6 (line 408) admits "single annotator (no inter-rater check)." Labels are an input here, so impact bounded; κ still absent. |
| CRIT-4 | No baseline comparison | ❌ Open | Still no random-split / static-only / human comparison; future work (§6 line 408). |
| CRIT-5 | Overgeneralization from niche | ✅ Resolved | §5.6 size bins + §5.10 + §5.10 "Implications for practice" scope the recommendation to <30-file repos (line 404). |

## Defensibility vs. publishability

- **Defensible as a conference paper?** Yes. The empirical core is honest and the contribution is venue-appropriate.
- **Publishable?** Yes after MINOR work. The round-1 blocker — a testing paper that cited no oracle/adequacy literature and measured no coverage — is gone: the oracle/adequacy/test-gen literature is now present and correctly used (§2.3, §5.2, §7), and the central claim is softened to match the evidence. What remains are quality improvements, not gates: (1) the "32 tactics" inconsistency (P2), (2) reporting Reduced Coupling on a metric the paper says cannot measure it (P4), and (3) the headline still being an inference rather than a coverage measurement (S2/P1). Adding even one line/branch-coverage delta on the modified files would elevate this from a credible negative-result paper to a strong one — but it is no longer required for acceptance.

## Decisions required

MUST/SHOULD items for the next revision.

1. **Coverage measurement (S2, SHOULD):** Consider running line/branch coverage on the modified files for the 15 repos with a non-trivial suite, so "test-adequacy gap" becomes a measured number rather than an inference. Optional but high-value.
2. **Tactic-catalog count (P2, SHOULD):** Resolve "32 tactics" — list them in the replication package and point to it, or scope §2.1/§4.3 to the 3 tactics actually applied.
3. **Reduced Coupling reporting (P4, SHOULD):** Either drop the MI-based Reduced Coupling line, or evaluate it on fan-out (already collected in Table 7), to remove the metric/claim inconsistency.

---

## RETURN SUMMARY

**(a) Decision + change:** MINOR REVISION — moved up from MAJOR REVISION (round 1). The three round-1 MUSTs for a testing audience (no oracle literature; adequacy asserted not measured; untested≠safe didn't exclude behavior-preserving edits; one-cite test-gen prescription) are resolved via §2.3, the softened §5.2 claim, and the expanded test-gen citations.

**(b) CRIT status:**
- CRIT-1 ✅
- CRIT-2 ⚠️
- CRIT-3 ⚠️
- CRIT-4 ❌
- CRIT-5 ✅

**(c) Top 5 remaining issues:**
1. [SHOULD] §5.2 (l.266) — adequacy still inferred from pass/fail proxy; no coverage/mutation number measured.
2. [SHOULD] §2.1/§4.3 (l.67,195) — "32 tactics" unlisted, contradicts "3 applied" and source's "over 40."
3. [SHOULD] Table 5 + §6 (l.334,412) — Reduced Coupling reported on MI, a metric the paper says cannot measure it.
4. [OPEN/DEFER] §6 (l.408) — no random-split/static-only/human baseline (CRIT-4); absolute not relative capability.
5. [NICE] §2.3/§5 — gate not positioned against regression-test-selection/safe-refactoring-testing literature (S5).
