# Critical Issues — Must Fix Before Submission

**Paper:** paper/tactic_implementation/main.tex
**Date:** 2026-06-10
**Source:** All three reviewer profiles (SE Researcher, Industry Practitioner, Consistency Checker)

---

## DESK-REJECT risks

| # | Issue | Location | Fix |
|---|-------|----------|-----|
| D1 | `\begin{acks}` is commented out — no AI disclosure | End of doc | Uncomment, add names and roles of all AI tools used (e.g., Qwen3-Coder for code generation, Claude for writing assistance) |

---

## MUST fix (submission-blocking)

| # | Issue | Location | Fix |
|---|-------|----------|-----|
| M1 | Section 4 (Implementation) is missing | §1 roadmap promises it | Write a dedicated Implementation section covering pipeline architecture, prompting strategy, and planner loop |
| M2 | Section 7 (Conclusion) is missing | §1 roadmap promises it | Write Conclusion: summary of findings, main takeaway, future work |
| M3 | Section numbers in §1 roadmap do not match actual sections | §1 | After writing M1+M2, renumber roadmap to match actual section numbers |
| M4 | Abstract lists stages "(1)…and (3)…" — stage (2) is unnamed | Abstract | Name or describe the missing stage |
| M5 | `\ref{sec:eval_arch_detection}` and `\ref{sec:eval_pipeline}` are undefined in this document — will render as `??` | §3.1, §4.1, §4.4 | Either define the labels (add brief inline summary of each referenced study) or remove the references and rephrase |
| M6 | Failure count inconsistency: §3.3 says 14 failed; §4.6 says 10 + 5 = 15 | §3.3, §4.6 | Reconcile: correct one of the two numbers |
| M7 | Null hypothesis stated but no statistical test reported | §3.1, §5 (Results) | Run `scipy.stats.wilcoxon` on the 42 paired (before, after) MI values; report W, p-value, and effect size r |
| M8 | `anonymous` flag in document class — check vs. submission policy | Line 3 | Verify EASE 2026 double-blind policy; remove or keep accordingly |

---

## MUST fix (claim integrity)

| # | Issue | Location | Fix |
|---|-------|----------|-----|
| M9 | Title and abstract claim "implement" and "improve maintainability" without behavioral verification | Title, Abstract | Qualify: "syntactic/metric improvement without behavioral verification" — or run test suites on a subset of improved repos and report pass rates |
| M10 | MI gaming confound: 12 of 18 improvements = adding an MI=100 file; this is metric-arithmetic, not architectural improvement | §4.2–4.3, Discussion | Add a trivial baseline (what does adding any simple file produce?), or explicitly discuss that the observed gains are partially metric-arithmetic and defend the architectural value of the LLM's specific decomposition choices |
| M11 | End-to-end success rate unreported: paper reports 42.9% (of completed), actual is 18/56 = 32.1% | §4.1, Discussion | Report both figures with explicit explanation of the difference |
| M12 | 40.5% "stable" cases include runs where code was modified but ΔMI = 0 — framed as neutral, should be framed as failed interventions | §4.1, Discussion | Reframe: distinguish planner-failure stable (pipeline failure) from no-op stable (code changed but MI unchanged) |

---

## MUST fix (practitioner value)

| # | Issue | Location | Fix |
|---|-------|----------|-----|
| M13 | No "Practitioner Guidance" or "Implications for Practice" section | Discussion | Add a subsection with at minimum: (a) use only on tiny/small repos; (b) always validate with test suite; (c) end-to-end success rate is 32.1%; (d) treat stable outcomes as failures |
| M14 | The clearest actionable finding — "median ΔMI = 0.00 for repos >80 files, do not use there" — is buried in Table 3 and never stated as guidance | §4.3 | State explicitly as a practitioner recommendation |

---

## SHOULD fix (significant but not blocking)

| # | Issue | Fix |
|---|-------|-----|
| S1 | Model identifier `qwen3-coder-next:cloud` is not reproducible | Replace with specific Qwen3-Coder release tag or Huggingface model ID |
| S2 | Fan-out and docstring coverage "collected" but never reported | Either add a supplementary table or remove the claim that they were collected |
| S3 | No comparison baseline (random tactic, trivial extraction) | Add even a one-row baseline to Table 2 |
| S4 | Causal claim: "validated labels explain the 42.9% vs 18.2% difference" cannot be supported — different datasets | Reframe as "consistent with the hypothesis" rather than an explanation |
| S5 | One before/after code diff would be worth more than all the MI tables to a practitioner audience | Add one 10-line diff example in §4.2 or the new Implementation section |
| S6 | EASE 2026 page limit: verify that this paper fits the correct submission category (short paper vs. full paper) | Check CFP page limit |
| S7 | Table 4 column "Impr. / Worse. / Stable" has three values in one cell | Split into three numeric columns |

---

## Summary counts

| Priority | Count |
|----------|-------|
| DESK-REJECT | 1 (D1) |
| MUST — structural | 8 (M1–M8) |
| MUST — claim integrity | 4 (M9–M12) |
| MUST — practitioner | 2 (M13–M14) |
| SHOULD | 7 (S1–S7) |
| **Total MUST** | **14** |
