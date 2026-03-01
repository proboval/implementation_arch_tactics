# Verification Scripts

Scripts to validate all numerical claims in `paper/v1/main.tex` against raw experiment data.

## Prerequisites

```bash
pip install scipy numpy
```

## Usage

Run from the repository root (`implementation_arch_tactics/`):

```bash
# On Windows (MSYS/Git Bash) — force UTF-8 output
PYTHONUTF8=1 python paper/v1/scripts/verify_data.py
PYTHONUTF8=1 python paper/v1/scripts/verify_stats.py
PYTHONUTF8=1 python paper/v1/scripts/verify_artifacts.py
```

## Scripts

### verify_data.py
Verifies all `\CHECK{DATA}{...}` markers against the experiment CSV.

**Input:** `experiments/improvement_maintainability_experiment_3.csv`

**Checks:**
- Overall counts: total, null, paired, improved, stable, degraded
- Percentages: null%, improved%, stable%, degraded%
- Descriptive statistics: mean, median, std of MI before/after
- Per-tactic breakdown (Table 2): N, null, improved, stable, degraded, mean dMI
- Per-architecture breakdown (Table 3): N, null%, improved, degraded, mean dMI
- Specific repo values: get_subscribe delta, whoogle before/after
- Top 3 individual gains
- Whether all degradations are in modular_monolith

### verify_stats.py
Recomputes all `\CHECK{STAT}{...}` markers — statistical tests from raw paired data.

**Input:** `experiments/improvement_maintainability_experiment_3.csv`

**Checks:**
- Shapiro-Wilk normality test (justifies Wilcoxon choice)
- Wilcoxon signed-rank test on all 121 pairs (correct approach)
- Wilcoxon on 29 non-zero pairs (current paper approach, for comparison)
- Matched-pairs rank-biserial correlation r (correct paired effect size)
- Cliff's delta (current paper approach — note: wrong for paired data)
- Per-architecture mean dMI
- Reduced Coupling improvement rate

### verify_artifacts.py
Verifies supplementary metrics from `artifacts_experiment_3/`.

**Input:** `artifacts_experiment_3/artifacts/static_analysis/BEFORE/` and `AFTER/`

**Checks:**
- Number of paired repos (expect 123)
- Fan-out: changed count, mean delta, increased/decreased
- Docstring coverage: changed count, mean delta, increased/decreased
- Package count changes
- MI cross-validation between artifacts and CSV

## Output Format

Each check prints `[OK]` or `[!!]` with the paper value and computed value:
```
  [OK] total_repos: paper=162, computed=162  [OK]
  [!!] stable_pct_of_paired: paper=56.8, computed=76.0  [MISMATCH]
```

## Known Mismatches

1. **stable_pct_of_paired**: Paper says "56.8% of completed cases" but 92/121=76.0%. The 56.8% is 92/162 (of total). Denominator mismatch in text.
2. **Wilcoxon W**: Paper says W=75.0, scipy computes W=360.0. Different W conventions (T- vs T+). p-value matches.
3. **Cliff's delta**: Value (0.017) is correct but Cliff's delta is the wrong metric for paired data. Should use matched-pairs rank-biserial r=0.28.
