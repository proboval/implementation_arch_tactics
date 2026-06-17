# Revision Roadmap (Prioritized)

**Target:** diploma/v3
**Date:** 2026-06-17
**Legend:** Defense = needed to defend; Pub = needed for journal/conference. Effort: Low/Med/High.

## Priority Overview

| P | Task | Effort | Impact | Gate | Source |
|---|------|--------|--------|------|--------|
| **P1** | Align title + Ch.3 terminology with the code-level reframing | Low | Critical | Defense | EIC-S3, R2-D3, F15, F23 |
| **P2** | Deliver or withdraw the §3.10.4 architecture-level metrics | Med | Critical | Defense | R1-T2, R2-S3 |
| **P3** | Add LOC-weighted ΔMI robustness column | Low–Med | Critical | Defense | R1-T1, R3-P2 |
| **P4** | De-confound the 18.2%→42.9% label-quality claim | Low | High | Defense | R1-M2, C6 |
| **P5** | Own the harness-design confound in §5.6/§5.11.3 | Low | High | Defense | R2-D2, C5 |
| **P6** | Name regression-to-the-mean + baseline-MI vs ΔMI check | Low | High | Defense | R3-P1 |
| **P7** | Reproducibility manifest: query+date, per-repo SHA+label, artifact link | Med | High | Defense | R1-R4, R1-R5, F5 |
| **P8** | Mechanical/consistency fixes | Low | Med | Defense | F6, F11, F12, F14 |
| **P9** | Non-architectural baseline (random split; static-analysis-only) | High | Critical | Pub | C2/C4 |
| **P10** | Second annotator + Cohen's κ (≥20–30 repos) | Med | Critical | Pub | C3 |
| **P11** | Verbatim prompts appendix + model/Radon version pinning | Low | High | Pub | R1-R1/R2/R3 |
| **P12** | Detection variance (repeat best config 3–5×) | Med | Med | Pub | R1-M1 |

## Detailed Action Items (Defense gate)

### P1 — Title & terminology alignment
- Retitle toward "…Code-Level Tactic Implementation Guided by Architectural Context…" **or** add a reframing paragraph in §1.1 if the title is administratively fixed.
- Replace "architecture-aware" with "guided by architectural context" in Ch.3 intro and §3.1.
- **Sections:** title, §1.1, §3 intro, §3.1. **Verify:** no remaining "architecture-aware" in body; conclusion term used throughout.

### P2 — Architecture-level metrics
- If computed: add a table of cyclic-dependency ratio, inter-module coupling intensity, package-tangle % (before/after) for the 42 Study-3 repos in §5.6.
- If not computed: delete the §3.10.4 promise and the corresponding future-work overlap.
- **Verify:** §3.10.4 claims and §5.6 reporting match exactly.

### P3 — LOC-weighted MI
- Recompute repository-level MI as a LOC-weighted mean; report ΔMI unweighted vs weighted side by side; re-run Wilcoxon + sensitivity on the weighted series.
- **Sections:** §3.6.1 (define), §5.2.2, §5.6. **Verify:** if weighting shrinks/removes the effect, state it as the cleanest evidence for the mechanical-splitting interpretation.

### P4 — De-confound label-quality claim
- State explicitly whether the 57 labeled repos are a subset of the 162.
- Restate "validated labels raise improvement 18.2%→42.9%" as associational, **or** run a within-sample arm (same repos, LLM-label vs human-label).
- **Sections:** §5.1, §5.5, §6 Obj.4. **Verify:** no causal language unsupported by within-sample data.

### P5 — Harness-design confound
- Add a paragraph: the Patch Agent cannot edit `__init__.py`, is capped at 400 lines/single-file/≤5 iterations, therefore cannot create packages by construction; the code-level ceiling is jointly an LLM and a harness property.
- **Sections:** §5.6.6, §5.11.3, App reference. **Verify:** central conclusion explicitly bounds its generality.

### P6 — Regression to the mean
- Add as an internal-validity threat; compute correlation/regression of baseline MI vs ΔMI; report whether low-baseline repos drive gains.
- **Sections:** §5.12.1, §5.5.4. **Verify:** alternative explanation named and quantified.

### P7 — Reproducibility manifest
- Record exact GitHub Search query, collection date, sort, screened count, and selection funnel (raw hits → 162 / 57).
- Publish a manifest: repo URL + commit SHA + (for the 57) label.
- Add a Data Availability statement with a working artifact link/DOI.
- **Sections:** §3.3, §4.2, new Data Availability. **Verify:** an independent reader can reconstruct both datasets.

### P8 — Mechanical fixes
- Replace `\chaptermark` placeholder strings (Ch.1, Ch.2) with real titles (F6).
- Relabel Study-3 "25.0%" as cloning failures, distinct from Study-1 LLM failures (F11).
- Reconcile 57→56 attrition (F12).
- Confirm whether Deferred Binding Time was ever selected; report frequency or drop from catalog (F14).

## Detailed Action Items (Publication gate)

### P9 — Baseline comparison
- Implement a random file-splitting arm (same #files extracted, no architectural reasoning) and a static-analysis-only arm; compare ΔMI distributions against the LLM pipeline. **Sections:** §3, §5.

### P10 — Second annotator
- Recruit a second annotator; label ≥20–30 repos oversampling modular-monolith; report per-class Cohen's κ; discuss disagreements. **Sections:** §3.3, §5.4, §5.12.1.

### P11 — Prompts & versions
- Add verbatim prompts (detection P1–P4, tactic selection, implementation) to the appendix; pin model snapshots/dates, Radon, Python, BM25 library versions. **Sections:** App, §3.6.1, §3.8, §4.

### P12 — Detection variance
- Repeat the best configuration (Qwen3+P2) 3–5× at temp 0.2; report mean ± SD accuracy. **Sections:** §5.4.

## Verification Criteria for Re-Review

| P | Pass criterion |
|---|----------------|
| P1 | No "architecture-aware" in body; title/abstract/conclusion consistent. |
| P2 | §3.10.4 promise and §5.6 results match (table present, or promise removed). |
| P3 | LOC-weighted ΔMI reported with re-run significance/sensitivity. |
| P4 | 162↔57 overlap stated; label claim associational or within-sample. |
| P5 | Harness constraints named as a co-cause of the code-level ceiling. |
| P6 | Regression-to-mean addressed with a baseline-MI vs ΔMI statistic. |
| P7 | Query+date+funnel documented; per-repo manifest + artifact link present. |
| P8 | All four mechanical items fixed. |
| P9 | ≥1 baseline arm compared. |
| P10 | Second-annotator κ reported. |
| P11 | Prompts in appendix; versions pinned. |
| P12 | Detection variance reported. |

## CRIT-* status after this roadmap is executed (expected)

| ID | After Defense items (P1–P8) | After Pub items (P9–P12) |
|---|---|---|
| CRIT-1 | ⚠️→✅ (reframe complete + arch metrics + LOC-weighted) | ✅ |
| CRIT-2/4 | ⚠️ (confound quantified, not controlled) | ✅ (baseline run) |
| CRIT-3 | ❌ (acknowledged only) | ✅ (κ reported) |
| CRIT-5 | ✅ | ✅ |
