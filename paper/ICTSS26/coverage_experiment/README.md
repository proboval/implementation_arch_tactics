# Coverage / positive-control experiment (closes review item P1-1)

The round-1 panel's blocking CRITICAL was: *the test-adequacy claim in §5.2 is
inferred from a null result (0 regressions) but never measured.* This experiment
supplies the measurement, turning the inferred claim into an empirical one.

## What it measures

For every repository the pipeline actually modified (`pipeline_status =
applied`, 28 repos), [`measure_edit_coverage.py`](measure_edit_coverage.py):

1. **Edit coverage (RQ3).** Clones the original repo, runs its test suite under
   `coverage.py`, and reports the line coverage of the files the LLM edited
   (`common_files_changed`). *Low coverage of edited files ⇒ the suite cannot
   detect a regression there ⇒ "0 regressions" means untested, not safe.*
2. **Positive control (RQ2, `--positive-control`).** Injects a trivial
   behaviour-breaking mutation into a covered line of an edited file and checks
   that at least one test then fails. *A detected mutation proves the gate can
   fire — so the observed null is meaningful, not a broken harness.*

Output: `coverage_results.csv` (repo, has_tests, suite_ok, modified_cov_pct,
overall_cov_pct, positive_control_detected, note).

## How to run

```bash
cd paper/ICTSS26/coverage_experiment
python3 measure_edit_coverage.py \
    --dataset ../../tactic_implementation/artifacts/improvement_maintainability_dataset.csv \
    --out coverage_results.csv \
    --positive-control --timeout 600
# quick smoke test first:  add  --limit 3
```

Needs `git`, `python3 ≥ 3.9`, and network. Each repo is built in its own venv,
so the host is not polluted; repos that fail to clone/install/collect are logged
and skipped (same attrition policy as the main pipeline). Expect some repos to
fail dependency install — report the N that did, do not hide it.

## How the result feeds the paper

- Replace the §5.2 caveat ("coverage … not measured") with the measured numbers:
  e.g. *"the existing suite covered a median of X% of the edited lines (0% in K
  of N repos); a seeded-fault positive control fired in M of the repos with
  non-zero coverage, confirming the gate works."*
- This converts the test-adequacy gap from an inference into a finding and
  resolves the panel's only remaining blocking item (CRIT-4 / P1-1).

## Preliminary static proxy (already available, no run needed)

See [`preliminary_static_proxy.md`](preliminary_static_proxy.md): of the 8 repos
where pre-existing files were edited, only 1 (whoogle-search) had any test that
even *imports* the modified module. Indicative but static and small-N — the
dynamic script above is the instrument to cite.
