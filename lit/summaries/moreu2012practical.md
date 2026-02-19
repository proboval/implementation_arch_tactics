## A Practical Method for the Maintainability Assessment in Industrial Devices Using Indicators and Specific Attributes

| Field | Value |
|-------|-------|
| **Key** | `moreu2012practical` |
| **Authors** | Moreu De Leon et al. |
| **Venue** | Reliability Engineering and System Safety (2012) |
| **Level** | L1-Foundational |

### Motivation & Gap
Industrial maintainability assessment lacks a practical, standardized procedure that can be applied at any stage of an asset's lifecycle. Existing approaches are either purely statistical (MTTR-based) or expert-based without structured indicator frameworks.

### Contribution
Proposes a structured expert-based method for computing six maintainability indicators (one general and five per maintenance level) from 17 weighted attributes grouped into design, staff/work conditions, and logistics support categories. Demonstrated on a bridge crane case study. Note: this paper addresses hardware/industrial device maintainability, not software maintainability.

**Relevance:** LOW

### Models & Tools
- **LLM/AI models:** N/A
- **Tools:** N/A (manual expert-based assessment with weighted formulas)
- **Dataset:** Bridge crane case study (single industrial device)

### Challenges
The method is subjective (expert-assigned 0--4 scores), requires trained evaluators for comparability, and was validated on only one industrial device. The equal-weight assumption in the case study does not reflect domain-specific attribute importance.

### Key Quotes
> "Maintainability may be quantified using appropriate measures or indicators and is then referred to as maintainability performance." (p. 84, citing EN 13306:2010)

### Key Takeaway
While this paper addresses hardware rather than software maintainability, the concept of decomposing maintainability into weighted sub-attributes assessed at multiple levels parallels the thesis's approach of decomposing ISO 25010 maintainability into sub-characteristics (modularity, analysability, modifiability, testability) and measuring them via static analysis metrics.
