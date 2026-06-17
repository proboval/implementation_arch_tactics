# Revision Roadmap (Prioritized)

## Priority Overview

| Priority | Task | Effort | Impact | Reviewer Source |
|----------|------|--------|--------|----------------|
| **P1** | Address MI construct validity — add architecture-level metric OR reframe claim | High | Critical | DA C1, C2; EIC; R2; R3 |
| **P2** | Add baseline comparison (random splitting + static analysis) | High | Critical | DA C4 |
| **P3** | Second-annotator subset + Cohen's $\kappa$ | Medium | Critical | DA C3; R1; R2; EIC |
| **P4** | Condense Ch. 4 ~50%; move parameters to appendix; add CIs and multiple-comparison analysis | Medium | High | EIC; R1 |
| **P5** | Add cost-benefit estimate | Low | Medium | R3 |
| **P6** | Add automation bias / training-data bias discussion | Low | Medium | R3 |
| **P7** | Scope tactic catalog to implemented 4 (or add exclusion rationale) | Low | Medium | R2 |

## Detailed Action Items

### P1 — MI Construct Validity
- **Option A (preferred)**: Add an architecture-level metric (cyclic dependency ratio, modularity index, or inter-module coupling intensity) and re-run analysis on both MI and the new metric
- **Option B**: Reframe all claims to "code-level tactic implementation guided by architectural context"
- **Sections affected**: Abstract, §1.1, §3.6, §5.1, §5.7, §6.1

### P2 — Baseline Comparison
- Implement random file-splitting baseline (same number of files extracted, no architectural reasoning)
- Add static-analysis-only condition (e.g., pylint or Radon-based refactoring suggestions without LLM)
- Compare $\Delta MI$ distributions across conditions
- **Sections affected**: §3.9, §5.1, §5.3

### P3 — Second Annotator
- Recruit a second annotator (advisor or colleague familiar with SE architecture)
- Have them label a random subset of 20–30 repositories (oversampling modular monolith)
- Report Cohen's $\kappa$ for each style; discuss disagreements qualitatively
- **Sections affected**: §3.3, §5.2, §5.3, §6.3

### P4 — Condense Ch. 4 + Expand Analysis
- Move to appendix: BM25 $k$ justification, backup directory structure, iteration limits, per-iteration artifact format
- Keep in main text: system architecture overview, prompt construction, LLM invocation, key design decisions
- Add 95% CIs to Tables 5.2, 5.4, 5.5
- Add Bonferroni-Holm footnote to Table 5.3
- Add sensitivity analysis (excluding top-3 outliers from Wilcoxon test)

### P5 — Cost-Benefit Estimate
- Estimate per-repository: API tokens consumed, execution wall-clock time, cost per repository
- Estimate break-even: what MI gain justifies the cost?
- Distinguish by repository size category

### P6 — Automation Bias Discussion
- Discuss how LLM training data overrepresents certain architectural patterns (layered MVC)
- Discuss risk of systematic preference favoring certain styles over equally valid alternatives
- Add to threats to validity or integrated discussion

### P7 — Tactic Catalog Scope
- Either: remove unimplemented tactics from §2.4 (keep only Decomposability, Reduced Coupling, Localized Modification, Deferred Binding Time)
- Or: add explicit subsection explaining why the other 16 tactics were excluded (scope, feasibility, Python-specific constraints)

## Verification Criteria for Re-Review

| Priority | Verification Check |
|----------|-------------------|
| P1 | Architecture-level metric reported alongside MI; OR all "architecture-aware" claims replaced |
| P2 | At least one baseline condition added and compared |
| P3 | Second-annotator labels and Cohen's $\kappa$ reported |
| P4 | Ch. 4 reduced by ≥40%; CIs present for all key effect sizes |
| P5 | Cost-benefit estimates included |
| P6 | Automation bias discussion added |
| P7 | Tactic catalog scoped to match implementation |
