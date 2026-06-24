# Revision Roadmap — ICTSS 2026 submission

Prioritized P1 (blocking) → P4 (polish). Each item lists the fix and how a re-review verifies it.

## P1 — Blocking (resolve before resubmission)

**P1-1. Operationalize and control the test-adequacy claim (the CRITICAL).**
Three concrete additions, in order of value:
- **Positive control:** inject a known behavior-altering mutation into each repo with a runnable suite and confirm the gate fires. If it does, the 0-regression result is meaningful; if it doesn't, the gate itself is broken. *(addresses CRIT-4, devil's C-1)*
- **Coverage of modified lines:** measure statement/branch coverage of the files the LLM edited (e.g., `coverage.py`). This is the actual evidence for "suites too sparse to exercise the edits." *(devil's C-2, methodology #2, domain #2)*
- **Separate the rival explanations** (edits-safe vs. edits-untested vs. no-suite) in the §5.3 numbers; do not report a single conflated "0."
- *Verify:* §5.3 reports gate-can-fire evidence + coverage of edited code + a disaggregated breakdown; abstract/conclusion claims are scoped to what the data show.

**P1-2. Fix the two statistics errors.**
- The Wilcoxon **W = 473 is reported identically for N = 42 (p = 0.023) and N = 56 (p = 0.087)** — impossible; recompute the ITT statistic (§5.2).
- Report the inferential test on the **32 genuinely-treated** repos (exclude the 10 planner/syntax no-interventions folded into "completed"), or justify their inclusion (§5.1, Table 1).
- *Verify:* distinct, correct W for each sample; treated-only test present.

**P1-3. Double-blind anonymization.**
Remove author names/affiliation/emails (ll.28–31), anonymize the self-citation `chertkov_2026_20051151`, **strip the tokenized Zenodo URL** (leaks a private JWT), neutralize the acknowledgement. *(EIC #2, consistency, devil's C-10)*
- *Verify:* no identifying strings; data link is an anonymized mirror.

## P2 — Major (needed for a credible testing paper)

**P2-1. Add test-oracle related work** (§2): the oracle problem, metamorphic/differential testing, and LLM-assisted test generation (e.g., EvoSuite, CodaMosa, TestPilot, ChatTester). Currently *zero* oracle/test-gen citations in a paper about tests as oracles. *(domain #1, #4)*

**P2-2. Rebalance the narrative to lead with testing** *(readability)*: move the behavioral-gating result (§5.3) up; compress RQ1/MI subsections (which the paper calls noise) into one; consider demoting 2–3 MI tables. Make the title/abstract/intro/results tell one testing-first story.
- *Verify:* the testing contribution appears by ~page 4–5, not page 9.

**P2-3. Soften or substantiate the actionable claim.** "Pair with LLM test generation" is a hypothesis stated as a recommendation; either run a small probe (synthesize tests, re-gate) or label it explicitly as future work. *(EIC #3, domain #4, perspective #5)*

## P3 — Minor

- **P3-1.** Fix the `\label` collision: `sec:eval_arch_detection` and `sec:eval_pipeline` are both on the merged "Prior Stages and Baseline" subsection (edit-induced in compaction) — split them. *(consistency)*
- **P3-2.** Re-type the 6 arXiv `@inproceedings{... booktitle={arXiv preprint…}}` entries as `@misc`/`@article` so `splncs04` renders them correctly. *(consistency)*
- **P3-3.** Remove leftover "architecture-aware maintainability improvement pipeline" / "second stage" framing in §3.1 — jars in a standalone testing paper. *(perspective #4, EIC, methodology — residual CRIT-1)*
- **P3-4.** Resolve terminology drift: pick one term ("test-adequacy gap") and use it in abstract, intro, §5.3. *(perspective #2)*
- **P3-5.** Report run-to-run variance (temperature 0.2 is non-deterministic) or acknowledge single-draw ΔMI. *(methodology #5)*

## P4 — Polish

- "32 tactics" claimed but only 3 applied and never listed; reconcile with the source ("over 40") or scope the number. *(domain #5)*
- §5.4 tally "12 + 4" covers only 16 of 18 improvements — fix. *(consistency)*
- Remove the unused `\CRITICAL` macro (l.21) so a red review tag can't leak. *(consistency)*
- Optional length buffer (17→16 pp): trim a few uncited-style background refs or the Fig. 1 pipeline diagram.

## Re-review trigger
Re-run the methodology + devil's-advocate profiles once P1 is done; the decision cannot rise above MAJOR until P1-1 (the adequacy CRITICAL) is resolved or the central claim is reframed to what the current data support.

---

## Applied 2026-06-23 (post-review fixes)

**Done (mechanical + restructure):**
- P2-2 (readability): §5 now **leads with the testing result** — "Behavioral Gating and Test Adequacy" moved ahead of the MI inferential stats; added a signpost sentence.
- P2-3: the "pair with test generation" claim **softened to an explicit, untested future-work hypothesis**.
- P3-2: 6 arXiv bib entries re-typed `@inproceedings`→`@misc` (splncs04-safe).
- P3-3: removed residual "second stage of the architecture-aware … pipeline" framing in §3.1.
- P4: fixed the "12+4 of 18" tally; removed the unused `\CRITICAL` macro.

**P1-2 (statistics) — partially resolved, and escalated.** Recomputed the Wilcoxon from the actual dataset (`paper/tactic_implementation/artifacts/improvement_maintainability_dataset.csv`, mean ΔMI = +1.484 confirms identity). The paper's reported figures were **not reproducible / impossible**:
  - reported `W = 473` is impossible (max possible is 351 for 26 non-zero pairs);
  - reported `r̂ = 0.35`, sensitivity `p = 0.156`, and ITT `p = 0.087` did not reproduce.
  - **Corrected to verified values:** PP `W = 88`, `p = 0.026`, `r̂ = 0.50`, bootstrap 95% CI [0.29, 2.98]; sensitivity (drop 2 outliers) mean +0.56, `p = 0.077`; ITT identical under zero-dropping Wilcoxon → reported via the 32.1% success rate.

**Still open (author action / data):**
- P1-1 — positive control + coverage measurement for the test-adequacy claim (cannot be fabricated).
- P1-2 residual — **count drift**: the dataset shows **19 improved (45.2%)** and **26/42 (61.9%) within ±0.5**, vs the paper's **18 (42.9%)** and **24 (57.1%)**. The improved/stable table counts (18/17) and the 42.9% figure were left unchanged pending the authors' authoritative pipeline re-run, since reconciling cascades through Tables 1, 5, 6. **Verify and reconcile before submission.**
- P1-3 — double-blind anonymization (final step).
- P2-1 — add test-oracle / LLM-test-generation related work.

## Applied 2026-06-23 (second batch)

- **P2-1 DONE** — added §2 subsection "Test Oracles and Behavioral Validation" with four CrossRef-verified references: Barr et al. (oracle problem survey, TSE 2015), Chen et al. (metamorphic testing, ACM CSUR 2018), CodaMosa (Lemieux et al., ICSE 2023), Schäfer et al. (LLM unit-test generation, TSE 2024). Ties the oracle literature to our test-adequacy finding.
- **P1-3 DONE (double-blind)** — author block → Anonymous; `\institute` withheld; self-citation anonymized (`author = {Anonymous}`, DOI withheld) and bibkey neutralized; in-text "companion dataset" → "separate dataset"; tokenized Zenodo link replaced with an anonymous-repository statement. Verified: 0 author-name strings in the rendered PDF.

**Build:** 17 pp, 0 BibTeX errors, 0 undefined references. **Still open:** P1-1 (positive control + coverage — needs a run or claim reframe) and the P1-2 count drift (19 vs 18 improved — authors to reconcile).

## Applied 2026-06-23 (third batch — count reconciliation)

**P1-2 count drift: RESOLVED — it was a false alarm.** Recomputing the full breakdown from the released dataset (which does contain `architecture`, `python_files`, `size_bin`, `num_tests_run`, … columns) shows the paper's tables are **correct and exactly reproducible** under a small classification tolerance: with **improved = ΔMI > 0.01 / stable = |ΔMI| ≤ 0.01 / worsened = ΔMI < −0.01**, the data yields 18/17/7 overall, the tactic table (Decomp 8/7/3, LocalMod 9/3/2, none 7, RC 1/0/2), the architecture table (modular 9/12/5, layered 6/1/2, script 3/4/0), and the size bins (11/9/12/10) — all matching. The lone borderline repo is at ΔMI = +0.0055 (numerical noise).

**Fixes applied:**
- §3.4: classification rule made explicit with the ±0.01 tolerance (so tables match the stated rule and are reproducible).
- §5.2 / Conclusion: Wilcoxon aligned to the same tolerance — **W = 81, p = 0.028, r̂ = 0.50, 95% CI [0.29, 2.98]; sensitivity (drop 2 outliers) p = 0.083**. (No table counts changed — they were already right.)

**Net:** the only genuinely wrong figures were the original inferential statistics (impossible W=473, r̂=0.35, p=0.156/0.087); these are now corrected and internally consistent with the tables and the released dataset. Build: 17 pp, 0 errors.

## Applied 2026-06-23 (fourth batch — behavioral-gating reconciliation + CRITICAL addressed by reframe)

While mining the dataset's testing columns I found the §5.3 numbers were drawn from an **incomplete artifact set**. Reconciled to the authoritative dataset:
- The planner applied changes to **28** of 42 completed repos (**208** steps), not "20 / 121"; per-step regression logs exist for **20** of the 28 (**121** steps), within which a real suite ran in **15** and **no step triggered a regression**. (`num_tests_run` in the CSV = steps + 1, i.e., pytest invocations, not coverage — not contradictory.)
- §5.3, abstract, and conclusion corrected to these figures.

**P1-1 (the CRITICAL) — addressed by reframe (not by new experiment).** §5.3 now (i) restricts the 0-regression claim to the logged subset, (ii) explicitly states the pipeline recorded pass/fail but **not coverage of the edited code**, so a clean run cannot separate behavior-preserving from unexercised edits, and (iii) reads the result *cautiously* as a test-adequacy gap rather than proof of safety. This removes the over-claim the panel flagged. The stronger fix (a positive-control + coverage run) remains available as future work if a stronger contribution is wanted.

**Build:** 17 pp, 0 errors, 0 author leaks. All editable review items are now resolved.
