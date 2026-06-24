# Reviewer Review (post-draft mode)

**Reviewer profile:** perspective-examiner
**Persona:** Professor of SE measurement, technical debt, and industry relevance (Seaman-style)
**Target:** ICTSS 2026 conference paper — "Can Regression Tests Catch Unsafe LLM Refactorings? Behavioral Gating of Architectural Tactic Implementation" (`paper/ICTSS26/main.tex`)
**Date:** 2026-06-23
**Mode:** post-draft
**Frame:** Springer LNCS / ICTSS (software testing venue), ≤15pp+2ref, double-blind. Reviewed as a conference submission, with publishability foregrounded over thesis defensibility.

---

## Summary judgment

The testing reframe is the right move and it largely works: the paper now tells one honest story — *the regression gate never fired, and the reason is a test-adequacy gap, not LLM reliability*. That is a genuine, publishable finding for a testing venue, and the abstract's plain-language rewrite is a real asset. But the reframe is not complete. The paper still carries two competing protagonists — the MI/maintainability study (RQ1) and the behavioral-oracle study (RQ2/RQ3) — and the maintainability machinery (five tables, sensitivity analysis, size/tactic/style breakdowns) consumes roughly two-thirds of the results while the headline finding gets one subsection. A reader arriving from the title expects testing and is instead walked through a maintainability experiment before the payoff. On measurement validity my central concern is now *inverted but unresolved*: the paper is admirably candid that MI is a weak proxy, but the **central testing claim rests on a null result whose construct validity is never examined** — "the gate never fired" could mean tests are inadequate (the paper's reading) OR that the edits genuinely preserved behavior (the unfalsifiable alternative), and the paper cannot distinguish them. Provisional decision: **MAJOR REVISION** — accept the finding, fix the narrative balance and the null-result interpretation.

## Structural completeness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| S1 | One coherent story after the testing reframe | ⚠️ Partial | Title/abstract/conclusion are testing-first, but §5.1–5.2 and §5.5–5.10 (5 of 8 results subsections + 5 of 6 tables) are the old maintainability study. The testing payoff is a single subsection (§5.3). The arc reads as "maintainability paper with a testing section bolted on front and back." | MUST |
| S2 | Construct validity of the *testing* claim | ❌ Missing | The whole contribution hinges on interpreting a zero-failure result as "test-adequacy gap." No evidence rules out the benign reading (edits were behavior-preserving). No coverage measurement on the 21 executing steps, no mutation/seeded-fault sanity check that the harness *can* catch a known break. Without this the headline is asserted, not measured (CRIT-1 analog for testing). | MUST |
| S3 | Practical/industry impact stated and scoped | ✅ Present | §5.10 implications (i)–(iv) are concrete and honestly scoped (~32% end-to-end, small repos only, prefer Localized Modification). Good. | — |
| S4 | Cost framing for a tool pitched as practical | ❌ Missing | No tokens, wall-clock, $/repo, or break-even by size. A practitioner cannot decide whether to run this. 256k context × up-to-10 planner iterations × self-healing is not free. | SHOULD |
| S5 | MI construct limitation reconciled with use | ✅ Present | §2.1, §5.7 (supplementary metrics), §5.10(iii), and Threats all concede MI is a weak proxy and foreground the behavioral question instead. This is the v3 CRIT-1 fix landing correctly. | — |
| S6 | Necessity of every table/figure | ⚠️ Weak | Six tables + one pipeline figure in a testing paper. Tables 5–6 (size/tactic/style) and the sensitivity prose support RQ1, which is now secondary. At ≤15pp, at least Table 5 or 6 should fold into text or move to the replication package to make room for the missing test-adequacy evidence (S2). | SHOULD |
| S7 | Terminology consistency | ⚠️ Weak | "behavioral gating" / "behavioral safety gate" / "regression gate" / "behavioral oracle" used semi-interchangeably; "test-adequacy gap" appears once (§5.3) but the abstract calls it "shortage of tests" and the intro "the adequacy of existing test suites is uncontrolled." Pick one term per concept and define it once. Also "architecture-aware" survives in §3.1 ("architecture-aware maintainability improvement pipeline") — a leftover from the old framing that now jars. | SHOULD |

## Persuasive effectiveness

| # | Dimension | Status | Gap | Priority |
|---|-----------|--------|-----|----------|
| P1 | Abstract accessibility to non-experts | ✅ Strong | The rewrite is genuinely good: "when an AI rewrites code, how do we know it has not quietly broken something?" lands the problem in one sentence; the *untested ≠ safe* distinction is crisp. Best-written part of the paper. Keep it. | — |
| P2 | Null result interpreted convincingly | ❌ Unconvincing | §5.3: "zero of the 121 steps introduced a new test failure ... This null result does not establish that the edits were behavior-preserving." Correct caveat, but the paper then *does* lean on the null to claim test inadequacy without independent evidence. A reviewer asks: did you ever confirm the gate can catch anything? One seeded regression would convert an absence of evidence into evidence of absence. | MUST |
| P3 | Title/intro/conclusion tell one story | ⚠️ Weak | The title asks a yes/no question ("Can regression tests catch...?") that the paper answers "we couldn't tell, because the tests are too sparse." That is a fine answer, but the body delays it behind the maintainability experiment. The *question* in the title is barely engaged until §5.3 (page ~9). | MUST |
| P4 | Measurement validity of MI handled honestly | ✅ Strong | The sensitivity analysis (outlier removal kills significance), the ITT vs per-protocol dual reporting, the size-bin table, and the explicit "metric arithmetic" admission (§5.9) are exactly the honest contextualization I look for. This is exemplary. | — |
| P5 | Practical impact is actionable | ⚠️ Weak | Implications are sound but the strongest practical claim — "pair refactoring with LLM-assisted test generation" — is asserted, not demonstrated or even cost-bounded. It is a hypothesis dressed as a recommendation. Flag it as future work, not a finding. | SHOULD |
| P6 | Numbers consistent across the paper | ⚠️ Weak | Abstract says "56 real open-source projects"; §3.3 says 57 labeled → one unavailable → 56 → 42 paired. Fine, but the abstract's "56" and the intro's "56" should be reconciled with the "57 manually labeled" in §3.3/§3.7 so a careful reader does not stumble. Also §3.1 says "second stage" and references a detection stage evaluated "separately" — confusing in a standalone paper where the reader never sees stage one. | SHOULD |

## Construct & measurement validity (primary lens)

**The MI proxy — well handled.** The paper no longer overclaims architecture-level maintainability from a file-level metric. §5.7's supplementary fan-out/package/depth table (all unchanged) is the decisive honesty move: it demonstrates, not merely concedes, that the pipeline edits at the code level. The "webapp-color vs Paper2Rebuttal" contrast (§5.4) showing MI cannot distinguish trivial splitting from genuine separation is precisely the construct-validity argument a measurement reviewer wants. CRIT-1 and CRIT-2 are effectively resolved *for the maintainability sub-claim* by reframing plus the supplementary metrics and sensitivity analysis.

**The test-as-oracle construct — NOT handled (the new central risk).** The paper has traded one contested proxy (MI for maintainability) for another it never validates: a **passing/empty regression run as a measure of behavioral safety**. The reasoning chain is:

> gate never fired (121 steps, 0 new failures, only 21 steps executed any test) ⇒ test-adequacy gap ⇒ "green run means untested, not safe."

The inference is plausible and probably correct, but it is *not measured*. Three checks are missing and at least one is cheap:
1. **Coverage of the modified lines** on the 15–21 steps where tests actually ran. If coverage of the edited code is near zero, that *measures* the adequacy gap directly instead of inferring it. (MUST — this is the construct validity of the headline.)
2. **A seeded-fault / mutation sanity check**: inject a known behavioral break into a covered repo and confirm the gate fires. Establishes the harness has discriminating power. Without it, "the gate never fired" is consistent with a harness that *can't* fire. (MUST.)
3. **The benign alternative explanation is never weighed**: for the 21 executing steps, perhaps the edits really were behavior-preserving (extracting a config module need not change behavior). The paper assumes inadequacy uniformly; it should separate "no test touched the change" from "tests touched it and passed."

Until #1/#2 exist, the headline ("the chief obstacle is the shortage of tests, not the AI") is a strong hypothesis, not a demonstrated result. For a *testing* venue this is the load-bearing claim and the reviewers will press exactly here.

## Practical / industry impact

- **Actionable, scoped findings (good):** small repos only, ~32% end-to-end, avoid Reduced Coupling. A practitioner can act on these.
- **Cost-blind (gap):** no token/time/$ accounting; "pair with test generation" has unknown cost and is the recommendation most likely to be quoted. Add even a rough per-repo cost and the break-even repo size.
- **Stakeholder framing (gap):** the most affected stakeholder — a maintainer of a *large* repo, where median ΔMI = 0.00 — is told the tool does nothing for them, but this is buried in §5.5. The honest headline "useful only for small, test-poor repos, where it is also least verifiable" deserves to be stated as the scope up front.

## Readability — sentence/structure level (primary lens)

Concrete fixes, with rewrites:

- **§3.1, leftover framing:** "This section describes the second stage of the architecture-aware maintainability improvement pipeline." In a standalone testing paper this confuses (what first stage? what is "architecture-aware" now?). Rewrite: *"We evaluate the tactic-selection and implementation stage of the pipeline, using pre-validated architecture labels (detection is reported in a companion artifact) so that detection error does not confound the results."*
- **§5.3, the key sentence is buried mid-paragraph:** the finding "a green test run after an LLM refactoring is therefore weak evidence of safety—it frequently means the change was *untested*, not *validated*" should open the subsection, not close it. Lead with the result.
- **Abstract → body term drift:** abstract "shortage of tests"; intro "adequacy ... is uncontrolled"; §5.3 "test-adequacy gap." Standardize on **"test-adequacy gap"** and use it verbatim in the abstract so the reader carries one phrase through.
- **§3.7 / §5.1 cross-study comparison** ("18.2%, +0.48" prior run vs 42.9% now, "consistent with, though not proof of ... since the datasets also differ") appears twice (§3.7 and §5.1) and each time half-retracts itself. In a 15-page paper, state it once, briefly, and stop hedging in two places.
- **Title vs delivery:** the title is a yes/no question; the answer ("we couldn't tell") should appear in the abstract's first finding sentence so the title is not left hanging. Consider tightening the abstract's middle paragraph to surface the answer earlier.
- **§4 length:** the Implementation section (Phases 1–5, pseudocode-level detail on BM25 k1/b, 400-line limits, timeouts) is proportionate for a thesis chapter but heavy for a 15-page testing paper where Phase 4's behavioral gating is the only part the thesis of the paper depends on. Compress Phases 1–3 and 5; keep "Behavioral gating" at full detail.

## Standing critical issue coverage

| ID | Issue | Status in this draft | Remaining action |
|---|---|---|---|
| CRIT-1 | MI ≠ architecture-level maintainability | ✅ Resolved | Reframed to code-level + supplementary metrics (§5.7) + behavioral focus. **But a new CRIT-1' has opened:** the test-as-oracle construct is now unvalidated (see Construct Validity, S2/P2). |
| CRIT-2 | File-splitting confound; no baseline | ⚠️ Partial | Confound is named and the arithmetic mechanism is shown (§5.4, §5.9); sensitivity analysis demonstrates fragility. Still **no random-split / do-nothing baseline** — acknowledged as future work in Threats. Acceptable for a conference paper given the candor, but a reviewer may still ask. |
| CRIT-3 | Single-annotator ground truth | ❌ Open | Threats (§6) states "single annotator (no inter-rater check)." Honestly disclosed but unaddressed. Lower stakes here since labels are upstream of the testing finding. |
| CRIT-4 | No comparison condition | ❌ Open | Disclosed as future work. The testing finding does not strictly need a baseline, but the maintainability sub-claim does. |
| CRIT-5 | Overgeneralization from niche | ✅ Resolved | Strongly scoped: §5.5 size table, §5.9 "noise" admission, §5.10(i) "small repositories only." No overgeneralization remains. |

## Defensibility vs. publishability

- **Defensible as MS-thesis-derived work?** Yes — the honesty, scoping, and threats treatment are above the bar.
- **Publishable at ICTSS as-is?** **No, after major work.** The finding is venue-appropriate and novel for a testing audience, but (a) the central testing claim is inferred, not measured — needs coverage data and a seeded-fault sanity check (S2/P2); (b) the narrative is still maintainability-led and must be rebalanced testing-first to match the title (S1/P3); (c) compaction is needed to fit 15pp while adding the missing evidence. With those, this is a credible ICTSS short/full contribution.

## Decisions required

1. **Validate the oracle claim:** Will you add (a) coverage-of-modified-code on the executing steps and (b) at least one seeded-fault test proving the gate *can* fire? Without one of these, can the headline survive review?
2. **Pick the protagonist:** Commit to testing-first. Will you move the maintainability tables (5–6) to the replication package / compress to text and promote §5.3 to the lead results subsection?
3. **Separate "untested" from "tested-and-passed":** For the 21 executing steps, will you report how many actually exercised the edited code, so "test-adequacy gap" is measured rather than assumed?
4. **Cost framing:** Will you add per-repo token/time/$ and a break-even repo size, given the practical pitch?
5. **Terminology lock:** Adopt "test-adequacy gap" verbatim across abstract/intro/results and retire "architecture-aware" (§3.1) and the duplicated cross-study hedge (§3.7/§5.1)?

---

_Priority definitions:_
- **MUST:** blocks publication or makes the central claim unsupported.
- **SHOULD:** significantly weakens credibility/quality — fix if feasible.
- **NICE:** strengthens the paper — optional polish.
- **DEFER:** legitimately out of scope — note as future work.
