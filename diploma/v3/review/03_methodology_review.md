# Methodology Review — Dr. Aybüke Aurum

## Research Design
The thesis follows a within-subjects repeated-measures design where each repository serves as its own control. This is appropriate for the research question and reduces between-repository variance. The three-study progression is a logical structure for an exploratory investigation. However, the overall design would be stronger with clearer pre-registration of hypotheses and analysis plans.

## Strengths
- **Appropriate statistical tests.** The use of Wilcoxon signed-rank (non-parametric, paired) is correctly justified by the Shapiro-Wilk test showing non-normality ($W=0.34, p<0.001$). Reporting the matched-pairs rank-biserial correlation $r=0.28$ as the effect size distinguishes statistical from practical significance — many papers stop at the $p$-value.
- **Failure accounting.** The 25.3% failure rate is reported and retained in the denominator rather than discarded. This is methodologically honest and relatively rare in LLM-based automation studies, where failures are often silently excluded.
- **Multi-metric triangulation.** Using MI, fan-out, package count, and docstring coverage together reduces the risk of mono-operation bias. The explicit acknowledgment that MI is debated and that tools disagree is a mark of methodological maturity.
- **Controlled evidence comparison in Study 2.** The four prompt configurations (P1–P4) with incremental evidence addition is a clean factorial design for isolating the contribution of each evidence type. The finding that code signatures *degrade* performance is a non-obvious result that justifies the controlled design.

## Weaknesses
- **Single annotator threat is underexplored.** The ground-truth labels for Study 2 (and by extension Study 3) were assigned by one annotator. For the modular monolith / layered boundary — which the paper itself identifies as the hardest distinction — inter-annotator reliability is critical. Without at least a second annotator on a subset and a reported Cohen's $\kappa$ or similar, the ground truth is a potential confound that undermines all derived claims.
- **No correction for multiple comparisons.** Study 1 tests one hypothesis (MI change), which is fine. But Study 2 tests 20 model-prompt combinations without any adjustment (Bonferroni, Holm, or FDR). With 20 comparisons, the probability of at least one false positive at $\alpha=0.05$ is approximately $1 - (0.95)^{20} = 64\%$. This does not invalidate the strong consistent patterns (all 5 models improve with import graphs), but the individual model-vs-model accuracy comparisons should not be overinterpreted.
- **The single-LLM implementation limitation.** All three studies use Qwen3-coder-next for implementation, but only Study 2 compares models (for detection). The claim "LLMs can support maintainability improvement" is conflated with "this specific LLM in this specific configuration can..." The paper acknowledges this in §6.3 (Limitations), but it should be more prominent in the abstract and conclusions to prevent overgeneralization.
- **No behavioral preservation verification.** The paper acknowledges this (§4.7, §5.7) but it remains a fundamental methodological weakness. Without test suite execution, MI improvements may reflect code that is structurally "simpler" but semantically broken. The distinction is critical for any claim about practical applicability.
- **Confidence calibration analysis lacks a decision-theoretic framing.** Study 2 shows LLM confidence does not distinguish correct/incorrect predictions, which is useful. But the analysis could go further: what is the optimal confidence threshold for precision-recall tradeoff? What is the expected cost of a false positive detection vs. a false negative? Without this, the finding is descriptive rather than actionable.

## Specific Methodological Issues

| Location | Issue | Severity |
|----------|-------|----------|
| §3.3 | Dataset inclusion requires `requirements.txt`. This excludes many modern Python projects using `poetry`, `pipenv`, `pyproject.toml` alone. Is the dataset biased toward older or less modern projects? | MAJOR |
| §3.9, Eq. 3.2 | $H_0: MI_{after} - MI_{before} = 0$ — this is a point null. An equivalence test (e.g., TOST) or a minimum clinically important difference would be more informative, since a statistically significant but trivially small effect is likely with $N=121$. | MINOR |
| §5.3.2 | Study 3 descriptive statistics are presented without confidence intervals. The mean $\overline{\Delta MI} = +1.484$ is reported, but a 95% CI would help assess precision. | MINOR |
| §5.3 | Repository failures in Study 3 include "Ollama API rate limiting (HTTP 429)". This is an infrastructure failure, not a pipeline failure — it should be separated from algorithmic failures in the failure analysis. | MINOR |

## Suggested Improvement
**Priority 1**: Obtain a second annotator for at least the 33 modular monolith repositories and report inter-annotator agreement.
**Priority 2**: Report confidence intervals for all key effect sizes ($\Delta MI$ per study, per tactic, per architecture).
**Priority 3**: Add a sensitivity analysis excluding the top-3 outlier improvements to show how much of the significant result is driven by extreme values.
