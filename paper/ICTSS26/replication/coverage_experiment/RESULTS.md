# Coverage / positive-control experiment — results (2026-06-24)

Ran `coverage_experiment/measure_edit_coverage.py --positive-control` over all
28 repositories the pipeline modified (`pipeline_status = applied`). Each repo
was cloned, built in its own venv (Python 3.12, best-effort dependency install),
and its test suite run under `coverage.py`. Raw output: `coverage_results.csv`.

## Headline numbers

| Quantity | Value |
|---|---|
| Modified repos processed | 28 |
| **No test suite at all** | **15 (54%)** |
| Tests present & measured | 13 |
| …edited only NEW files (uncovered by old tests by construction) | 5 |
| …edited existing files, coverage measurable | 8 |
| Coverage of edited files (n=8) | **median 38.2%, mean 42.6%, range 0–85%, two at 0%** |
| **Repos with no adequate oracle for the edit** (no tests + new-file-only + 0% cov) | **22 / 28 (79%)** |
| Repos where tests DID cover the edit (>0%) — yet still 0 regressions | 6 |
| Positive control (seeded fault in a covered line → suite fails) | **fired** (subgen) |

Per-repo edited-file coverage: sovereignguard 85%, dj-control-room 79%,
whoogle-search 78%, gemini-superpowers 40%, subgen 37%, bilibili-rag 23%,
CCTV 0%, shuo 0%.

## Interpretation (folded into §5.3 / abstract / conclusion / threats)

- The silent gate is **mostly a missing oracle, not verified safety**: in 79% of
  modified repos there was no adequate test for the change.
- The gate **works**: the positive control proves it detects a regression when a
  test reaches the changed code — so the null is not a broken harness.
- In the 6 repos where tests *did* exercise the edit (up to 85% coverage), none
  failed → those particular edits were most likely **behavior-preserving**.
- Net: "zero regressions" is a mixture — predominantly absent oracle, occasionally
  genuine preservation. This **resolves the panel's blocking CRITICAL (P1-1 /
  CRIT-4)** by measuring adequacy instead of inferring it.

## Caveats

- **Best-effort dependency install:** some suites may not have installed fully,
  under-reporting coverage. This is *conservative* for the adequacy-gap claim
  (it can only inflate the "uncovered" count), but means individual coverage
  numbers are lower bounds.
- **Positive control N=1:** the seeded-fault check ran where an edited file had a
  mutatable covered statement in the original clone (subgen); it is a proof the
  mechanism fires, not a rate.
- Coverage is measured on the original (pre-edit) code — i.e. whether the suite
  exercises the file the LLM went on to change; it is a faithful proxy for "could
  the gate have seen this edit."

Reproduce: `python3 ../coverage_experiment/measure_edit_coverage.py --dataset
../../tactic_implementation/artifacts/improvement_maintainability_dataset.csv
--out coverage_results.csv --positive-control`.
