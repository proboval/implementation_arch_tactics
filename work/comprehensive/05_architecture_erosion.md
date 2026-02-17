# Architecture Erosion & Drift

**Learning objectives.** After reading this chapter you will be able to (1) define architecture erosion and architecture drift and explain the difference between them, (2) describe the causes, symptoms, and consequences of erosion using Li et al.'s taxonomy, (3) explain why detection alone does not solve erosion using empirical evidence from the Rosik et al. case study, (4) summarize how practitioners discuss architectural tactics informally based on Bi et al.'s Stack Overflow mining study, and (5) articulate the detection-remediation disconnect that motivates automated architectural improvement.

---

## 5.1 What Is Architecture Erosion?

Every software system begins with an *intended architecture* --- a set of design decisions about how modules, layers, and components should interact. Over time, the *implemented architecture* (what is actually in the code) diverges from that intent. This divergence is the broad phenomenon of **architecture erosion**.

### 5.1.1 A Four-Perspective Definition

Li et al. [@li2021understanding] conducted the first systematic mapping study dedicated exclusively to architecture erosion (AEr), analyzing 73 primary studies published between 2006 and 2019. One of their most important contributions is a refined definition that unifies four complementary perspectives found across the literature:

| Perspective | Definition | Studies |
|-------------|-----------|---------|
| **Violation** | The implemented architecture violates rules or constraints of the intended architecture | 30 |
| **Structure** | Internal structural flaws accumulate (e.g., cyclic dependencies, god classes) | 9 |
| **Quality** | Observable quality attributes (maintainability, performance) degrade over time | 6 |
| **Evolution** | The architecture becomes resistant to change; modifications are increasingly costly | 3 |

The synthesized definition reads:

> "Architecture erosion happens when the implemented architecture violates the intended architecture with flawed internal structure or when architecture becomes resistant to change." [@li2021understanding]

This multi-perspective view is important because it means erosion is not just about breaking rules. A system can be "correct" with respect to its layer boundaries and still suffer erosion if its quality metrics are degrading or if every change requires touching dozens of files. Students should internalize this: **erosion is a spectrum, not a binary**.

### 5.1.2 Erosion vs. Drift

Although the terms are sometimes used interchangeably, they capture different failure modes:

- **Architecture Erosion** is the violation of the intended architecture. Explicit rules, constraints, or design decisions are broken. For example, a layered architecture specifies that controllers must not access the database directly --- if a developer adds a direct SQL call in a controller, that is erosion.

- **Architecture Drift** is the gradual, often imperceptible divergence where the implemented architecture no longer matches the design intent, even though no single rule may be obviously broken. The system "drifts" because small, individually reasonable decisions accumulate into an architecture that nobody designed.

Think of erosion as *breaking the rules* and drift as *losing the map*. Both lead to the same outcome --- an architecture that is harder to maintain, extend, and reason about --- but they require different detection strategies. Erosion can be caught by conformance checkers that compare code against explicit rules. Drift requires comparing the actual dependency structure against a high-level model of what the architecture *should* look like.

### 5.1.3 Causes of Erosion

Li et al. classify 13 categories of erosion causes into three groups [@li2021understanding]:

**Technical causes:**

| Cause | Frequency | Description |
|-------|-----------|-------------|
| Architecture violation | 24.7% | Direct violations of intended architecture constraints |
| Evolution issues | 23.3% | System grows in ways the original architecture did not anticipate |
| Technical debt | 17.8% | Shortcuts and workarounds that accumulate over time |

**Non-technical causes:**

| Cause | Frequency | Description |
|-------|-----------|-------------|
| Knowledge vaporization | 15.1% | Original design rationale is lost as team members leave or documentation becomes stale |
| Organizational factors | Moderate | Communication gaps between teams, silos, unclear ownership |
| Time pressure | Moderate | Deadlines force shortcuts that violate architecture constraints |

**Mixed causes:**

Technology evolution (new frameworks, language features, platform changes) and requirements churn create situations where both technical and organizational forces push the system away from its intended architecture.

**Knowledge vaporization** deserves special attention. It refers to the phenomenon where the *reasons* behind architectural decisions are lost. The code remains, but nobody remembers *why* a particular module boundary exists, *why* a certain dependency was forbidden, or *what* quality attribute a particular structure was protecting. When this knowledge evaporates, developers unknowingly make changes that violate the intent.

### 5.1.4 Consequences

The consequences of erosion are severe and empirically documented:

- **83.8% of consequence-mentioning studies report quality degradation** [@li2021understanding]. The most affected quality attributes are maintainability, evolvability, and extensibility.
- Erosion increases defect rates, reduces developer productivity, and makes the system brittle.
- Li et al. identify a **technical debt vicious cycle**: technical debt causes erosion, and erosion generates more technical debt. Once this cycle begins, it accelerates.

> "Technical debt is both a cause and consequence of AEr, forming a vicious cycle." [@li2021understanding]

### 5.1.5 The Tool Landscape

Li et al. catalog **35 tools** for erosion detection across the 73 studies. However, the landscape has significant limitations:

- **57.1% of tools** are based on Architecture Conformance Checking (ACC) --- they compare actual dependencies against allowed ones.
- **Over 50% support only one programming language**, and that language is overwhelmingly Java.
- There is a major **research-practice gap**: 82.2% of erosion studies come from academia, and developers report that they do not use dedicated erosion-detection tools in practice.

### 5.1.6 Example: Layer Violations in a Web Application

Consider a standard 3-layer backend architecture:

```
Intended architecture:

    +----------------+
    |  Controller    |  <- Handles HTTP requests
    +-------+--------+
            | (allowed)
            v
    +----------------+
    |   Service      |  <- Contains business logic
    +-------+--------+
            | (allowed)
            v
    +----------------+
    |  Repository    |  <- Handles database access
    +----------------+
```

The intended architecture enforces a strict rule: **each layer may only depend on the layer directly below it**. The Controller layer calls Service methods; the Service layer calls Repository methods. The Controller should never access the Repository directly.

Now consider what happens under time pressure. A developer needs to display a simple count on a dashboard. Writing a service method feels like overhead for a one-line query, so they write:

```python
# controller/dashboard.py  -- EROSION: direct repository access
from repository.user_repo import UserRepository

class DashboardController:
    def get_user_count(self, request):
        repo = UserRepository()
        count = repo.count_all()  # Bypasses service layer!
        return {"user_count": count}
```

This is a **layer violation** --- a textbook case of architecture erosion. The Controller now depends directly on the Repository, bypassing the Service layer. The correct implementation routes through a service:

```python
# controller/dashboard.py  -- CORRECT: goes through service layer
from service.user_service import UserService

class DashboardController:
    def get_user_count(self, request):
        service = UserService()
        count = service.get_user_count()
        return {"user_count": count}

# service/user_service.py
from repository.user_repo import UserRepository

class UserService:
    def get_user_count(self):
        repo = UserRepository()
        return repo.count_all()
```

One violation seems harmless. But when dozens of controllers bypass services, the service layer loses its purpose, business logic scatters across controllers, and the architecture erodes to the point where refactoring becomes prohibitively expensive.

---

## 5.2 Architecture Drift in Practice

### 5.2.1 The IBM Dublin Case Study

While Li et al. provide the theoretical taxonomy, Rosik et al. [@rosik2011assessing] provide the empirical ground truth. They conducted a **2-year longitudinal case study** at IBM Dublin Software Lab, studying the development of DAP 2.0 (Domino Application Portlet), a commercial system of approximately **28,500 lines of code** (16 packages, 95 classes).

What makes this study exceptional is its design:

- It is **longitudinal** (November 2005 -- October 2007), not a one-time snapshot.
- It is conducted **in vivo** --- on a real commercial project during active development, not on a student project or a post-hoc analysis of an open-source codebase.
- It uses **Reflexion Modelling**, a technique that compares the *planned* architecture (a high-level model drawn by the architect) against the *actual* architecture (dependencies extracted from the source code). Discrepancies appear as *divergent edges* --- connections that exist in the code but should not exist according to the plan.

### 5.2.2 Key Findings

Over 6 evaluation sessions spanning 2 years, the researchers found:

| Metric | Value |
|--------|-------|
| Total architectural inconsistencies | 9 divergent edges reflecting 15 violating source-code relationships |
| Violations found in first session | 5 (drift begins immediately, even during initial development) |
| Violations fixed by developers | **0 out of 9** |
| Convergent edges hiding violations | 5 of 8 analyzed convergent edges contained hidden divergent relationships |
| Worst hidden case | 1 convergent edge masked 41 out of 44 inconsistent relationships |

The most striking finding is that **none of the 9 identified violations were ever fixed**. The researchers detected them, presented them to the developers, and the developers chose --- deliberately --- not to fix them.

### 5.2.3 Why Violations Persist: Developer Voices

The think-aloud sessions and retrospective interviews captured revealing developer statements:

> "You've seen my surprise the last time, when we ran the tool against the existing code base." --- Developer, expressing genuine surprise at the violations [@rosik2011assessing]

Surprise indicates that the violations were **unintentional** --- the developers did not know they were breaking the architecture. Yet even after learning about the violations, they did not fix them. The reasons are illuminating:

> "Maybe trying to fix these 'minor' issues would've possibly caused larger issues to appear and so made them not worth exploring..." [@rosik2011assessing]

> "If performance can be gained by breaking an architectural design, then this can sometimes be acceptable... time pressure is probably the main factor in some of the decision making that goes on during such a development." [@rosik2011assessing]

These quotes reveal three distinct barriers to remediation:

1. **Risk aversion**: Fixing a violation might introduce bugs elsewhere (ripple effects).
2. **Cost-benefit calculus**: Minor violations are perceived as low-risk and not worth the effort.
3. **Time pressure**: Fixing architectural issues is never "in scope" when there are features to deliver.

### 5.2.4 The Batch Detection Problem

The study used **batch processing** --- evaluation sessions were conducted at roughly 4--5 month intervals. This schedule proved inadequate. By the time violations were detected, they had been present for months, other code had been built on top of them, and removing them would have required significant rework.

Rosik et al. conclude that **continuous, lightweight monitoring** is far more effective than periodic reviews. If violations are caught within hours or days, they can be fixed while the developer still has context and before dependent code accumulates. This finding aligns with modern CI/CD practices where static analysis runs on every commit.

### 5.2.5 False Negatives in Reflexion Modelling

A particularly troubling finding is that Reflexion Modelling itself can **conceal violations**. When a planned connection exists between two modules (a *convergent edge*), any additional unplanned connections between the same modules are hidden within the aggregate. Rosik et al. found that 5 out of 8 convergent edges contained hidden divergent relationships. In the worst case, a single convergent edge masked 41 out of 44 inconsistent relationships.

This means the 9 detected violations are likely an **undercount**. The real number of architectural inconsistencies was almost certainly higher, but the detection technique itself obscured them.

---

## 5.3 Practitioner Knowledge About Tactics

### 5.3.1 Mining Stack Overflow

If erosion is pervasive and detection tools are underused, how do practitioners actually learn about and discuss architectural tactics? Bi et al. [@bi2021mining] investigated this question by mining Stack Overflow, the largest Q&A platform for developers.

Their approach was semi-automatic:

1. **Dictionary training**: Used Word2vec on 2,301 Stack Overflow posts tagged with "software architecture" or "software design" to build a semantic dictionary of architecture tactic terms and their synonyms.
2. **Classification**: Trained six machine learning classifiers on 1,165 manually labeled posts. The best performer was **SVM with the trained dictionary**, achieving an F-measure of **0.865**.
3. **Mining**: Applied the classifier to the full Stack Overflow corpus (2012--2019), extracting 5,103 candidate posts, of which **4,195 were manually verified** as genuine QA-tactic discussions (82.2% precision).
4. **Analysis**: Mapped the mined posts to 21 architecture tactics and 8 quality attributes (following ISO 25010).

### 5.3.2 What Practitioners Discuss

The most-discussed quality attributes and tactics on Stack Overflow reveal clear practitioner priorities:

| Quality Attribute | Instances | Share |
|-------------------|-----------|-------|
| Performance | 1,725 | 41.1% |
| Security | 987 | 23.5% |
| Reliability | 612 | 14.6% |
| Maintainability | 398 | 9.5% |
| Other (Compatibility, Usability, Portability, Functional Suitability) | 473 | 11.3% |

| Most-Discussed Tactics | Instances |
|------------------------|-----------|
| Time out | 470 |
| Authentication | 389 |
| Resource pooling | 356 |
| Heartbeat | 298 |
| Checkpoint/Rollback | 245 |

**Performance and Security tactics dominate** Stack Overflow discussions. Maintainability tactics receive less attention, which is consistent with the general observation that maintainability is often a *non-functional* concern that developers defer in favor of immediate functional and performance requirements.

### 5.3.3 Tactics and Maintainability

For the purposes of this thesis, the most relevant finding is which tactics practitioners associate with maintainability improvements:

| Tactic | Effect on Maintainability |
|--------|--------------------------|
| Heartbeat | Positive |
| Time stamp | Positive |
| Sanity checking | Positive |
| Functional redundancy | Positive |
| Analytical redundancy | Positive |
| Recovery from attacks | Positive |
| Authentication | Positive |
| Resource pooling | **Negative** (can hinder maintainability) |

This finding is nuanced. Tactics designed primarily for reliability or security (like Heartbeat, Sanity checking) can have **positive side-effects on maintainability** because they promote modular, well-separated components. Conversely, Resource pooling --- while excellent for performance --- can increase coupling and make the system harder to maintain.

### 5.3.4 Little-Known Relationships

Perhaps the most surprising finding is that **approximately 21% of the QA-tactic relationships discovered on Stack Overflow are "little-known"** --- they are not documented in the academic literature or standard textbooks like Bass et al. [@bass2021software]. These relationships emerge from real-world experience: practitioners discover through building systems that certain tactics affect quality attributes in ways that formal catalogs do not predict.

> "About 21% of the extracted QA-AT relationships are additional to the ones documented in the literature, which we call 'little-known' design relationships." [@bi2021mining]

### 5.3.5 Discussion Context

The study also analyzed *how* practitioners discuss tactics. Four main discussion topics emerged:

| Topic | Share | Description |
|-------|-------|-------------|
| Architecture patterns | 47% | How to implement a tactic within a given architectural pattern |
| Design context | 28% | When and where to apply a tactic based on project constraints |
| Design decision evaluation | 15% | Trade-offs and comparisons between alternative tactics |
| AT application in existing systems | 11% | How to introduce a tactic into an existing codebase |

The dominance of "architecture patterns" (47%) suggests that practitioners think about tactics primarily in terms of their interaction with patterns --- reinforcing the pattern-tactic relationship discussed in earlier chapters. The relatively small share of "AT application in existing systems" (11%) is notable: it confirms that **introducing tactics into existing code is rare in practice**, even though it is exactly what is needed to combat erosion.

---

## 5.4 The Detection-Remediation Disconnect

### 5.4.1 Synthesizing the Evidence

The three studies reviewed in this chapter converge on a single, critical insight: **detecting architectural problems is not the same as fixing them**. Let us trace the argument:

1. **Li et al. (2021)** establish that erosion is pervasive, well-documented, and severe. They catalog 35 detection tools and identify 13 categories of causes. Yet they also report an 82.2% research-practice gap --- developers do not use these tools. The study explicitly suggests that "leveraging machine learning to automatically detect AEr symptoms" is a promising direction, but stops short of proposing automated *remediation*.

2. **Rosik et al. (2011)** prove empirically that detection alone fails. They detected 9 violations, presented them to the developers, and **zero were fixed**. The barriers are not ignorance but rather risk, cost, and time. Developers *knew* about the problems and still chose to live with them.

3. **Bi et al. (2021)** show that knowledge about tactics exists in the developer community --- 4,195 Stack Overflow posts discuss how tactics relate to quality attributes. But this knowledge is **fragmented, informal, and biased** toward Performance and Security. Maintainability tactics are under-discussed, and only 11% of discussions address applying tactics to existing systems.

### 5.4.2 The Gap

The synthesis reveals a **three-part gap**:

| Gap | Evidence |
|-----|----------|
| **Detection exists but is underused** | 35 tools cataloged, but 82.2% of research is academic; developers do not adopt them [@li2021understanding] |
| **Detection does not lead to action** | 0/9 violations fixed even after explicit identification [@rosik2011assessing] |
| **Knowledge exists but is fragmented** | 4,195 SO posts on tactics, but 21% of relationships are undocumented; maintainability is under-discussed [@bi2021mining] |

What is missing is the **middle step** --- a mechanism that takes detected problems and implements solutions. Currently, the workflow is:

```
Detection  ->  [Manual analysis]  ->  [Manual design]  ->  [Manual implementation]
   OK              Expensive            Requires             Time-consuming
                                        expertise             and risky
```

Each manual step is a barrier. Each barrier gives developers a reason to defer the fix. The result is the vicious cycle that Li et al. describe: erosion generates technical debt, which generates more erosion, which further degrades the architecture.

### 5.4.3 Automated Remediation as the Missing Link

This is where the thesis contribution enters. The central research question is not "can we detect erosion?" (we can) or "do tactics exist to address it?" (they do) but rather: **can an LLM bridge the gap between detection and implementation?**

The envisioned workflow replaces manual steps with LLM-driven automation:

```
Detection  ->  [LLM: select tactic]  ->  [LLM: generate implementation]  ->  Validation
   OK              Automated                   Automated                     Static
                                                                             analysis
```

If an LLM can reliably (a) analyze a detected violation, (b) select an appropriate architectural tactic from a catalog, and (c) implement that tactic in the existing codebase while preserving behavior, then the three barriers identified by Rosik et al. --- risk, cost, and time --- are substantially reduced:

- **Risk** is reduced because the LLM's changes can be validated by static analysis and testing before deployment.
- **Cost** is reduced because no human architect needs to design the solution.
- **Time** is reduced because implementation is automated --- it can run in a CI/CD pipeline on every commit, addressing Rosik et al.'s recommendation for continuous monitoring.

The remaining chapters of this guide explore whether this vision is achievable. Chapter 6 examines how we measure whether the LLM's changes actually improve maintainability. Chapters 7 and 8 examine the LLM capabilities and limitations that determine the feasibility of automated tactic implementation.

---

## Review Questions

1. **Define** architecture erosion and architecture drift. Give one example of each in the context of a layered web application.

2. Li et al. identify four perspectives on architecture erosion. **List** all four and **explain** why the "quality degradation" perspective is particularly relevant for long-lived systems.

3. The IBM Dublin case study found that 0 out of 9 detected violations were fixed. **Identify** three barriers to remediation from the developer interviews and **explain** how each one could be addressed by an automated approach.

4. Bi et al. found that 21% of QA-tactic relationships on Stack Overflow are "little-known." **Discuss** what this implies about the completeness of formal tactic catalogs and its consequences for automated tactic selection.

5. **Draw** the detection-remediation disconnect as a diagram. Label each gap and identify which gap an LLM-based approach would address.

6. Rosik et al. recommend continuous monitoring over batch detection. **Explain** why, using the concept of *accumulated dependencies* on top of violations.

7. Li et al. report that 57.1% of erosion detection tools are Java-focused. **Discuss** the implications of this language bias for projects written in Python, JavaScript, or Go.
