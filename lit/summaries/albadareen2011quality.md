## Software Quality Models: A Comparative Study

| Field | Value |
|-------|-------|
| **Key** | `albadareen2011quality` |
| **Authors** | AL-Badareen et al. |
| **Venue** | ICSECS 2011, CCIS 179, Springer (2011) |
| **Level** | L1-Foundational |

### Motivation & Gap
Multiple software quality models (McCall, Boehm, FURPS, Dromey, ISO 9126) exist but prior comparisons between them are inconsistent -- the same factors are classified differently depending on the researcher's perspective, creating confusion when selecting a model for evaluation.

### Contribution
Proposes a mathematical (weight-based) comparison method for software quality models, applying it to five well-known models. Results show McCall scores highest in overall factor coverage (63.67%), while FURPS is the most limited (20.34%), and ISO 9126 provides the best standardized framework but lacks factors like correctness and reusability.

**Relevance:** LOW

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** N/A (manual weighted comparison)
- **Dataset:** N/A -- analytical comparison of 5 quality models

### Challenges
The comparison uses equal weighting across all factors (general comparison), which may not reflect the relative importance of factors in specific domains; expert weighting for domain-specific comparison is left to future work.

### Key Quotes
> "The inconsistency in the definitions of software quality factors results contradictions in the developed models." (p. 47)

### Key Takeaway
When justifying the use of ISO 25010 for maintainability evaluation in the thesis, this paper provides background showing that earlier models (McCall, Boehm, FURPS, Dromey) each have coverage gaps, supporting the choice of the ISO standard as the most balanced quality framework.
