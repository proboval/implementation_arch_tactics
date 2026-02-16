## Architectural Tactics in Software Architecture: A Systematic Mapping Study

| Field | Value |
|-------|-------|
| **Key** | `marquez2022architectural` |
| **Authors** | Marquez G., Astudillo H., Kazman R. |
| **Venue** | Journal of Systems and Software (2022) |
| **Tier** | Q1 (JSS, Elsevier) |
| **Citations** | ~50+ (co-authored by Rick Kazman, SEI) |
| **Level** | L1-Foundational |

### Motivation & Gaps
- **Problem:** Since their introduction in 2003, architectural tactics have been extended and adapted for additional quality attributes and newer system types, making it hard for researchers and practitioners to master this growing body of specialized knowledge. The evolution of tactics has led to increasingly unknown information about how they are identified, described, and what data sources are used to recognize them.
- **Motivation:** There was no comprehensive systematic review organizing the entire body of architectural tactics research across all quality attributes, identification techniques, description mechanisms, and data sources. This lack of systematic synthesis limits the replication and advancement of tactics research.
- **Gap:** No prior systematic mapping study had surveyed the full landscape of architectural tactics literature to determine which quality attributes have been addressed, how tactics are identified and described, what data sources are used, and which taxonomies have been proposed or updated. The study reveals that most proposed tactics do not conform to the original SEI definition, and there is little industrial evidence about their use.

### Contribution
This paper presents the most comprehensive systematic mapping study (SMS) of architectural tactics research to date. Reviewing 552 candidate studies and selecting 91 primary studies (79 via database search + 12 via snowballing), it maps the entire body of knowledge on architectural tactics across five dimensions: quality attributes addressed, techniques for identifying tactics, data sources for recognizing tactics, mechanisms for describing tactics, and proposed/updated tactic taxonomies. It is co-authored by Rick Kazman, one of the original architects of the tactics concept at the SEI, lending it significant authority.

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 5  |   3   |  1  |   2    | 16/25 |

**Relevance:** HIGH

This paper provides the definitive landscape of architectural tactics research, which is essential for the thesis to position its contribution (automated tactic implementation via LLM). It catalogues all quality attributes addressed by tactics (12 total), documents how tactics are identified and described, and critically identifies key gaps -- particularly the lack of automated implementation approaches and limited industrial evidence -- that the thesis directly aims to fill. The finding that modifiability (the closest QA to maintainability) has received only 1 dedicated study highlights a clear research gap the thesis addresses.

### Method & Validation
- **Type:** Systematic Mapping Study (SMS)
- **Validation:** Rigorous multi-stage selection protocol / Snowballing / Multi-author review
- **Evidence:** 552 candidate studies screened across 7 digital libraries (IEEE Xplore, SpringerLink, Scopus, ACM, Web of Science, ScienceDirect, Wiley), yielding 91 primary studies (2003--2021). Data extraction template with 13 items. Thematic analysis for classification. Three validity threat categories addressed (conclusion, internal, external, construct).

### Models & Tools
- **LLM/AI models:** N/A (this is a systematic mapping study, not an empirical tool evaluation); the study catalogues ML techniques found in primary studies: SVM, decision trees, Bayesian logistic regression, AdaBoost, SLIPPER, Bagging, BERT-based multi-class classification, LDA topic modeling
- **Tools/frameworks:** Mendeley (reference management); Parsif.al (systematic review management); 7 digital libraries (IEEE Xplore, SpringerLink, Scopus, ACM Digital Library, Web of Science, ScienceDirect, Wiley); thematic analysis following Braun et al.; Wieringa et al. classification scheme for research types
- **Languages:** N/A (literature review covering studies in multiple programming languages)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Total primary studies analyzed | 91 (79 from database search + 12 from snowballing) |
| Initial candidate pool | 552 studies from 7 databases |
| Publication period covered | 2003--2021 (16 years) |
| Most-studied QA | Security (18 studies), followed by fault tolerance (5), availability (4), performance (4), safety (4) |
| Modifiability studies | Only 1 study (S69) focused specifically on modifiability tactics |
| Studies lacking tactic identification method | 71% (65 of 91) do not describe how tactics were identified |
| Studies lacking data source description | 69% (63 of 91) do not describe data sources used |
| Studies lacking tactic description mechanism | 59% (54 of 91) do not describe how tactics are characterized |
| Research type distribution | 47.3% solution proposals, 39.6% evaluation research, remainder philosophical/experience |
| Contribution type distribution | 48.4% frameworks, 16.5% models, 15.4% guidelines, 7.7% lessons learned, 6.6% theories |
| Validation methods | 46.2% case studies, 25.3% unspecified, 16.5% experiments, 11% illustrative examples |
| Tactic identification techniques | Manual mapping (10), code analysis (10), text analysis (4), multifacetic (3), not described (65) |
| Data sources for recognizing tactics | Source code (12), documentation (7), web repositories (3), design decisions (3), patterns (1), experts (1), standards (1) |
| Tactic description mechanisms | Models (15), specific templates (12), narrative description (9), formal language (1) |
| Taxonomies identified | 10 new/updated taxonomies (security, safety, fault-tolerance, scalability, deployability, modifiability) |
| ML techniques for tactic detection | SVM, decision trees, Bayesian logistic regression, AdaBoost, SLIPPER, Bagging |
| NLP techniques for tactic detection | BERT-based multi-class classification, LDA topic modeling |
| Industrial evidence | Only 13 studies used industrial systems for validation |
| Quality attributes in original SEI taxonomy | 7 (security, availability, performance, modifiability, interoperability, usability, testability) |
| Quality attributes found in SMS | 12 (adds adaptability, dependability, reliability, deployability, scalability, fault tolerance, safety) |

### Key Quotes
> "Little rigor has been used to characterize and define architectural tactics; most architectural tactics proposed in the literature do not conform to the original definition; and there is little industrial evidence about the use of architectural tactics." (Abstract)

> "The painstaking review, analysis and summarization of tactics proposals led us to the unexpected, but also unavoidable, conclusion that most tactics proposed in the literature do not conform to the description of the original definition, which posited them as design decisions to preserve quality attributes in presence of stimuli." (Section 8, Conclusions)

> "Tactics have become relevant to map architecture decisions onto source code, and automation opportunities beckon within reach." (Section 8, Research opportunity #2)

> "70% of studies do not explicitly describe their method to identifying tactics." (Section 8, Conclusions)

> "There is little industrial evidence regarding the use of tactics." (Section 5.3)

> "Machine Learning techniques such as Decision Tree, Support Vector Machine, and AdaBoost emerge as an alternative to identify and classify tactics in source code." (Key findings of RQ2)

> "An architectural tactic is a design decision that influences the control of a quality attribute response. Each architectural tactic is a design option for the architect." (Section 2, quoting Bass et al.)

### Challenges & Limitations
1. **Lack of rigorous tactic characterization:** Most studies do not follow a systematic process for defining or characterizing tactics. There is no widely agreed-upon method for defining a tactic, and most proposed tactics deviate from the original SEI definition.
2. **Limited industrial evidence:** Only 13 of 91 studies used industrial systems for validation, indicating that tactics remain primarily an academic concept with insufficient industrial uptake.
3. **Incomplete reporting:** 71% of studies do not describe how tactics were identified, 69% do not describe data sources, and 59% do not describe their characterization mechanism.
4. **Quality attribute coverage imbalance:** Security dominates (18 studies), while maintainability-related attributes like modifiability (1 study) and testability (0 dedicated studies) are severely underrepresented.
5. **Code-centric bias:** Studies using source code analysis address only one dimension of tactics. Tactics also involve decision-making and architectural reasoning that cannot be recovered from code alone.
6. **Threats to validity:** Single-author initial screening (mitigated by two-author review), search string limitations, potential bias from venue selection. Review period ended August 2021, so post-2021 work is not captured.

### Dataset / Benchmark
- **Name:** Systematic Mapping Study corpus (architectural tactics literature 2003--2021)
- **Size:** 91 primary studies (79 from database search + 12 from snowballing) selected from 552 candidate studies across 7 digital libraries; search string: ("software" OR "architecture") AND "architectural" AND "tactic*"; data extraction template with 13 items
- **Domain:** Software architecture research -- covers 12 quality attributes (security, availability, performance, modifiability, interoperability, usability, testability, adaptability, dependability, reliability, deployability, scalability, fault tolerance, safety)
- **Availability:** Open Science repository containing search protocol, tables/figures, and metadata from primary studies (referenced as [11] in the paper)

### Key Takeaway
The thesis fills two major gaps identified by this SMS: (1) the near-absence of maintainability/modifiability-focused tactics research (only 1 of 91 studies), and (2) the identified research opportunity that "automation opportunities beckon within reach" for mapping architecture decisions to source code. The thesis's use of LLMs to automate tactic implementation directly addresses the finding that existing tactic identification techniques (ML classifiers, NLP, manual mapping) only detect tactics but do not implement them. Furthermore, the paper's catalogue of 12 quality attributes and 10 tactic taxonomies provides a structured vocabulary the thesis can reference when selecting which tactics to implement for maintainability improvement.

### Snowball References
**Backward:**
- `bass2021software` -- Bass L., Clements P., Kazman R. "Software Architecture in Practice" (4th ed., 2021) -- the foundational reference for all tactic taxonomies
- `harrison2010how` (S4/S11) -- Harrison N.B., Avgeriou P. -- fault-tolerance tactics in patterns, pattern-tactic interaction
- `kim2009qualitydriven` (S5/S6) -- Kim S. et al. -- quality-driven architecture using tactics with feature models
- `mirakhorli2016detecting` (S58) -- Mirakhorli M., Cleland-Huang J. -- ML techniques for tactic detection in source code
- `ryoo2009systematic` (S10) -- Ryoo J., Laplante P., Kazman R. -- identifying tactics from security patterns
- `koziolek2013peropteryx` (S15) -- Koziolek A. et al. -- PerOpteryx, automated architecture improvement using tactics
- `bi2021mining` (S87) -- Bi T. et al. -- mining architecture tactics from Stack Overflow

**Forward:** Check Google Scholar for papers citing this (post-2022 works on tactic automation, LLM-based architecture, maintainability tactics)
