# Reviewer Review (post-draft mode)

**Reviewer profile:** devils-advocate
**Persona:** Rigorous critical empiricist (Briand-style inference dismantler)
**Target:** ICTSS 2026 submission — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** Conference paper, ICTSS 2026 (Springer LNCS, software *testing* venue, double-blind, ≤15pp). Judged as a testing contribution, not an MS thesis.

---

## Summary judgment

The paper is honestly written and refreshingly self-critical about its maintainability result — the authors pre-empt almost every confound a reviewer would raise (outliers, file-splitting arithmetic, ITT vs. per-protocol, attrition). But the honesty is concentrated on the *secondary* result (MI), while the *headline* result — the one promoted to the title, the abstract, and the "main finding" — rests on the weakest evidence in the paper. The central testing claim ("regression tests cannot validate LLM architectural edits because OSS suites are inadequate oracles") is inferred from a **null result** (0 regressions) on a **tiny, uncontrolled** sample (15 repos with meaningful test runs, 21 passing executions) where the testing variable was **never manipulated or designed for** — it is an observational by-product of a pipeline whose actual independent variable was tactic implementation. A null is being read as a positive finding about the world, when at least three rival explanations (edits were safe; edits missed tested code; the gate itself is measurement-limited) are not separated by the design. For a testing venue, this is the load-bearing weakness. I do not issue a decision, but I flag two CRITICALs that, under the checkpoint rule, block ACCEPT until arbitrated.

## Standing critical issue coverage (mapped to this paper)

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability | ✅ Largely resolved by reframing — paper explicitly says it "operates at the code level, not the architecture level" (§5.10, §6) and demotes MI to a weak proxy. The construct overreach is now confined to the residual phrase "architecture-aware maintainability improvement pipeline" (§3.1) | Drop or qualify "architecture-aware"; otherwise resolved |
| CRIT-2 | File-splitting confound; no baseline | ⚠️ Partial — confound is *named* explicitly (§5.4, §5.10) and outliers removed in sensitivity analysis, but still **no random-split / do-nothing control**; deferred to future work (§6) | A no-op/random-split baseline is cheap and would settle the arithmetic-artifact question |
| CRIT-3 | Single-annotator ground truth | ❌ Open — §6 concedes "single annotator (no inter-rater check)"; labels feed the by-style analysis (Table 5) | Out of scope to fully fix, but limits the by-architecture claims |
| CRIT-4 | No baseline comparison | ❌ Open — for the *testing* claim there is no comparison oracle (e.g., mutation testing, coverage-instrumented run, generated tests). The null is uncontrolled | This is now the **central** gap, not a secondary one (see C-2 below) |
| CRIT-5 | Overgeneralization from niche | ⚠️ Partial — MI overgeneralization is well-controlled (§5.6, practice implication "apply only to <30 files"), but the *testing* claim "open-source test suites are inadequate behavioral oracles" is generalized from 15 repos to a field-level statement |

---

## 1. Strongest counter-argument (the core attack)

**The paper's headline contribution is a positive interpretation of a null result that the design cannot support, dressed as a testing finding at a testing venue.**

The title, abstract ("Our main finding is..."), and conclusion ("two results stand out... more importantly...") all promote a single inference: *because the regression gate never fired across 121 steps, open-source test suites are inadequate oracles for LLM architectural edits.* Strip the prose and the evidence is: **0 / 121 steps regressed; 21 / 121 steps ran any passing test; tests "executed meaningfully" in 15 / 20 repos** (§5.3). From a null of "nothing happened," the paper selects one explanation — the test-adequacy gap — and elevates it to a causal, field-level claim. But a null result is consistent with **at least three mutually exclusive worlds**, and the design separates none of them:

1. **The adequacy-gap world** (the paper's claim): tests existed but never touched the modified code.
2. **The safe-edit world**: the LLM's edits — dominated by extracting MI=100 config/utility modules and splitting near-MI=0 files (§5.5: "12 of 18 improvements extracted a new module scoring MI=100") — were *genuinely behavior-preserving*, so a correct test suite would also have stayed green. Mechanical, low-risk extractions are exactly the edits least likely to break behavior. The paper's own evidence that the edits were trivial (package count unchanged, fan-out ≈unchanged, §5.10) actively *supports* the safe-edit explanation over the adequacy-gap one.
3. **The measurement-limited world**: the gate detects only *new* failures vs. a baseline `pytest -q` run with a 300 s timeout; flaky tests, timeouts, environment-dependent suites, and tests that error at *collection* (and are thus absent from both baseline and post-change) are silently invisible. "21 passing executions" out of 121 means the gate had usable signal **17% of the time**; the other 83% is not "inadequate oracle," it is *no measurement*.

To assert the adequacy-gap explanation over the safe-edit explanation, you must show that the edits *would* have broken behavior under an adequate oracle. The paper offers no such instrument — no mutation score, no coverage delta on the modified lines, no manually verified behavioral diff on a sample, no injected-bug positive control to show the gate *can* fire. Without a positive control, "the gate never triggered" is uninterpretable: a gate that never fires is observationally identical whether the world is full of safe edits or the gate is broken. **The headline claim therefore has no empirical basis distinct from "we ran a small pipeline and not much happened, and OSS projects are under-tested" — the latter being well established and not a contribution.**

Quantitatively: the entire testing contribution rests on the *absence* of events in a sample where the number of *informative* trials is **21** (passing executions) across **15** repos — and of those, the subset that actually exercised *modified, cross-module* lines is reported as effectively zero. A contribution whose evidentiary base is "≈0 informative trials" cannot headline a testing venue.

A secondary structural objection compounds this: **testing was not the designed independent variable.** §3.1 states the independent variable is "the application of an architectural tactic... given a known repository architecture" and the dependent variable is "software maintainability... MI." The pre-test/post-test design, the Wilcoxon test, the dataset, and the hypothesis $H_0$ are all built around MI. Regression testing enters only as a *gating mechanism* inside Phase 4. The testing finding is thus a **post-hoc reinterpretation of a by-product** of a maintainability experiment — repackaged for a testing venue. That is not disqualifying per se, but it means the paper has no design power behind its headline question: there was no sampling for test-suite quality, no stratification by coverage, no manipulation of oracle strength.

## 2. Issue list (severity-ranked)

| # | Severity | Issue | Dimension | Location | Description |
|---|----------|-------|-----------|----------|-------------|
| C-1 | **CRITICAL** | Positive inference from an uncontrolled null | Conclusion/Construct validity | §5.3, §5.10, Abstract, §7 | "0 regressions ⇒ test-adequacy gap" is one of ≥3 rival explanations (safe edits; untouched code; measurement limits). No positive control shows the gate *can* fire; no coverage/mutation instrument distinguishes "untested" from "tested-and-safe." The headline claim is an over-read of a null. |
| C-2 | **CRITICAL** | No oracle-quality measurement; testing claim has no metric | Methodology/Construct | §3, §4 (Phase 4), §5.3 | The paper asserts oracle *inadequacy* but never *measures* adequacy. No coverage of modified lines, no mutation score, no manual behavioral verification on any sample. "Adequacy gap" is named as a conclusion, not operationalized as a variable. For a testing venue this is the missing instrument. |
| C-3 | **MAJOR** | Headline generalization from n=15 / 21 informative trials | External validity | §5.3, §7, Abstract | Field-level claim ("existing open-source test suites are inadequate behavioral oracles") generalized from 15 repos with runs and ~21 passing executions, single model, single language. Underpowered for a headline. |
| C-4 | **MAJOR** | Testing framing is post-hoc; not the designed IV | Methodology | §3.1 vs. Title/Abstract | Design IV is tactic application; DV is MI. Testing is a Phase-4 by-product, not sampled, stratified, or manipulated. The testing contribution rides on an experiment built for a different question. |
| C-5 | **MAJOR** | Novelty of the testing claim vs. prior knowledge | Contribution/Originality | §2.3, §5.3 | "OSS projects are under-tested / low-coverage" is long established (decades of coverage studies). The paper must show what is *new*: that adequacy specifically *fails for cross-module LLM edits* — but it provides no comparison to a code-level-edit condition to isolate the "architectural" part. Risk of restating known facts as a finding. |
| C-6 | MINOR | Gate design unvalidated against flakiness/timeouts/collection errors | Internal validity | §4 (Phase 4) | 300 s timeout, baseline-diff design, and `--tb=line` mean flaky/slow/collection-erroring suites are silently non-informative; counted toward "inadequacy" rather than "unmeasured." |
| C-7 | MINOR | "self-healing" confound on the gate's hit rate | Internal validity | §4 (Phase 4) | Up to two self-healing retries feed failing output back to the model before a step is abandoned. Any regression the gate *did* catch could be silently repaired, deflating the observed 0/121 — the 0 is partly an artifact of the loop, not only of test sparsity. Not discussed. |
| C-8 | MINOR | Residual construct overreach: "architecture-aware" | Construct validity | §3.1 | Pipeline is shown to operate at code level (§5.10); calling it the "architecture-aware maintainability improvement pipeline" contradicts the paper's own conclusion. |
| C-9 | MINOR | Sample/number consistency (thesis vs. paper) | Reliability | §3.3, §5.1 | "56 / 57 / 42" repo bookkeeping is clear here, but the abstract says "56 real open-source projects" while the dataset is 57 labeled (one unavailable). Minor, ensure single source of truth. |
| C-10 | MINOR | Live Zenodo token in submission | Reproducibility/Anonymity | §Data Availability | Embedded access token in the URL and named institution/emails — double-blind venue; this de-anonymizes and may expire. |

> Per the checkpoint rule, **C-1 and C-2 are upheld CRITICALs and block ACCEPT** until the editorial phase arbitrates.

## 3. Ignored alternative explanations

The paper rules out *none* of the following for its headline null:

1. **Safe-edit explanation.** The edits were dominated by mechanical extraction of trivial MI=100 modules and splitting of near-MI=0 files (§5.5). These are precisely the edits least likely to alter behavior, so a perfect oracle would *also* stay green. The paper's own structural-metric result (package count and depth unchanged, fan-out ≈unchanged, §5.10) is stronger evidence for "edits were trivial and safe" than for "tests were inadequate." This rival is never addressed.
2. **Edits-missed-tested-code explanation.** Even with adequate suites, if the LLM modified files outside the tested subset, the gate would not fire — a *targeting* problem, not an *oracle adequacy* problem. The paper conflates these.
3. **Measurement-limited / no-signal explanation.** 100 of 121 steps had no passing test execution at all. "No measurement" is being scored as "inadequate oracle."
4. **Self-healing deflation (C-7).** Caught regressions could be silently repaired before the step terminates, mechanically lowering the observed regression count independent of test adequacy.
5. **Selection toward untested repos.** The `requirements.txt`/backend filter and "10 stars, 5 Python files" criteria (§3.3) bias toward small, hobby-grade projects that are *known* to be under-tested — so the adequacy gap may be an artifact of dataset selection, not a property of "open-source test suites" generally.

## 4. Missing stakeholder perspectives

- **The testing researcher** (this venue's core reader): would demand a positive control and an adequacy metric (mutation/coverage) before accepting an oracle-adequacy claim — the paper offers neither.
- **The mutation-testing community**: mutation analysis is the textbook instrument for exactly "is this suite adequate to catch behavioral changes?" Its absence is conspicuous at a testing venue and would be the obvious reviewer ask.
- **Large-repo / industrial maintainers**: where suites are denser and edits riskier, the entire null could invert; the paper's scope ("<30 files") quietly excludes the population where the testing question actually bites.
- **Tool builders**: would value the negative result *if* it were properly bounded — but need the adequacy gap quantified (coverage of modified lines) to act on it.

## 5. Observations (genuine strengths — to keep the critique credible)

- The MI analysis is **exemplary in its self-criticism**: outlier sensitivity (§5.4), ITT vs. per-protocol reporting (§5.1, §5.4), attrition-bias check (§5.11), and the explicit demotion of MI to "weak proxy" (§5.10) are exactly what most papers omit. CRIT-1 and much of CRIT-2 are effectively answered by reframing.
- Foregrounding a **negative/honest result** rather than overselling capability is commendable and the right instinct for a testing audience.
- The **test-gated planner loop** (baseline-diff regression detection, snapshot/rollback, BM25 retrieval, bounded self-healing) is a methodologically reasonable engineering design and is reproducibly described.
- The **supplementary architecture-level metrics** (Table 6) are the paper's most quietly important contribution: they honestly demonstrate the pipeline does *not* reach the architecture level, which strengthens (not weakens) trust in the authors.
- The replication package (prompts, per-step test outcomes, artifacts) is a real asset — the per-step test-execution data is exactly what a reviewer would need to *re-examine* C-1.

## Defensibility vs. publishability

- **As a testing-venue contribution as-is?** Not yet. The headline rests on two upheld CRITICALs (uncontrolled null; no adequacy instrument). The robust, defensible result — "a green run of a sparse suite is weak evidence of safety, and our pipeline operates only at the code level" — is real but is (a) partly known and (b) not yet demonstrated *specifically* for cross-module LLM edits with a control.
- **What would lift it to publishable:** (i) a **positive control** — inject a known behavioral bug and show the gate fires; (ii) an **adequacy metric** — coverage of the *modified lines* per step, turning "untested" into a measured quantity; (iii) reframe the claim from "tests are inadequate oracles" (field-level) to "in N repos, M% of LLM-modified lines were uncovered, so the gate had no signal" (sample-bounded, measured); (iv) address the safe-edit rival explicitly; (v) account for self-healing deflation in the 0/121.

## Decisions required (for the editorial phase to arbitrate)

1. **Null interpretation (C-1):** Will the authors add a positive control and/or coverage-of-modified-lines metric to distinguish "untested" from "tested-and-safe," or will they downgrade the claim to a bounded, descriptive observation? Without one of these, the headline is unsupported.
2. **Adequacy operationalization (C-2):** Will "oracle inadequacy" be measured (coverage/mutation), or remain an asserted interpretation of a null?
3. **Framing honesty (C-4/C-5):** Will the abstract/title be re-scoped to reflect that testing was a by-product of a maintainability experiment and that the under-testing of small OSS projects is prior knowledge, with the genuinely new sliver isolated?

---

_I do not issue a decision; per profile I hand the EIC the issue list above. The two upheld CRITICALs (C-1, C-2) block ACCEPT under the checkpoint rule until resolved or downgraded._
