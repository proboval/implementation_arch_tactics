# Replication Package

**Paper:** *Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating
of Architectural Tactic Implementation* (ICTSS 2026).
**Status:** anonymized for double-blind review (author identities and access
tokens removed; `GITHUB_TOKEN` in `pipeline_source/config.py` is a placeholder).

## Contents

```
coverage_experiment/      The behavioral-validation experiment (RQ2/RQ3, §5.2)
  measure_edit_coverage.py  Clones each modified repo, runs its suite under
                            coverage.py, reports coverage of the LLM-edited files,
                            and (--positive-control) seeds a fault to confirm the
                            gate fires.
  coverage_results.csv      Raw per-repo output (28 modified repositories).
  RESULTS.md                Summary: 54% no test suite; 79% no adequate oracle;
                            median 38% edit coverage; positive control fired.
dataset/
  improvement_maintainability_dataset.csv   The 56-repo outcome dataset
                            (architecture, chosen_tactic, mi_before/after, delta_mi,
                            size_bin, num_steps_applied, num_tests_run, outcome, …).
artifacts/
  static_analysis/          Per-repo Radon MI logs, code/architecture/documentation
                            maintainability, and architecture proxies (BEFORE/AFTER).
  tactic_application/        Per-repo planner records: repo_index.json and step_*.json
                            (each step's pytest result + `regression` flag). Repo-file
                            backups are omitted to keep the package lean.
pipeline_source/            The pipeline (Pipes & Filters): tactic selection +
                            test-gated implementation loop, static analysis, dataset
                            construction. `config.py` token is a placeholder.
prompts/
  prompts.md                Prompt material; the exact tactic-selection and
                            patch-generation templates also live inline in
                            pipeline_source/agent_filters/tactic_implementation.py
                            and tactic_definition.py.
```

## Reproducing the key results

**Maintainability statistics (§5.2).** From `dataset/improvement_maintainability_dataset.csv`,
compute ΔMI = mi_after − mi_before over the 42 rows with both values. With the
±0.01 classification tolerance: 18 improved / 17 stable / 7 worsened. Paired
Wilcoxon signed-rank (ties = |ΔMI| ≤ 0.01 dropped): **W = 81, p = 0.028**,
matched-pairs rank-biserial **r̂ = 0.50**; 10,000-resample bootstrap 95% CI for
mean ΔMI **[0.29, 2.98]**; dropping the two outliers → p = 0.083.

```python
import csv, numpy as np
from scipy import stats
d=[float(r["mi_after"])-float(r["mi_before"])
   for r in csv.DictReader(open("dataset/improvement_maintainability_dataset.csv"))
   if r["mi_before"] and r["mi_after"]]
d=[x for x in d if abs(x)>0.01]
print(stats.wilcoxon(d))   # W=81, p≈0.028
```

**Behavioral gating / test adequacy (§5.2, RQ2/RQ3).** Re-run the coverage
experiment (needs `git`, `python3 ≥ 3.9`, network):

```bash
cd coverage_experiment
python3 measure_edit_coverage.py \
    --dataset ../dataset/improvement_maintainability_dataset.csv \
    --out coverage_results.csv --positive-control
```

Each repo builds in its own venv (host not polluted); repos that fail to
clone/install are logged and skipped. Coverage uses best-effort dependency
installation, so per-repo coverage figures are lower bounds.

**Per-step gating record.** `artifacts/tactic_application/<repo>/step_*.json`
contains each modification's pytest outcome and `regression` flag (0 across all
logged steps); `artifacts/static_analysis/<repo>/` holds the MI and architecture
metrics behind the results tables.

## Requirements
`python3 ≥ 3.9`, `git`; for the stats snippet, `numpy` + `scipy`; for the pipeline,
see `pipeline_source/` imports (radon, an Ollama-served LLM, etc.).
