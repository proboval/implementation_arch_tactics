## Methodology for Maintainability-Based Risk Assessment

| Field | Value |
|-------|-------|
| **Key** | `abdelmoez2006methodology` |
| **Authors** | Abdelmoez et al. |
| **Venue** | IEEE RAMS (2006) |
| **Level** | L2-Intersection |

### Motivation & Gap
Software spends more than 65% of its lifecycle in maintenance, yet few methods quantify maintainability risk at the architectural level. Existing approaches (e.g., Maintainability Index) operate at code level, not at the architecture design level where early intervention is most cost-effective.

### Contribution
Proposes a methodology for estimating maintainability-based risk of system components using architectural artifacts (UML models). Risk is computed as the product of unconditional change probability (derived from change propagation probabilities between components) and maintenance impact (size of change). Demonstrated on a NASA CM1 case study.

**Relevance:** MEDIUM

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** Software Architectures Change Propagation Tool (SACPT), UML-RT models
- **Dataset:** NASA CM1 case study (Metrics Data Program)

### Challenges
The methodology requires detailed UML artifacts (sequence diagrams, structure diagrams) that may not be available for legacy systems; only one change scenario was evaluated in the case study, limiting generalizability.

### Key Quotes
> "A software product spends more than 65% of its lifecycle in maintenance. Software systems with good maintainability can be easily modified to fix faults or to adapt to changing environment." (p. 337)

### Key Takeaway
The change propagation probability model demonstrates that architectural coupling directly determines maintainability risk -- a highly coupled component (CCM) became the riskiest even without direct change, validating that the thesis's tactic-based decoupling approach should measurably reduce propagation-based maintainability risk.
