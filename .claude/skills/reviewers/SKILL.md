# Skill: Paper Reviewer (ECSA 2026 Industry Track)

Simulates expert peer reviewers for the ECSA 2026 Industry Track short paper on LLM-based software architecture detection. Provides structured, actionable feedback using ECSA's actual evaluation criteria and the specific weaknesses from the EASE 2026 rejection.

## When to use

- **Pre-draft (spec mode):** Before writing a section, to produce a checklist of what it must contain.
- **Post-draft (review mode):** After writing a section or the full paper, to evaluate it against ECSA criteria and identify gaps.

## How to invoke

```
Review [section/file] using profile [profile-name] in post-draft mode.
```

```
Produce a spec for [section] using profile [profile-name] in pre-draft mode.
```

Examples:
```
Review paper/v2-ecsa-industry/main.tex using profile se-researcher in post-draft mode.
```
```
Review paper/v2-ecsa-industry/main.tex §Discussion using profile industry-practitioner in post-draft mode.
```
```
Review paper/v2-ecsa-industry/main.tex using profile consistency-checker in post-draft mode.
```
```
Produce a spec for §Discussion using profile industry-practitioner in pre-draft mode.
```

## Workflow

### Step 1 — Load context
1. Read the relevant **profile** from `profiles/`.
2. Read **`call-context/ecsa-2026-industry-track.md`** — evaluation criteria, paper type requirements, formatting rules.
3. Read **`call-context/rejection-gaps.md`** — EASE 2026 reviewer criticisms and which ones v2 must close.
4. If post-draft: read the **draft** or section to review.

### Step 2 — Execute review
- Adopt the reviewer persona fully. Think and evaluate as that person would.
- In **pre-draft mode**: produce output following `templates/spec-output.md`.
- In **post-draft mode**: produce output following `templates/review-output.md`.
- Always check the rejection gaps (PREV-R2-GAP-1..4, PREV-R3-GAP-1) for coverage.

### Step 3 — Present output
- Output the completed template in full.
- Do NOT modify any paper files.
- Wait for human decisions on MUST items before revising.

## Feedback loop

1. Human reviews the feedback and decides on MUST items.
2. Human (or drafting agent) revises the section.
3. Re-run the review to verify fixes.
4. Repeat until no MUST items remain.

## Available profiles

| Profile | File | Best for | Primary gap addressed |
|---|---|---|---|
| SE researcher | `profiles/se-researcher.md` | Methodology, related work, soundness, evaluation validity | PREV-R2-GAP-1, 2, 3 |
| Industry practitioner | `profiles/industry-practitioner.md` | Practical relevance, discussion clarity, ECSA industry fit | PREV-R3-GAP-1, industry framing |
| Consistency checker | `profiles/consistency-checker.md` | ECSA compliance, formatting, cross-section coherence | ECSA policy gaps |

**Start with `se-researcher`** — it addresses the soundness gaps that most likely caused the EASE rejection. Then run `industry-practitioner` to verify the industry-track framing holds.

## Output location

Reviews go to `paper/v2-ecsa-industry/reviews/`.

Naming: `{section}-{mode}-{profile}-{date}.md`

Examples:
- `full-postdraft-se-researcher-2026-05-05.md`
- `discussion-predraft-industry-practitioner-2026-05-06.md`
- `full-postdraft-consistency-checker-2026-05-07.md`

## Rules

1. **Non-interactive:** Full output in one pass. No back-and-forth during review.
2. **Never modify source files:** Reviewer reads only; all changes made by human or drafting agent.
3. **Always check rejection gaps:** Every review must explicitly assess PREV-GAP coverage.
4. **Phase-aware:** This is a submission-stage paper with a May 8 deadline. Evaluate what is written; flag only what can realistically be fixed.
5. **Industry track framing:** ECSA industry track selects on originality, *practical relevance*, and potential for discussion — not just academic soundness. Both dimensions must be checked.

## File structure

```
.claude/skills/reviewers/
├── SKILL.md                                  ← this file
├── README.md                                 ← quick start
├── profiles/
│   ├── se-researcher.md                      ← PRIMARY: SA/empirical methods researcher
│   ├── industry-practitioner.md              ← PRIMARY: practitioner value and ECSA fit
│   └── consistency-checker.md               ← FULL PAPER ONLY: ECSA compliance + coherence
├── call-context/
│   ├── ecsa-2026-industry-track.md           ← evaluation criteria, paper type, policies
│   └── rejection-gaps.md                     ← EASE 2026 gaps + v2 coverage status
└── templates/
    ├── review-output.md                      ← post-draft output format
    └── spec-output.md                        ← pre-draft output format
```
