# Skill: Thesis Reviewer (Innopolis MS Thesis 2026)

Simulates an expert review committee for the Master's thesis **"Automated Implementation of Architectural Tactics for Software Quality Improvement"** (Innopolis University, 2026). Produces a structured, multi-reviewer panel assessment — a defense-committee chair, three specialist examiners, a devil's advocate, and a consistency checker — followed by an editorial synthesis and a prioritized revision roadmap.

The realized output of this process for thesis v3 lives in `diploma/v3/review/`. This skill regenerates that workflow for any thesis version.

## When to use

- **Pre-draft (spec mode):** Before writing a chapter/section, to produce a checklist of what an examiner will require.
- **Post-draft (review mode):** After a chapter or the full thesis is drafted, to evaluate it against MS-thesis defense criteria and identify blocking gaps before the defense.

## How to invoke

```
Review [chapters/full thesis] using profile [profile-name] in post-draft mode.
```
```
Run a full panel review of diploma/v3 (all profiles + editorial synthesis).
```
```
Produce a spec for [chapter] using profile [profile-name] in pre-draft mode.
```

Examples:
```
Review diploma/v3/chapters/chapter5.tex using profile methodology-examiner in post-draft mode.
```
```
Run a full panel review of diploma/v3.
```
```
Produce a spec for chapter 5 (Evaluation) using profile domain-examiner in pre-draft mode.
```

## Workflow

### Step 1 — Load context
1. Read **`call-context/ms-thesis-evaluation.md`** — Innopolis MS-thesis defense criteria, expected structure, and the bar each criterion sets.
2. Read **`call-context/thesis-profile.md`** — this thesis's profile, claims, and the standing critical issues (CRIT-1..N) the panel tracks across versions.
3. Read the relevant **profile(s)** from `profiles/`.
4. If post-draft: read the **chapter(s)** or full thesis under review (LaTeX `.tex` files in `chapters/`). Never read the `.pdf` directly — read the `.tex` sources.

### Step 2 — Execute the review
- Adopt the reviewer persona fully. Think and judge as that examiner would.
- In **pre-draft mode**: produce output following `templates/spec-output.md`.
- In **post-draft mode (single profile)**: produce output following `templates/reviewer-review.md`.
- In **full-panel mode**: produce, in order, the artifacts below (this reproduces `diploma/v3/review/`):
  1. `templates/reviewer-config-card.md` (Phase 0 — confirm/refresh the review team and thesis profile)
  2. One `templates/reviewer-review.md` per examiner profile (EIC, methodology, domain, perspective)
  3. One devils-advocate review (same template, CRITICAL/MAJOR/MINOR issue list)
  4. `templates/editorial-decision.md` (Phase 2 — cross-reviewer matrix, arbitration, decision letter)
  5. `templates/revision-roadmap.md` (prioritized P1..Pn action items + re-review verification criteria)
- Always assess coverage of the standing critical issues (CRIT-* in `thesis-profile.md`).

### Step 3 — Present output
- Output the completed template(s) in full.
- **Never modify the thesis source files.** The reviewer reads only; all changes are made by the author or a drafting agent.
- Wait for the author's decisions on MUST / P1 items before any revision.

## Editorial decision rules

The EIC decision is one of **ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT**, mapped to thesis-defense readiness:

| Decision | Thesis meaning |
|---|---|
| ACCEPT | Defense-ready; only cosmetic edits remain. |
| MINOR REVISION | Defensible after small, well-scoped fixes (no new experiments). |
| MAJOR REVISION | Sound core, but a blocking validity/scope issue needs substantive work before defense. |
| REJECT | Central claim is unsupported by the current evidence and cannot be salvaged by editing alone. |

**Checkpoint rule:** If the devil's advocate raises any **CRITICAL** issue that the panel upholds, the decision **cannot be ACCEPT** — it is MAJOR REVISION at best until that issue is resolved or the claim is reframed.

## Feedback loop

1. Author reviews the feedback and decides on MUST / P1 items.
2. Author (or drafting agent) revises the chapter.
3. Re-run the relevant profile (or full panel) to verify fixes against the roadmap's verification criteria.
4. Repeat until no MUST / P1 items remain and no CRITICAL issue stands.

## Available profiles

| Profile | File | Persona archetype | Evaluates |
|---|---|---|---|
| EIC / committee chair | `profiles/eic.md` | Editor & architecture authority | Overall significance, originality, defense readiness, journal-publishability |
| Methodology examiner | `profiles/methodology-examiner.md` | Empirical-SE methods professor | Research design, statistical rigor, validity threats, reproducibility |
| Domain examiner | `profiles/domain-examiner.md` | Software-architecture specialist | Literature coverage, tactic/architecture theory, domain contribution |
| Perspective examiner | `profiles/perspective-examiner.md` | SE-measurement & industry-relevance professor | Construct/measurement validity, practical impact, cross-disciplinary fit |
| Devil's advocate | `profiles/devils-advocate.md` | Rigorous critical empiricist | Strongest counter-argument, confounds, overgeneralization, alternative explanations |
| Consistency checker | `profiles/consistency-checker.md` | QA pass (not an evaluator) | Innopolis template compliance, formatting, internal/numeric consistency, citations |

**For a single targeted pass, start with `methodology-examiner`** (it owns the validity gaps that most often block a defense). For a complete assessment, run the **full panel**.

## Output location

Reviews go to `diploma/<version>/review/` (e.g., `diploma/v3/review/`).

- **Full panel** uses the numbered phase convention already in `diploma/v3/review/`:
  `01_reviewer_configuration.md`, `02_eic_review.md`, `03_methodology_review.md`, `04_domain_review.md`, `05_perspective_review.md`, `06_devils_advocate_review.md`, `07_editorial_decision.md`, `08_revision_roadmap.md` (+ optional analysis notes `09_*`).
- **Single profile / spec:** `{chapter}-{mode}-{profile}-{date}.md`
  e.g. `chapter5-postdraft-methodology-examiner-2026-06-17.md`.

## Rules

1. **Non-interactive:** full output in one pass; no back-and-forth mid-review.
2. **Never modify source files:** the reviewer reads only.
3. **Never read PDFs:** review the `.tex` chapter sources, not `thesis.pdf`.
4. **Always track CRIT-\*:** every review explicitly assesses the standing critical issues from `thesis-profile.md`.
5. **Calibrate to the artifact:** this is a Master's thesis, not a journal paper — require depth and honest limitations, but do not impose demands beyond an MS scope. Where the thesis is also targeted at a journal/conference, flag publishability separately from defensibility.
6. **Evidence-anchored:** cite specific sections/lines/tables. Do not invent weaknesses.

## File structure

```
.claude/skills/reviewers/
├── SKILL.md                              ← this file
├── README.md                             ← quick start
├── profiles/
│   ├── eic.md                            ← committee chair / editor
│   ├── methodology-examiner.md           ← PRIMARY: empirical methods, validity, statistics
│   ├── domain-examiner.md                ← software-architecture domain contribution
│   ├── perspective-examiner.md           ← measurement validity, practical impact
│   ├── devils-advocate.md                ← adversarial challenge (CRITICAL/MAJOR/MINOR)
│   └── consistency-checker.md            ← FULL THESIS ONLY: template + consistency QA
├── call-context/
│   ├── ms-thesis-evaluation.md           ← Innopolis defense criteria & expected structure
│   └── thesis-profile.md                 ← this thesis's profile + standing CRIT-* issues
└── templates/
    ├── reviewer-config-card.md           ← Phase 0: review team + thesis profile
    ├── reviewer-review.md                ← individual reviewer output
    ├── editorial-decision.md             ← cross-reviewer synthesis + decision letter
    ├── revision-roadmap.md               ← prioritized action items + re-review criteria
    └── spec-output.md                    ← pre-draft chapter spec
```
