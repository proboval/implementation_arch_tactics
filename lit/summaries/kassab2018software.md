## Software Architectural Patterns in Practice: An Empirical Study

| Field | Value |
|-------|-------|
| **Key** | `kassab2018software` |
| **Authors** | Kassab et al. |
| **Venue** | Innovations in Systems and Software Engineering (2018) |
| **Level** | L2-Intersection |

### Motivation & Gap
Little contemporary data documents the actual practices used by software professionals when selecting and incorporating architectural patterns in industry. The paper addresses this gap through a large-scale empirical survey.

### Contribution
A comprehensive survey of 809 software professionals from 39 countries revealing that functionality (not quality requirements) is the primary driver for pattern selection in practice, and that patterns are almost always modified via tactics during implementation.

**Relevance:** MEDIUM

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** QuestionPro web-based survey tool
- **Dataset:** 809 survey respondents (126 fully completed), 39 countries, May 2015 -- March 2016

### Challenges
Low completion rate (15.6%) limits statistical power; self-selection bias from LinkedIn professional groups may skew results toward experienced architects and developers.

### Key Quotes
> "The structure and behavior of tactics is more local and low level than the architectural pattern and therefore must fit into the larger structure and behavior of patterns applied to the same system" (p. 267, citing Kassab et al. 2012)

### Key Takeaway
Architectural patterns in practice are rarely applied as-is -- 63% of projects modify patterns with tactics, confirming that automated tactic implementation must account for existing pattern structures and their modification constraints.
