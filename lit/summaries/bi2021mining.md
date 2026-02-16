## Mining Architecture Tactics and Quality Attributes Knowledge in Stack Overflow

| Field | Value |
|-------|-------|
| **Key** | `bi2021mining` |
| **Authors** | Tingting Bi, Peng Liang, Antony Tang, Xin Xia |
| **Venue** | Journal of Systems and Software, 180, 111005 (2021) |
| **Level** | L2-Intersection |

### Motivation & Gaps
- **Problem:** Architecture Tactics (ATs) are architectural building blocks for addressing Quality Attributes (QAs), but the relationships between ATs and QAs have not been systematically explored from real developer discussions. Manually mining this QA-AT knowledge from developer forums is labor-intensive and difficult.
- **Gap:** While some research focused on mining AT knowledge from source code, little was known about the empirical relationships between ATs and their impacts on QAs as discussed by practitioners. Approximately 21% of QA-AT relationships found in Stack Overflow are "little-known" and not documented in existing literature.

### Contribution
The paper proposes a semi-automatic dictionary-based mining approach to extract architecture tactics (AT) and quality attributes (QA) knowledge from Stack Overflow posts. Using Word2vec for dictionary training and SVM for classification, the approach achieves an F-measure of 0.865 and a Performance (manual verification accuracy) of 82.2%, mining 4,195 verified QA-AT posts. The study then empirically analyzes the mined posts to reveal design relationships between 21 ATs and 8 QAs (ISO 25010), discovering that ~21% of the extracted QA-AT relationships are "little-known" (not documented in existing literature).

### Relevance

| AT | SA | Maint | LLM | Static | Total |
|:--:|:--:|:-----:|:---:|:------:|:-----:|
| 5  | 3  |   3   |  1  |   0    | 12/25 |

**Relevance:** HIGH

### Method & Validation
- **Type:** Tool + Empirical Study
- **Validation:** ML classifier evaluation (precision/recall/F-measure across 6 algorithms), manual verification of 4,195 mined posts by two annotators (Cohen's kappa = 0.81), comparison with literature-documented QA-AT relationships

### Models & Tools
- **LLM/AI models:** Word2vec (for dictionary training and term semantic similarity), SVM, Bayes, Decision Tree, Logistic Regression, Random Forest, Bagging (for classification)
- **Tools:** scikit-learn (Python 3.7) for classifier training, MAXQDA for qualitative data labelling, Weka for Information Gain Ratio calculation, Gephi for dictionary visualization
- **Languages:** N/A (mining from Stack Overflow text posts, language-independent)

### Key Findings
| Finding | Value/Detail |
|---------|-------------|
| Best classifier | SVM with trained dictionary achieves F-measure 0.865 |
| Dictionary improvement | Trained dictionary improves all 6 ML algorithms (4.2%--21.7% F-measure gain) |
| Mining performance | 82.2% of mined posts confirmed as true QA-AT posts (4,195 out of 5,103) |
| Most discussed QA | Performance (1,725 instances out of 4,195 posts) |
| Most discussed AT | Time out (470 instances) |
| Little-known relationships | ~21% of QA-AT relationships from SO are not documented in literature |
| ATs for Maintainability | Heartbeat, Time stamp, Sanity checking, Functional redundancy, Analytical redundancy, Recovery from attacks, Authentication positively impact Maintainability; Resource pooling can hinder Maintainability |
| AT catalog | 21 architecture tactics studied (Heartbeat, Audit trail, Resource pooling, Authentication, Checkpoint, Rollback, Spare, Redundancy replication, Voting, Shadow operation, Secure session, Time out, Time stamp, Sanity checking, Functional redundancy, Scheduling, FIFO, Analytical redundancy, Resisting attacks, Maintain data confidentiality, Recovering from attacks) |
| Design considerations | 4 discussion topics: Architecture patterns (47%), Design context (28%), Design decision evaluation (15%), AT application in existing systems (11%) |
| QA taxonomy used | ISO 25010: Performance, Maintainability, Compatibility, Usability, Reliability, Functional Suitability, Security, Portability |

### Dataset / Benchmark
Stack Overflow posts from 2012-01-01 to 2019-06-30. Training set: 1,165 manually labelled QA-AT posts (containing 1,203 QA-AT instances across 21 ATs) plus 1,200 non QA-AT posts. Dictionary training: 2,301 posts tagged with "software architecture" or "software design". Mining output: 5,103 mined posts, of which 4,195 were manually verified as true QA-AT posts (82.2% Performance). Complete replication package available online.

### Challenges & Limitations
- Data sourced only from Stack Overflow, limiting generalizability to other developer communities (GitHub, Twitter, Stack Exchange).
- Semi-automatic mining cannot retrieve all QA-AT posts; some ATs may be missing from the training dictionary.
- Manual labelling of QA-AT relationships is subject to researcher interpretation; mitigated through pilot studies and inter-rater agreement (Cohen's kappa = 0.81).
- The trained dictionary approach depends on seed words identified by domain experts, which may introduce bias toward well-known ATs.
- The degree of positive/negative impact of ATs on QAs is measured by incident count rather than a formal impact assessment.
- Knowledge from the mined posts reflects developer perceptions rather than controlled experimental evidence.

### Key Quotes
> "We proposed a semi-automatic approach, which can mine QA-AT posts in SO. Our approach can achieve an F-measure (0.865) by SVM with a trained dictionary to exploit term semantics for QA-AT posts mining." (Section 1, p. 3)

> "About 21% of the extracted QA-AT relationships are additional to the ones documented in the literature, which we call 'little-known' design relationships." (Section 4.2.1)

### Key Takeaway
This paper provides an empirically-grounded mapping of which architecture tactics positively or negatively affect which quality attributes (including Maintainability), based on real developer discussions rather than textbook prescriptions. The AT-to-QA relationship matrix (Table 6) and the catalog of 21 ATs with their synonym dictionaries (Table 1) can serve as the basis for the thesis's tactic selection logic -- particularly the finding that specific tactics like Time stamp, Sanity checking, and Analytical redundancy benefit Maintainability, while Resource pooling can hinder it.
