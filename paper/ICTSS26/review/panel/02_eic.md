# Reviewer Review (post-draft mode)

**Reviewer profile:** eic (Editor-in-Chief / committee chair)
**Persona:** Editor of a leading SE venue; authority on architecture, refactoring, design patterns (Fowler-type lens)
**Target:** ICTSS 2026 submission — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** ICTSS 2026 (Springer LNCS, one-column, software-testing venue; full paper 12–15 pp + ≤2 ref; double-blind). Conference-paper bar, with standing CRIT-1..5 still assessed.

---

## Summary judgment

This is a markedly smarter paper than the v3 thesis it descends from. The authors have done the one thing that turns a weak result into a publishable one: they stopped pretending the maintainability story was the contribution and reframed around the honest, transactional finding — *the regression gate caught nothing because the test suites were too sparse to catch anything*. That "test-adequacy gap" is a clean, citable, negative result that genuinely belongs at a testing venue, and the writing (especially the plain-language abstract and the §5.3 framing) is the strongest I have seen from this project. What blocks acceptance as-is is that the paper's own headline — RQ2/RQ3, the behavioral gate — rests on a thin slice of evidence (121 steps, only 21 with any passing execution, 15 repos with meaningful tests, **zero** triggers) and the paper does not yet do enough to convert "the gate never fired" into a *characterized, generalizable* claim. The maintainability half (RQ1) is now correctly demoted but still occupies disproportionate space and still carries the unresolved file-splitting confound. **Provisional decision: MAJOR REVISION**, leaning positively — the contribution is real and venue-appropriate, but the central testing claim needs more rigorous backing and the structure needs rebalancing toward RQ2/RQ3.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | Problem framed as a *testing* problem | ✅ Present | Intro (§1, ll.47–51) lands the validation-not-generation framing cleanly and cites DePalma/Liu/Shokri/Horikawa to motivate the oracle question. Strong venue fit. | — |
| S2 | RQs aligned to venue | ⚠️ Partial | RQ2/RQ3 (§1, ll.56–57) are the testing contribution; RQ1 is a maintainability question that the paper itself later calls a weak proxy (§5.10). RQ1 reads as legacy. Consider demoting RQ1 to a setup/precondition rather than a co-equal research question. | SHOULD |
| S3 | Method for the *gating* mechanism | ✅ Present | §4.4 "Behavioral gating" is concrete: baseline pytest capture, snapshot/apply/re-run, rollback on new failures, two self-healing attempts. This is the methodological core and it is adequately described. | — |
| S4 | Test-adequacy measurement | ❌ Missing | The central claim is that suites are inadequate oracles, yet adequacy is never *measured*. No coverage numbers (line/branch) on the modified files, no statement of how many repos had any test touching changed code beyond a count. "Exercised the modified code paths" (§5.3, l.274) is asserted, not instrumented. A coverage tool run on the diffed files is the obvious, cheap evidence and its absence is the biggest hole in the paper's own thesis. | MUST |
| S5 | Threats to validity | ✅ Present | §6 is honest and covers internal/external/construct/conclusion. Single annotator, single model, outlier-driven significance, and the oracle gap are all admitted up front. | — |
| S6 | Reproducibility | ⚠️ Partial | Zenodo package, model ID, generation params present (§Data Availability). But the Zenodo link carries a **private access token in the URL** (l.435) — a double-blind and a de-anonymization problem (see P5). Prompts are "in the replication package," not in-paper; for a testing venue the gating prompt and self-heal prompt matter and at least the gate logic deserves an algorithm box. | MUST |
| S7 | Anonymization (double-blind) | ❌ Missing | Author names, emails, and institution are in the header (ll.28–31); the AI-tools acknowledgment and Zenodo token further de-anonymize. The CFP requires anonymized submission (cfp ll.101–102). This must be fixed before submission regardless of technical merit. | MUST |
| S8 | Length / format | ✅ Present | LNCS one-column, well within 15 pp. Format compliant. | — |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | The headline "0 regressions / test-adequacy gap" | ⚠️ Weak | The finding is interesting but the evidence base is thin and partly definitional. Zero triggers across 121 steps is consistent with (a) sparse tests, (b) genuinely safe edits, (c) a gate that rarely had a runnable suite. The paper asserts (a) and dismisses (b) (§5.3, l.273), but cannot *rule out* (b) precisely because there is no coverage instrumentation (S4). The strongest version of this paper proves the suites did not cover the edits, rather than inferring it from a null. | MUST |
| P2 | Significance for a testing audience | ⚠️ Weak | The actionable take — "pair refactoring with test generation" (§5.3 l.276; §7 l.423) — is asserted, not demonstrated. A reviewer at a testing venue will ask: did you *try* generating tests and re-running the gate? Even a small probe (e.g., Pynguin/LLM-generated tests on 3–5 repos, showing the gate now fires) would convert a recommendation into a contribution. Without it, the paper diagnoses a gap it does not begin to close. | SHOULD |
| P3 | RQ1 / maintainability material | ⚠️ Weak | §5.1–5.9 (Tables 1–6, the case studies, size/tactic/style breakdowns) consume the majority of the paper to argue a result the authors themselves conclude is "at best a weak proxy" (§5.10 l.399) and an artifact of MI arithmetic (§5.5 l.290; §5.10 l.399). This is well-reasoned but over-weighted: it crowds out the testing contribution the venue cares about. Compress to ~1.5 pages and reinvest in P1/P2/S4. | SHOULD |
| P4 | Statistical honesty | ✅ Strong | The sensitivity analysis (§5.2 l.265: significance collapses to p=0.156 sans two outliers), the ITT vs per-protocol split (l.267, p=0.087), and the "24/42 within ±0.5 ≈ noise" admission are exemplary intellectual honesty. This is exactly the candor that makes the negative result credible. | — |
| P5 | Self-anonymization integrity | ❌ Unconvincing | Beyond the header, the Zenodo URL embeds a JWT access token (l.435) that resolves to the authors' account — a hard de-anonymization leak and a security smell (tokens should never be pasted into a paper). | MUST |
| P6 | Causal story for "0 triggers" | ⚠️ Weak | §5.3 conflates "no runnable suite," "no tests touching modified code," and "tests passed" into one null. Disaggregate: of 121 steps, how many had (i) no suite, (ii) a suite but 0 covering tests, (iii) covering tests that passed, (iv) covering tests that failed→rollback? The current text gives 21 "passing executions" and "15 repos with meaningful tests" but not the clean breakdown that would make the claim airtight. | MUST |

## Standing critical issue coverage

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability; "architecture-aware" framing | ⚠️ Partial | Largely defused by reframing: the paper repeatedly states the pipeline "operates at the code level, not the architecture level" (§5.8 l.382; §7 l.421) and adds fan-out/package/depth metrics (Table 6) showing no architectural change. But the residual phrase "architecture-aware maintainability improvement pipeline" survives in §3.1 (l.88) and "architectural tactic" framing pervades — a careful reviewer will note the construct claim is hedged in results but still asserted in the methodology. Scrub the residual "architecture-aware" language. |
| CRIT-2 | File-splitting confound; no random-split baseline | ❌ Open | The confound is now *named* clearly (§5.5 l.290 "metric arithmetic," §5.4 case studies, §6 "regression to the mean") but still not *controlled*. No do-nothing/random-split baseline; §6 (l.407) defers it to future work. For a venue judging on technical quality, this remains the single biggest internal-validity hole behind RQ1. |
| CRIT-3 | Single-annotator ground truth; no κ | ❌ Open | §6 (l.407) admits "single annotator (no inter-rater check)." Unchanged from v3. Less central now that detection is offloaded to a companion dataset, but the validated-label premise (§3.4) still rests on one annotator. |
| CRIT-4 | No comparison condition | ❌ Open | Still no baseline (random split, static-only, or human). §6 defers it. For RQ1 this caps the claim at "absolute capability." Note: for RQ2/RQ3 the relevant missing comparison is the *test-generation* probe (P2). |
| CRIT-5 | Overgeneralization from niche | ✅ Resolved | Genuinely fixed. The paper now *foregrounds* that gains are confined to tiny/script repos (Table 4; §5.5; §5.10 l.399) and scopes the practical advice to "<30 files, ~32% success" (§5.10 l.403). The niche is the finding, not hidden. |

## Defensibility vs. publishability

- **Sound conference paper?** Not yet — after MUST items. The reframing is the right call and the negative result is real, but the headline testing claim (CRIT-equivalent for this venue: the test-adequacy gap) is currently *inferred from a null* rather than *measured*. Add coverage instrumentation (S4/P1/P6) and it becomes defensible.
- **Publishable at ICTSS as-is?** No. Three submission-blocking issues independent of merit: anonymization (S7), the leaked Zenodo token (P5), and the un-instrumented central claim (S4). With those fixed plus structural rebalancing, this is a credible ICTSS full paper — the topic (regression testing as an oracle for generative-AI code changes, test adequacy for AI outputs) maps directly onto the CFP's "Testing and validation of generative AI outputs," "Regression testing," and "Test adequacy and coverage criteria" tracks. The negative-result framing is a fit, not a liability, for this community.

## Decisions required

MUST-priority items needing an author decision before the next revision.

1. **Instrument adequacy, don't infer it (S4/P1/P6):** Will you run a coverage tool (line/branch) over the *modified files* and report what fraction of edited code was exercised by the suite? This is the evidence that turns "the gate never fired" into "the suites provably did not cover the edits." Without it, alternative explanation (b) — the edits were actually safe — stands unrefuted.
2. **Close, or probe, the gap you diagnose (P2):** Will you add even a small test-generation experiment (re-run the gate after synthesizing tests on a handful of repos) to show the gate *can* fire? This is what elevates the paper from "we found a gap" to a contribution a testing venue rewards.
3. **Anonymize and de-leak (S7/P5):** Strip author/affiliation/email from the header and the AI-ack, and replace the tokenized Zenodo URL with an anonymized artifact link (or anonymous.4open.science). The embedded JWT must go.
4. **Rebalance structure (P3):** Will you compress RQ1/MI material (§5.1–5.9) to ~1.5 pp and reinvest the space in RQ2/RQ3 (the gate's behavior, the adequacy breakdown, the test-gen probe)? Right now the paper spends most of its pages on the result it concludes is noise.
5. **Decide RQ1's status (S2) and scrub residual construct claims (CRIT-1):** Either keep RQ1 as a co-equal question and own the confound (CRIT-2 baseline), or demote it to a precondition. Remove the surviving "architecture-aware" phrasing (§3.1 l.88).

---

_Priority definitions:_
- **MUST:** blocks acceptance or leaves the central claim unsupported — fix before submission.
- **SHOULD:** significantly weakens credibility/quality — fix if feasible.
- **NICE:** strengthens the paper — optional polish.
- **DEFER:** legitimately out of scope for a conference paper — note as future work.
