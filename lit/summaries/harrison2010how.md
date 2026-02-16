## How Do Architecture Patterns and Tactics Interact? A Model and Annotation

| Field | Value |
|-------|-------|
| **Key** | `harrison2010how` |
| **Authors** | Neil B. Harrison, Paris Avgeriou |
| **Venue** | The Journal of Systems and Software, vol. 83, pp. 1735-1758 (2010) |
| **Tier** | Q1 (JSS, Elsevier) |
| **Citations** | ~200+ (highly cited in SA/tactics literature) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Architects and developers do not understand how architectural tactics structurally and behaviorally impact architecture patterns when implemented, leading to uninformed design choices and compromised quality attribute satisfaction.
- **Motivation:** Current pattern documentation does not mention tactics at all, and existing descriptions of pattern-quality attribute relationships are too high-level to identify specific parts of a pattern impacted by tactics or what that impact consists of. Without this detailed knowledge, architects can easily miss important interactions and cause unintended architecture drift.
- **Gap:** No prior work provided a systematic model categorizing the types (structural and behavioral) and magnitudes of changes that tactics impose on pattern participants, nor a lightweight annotation method for documenting these interactions on architecture diagrams.

### Contribution

This paper develops a formal model for how architecture patterns and architectural tactics interact, categorizing the types of structural and behavioral changes that tactics impose on pattern participants (components and connectors). The model defines a five-point impact magnitude scale (Good Fit ++ to Poor Fit --) and proposes a lightweight annotation method for architecture diagrams that visually documents where and how tactics are implemented within patterns. The work is validated through three industrial case studies involving architecture reviews of real systems.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 5  |   3   |  1  |   0    | 14/25 |

**Relevance:** HIGH

This paper is directly foundational for the thesis because it provides the most detailed taxonomy of how architectural tactics structurally and behaviorally modify architecture patterns. Understanding these interaction types (Implemented-in, Replicates, Add-in-pattern, Add-out-of-pattern, Modify) is essential for designing an LLM-based pipeline that implements tactics correctly: the LLM must know what kind of structural change a tactic requires within a given pattern. The impact magnitude scale can serve as a basis for predicting implementation difficulty and estimating how much an LLM-generated transformation will alter existing architecture.

### Method & Validation
- **Type:** Framework / Model + Case Study
- **Validation:** 3 industrial case studies with architecture reviews; informal interviews with participants; annotated real architecture diagrams from Google, ambulance system, speech recognition system, manufacturing system, time-tracking system, and subscription management system
- **Evidence:** Qualitative participant observations from architecture reviews confirmed the annotation's utility for identifying tactic impact locations, showing tactic interactions, and guiding implementation decisions. The model is grounded in systematic analysis of reliability tactics across multiple patterns (Pipes and Filters, Layers, Broker, Blackboard, MVC, Client-Server, Repository).

### Models & Tools
- **LLM/AI models:** N/A
- **Tools/frameworks:** No specific software tools; the annotation method is manual and notation-agnostic, applicable to UML component diagrams, box-and-line diagrams, and other standard architecture notations
- **Languages:** N/A (architecture-level model, not tied to a programming language)

### Key Findings

| Finding | Value/Detail |
|---------|-------------|
| Five types of structural changes to pattern components | Implemented-in, Replicates, Add-in-pattern, Add-out-of-pattern, Modify (ordered by increasing impact) |
| Corresponding connector changes | Range from no change (Implemented-in) to new connectors outside pattern structure (Add-out-of-pattern) |
| Five-point impact magnitude scale | Good Fit (++), Minor Changes (+), Neutral (~), Significant Changes (-), Poor Fit (--) |
| Key impact threshold | 3 or fewer participant changes = lower impact; more than 3 = higher impact |
| Behavior interaction types | Adding action sequences within/outside existing sequences; four types of timing impact (adding new timing explicit/implicit, changing existing timing explicit/implicit) |
| Pattern-tactic compatibility varies widely | e.g., Pipes-and-Filters: Voting/Active Redundancy = Good Fit (++), but Ping/Echo = Poor Fit (--) |
| Tactics can enable other tactics | Authorization infrastructure can be reused for Ping/Echo (shared central controller), reducing subsequent tactic implementation effort |
| Tactic implementation order matters | A previously implemented tactic can change the impact category of a subsequent tactic (e.g., from Add-out-of-pattern to Implemented-in) |
| Adding components outside patterns causes architecture drift | Case Study 3 shows snowball effect: layer-bypass for performance required duplicate authorization components, impacting maintainability |
| Brownfield vs. greenfield distinction | In legacy systems, tactics must fit existing patterns regardless of difficulty; in new systems, pattern-tactic compatibility can inform pattern selection |

### Key Quotes

> "Tactics that are implemented in existing architectures can have significant impact on the architecture patterns in the system." (p. 1735)

> "Because tactics must be realized within architecture patterns, the relationship between the two needs special study." (p. 1736)

> "Bass et al. explain that tactics are 'architectural building blocks' from which architecture patterns are created; that patterns package tactics." (p. 1738)

> "The structure and behavior of a tactic ranges from highly compatible with the structure and behavior of a pattern to almost completely incompatible with them." (p. 1739-1740)

> "Implementing tactics is actually a form of 'architecture drift'." (p. 1746)

> "This architecture illustrates the case where the addition of components outside the architecture patterns has a snowball effect -- adding the layer bypass component caused an extra authorization component to be added, with duplicated code." (p. 1755)

> "The close relationship between maintainability and extensibility makes this architecture a cause for concern." (p. 1755)

### Challenges & Limitations

1. **Runtime tactics only:** The paper focuses exclusively on runtime tactics and explicitly excludes design-time tactics (e.g., "hide information" for modifiability), which are also important for maintainability.
2. **Qualitative magnitude scale:** The five-point impact scale is subjective and based on expert judgment rather than quantitative measurement; the authors acknowledge each pattern-tactic pair must be individually examined.
3. **Limited pattern-tactic coverage:** Detailed interaction data is provided only for reliability tactics on Pipes-and-Filters and Layers; other quality attributes and patterns remain unanalyzed.
4. **Scalability of annotation:** The annotation method was tested with up to 6 tactics and 3 patterns; it may become unwieldy for large, complex systems with many tactics.
5. **No formal validation metrics:** Validation relies on informal interviews and participant observations from architecture reviews rather than controlled experiments.
6. **No automation support:** The model and annotation are entirely manual; no tool support is provided for automatically detecting or applying pattern-tactic interactions.

### Dataset / Benchmark
- **Name:** No formal named dataset; 3 industrial case studies + prior architecture diagram corpus
- **Size:** 47 architecture diagrams (from prior work) + 3 industrial systems (manufacturing, time-tracking, subscription management) + real architecture diagrams from Google, ambulance system, and speech recognition system
- **Domain:** Manufacturing (Pipes-and-Filters), web-based time-tracking (Repository/Broker/Layers), magazine subscription management (MVC/Repository/Layers)
- **Availability:** Not publicly available (proprietary industrial systems)

### Key Takeaway

The taxonomy of structural changes (Implemented-in, Replicates, Add-in-pattern, Add-out-of-pattern, Modify) and the five-point impact magnitude scale provide a concrete framework for the thesis to classify what kind of code transformations the LLM must perform when implementing a given tactic in a given pattern. Tactics that are "Add-out-of-pattern" or "Modify" type changes are harder and more error-prone -- the LLM pipeline should prioritize tactics with Good Fit or Minor Changes ratings for the target architecture, and the impact scale can be used to evaluate whether LLM-generated changes preserve architectural integrity or cause drift.

### Snowball References

**Backward:**
- `bass2003sap` -- Bass, Clements, Kazman. *Software Architecture in Practice* (2003). Defines tactics taxonomy and ATAM.
- `bachmann2007modifiability` -- Bachmann, Bass, Nord. *Modifiability Tactics* (2007). SEI technical report on modifiability-specific tactics.
- `buschmann1996posa` -- Buschmann et al. *Pattern-Oriented Software Architecture* (1996). Foundational pattern catalog.
- `avgeriou2005patterns` -- Avgeriou, Zdun. *Architectural Patterns Revisited* (2005). Pattern language for architecture patterns.
- `harrison2008incorporating` -- Harrison, Avgeriou. *Incorporating Fault Tolerance Techniques in Software Architecture Patterns* (2008). Precursor work analyzing reliability tactics in Layers.
- `bachmann2005designing` -- Bachmann et al. *Designing Software Architectures to Achieve Quality Attribute Requirements* (2005). Quality attribute reasoning framework.
- `rosik2008industrial` -- Rosik et al. *An Industrial Case Study of Architecture Conformance* (2008). Architecture drift detection.

**Forward:** Check Google Scholar for papers citing this -- particularly works on automated tactic implementation, tactic detection in code, and architecture erosion/drift detection.
