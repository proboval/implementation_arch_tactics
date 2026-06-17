# Perspective Review — Dr. Carolyn Seaman

## Cross-Disciplinary Relevance and Practical Impact
This thesis sits at the intersection of software architecture, AI for software engineering, empirical methods, and measurement science. The practical impact on open-source maintenance is potentially significant, particularly for small projects with limited resources for architectural improvement.

## Strengths
- **Practical significance of the failure rate.** The 25.3% failure rate is presented as a weakness, but from a practitioner's perspective it is a *critical finding*. Any team evaluating whether to adopt LLM-based refactoring needs this number. The paper correctly separates infrastructure failures from algorithmic ones, which is essential for risk assessment.
- **Size moderation analysis.** The finding that repository size is the dominant moderating factor (§5.3.2, Table 5.5) has immediate practical implications: the pipeline is appropriate for small repositories but ineffective for large ones. This is precisely the kind of actionable knowledge that practitioners need.
- **Honest assessment of confidence calibration.** The calibration inversion finding — Gemini reports highest confidence despite having the lowest accuracy (§5.2.6) — is both scientifically important and practically relevant. Developers who rely on LLM confidence as a reliability signal are being misled, and the paper documents this clearly.
- **The three-study architecture is pedagogical.** The narrative arc (build pipeline → discover limitation → isolate and diagnose → test fix) models good empirical practice. This makes the thesis valuable as a teaching case for research methodology in SE.

## Weaknesses
- **The practical recommendations (§6.1.6) are overly cautious.** The six recommendations are valid but conservative. The paper could be bolder: "For small script-based repos with files scoring MI < 20, this pipeline produces reliable improvements in >80% of cases with acceptable risk." The data in Study 3 supports a stronger positive claim for the appropriate niche.
- **No cost-benefit analysis.** The thesis evaluates whether the pipeline *can* improve maintainability, but does not ask whether the improvement is *worth* the cost. Each repository costs API calls, processing time, and human review overhead. How many person-minutes does a +1.484 MI improvement save over the project lifetime? Without this framing, the practical contribution is incomplete.
- **Limited discussion of threats in collaborative settings.** The paper treats LLM-based refactoring as a solo activity, but in practice, architectural changes require team coordination. If the LLM introduces a decomposition that doesn't match the team's mental model, the sociotechnical cost may outweigh the MI gain. This perspective is entirely absent.
- **The ethical and bias discussion is missing.** LLMs encode specific code patterns from their training data. If the training data overrepresents certain architectural styles (e.g., layered MVC from web frameworks), the pipeline may systematically favor those styles over equally valid alternatives. This is a form of automation bias that the thesis does not address.

## Broader Implications
The paper's core tension — architecture-level intent with code-level execution — reflects a fundamental limitation of current LLMs that extends beyond software engineering. The finding parallels observations in automated planning, legal reasoning, and medical diagnosis: LLMs can identify the correct *strategy* but struggle with the *tactical execution* across multiple interdependent steps. The thesis would benefit from explicitly connecting to this broader pattern, which would strengthen its cross-disciplinary relevance.

## Suggested Improvement
**Priority 1**: Add a cost-benefit estimate section — approximately how many API calls, tokens, and person-minutes per repository, and at what scale does the investment break even?
**Priority 2**: Explicitly discuss automation bias and the risk of LLMs encoding training-data architectural preferences.
**Priority 3**: Add a paragraph connecting the LLM strategy-execution gap to analogous findings in other AI application domains.
