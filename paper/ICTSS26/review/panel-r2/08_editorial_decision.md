# Editorial Decision — ICTSS 2026 (Round 2 re-review)

**Decision: MINOR REVISION** (up from MAJOR REVISION in round 1).
The devil's advocate **withdrew both round-1 CRITICALs**, so the checkpoint rule no longer blocks acceptance.

## Cross-reviewer matrix (R1 → R2)

| Reviewer | R1 | R2 |
|---|---|---|
| EIC | Major | Major (borderline Minor) |
| Methodology | Major | **Minor** (reproduced every statistic from the dataset) |
| Domain | Major | **Minor** |
| Perspective | Major | **Minor** (borderline Accept) |
| Devil's advocate | 2 CRITICALs (blocked Accept) | **No CRITICAL stands** |
| Consistency | Pass-with-fixes | Pass-with-fixes |

## Why it moved
The central over-claim was defused *honestly* — by removing the inflation, not by spin: §5.2 now restricts "0 regressions" to the logged subset, states coverage of edited code was **not measured**, and reads the null as *evidence of* (not *proof of*) a test-adequacy gap. The statistics were corrected and independently reproduced from the released dataset (W=81, p=0.028, r̂=0.50; sensitivity p=0.083). The testing-oracle literature was added and used correctly. Anonymization applied; 17 pp.

## MUST fixes applied after this round
- Stale `p = 0.156` (Discussion + Threats) → corrected to `0.083` (matched §5.3/Conclusion).
- Table 1 outcome labels → the stated ±0.01 tolerance (`>0.01 / |Δ|≤0.01 / <−0.01`).
- `\label` collision (`sec:eval_pipeline` duplicate) removed; cross-ref repointed.
- §5.2 "we report it first" → "we address it before the detailed maintainability analysis" (matches layout).
- Abstract + Conclusion: the field-wide generalization scoped to "in these projects / in our sample."

Build after fixes: 17 pp, 0 BibTeX errors, 0 undefined references, 0 author-name leaks.

## What remains (no longer blocking)
- **CRIT-4 (the one thing between MINOR and ACCEPT):** no positive control / coverage measurement. Both Methodology and EIC say a single cheap `coverage.py` run on edited files would likely move the paper to ACCEPT. Needs a run.
- **SHOULD:** structural rebalance (MI subsections still occupy the majority); list/scope the "32 tactics"; note multiple-comparison family for subgroup tables; add cost framing; Cohen's κ for labels (CRIT-3). None block.

**Bottom line:** the paper is defensible and submittable as a MINOR-revision-quality manuscript; one coverage run would make it a clear ACCEPT.

## P1-1 instrument delivered (2026-06-24)

The blocking item (measure test adequacy, not infer it) now has a ready-to-run instrument:
`coverage_experiment/measure_edit_coverage.py` (+ README protocol). It clones each
applied repo, runs the suite under coverage.py, reports line coverage of the LLM-edited
files, and (`--positive-control`) injects a seeded fault to confirm the gate can fire.
A preliminary static proxy (`coverage_experiment/preliminary_static_proxy.md`) already
shows that in 6 of 7 repos with tests + an edited pre-existing file, no test even imports
the modified module — directional support pending the dynamic run.

**Path to ACCEPT:** run the script (needs the repos' environments), fold the measured
coverage + positive-control numbers into §5.2, replacing the "coverage not measured" caveat.

## P1-1 / CRIT-4 — RESOLVED by measurement (2026-06-24)

The coverage + positive-control experiment was **run** (not just scoped) over all
28 modified repos (`experiment_ictss/coverage_results.csv`, summary in
`experiment_ictss/RESULTS.md`). Measured result, now folded into §5.3 / abstract /
conclusion / threats:

- **15/28 (54%) had no test suite; 22/28 (79%) had no adequate oracle** for the edit
  (no tests + new-file-only + 0% coverage); among the 8 repos editing existing files,
  median coverage of those files was **38%** (0–85%).
- **Positive control fired** (seeded fault in a covered line failed the suite) → the
  gate works; the null is not a broken harness.
- **6 repos whose tests covered the edit showed 0 regressions** → those edits were
  most likely behavior-preserving.

This converts the headline from an inferred null into a **measured, disaggregated**
finding and answers the devil's advocate's C-1/C-2 directly (rival explanations
separated; gate validated). Build remains 17 pp, 0 errors, 0 leaks.

**Net standing:** with P1-1 measured, the last blocking item is closed. Remaining
items are SHOULD-level (structural rebalance, "32 tactics" listing, multiple-
comparison note, cost framing, Cohen's κ) — none block acceptance.
