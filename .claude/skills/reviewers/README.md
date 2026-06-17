# Thesis Reviewer Skill — Innopolis MS Thesis 2026

Simulates an expert review committee for the Master's thesis *"Automated Implementation of Architectural Tactics for Software Quality Improvement"*. Produces a multi-reviewer panel assessment, an editorial decision, and a prioritized revision roadmap — the same workflow whose output lives in `diploma/v3/review/`.

## Quick start

From the repo root:

    Run a full panel review of diploma/v3.

Or a single targeted pass:

    Review diploma/v3/chapters/chapter5.tex using profile methodology-examiner in post-draft mode.

    Review diploma/v3 (full thesis) using profile devils-advocate in post-draft mode.

    Review diploma/v3 using profile consistency-checker in post-draft mode.

## Profiles

| Profile | Persona archetype | Focus |
|---|---|---|
| `eic` | Editor / defense-committee chair | Significance, originality, defense readiness, publishability |
| `methodology-examiner` | Empirical-SE methods professor | Research design, statistics, validity threats, reproducibility |
| `domain-examiner` | Software-architecture specialist | Literature, tactic/architecture theory, domain contribution |
| `perspective-examiner` | SE-measurement & industry relevance | Construct/measurement validity, practical impact |
| `devils-advocate` | Rigorous critical empiricist | Strongest counter-argument, confounds, overgeneralization |
| `consistency-checker` | QA pass (not an evaluator) | Innopolis template, formatting, numeric/internal consistency, citations |

**Single pass → start with `methodology-examiner`.** **Complete assessment → run the full panel.**

## Modes

**post-draft** — You have a draft. The reviewer evaluates it.

    Review diploma/v3/chapters/chapter3.tex using profile methodology-examiner in post-draft mode.

Output: structural-completeness + persuasive-effectiveness tables (MUST/SHOULD/NICE/DEFER) + CRIT-* coverage.

**pre-draft** — You're about to write a chapter. The reviewer produces a spec.

    Produce a spec for chapter 5 (Evaluation) using profile domain-examiner in pre-draft mode.

Output: required-content checklist + structural guidance + decisions for the author.

**full-panel** — All examiners + devil's advocate + editorial synthesis + roadmap.

    Run a full panel review of diploma/v3.

## Editorial decision

ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT, mapped to defense readiness.
**Checkpoint:** an upheld devil's-advocate CRITICAL issue blocks ACCEPT (MAJOR REVISION at best).

## Output location

Reviews → `diploma/<version>/review/`.

- Full panel: numbered phases `01_reviewer_configuration.md` … `08_revision_roadmap.md` (as in `diploma/v3/review/`).
- Single profile / spec: `{chapter}-{mode}-{profile}-{date}.md`.

## Standing critical issues (always tracked)

These are carried in `call-context/thesis-profile.md` and checked by every review. As of thesis v3:

| ID | Issue | v3 status |
|---|---|---|
| CRIT-1 | MI does not measure architecture-level maintainability (construct validity) | Open — drives MAJOR REVISION |
| CRIT-2 | File splitting trivially inflates MI; no non-architectural baseline | Open |
| CRIT-3 | Single-annotator ground truth (no inter-rater reliability) | Open |
| CRIT-4 | No baseline comparison (random split / static-analysis-only) | Open |
| CRIT-5 | Overgeneralization from small script-based repos | Open |

## Rules

1. Never modify thesis source files — read only.
2. Never read `thesis.pdf` — review the `.tex` chapter sources.
3. Every review assesses CRIT-* coverage.
4. Calibrate to MS-thesis scope; flag journal-publishability separately.
