# Reviewer Review (post-draft mode)

**Reviewer profile:** domain-examiner
**Persona:** Software-architecture & software-testing specialist (architectural tactics, technical debt, behavioral validation / test oracles)
**Target:** ICTSS 2026 conference paper — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** ICTSS 2026 (Springer LNCS, software-testing venue, ≤15pp+2ref, double-blind) — defensibility + publishability assessed separately

---

## Summary judgment

This is a substantially stronger framing than the thesis version it was carved from: by reframing the central question around *behavioral validation* and surfacing the **test-adequacy gap** as the headline finding, the paper turns the thesis's standing weaknesses (MI is a code-level proxy; no behavioral check) into the contribution itself, which is honest and well-suited to a testing venue. The empirical reporting is candid to a fault — outlier sensitivity, ITT vs. per-protocol rates, the null gate result are all in the open. The blocking problem for a *testing* audience is positioning: the paper makes claims about test oracles and test adequacy while engaging almost none of the canonical oracle / test-adequacy / LLM-test-generation literature (§2 cites exactly one test-related work, `cordeiro2024llm`, and it is a bug-fixing/refactoring agent study, not test generation). The architectural-tactics theory is used mostly correctly but with two loose spots (a "32 tactics" figure that contradicts the source and the paper's own "3 applied," and a Reduced Coupling result the construct cannot measure). The core empirical claim that the gate "never triggered because suites are too sparse" is sound and well-evidenced; the secondary maintainability claim is appropriately hedged. Provisional posture: **MAJOR REVISION** — accept the contribution, but the related-work coverage and the oracle/adequacy framing must be brought up to the standard of the venue.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Test-oracle literature | ❌ Missing | The paper's central object is "regression tests as a behavioral oracle," yet §2 cites no oracle literature — no Barr et al. oracle survey, no notion of the oracle problem, no metamorphic/differential-oracle alternatives. For a testing venue this is the load-bearing gap. The "Validation/Oracle Void" gap (§2.3) is asserted from refactoring papers, not from the testing field that owns the concept. | MUST |
| S2 | Test-adequacy / coverage literature | ❌ Missing | The headline finding is a *test-adequacy* gap, but adequacy is never defined or measured against any adequacy criterion (statement/branch/mutation coverage). No coverage instrumentation was run (§5.3 reasons only from pass/fail and "tests touching modified code"). The claim "suites too sparse to be oracles" is inferred, not measured. Cite and ideally apply an adequacy criterion (line/branch coverage delta, or mutation score on the modified files). | MUST |
| S3 | LLM-based test generation | ⚠️ Partial | The paper's prescription is "pair refactoring with LLM-assisted test generation" (§5.3, §6), but the only support is `cordeiro2024llm`. None of the now-standard LLM test-gen works are engaged (e.g., TestPilot/Schäfer et al., CodaMosa, ChatTester/ChatUniTest, or EvoSuite as the search-based baseline the field would expect). The recommendation is therefore unmoored from the literature it invokes. | MUST |
| S4 | Architectural-tactics grounding | ✅ Present | Tactics vs. patterns distinction is correct (§2.1); Bass/Clements and the Márquez mapping study are cited; ISO/IEC 25010 sub-characteristics named. Good for the venue. | — |
| S5 | Regression-testing positioning | ⚠️ Partial | "Regression testing as a safety gate" is the framing but there is no regression-testing-specific citation (regression test selection/prioritization, or behavior-preservation testing for refactoring à la safe-refactoring literature). The gate is engineering, not positioned against RT research. | SHOULD |
| S6 | Threats to validity | ✅ Present | §6 is honest and covers internal/external/construct/conclusion; construct section explicitly concedes MI cannot capture Reduced Coupling and that behavior preservation was unconfirmed. | — |
| S7 | Architecture-level metric | ✅ Present | §5.9 (Table 7) reports fan-out, package count, directory depth and uses them to make the code-level-not-architecture-level point explicitly — this resolves the long-standing CRIT-1 gap far better than the thesis did. | — |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Soundness of the oracle/test-adequacy argument | ⚠️ Weak | The reasoning chain is plausible and honest, but the conclusion "suites too sparse to be oracles" rests on a proxy (only 21/121 steps recorded any passing execution; gate never fired) rather than a coverage measurement (§5.3). A skeptical reader can object that "no new failure" could also mean the edits *were* behavior-preserving. The paper asserts the adequacy interpretation but never rules out the preservation interpretation with data. Add coverage/mutation evidence, or soften from "inadequate oracle" to "unable to exercise the changed paths under available coverage." | MUST |
| P2 | Correctness of tactic catalog claim | ⚠️ Weak | §2.1 says the Márquez catalog of "over 40" was "refined to a subset of 32 tactics," and §4.3 again says selection draws from "32 maintainability-oriented tactics," yet only 3 are ever applied (§3.5). The "32" figure is asserted twice with no listing, contradicts the thesis profile's "~20 cataloged / 4 implemented," and the 29 unused tactics are dead weight that a domain reader will question. Either list the 32 (replication package pointer is not enough for a domain claim) or scope the catalog to what the selector actually used. | SHOULD |
| P3 | Faithfulness of intervention to tactic | ✅ Strong | §5.5 honestly contrasts genuine responsibility separation (Paper2Rebuttal) against mechanical splitting (webapp-color) and concedes MI cannot distinguish them. This is exactly the faithfulness distinction a domain examiner looks for, and it is handled with integrity. | — |
| P4 | Reduced Coupling result interpretation | ⚠️ Weak | Table 5 reports Reduced Coupling outcomes by MI, then §6 concedes MI "cannot in principle capture the effect of Reduced Coupling." Reporting a tactic's effectiveness on a metric you state cannot measure it is internally inconsistent — the N=3 "never improved MI" line invites an unfair reading of the tactic. Either drop Reduced Coupling MI claims or evaluate it on fan-out/coupling (Table 7 already has fan-out). | SHOULD |
| P5 | Readability for an architecture/testing reader | ✅ Strong | The argument is followable: RQ1 (can it improve MI) → RQ2 (does the gate catch unsafe edits) → RQ3 (are suites adequate oracles), and §5 maps onto these. The lay-abstract style is unusually accessible. Tables are clear and captioned. | — |
| P6 | Currency of LLM-for-SE coverage | ✅ Strong | 2024–2025 LLM-refactoring work is well represented (MANTRA, agentic-refactoring, Liu, Martinez SLR, Piao, IPSynth). The refactoring side is current; only the *testing* side is dated/absent (see S1–S3). | — |
| P7 | Headline vs. evidence proportionality | ✅ Strong | The maintainability claim is correctly demoted ("real but fragile," significance vanishes without 2 outliers, §5.2/§5.10) and the testing claim is foregrounded. No overclaiming on the architecture side. | — |

## Standing critical issue coverage

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability | ✅ Resolved | §5.9 + Table 7 report fan-out/package/depth and state explicitly the pipeline "operates at the code level, not the architecture level." Construct framing in §6 matches. Best handling across all versions. |
| CRIT-2 | File-splitting confound; no baseline | ⚠️ Partial | The arithmetic artifact is now named openly (§5.4 sensitivity analysis, §5.5 "Common pattern," §5.10) and removing 2 outliers erases significance. But the confound is acknowledged, not controlled — the random-split baseline is still only future work (§6). |
| CRIT-3 | Single-annotator ground truth | ⚠️ Partial | §6 admits "single annotator (no inter-rater check)." Conceded, not fixed. For this paper the labels are an input (companion dataset), so the impact is bounded, but κ is still absent. |
| CRIT-4 | No baseline comparison | ❌ Open | Still no random-split / static-analysis-only / human-developer comparison. Acknowledged as future work (§6). Demonstrates absolute, not relative, capability. |
| CRIT-5 | Overgeneralization from niche | ✅ Resolved | §5.6 (size bins) and §5.10 confine gains to tiny/script repos; "Implications for practice" scopes the recommendation to <30-file repos. Generalization is appropriately bounded. |

## Defensibility vs. publishability

- **Defensible as a conference paper?** Yes after MUST items. The empirical core is honest and the contribution (test-adequacy gap as the real blocker for trusting LLM refactoring) is genuine and venue-appropriate. What blocks acceptance at a *testing* venue is not the experiment but the failure to engage the testing field's own literature on oracles and adequacy (S1–S3) and the inferential leap in P1.
- **Publishable as-is?** No. At ICTSS specifically, a paper whose title and contribution are about regression-test oracles and test adequacy, yet which cites no oracle and no adequacy literature and measures no coverage, will read as outside-field. After major work — add the oracle/adequacy/LLM-test-gen positioning, define "adequacy" operationally, and add at least a coverage delta on the modified files — this is a credible ICTSS short/full paper. The behavioral-gate + null-result story is exactly the kind of negative finding a testing venue values when it is properly grounded.

## Decisions required

MUST-priority items needing an author decision before the next revision.

1. **Oracle/adequacy framing (S1, S2, P1):** Will you (a) measure adequacy directly — run coverage (line/branch) and ideally mutation score on the modified files so "suites too sparse" is a measurement not an inference — or (b) reframe the claim to "available suites did not exercise the changed paths" and cite the oracle-problem / test-adequacy literature to position it? One of these is mandatory for a testing venue.
2. **LLM-test-generation grounding (S3):** Your central prescription is "pair with LLM test generation." Which works ground it (TestPilot, CodaMosa, ChatTester/ChatUniTest, EvoSuite as SBST baseline)? The recommendation cannot rest on `cordeiro2024llm` alone.
3. **Tactic catalog count (P2):** Resolve the "32 tactics" claim — list them, or scope the catalog to the tactics the selector actually used. The figure currently contradicts both the source ("over 40") and your own "3 applied."
4. **Reduced Coupling reporting (P4):** Decide whether to report Reduced Coupling on MI at all, given you state MI cannot measure it; if kept, evaluate it on the coupling/fan-out metric you already collect.

---

_Priority definitions:_
- **MUST:** blocks acceptance or makes a central claim unsupported — fix before submitting.
- **SHOULD:** significantly weakens credibility/quality — fix if feasible.
- **NICE:** strengthens the paper — optional polish.
- **DEFER:** legitimately out of scope for a 15-page paper — note as future work.
