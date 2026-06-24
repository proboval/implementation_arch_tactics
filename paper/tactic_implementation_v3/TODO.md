# TODO — tactic_implementation_v3 (EASE 2026 paper)

Status snapshot from review of repo + both feedback tracks (2026-06-23).
Paper: *"Can LLMs Implement Architectural Tactics?"* — [main.tex](main.tex)

## Two review tracks

| Track | Location | Verdict |
|---|---|---|
| Paper peer review (Falessi, EASE 2026) | [review/review_methodology_peer1.md](review/review_methodology_peer1.md) | **60/100 — Major Revision** |
| Thesis panel (`reviewers` skill, 6 personas) | [../../diploma/v3/review/](../../diploma/v3/review/) | **MAJOR REVISION (Jun 2026)** |

Evidence doc shared by both: [review/09_experiment_5_architectural_analysis.md](review/09_experiment_5_architectural_analysis.md).
Its "DA C1 / DA C2" = Devil's Advocate **CRIT-1 / CRIT-2** (the two CRITICALs that block ACCEPT).
Standing critical issues tracked in [thesis-profile.md](../../.claude/skills/reviewers/call-context/thesis-profile.md).

## Open / actionable items

- [ ] **(#1) Broken supplementary reference** — `main.tex` cites `examples/webapp-color-decomposability.diff`, which is **not in the repo**. Add it to the Zenodo package or drop the reference.
- [ ] **(#2) Docstring coverage** — still "collected" but not reported (fan-out now is, Table 7). Add it to the supplementary table or stop claiming it's collected.
- [ ] **(#3) RQ3 multiple-comparison** — add one sentence framing the tactic/architecture breakdowns (§5.4–5.5) as *exploratory* (closes peer-review issue #8).
- [ ] **(#4) Stable-category vs tactic table consistency** — "(none selected) = 7" (Table 5) vs "7 planner failures / 7 no-op" (§5.6) aren't obviously the same 7. Reconcile before a reviewer recomputes.
- [ ] **(#5) Verify inferential stats** — reproduce W=473, p=0.023, r̂=0.35, bootstrap CI [0.21, 3.04], and the sensitivity result (p=0.156) from [../tactic_implementation/artifacts/improvement_maintainability_dataset.csv](../tactic_implementation/artifacts/improvement_maintainability_dataset.csv). (No data CSV in this folder.)
- [ ] **(#6) Confirm Zenodo package contents** — exact prompt templates + full pipeline source (767 LOC) + model params actually present (peer-review issues #6, reproducibility).

## Bigger gaps still open (require new work, currently deferred)

- [ ] **CRIT-2 / CRIT-4 — empirical baseline** — no random-file-split / "do-nothing" control was run. Currently only analytical calibration (100/(N+1)) + outlier sensitivity. A trivial baseline would calibrate the metric-arithmetic effect. *Deferred to future work in Threats.*
- [ ] **CRIT-3 — inter-rater reliability** — labels from a single annotator; no second annotator / Cohen's κ. Acknowledged, not fixed.

## Already addressed in v3 (verify, don't redo)

Peer review (Falessi) — resolved:
- [x] #1 Wilcoxon test added (new §5.2)
- [x] #2 Bootstrap 95% CI + p-values
- [x] #3 Failure count reconciled → 14 (10 clone + 4 impl)
- [x] #4 Sampling criteria para (pool ~200, keywords, inclusion a/b/c)
- [x] #5 MI-gaming / metric-arithmetic para + sensitivity analysis
- [x] #7 Model ID `Qwen/Qwen3-Coder-34B-Instruct` + all gen params
- [x] #9 Failed-vs-completed covariate comparison
- [x] #10 Regression-to-the-mean discussion in Threats

Thesis CRIT issues:
- [x] **CRIT-1** resolved by reframing to "code-level, not architecture-level" + supplementary architecture-metrics table (§5.7)
- [x] **CRIT-5** scoped to small repos (<30 files); framed as "early feasibility evidence"

## Suggested next step

Pick one:
1. **Verify** the statistics against the CSV (#5) — makes the new §5.2 defensible.
2. **Fix** loose ends #1–#4 — small self-contained `main.tex` edits.
3. **Re-review** v3 with the `reviewers` skill (methodology-examiner or full panel) for an updated verdict + CRIT-* status.
