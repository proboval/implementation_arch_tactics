# Paper Reviewer Skill — ECSA 2026 Industry Track

Simulates ECSA 2026 peer reviewers. Produces structured feedback against the actual ECSA evaluation criteria and tracks the specific gaps from the EASE 2026 rejection.

## Quick start

From the repo root:

    Review paper/v2-ecsa-industry/main.tex using profile se-researcher in post-draft mode.

    Review paper/v2-ecsa-industry/main.tex using profile industry-practitioner in post-draft mode.

    Review paper/v2-ecsa-industry/main.tex using profile consistency-checker in post-draft mode.

## Profiles

| Profile | Perspective | Focus | Primary rejection gap |
|---|---|---|---|
| `se-researcher` | SA/empirical methods researcher | Methodology soundness, related work, evaluation validity, ground truth | PREV-R2-GAP-1, 2, 3 |
| `industry-practitioner` | Senior software architect in industry | Practical guidance clarity, ECSA industry track fit, discussion quality | PREV-R3-GAP-1, industry framing |
| `consistency-checker` | QA pass (not evaluator) | ECSA policy compliance, formatting, cross-section coherence | Formatting, policy gaps |

**Start with `se-researcher` and `industry-practitioner`** — these address the two dimensions ECSA scores: soundness and practical relevance.

## Modes

**post-draft** — You have a draft. The reviewer evaluates it.

    Review paper/v2-ecsa-industry/main.tex using profile se-researcher in post-draft mode.

Output: gap table with priorities (MUST/SHOULD/NICE/DEFER) + rejection gap tracking.

**pre-draft** — You're about to write a section. The reviewer produces a spec.

    Produce a spec for §Discussion using profile industry-practitioner in pre-draft mode.

Output: required dimensions checklist + decisions for human.

## Output location

Reviews → `paper/v2-ecsa-industry/reviews/`

Naming: `{section}-{mode}-{profile}-{date}.md`

Examples:
- `full-postdraft-se-researcher-2026-05-05.md`
- `discussion-predraft-industry-practitioner-2026-05-06.md`
- `full-postdraft-consistency-checker-2026-05-07.md`

## The EASE 2026 rejection gaps (always tracked)

Every review checks whether v2 closes these:

| Gap | Description | v2 Status |
|---|---|---|
| PREV-R2-GAP-1 | No ground truth for architecture classification | Partially fixed — 57 manually labeled repos |
| PREV-R2-GAP-2 | No repository size info despite context-window constraint | Open |
| PREV-R2-GAP-3 | No description of how tactics manifest in Python | Fixed — detection-only paper, no tactics applied |
| PREV-R2-GAP-4 | Semantic correctness / behaviour preservation not addressed | Fixed — detection-only paper |
| PREV-R3-GAP-1 | Paper tries to do too much (Detection + Selection + Implementation) | Fixed — detection only |

## Important dates

- Paper submission: May 8, 2026
- Notification: June 12, 2026
