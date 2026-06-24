# Reviewer Review (post-draft mode) — ROUND 2

**Reviewer profile:** perspective-examiner
**Persona:** Professor of SE measurement, technical debt, and industry relevance (Seaman-style)
**Target:** ICTSS 2026 conference paper — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft, re-review (round 2)
**Frame:** Springer LNCS / ICTSS (software testing venue), ≤15pp+2ref, double-blind. Reviewed as a conference submission, readability/impact foregrounded.

---

## Summary judgment

The revision is a clear, substantive improvement on every readability item I raised. The abstract is now genuinely excellent plain-language exposition; the "architecture-aware pipeline" leftover in §3.1 is gone; "test-adequacy gap" is now defined and used as the load-bearing term in §5.2 and the Discussion; coverage-was-not-measured is stated explicitly (§5.2, Conclusion); and the testing result has been promoted with an explicit signpost ("Because behavioral validation is this paper's primary question, we report it first"). The title→abstract→intro→conclusion spine now tells *one* testing story coherently.

The one readability promise that is only **half-kept** is the lead burial. The author *says* the testing result comes first, but it does not: §5.1 is still "Overall Quantitative Impact," two maintainability tables (outcome distribution + MI stats) and the cross-study hedge, and only then does §5.2 deliver the behavioral finding. A reader arriving from the title is still walked through the maintainability outcome distribution before the payoff. It is one subsection of burial now, not five — but the signpost in §5.2 contradicts the actual ordering, which reads slightly self-undermining ("we report it first" appearing in the *second* subsection).

Decision: **moves from MAJOR REVISION → MINOR REVISION (borderline ACCEPT)** on my lens. Every readability/terminology MUST from round 1 is resolved or nearly so. The remaining items are a one-block reorder, two residual term drifts, and one cost-framing gap — none of which block publication. The construct-validity-of-the-null concern I raised (the test-as-oracle claim is inferred, not measured) is *honestly disclosed* now (§5.2 "coverage unmeasured," Conclusion) but still not measured; I hold that as a SHOULD here since the paper no longer overclaims it — it is framed as a cautious reading, which is defensible for a feasibility paper.

## Standing critical issue coverage

| ID | Issue | Status | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability | ✅ Resolved | Reframed code-level + supplementary metrics (§5.8) + behavioral focus (§5.13 "weak proxy"). The new test-as-oracle construct is now *disclosed as unmeasured* (§5.2) rather than asserted — improved over round 1. |
| CRIT-2 | File-splitting confound; no baseline | ⚠️ Partial | Mechanism shown (§5.4 webapp-color vs Paper2Rebuttal), sensitivity analysis kills significance (§5.3, $p=0.083$). Still no random-split/do-nothing baseline; disclosed as future work (§6). Acceptable given candor. |
| CRIT-3 | Single-annotator ground truth | ❌ Open | Disclosed in §6. Upstream of the testing finding; low stakes. |
| CRIT-4 | No comparison condition | ❌ Open | Future work (§6). Testing finding does not need it. |
| CRIT-5 | Overgeneralization from niche | ✅ Resolved | Strongly scoped: size table (§5.5), "metric arithmetic" (§5.13), "small repositories only" (§5.13 impl. (i)). |

## What moved since round 1 (readability ledger)

- **§3.1 "architecture-aware" leftover** — ✅ FIXED. Now: "This study evaluates whether regression testing can validate LLM-generated architectural code changes." No jarring framing residue.
- **Abstract plain-language** — ✅ Strong, kept. "when an AI rewrites code, how do we know it has not quietly broken something?" The *untested ≠ safe* distinction lands.
- **§5.2 key sentence buried mid-paragraph** — ✅ FIXED. The finding "a green run is weak evidence of safety—it often means the change was *untested*, not *validated*" now leads the closing paragraph and the subsection opens with the explicit RQ2/RQ3-first signpost.
- **Coverage limitation stated** — ✅ FIXED. §5.2 explicitly: "the pipeline recorded test pass/fail but *not* whether the executed tests cover the modified code."
- **Lead still buried** — ⚠️ PARTIAL. §5.2 (not §5.1) carries the testing result; the maintainability outcome distribution still precedes it.
- **Term drift** — ⚠️ PARTIAL. "test-adequacy gap" now standardized in body, but abstract still says "shortage of tests" and intro says "adequacy ... is uncontrolled." The phrase is not carried verbatim into the abstract.
- **Duplicated cross-study hedge (§3.7 / §5.1)** — ⚠️ STILL DOUBLED. The "18.2%, +0.48 ... consistent with, though not proof of ... since the datasets also differ" sentence appears at line 136 (§3.7) and again near-verbatim at line 259 (§5.1).
- **Cost framing** — ❌ STILL ABSENT. No tokens/wall-clock/$/break-even, despite the practical pitch and the "pair with test generation" recommendation.

## Remaining unclear sentences + fixes

1. **§5.2 signpost vs. ordering (the residual lead burial).** "Because behavioral validation is this paper's primary question, we report it first (RQ2, RQ3), then turn to the maintainability effect (RQ1)." But §5.1 (Overall Quantitative Impact, two tables) already came first. *Fix:* swap §5.1 and §5.2 so the behavioral result is literally the first results subsection, OR demote §5.1 to a one-paragraph "Outcome distribution" preamble and let §5.2 be the first full subsection. The signpost should not have to apologize for the layout.

2. **Abstract term drift.** Abstract: "the chief obstacle ... is not the AI itself but the shortage of tests." Body settles on "test-adequacy gap." *Fix:* use "test-adequacy gap" once in the abstract's final paragraph so the reader carries one phrase end-to-end: "...the chief obstacle is a *test-adequacy gap*—the projects' suites rarely exercise the AI's changes."

3. **Doubled cross-study hedge.** §3.7 (line 136) and §5.1 (line 259) both state the 18.2%→42.9% comparison and both half-retract with "since the datasets also differ." *Fix:* keep it once (in §5.1, where the new numbers live), delete from §3.7 or reduce §3.7 to a bare pointer.

4. **Abstract "56" vs §3.3 "57."** Abstract/intro say 56 projects; §3.3 says 57 labeled → 1 unavailable → 56 → 42 paired. Careful reader stumbles. *Fix:* one clause in the abstract or intro — "56 of 57 labeled projects (one became unavailable)."

5. **§5.13 implications (iii) sentence is dense.** "Never equate an MI gain---or a passing run of a sparse test suite---with a safe, architectural improvement; validate with an adequate test suite, generating one if necessary." Two recommendations packed into one clause. *Fix:* split into two sentences — the "untested ≠ safe" point deserves its own line given it is the paper's thesis.

## Practical / industry impact (my secondary lens)

- Scoped findings remain strong and actionable (§5.13 (i)–(iv)): small repos, ~32% end-to-end, prefer Localized Modification, avoid Reduced Coupling.
- **Cost-blind still.** The most-quotable recommendation ("pair with LLM-assisted test generation") has no cost bound; 256k context × up-to-10 planner iterations × self-healing is not free. A single rough $/repo and break-even repo size would let a practitioner act. SHOULD.
- Large-repo stakeholder (median ΔMI = 0.00) is now honestly surfaced in the size table and Discussion — good.

## Defensibility vs. publishability

- **Defensible as MS-derived work?** Yes — candor and scoping are above the bar.
- **Publishable at ICTSS?** **Yes, after minor work.** The readability MUSTs are resolved; what remains (reorder §5.1/§5.2, two term/number fixes, drop one duplicated hedge, add a cost line) is minor-revision territory. The testing finding is venue-appropriate, the story is coherent front-to-back, and the honesty about the unmeasured oracle is itself a strength rather than a fatal gap for a feasibility paper.

## Decisions required

1. **Reorder for the lead:** Will you move §5.2 ahead of §5.1, or reduce §5.1 to a preamble, so the testing result is literally first?
2. **Lock the term in the abstract:** Adopt "test-adequacy gap" verbatim in the abstract?
3. **Cost line:** Add a rough per-repo token/$/time and break-even repo size?

---

_Priority definitions:_ MUST blocks publication / unsupported central claim · SHOULD weakens credibility · NICE optional polish · DEFER out of scope.
