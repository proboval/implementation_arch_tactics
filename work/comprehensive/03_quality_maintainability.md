# Software Quality & Maintainability

Software quality is not a monolithic concept. Over five decades of software engineering research, the community has progressively refined how we define, decompose, and measure quality -- with maintainability emerging as one of the most economically significant and technically challenging attributes. This chapter traces that evolution, establishes ISO/IEC 25010 as the authoritative framework, and shows how maintainability can be operationalized through concrete metrics and guidelines.

## 3.1 Evolution of Quality Models

Understanding modern maintainability requires understanding the intellectual lineage that produced it. Four major quality models, spanning from 1977 to 2011, have shaped how we think about software quality attributes. Each generation addressed limitations of its predecessors while introducing new perspectives and decompositions.

### McCall's Quality Model (1977)

McCall's model was the first systematic attempt to define and measure software quality. Developed for the U.S. Air Force, it introduced 11 quality factors organized into three perspectives based on how the software is used [@alqutaish2010quality]:

- **Product Operation** (daily use): correctness, reliability, efficiency, integrity, usability
- **Product Revision** (change and improvement): maintainability, flexibility, testability
- **Product Transition** (adaptation to new environments): portability, reusability, interoperability

McCall's key innovation was a hierarchical structure: **factors** (user-oriented) decompose into **criteria** (developer-oriented), which decompose into **metrics** (measurable indicators). For example, the factor *maintainability* decomposed into criteria like consistency, simplicity, conciseness, self-descriptiveness, and modularity.

However, McCall's metrics were "neither clearly nor completely defined" [@alqutaish2010quality], making practical measurement difficult. The model also treated quality factors as relatively independent, failing to capture the tradeoffs that architects face in practice (e.g., improving efficiency often reduces maintainability).

### Boehm's Quality Model (1978)

Boehm proposed a hierarchical model that began with a top-level question: "Does the software do what the user wants it to do?" This led to a tree structure rooted in **general utility**, which branched into three primary concerns:

- **As-is utility** -- the software works correctly and efficiently now
- **Maintainability** -- the software can be understood, modified, and tested
- **Portability** -- the software can be moved to new environments

Boehm's model contributed two important ideas. First, it placed maintainability as a first-class top-level concern rather than burying it among many peer factors. Second, it introduced the notion that quality attributes have a natural hierarchy where some attributes serve others. Maintainability in Boehm's model decomposed into understandability, modifiability, and testability -- a decomposition remarkably close to what ISO 25010 would formalize three decades later.

The limitation of Boehm's model was its focus on high-level characteristics without providing operational metrics or thresholds. It told architects *what* to care about but not *how* to measure it [@albadareen2011quality].

### ISO 9126 (2001)

ISO 9126 represented the first international consensus on software quality. Developed by the International Organization for Standardization, it defined six quality characteristics, each with sub-characteristics:

1. **Functionality** -- suitability, accuracy, interoperability, security, compliance
2. **Reliability** -- maturity, fault tolerance, recoverability, compliance
3. **Usability** -- understandability, learnability, operability, attractiveness, compliance
4. **Efficiency** -- time behavior, resource utilization, compliance
5. **Maintainability** -- analyzability, changeability, stability, testability, compliance
6. **Portability** -- adaptability, installability, co-existence, replaceability, compliance

ISO 9126 decomposed maintainability into four sub-characteristics:

- **Analyzability:** the effort needed to diagnose deficiencies or identify parts to be modified
- **Changeability:** the effort needed to implement a specified modification
- **Stability:** the risk of unexpected effects from modifications
- **Testability:** the effort needed to validate modified software

This model consolidated decades of quality research into a standardized vocabulary. Comparative analyses demonstrate that ISO 9126 provided the most balanced factor coverage among pre-2010 models [@alqutaish2010quality; @albadareen2011quality]. Al-Badareen et al. quantified this using a weight-based comparison method, finding that McCall scored 63.67% in overall factor coverage while FURPS (a simpler model from Hewlett-Packard) scored only 20.34% -- with ISO 9126 providing the most standardized and complete framework [@albadareen2011quality].

### ISO/IEC 25010 (2011)

ISO/IEC 25010 refined its predecessor by expanding to eight quality characteristics and restructuring sub-characteristics based on a decade of industry experience [@ISO25010]. The key changes relevant to maintainability were:

- "Changeability" was renamed to **modifiability** (a broader, more precise term)
- **Modularity** and **reusability** were added as explicit sub-characteristics
- "Stability" was subsumed by modifiability (modification without degradation)
- Security was elevated from a sub-characteristic of functionality to a top-level characteristic

### Evolution Comparison Table

The following table traces how the concept of "ease of change" evolved across quality models:

| Aspect | McCall (1977) | Boehm (1978) | ISO 9126 (2001) | ISO/IEC 25010 (2011) |
|--------|--------------|-------------|-----------------|---------------------|
| **Top-level structure** | 3 perspectives, 11 factors | Hierarchical utility tree | 6 characteristics | 8 characteristics |
| **Maintainability level** | One of 11 factors | Top-level branch (1 of 3) | One of 6 characteristics | One of 8 characteristics |
| **"Ease of change" term** | Flexibility | Modifiability | Changeability | Modifiability |
| **Decomposition depth** | Factors > Criteria > Metrics | Characteristics > Primitives | Characteristics > Sub-characteristics | Characteristics > Sub-characteristics |
| **Sub-characteristics** | Simplicity, conciseness, self-descriptiveness, modularity, consistency | Understandability, modifiability, testability | Analyzability, changeability, stability, testability | **Modularity, reusability, analysability, modifiability, testability** |
| **Metric operationalization** | Poorly defined | Absent | Partially defined (external metrics) | Quality-in-use + product quality metrics |
| **International consensus** | No (US Air Force) | No (academic) | Yes (ISO) | Yes (ISO/IEC JTC1) |
| **Coverage score** | 63.67% | N/A | Highest standardized | Supersedes ISO 9126 |

The progression shows a clear trend: maintainability has been refined from a vaguely defined "ability to fix bugs" into a multi-dimensional attribute with five distinct, measurable sub-characteristics. This thesis adopts ISO/IEC 25010 as its evaluation framework because it represents the current international consensus and provides the most fine-grained decomposition of maintainability available.

## 3.2 ISO/IEC 25010: The Standard Framework

ISO/IEC 25010 defines two quality models: a **product quality model** (8 characteristics describing internal and external quality) and a **quality-in-use model** (5 characteristics describing the user's experience). For evaluating architectural changes, the product quality model is the relevant one.

### The Eight Product Quality Characteristics

| # | Characteristic | Description |
|---|---------------|-------------|
| 1 | **Functional Suitability** | Degree to which a product provides functions that meet stated and implied needs |
| 2 | **Performance Efficiency** | Performance relative to the amount of resources used |
| 3 | **Compatibility** | Degree to which a product can exchange information with and perform functions alongside other products |
| 4 | **Usability** | Degree to which a product can be used to achieve goals with effectiveness, efficiency, and satisfaction |
| 5 | **Reliability** | Degree to which a system performs specified functions under specified conditions for a specified period |
| 6 | **Security** | Degree to which a product protects information and data |
| 7 | **Maintainability** | Degree of effectiveness and efficiency with which a product can be modified |
| 8 | **Portability** | Degree to which a system can be transferred from one environment to another |

### Deep Dive: Maintainability and Its Five Sub-Characteristics

Maintainability in ISO/IEC 25010 is decomposed into five sub-characteristics that together capture the full spectrum of what it means for software to be "easy to change." Each sub-characteristic targets a different aspect of the modification lifecycle -- from understanding what needs to change, to making the change, to verifying it worked correctly.

| Sub-characteristic | ISO Definition | Code-Level Indicators | Architecture-Level Indicators |
|-------------------|---------------|----------------------|------------------------------|
| **Modularity** | Degree to which a system is composed of discrete components such that a change to one component has minimal impact on other components | Low coupling between classes; high cohesion within classes; small, focused modules; absence of God classes | Clear component boundaries; well-defined interfaces; acyclic dependency graph; balanced component sizes |
| **Reusability** | Degree to which an asset can be used in more than one system, or in building other assets | Generic utility functions; parameterized classes; abstract base classes; absence of hardcoded dependencies | Shared service layers; library extraction; protocol-based interfaces; standardized data formats |
| **Analysability** | Degree of effectiveness and efficiency with which it is possible to assess the impact of an intended change, to diagnose deficiencies or causes of failures, or to identify parts to be modified | Clear naming conventions; comprehensive documentation; low cyclomatic complexity; small method size | Traceable architectural decisions; consistent layering; observable system state; separation of cross-cutting concerns |
| **Modifiability** | Degree to which a product or system can be effectively and efficiently modified without introducing defects or degrading existing product quality | Low coupling between objects (CBO); small method parameter lists; absence of feature envy; encapsulated data | Loose coupling between components; intermediary layers; stable interfaces; deferred binding strategies |
| **Testability** | Degree of effectiveness and efficiency with which test criteria can be established for a system and tests can be performed to determine whether those criteria have been met | Dependency injection; small testable units; deterministic behavior; absence of global state | Clear input/output contracts; mockable interfaces; observable side effects; isolated components |

Understanding these sub-characteristics is essential because architectural tactics target specific sub-characteristics. For example, the "Split Module" tactic primarily targets **modularity** (creating smaller, more independent components) and **modifiability** (localizing the impact of changes). When the thesis evaluates whether an LLM-implemented tactic succeeded, it must measure improvement in the targeted sub-characteristic specifically, not just a generic "maintainability score."

### Quality Attribute Scenarios

Bass, Clements, and Kazman provide a structured method for specifying quality requirements called **quality attribute scenarios** [@bass2021software]. A scenario has six parts:

1. **Source of stimulus** -- Who or what causes the change?
2. **Stimulus** -- What change or event occurs?
3. **Environment** -- Under what conditions? (design time, build time, runtime)
4. **Artifact** -- What part of the system is affected?
5. **Response** -- What should happen?
6. **Response measure** -- How do we know it succeeded?

A concrete maintainability scenario might read:

> A developer (source) wants to replace the payment gateway library (stimulus) during development (environment). The payment processing module (artifact) is modified with no side effects on other modules (response). The change is completed in fewer than 3 person-hours, affecting at most 2 modules, with all existing tests passing (response measure).

Quality attribute scenarios bridge the gap between abstract quality definitions and concrete, testable requirements. They provide the "before" and "after" framing that makes maintainability measurable.

## 3.3 Maintainability in Practice

### The 60-80% Problem

The economic importance of maintainability is difficult to overstate. Industry-wide data consistently shows that maintenance activities consume 60-80% of the total software lifecycle cost [@bass2021software]. For a typical enterprise system with a 15-year lifespan, this means that for every dollar spent on initial development, three to four dollars are spent on maintenance activities -- understanding code, diagnosing defects, implementing changes, and verifying correctness.

This cost distribution has a profound architectural implication: design decisions that reduce maintenance effort, even by small percentages, compound over the system's lifetime into substantial savings. A 10% reduction in the time needed to understand and modify a module translates to thousands of person-hours saved across a large codebase over a decade. This economic reality is what motivates the study of architectural tactics for maintainability improvement.

### Empirical Evidence: Molnar's Longitudinal Study

Molnar and Motogna provide the most rigorous longitudinal evidence for how maintainability behaves in real, evolving software systems [@molnar2020study]. Their study analyzed 111 releases of three open-source Java applications (FreeMind, jEdit, TuxGuitar), each spanning over a decade of development, using three quantitative maintainability models:

1. **Maintainability Index (MI):** A composite formula combining Halstead volume, cyclomatic complexity, lines of code, and optionally comment percentage. Widely used but has known limitations.

2. **ARiSA Compendium Model:** An object-oriented metrics model that measures maintainability through class-level metrics including coupling, cohesion, complexity, and size.

3. **SQALE (Software Quality Assessment based on Lifecycle Expectations):** A technical debt model implemented in SonarQube that estimates the effort required to fix all identified code issues, expressed as a ratio of remediation effort to development effort.

Their key findings reshape how we should think about measuring maintainability:

| Finding | Implication for Practice |
|---------|------------------------|
| SQALE is the most reliable system-level model | Use SonarQube Technical Debt Ratio for before/after comparisons at the system level |
| MI is confounded by system size at the system level | Do not rely on MI alone for cross-project or cross-version comparisons |
| MI correlates with SQALE at the class level (Spearman rho ~ -0.6) | MI remains useful for quick, fine-grained method/class complexity screening |
| Maintainability effort concentrates in a small subset of packages | Target "hotspot" packages for maximum impact -- in jEdit, 6 packages account for ~80% of maintenance effort |
| Mature application versions stabilize in quality | Early architectural investment pays compounding dividends over time |
| Major feature additions cause maintainability spikes | Milestone releases (e.g., FreeMind 0.8.0) can dramatically decrease maintainability if not accompanied by deliberate refactoring |
| Auto-generated code can dominate metrics | A single auto-generated package in FreeMind was the primary driver of its worst maintainability scores |

The hotspot concentration finding is particularly important for the thesis approach. If 80% of maintenance effort is concentrated in a small number of modules, then an LLM-based tactic implementation pipeline should prioritize identifying and transforming those specific modules rather than applying tactics uniformly across the entire codebase.

### Practical Example: Analyzing a Python Module with Radon

To make maintainability measurement concrete, consider a Python module analyzed with Radon, a static analysis tool that computes cyclomatic complexity (CC) and maintainability index (MI).

Given the following module:

```python
# payment_processor.py - A module with multiple responsibilities
import json
import logging
from datetime import datetime

class PaymentProcessor:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)
        self.logger = logging.getLogger(__name__)
        self.transactions = []

    def process_payment(self, amount, currency, card_number,
                        cvv, expiry, customer_id, order_id,
                        billing_address, shipping_address):
        # Validate card
        if len(card_number) != 16:
            raise ValueError("Invalid card number")
        if len(cvv) != 3:
            raise ValueError("Invalid CVV")
        month, year = expiry.split("/")
        if int(year) < datetime.now().year % 100:
            raise ValueError("Card expired")
        elif int(year) == datetime.now().year % 100:
            if int(month) < datetime.now().month:
                raise ValueError("Card expired")

        # Calculate fees
        if currency == "USD":
            fee = amount * 0.029 + 0.30
        elif currency == "EUR":
            fee = amount * 0.034 + 0.25
        elif currency == "GBP":
            fee = amount * 0.034 + 0.20
        else:
            fee = amount * 0.045 + 0.50

        # Process
        total = amount + fee
        transaction = {
            "id": f"TXN-{order_id}-{datetime.now().timestamp()}",
            "amount": amount,
            "fee": fee,
            "total": total,
            "currency": currency,
            "customer_id": customer_id,
            "order_id": order_id,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(transaction)

        # Log
        self.logger.info(f"Payment processed: {transaction['id']}")

        # Generate receipt
        receipt = f"""
        ====== RECEIPT ======
        Transaction: {transaction['id']}
        Amount: {amount} {currency}
        Fee: {fee} {currency}
        Total: {total} {currency}
        Date: {transaction['timestamp']}
        =====================
        """
        return transaction, receipt

    def get_daily_report(self, date):
        daily = [t for t in self.transactions
                 if t["timestamp"].startswith(date)]
        total_amount = sum(t["amount"] for t in daily)
        total_fees = sum(t["fee"] for t in daily)
        if len(daily) == 0:
            avg = 0
        else:
            avg = total_amount / len(daily)
        return {
            "date": date,
            "count": len(daily),
            "total_amount": total_amount,
            "total_fees": total_fees,
            "average": avg
        }
```

Running Radon on this module:

```bash
$ radon cc payment_processor.py -s -a
payment_processor.py
    C 7:0 PaymentProcessor
        M 8:4 __init__ - A (1)
        M 13:4 process_payment - C (12)
        M 57:4 get_daily_report - B (6)

Average complexity: B (6.33)

$ radon mi payment_processor.py -s
payment_processor.py - B (38.21)
```

**Interpreting the results:**

- **Cyclomatic Complexity (CC):** The `process_payment` method scores **C (12)**, meaning it has 12 independent paths through the code. Radon grades CC as: A (1-5, low risk), B (6-10, moderate), C (11-15, high risk), D (16-20, very high risk), E/F (>20, untestable). A CC of 12 indicates this method is difficult to test thoroughly and likely to harbor bugs in edge cases.

- **Maintainability Index (MI):** The module scores **B (38.21)** on a scale where A (>20) is maintainable, B (10-20) is moderately maintainable, and C (<10) is difficult to maintain. Note: Radon uses a 0-100 scale where higher is better. A score of 38.21 is above the threshold but signals room for improvement.

The problems are identifiable from the metrics:
- `process_payment` has **9 parameters** (violating Visser's Guideline 4: keep unit interfaces small, threshold <= 4)
- The method handles validation, fee calculation, transaction recording, logging, AND receipt generation (violating the Single Responsibility Principle)
- Multiple responsibility areas are interleaved in a single method body, reducing analysability

This is precisely the kind of module where architectural tactics -- specifically *Split Module* and *Increase Semantic Coherence* -- would improve measurable maintainability.

## 3.4 The SIG Maintainability Model

The Software Improvement Group (SIG), based on the work of Joost Visser and colleagues, developed a practitioner-oriented maintainability model that bridges the gap between abstract quality standards and daily coding decisions [@visser2016maintainable]. The model is grounded in the analysis of hundreds of real-world software systems and provides benchmarked thresholds for maintainability metrics.

### The 10 Guidelines

Visser's model defines 10 guidelines for writing maintainable code, each tied to a specific, measurable metric:

| # | Guideline | Metric | Threshold | Rationale |
|---|-----------|--------|-----------|-----------|
| 1 | **Write Short Units of Code** | Lines of code per unit (method/function) | <= 15 lines | Short units are easier to understand, test, and reuse. Long methods tend to accumulate multiple responsibilities. |
| 2 | **Write Simple Units of Code** | McCabe Cyclomatic Complexity per unit | <= 5 | Simple control flow reduces the number of test cases needed and makes behavior predictable. Each branch point adds a potential source of errors. |
| 3 | **Write Code Once (DRY)** | Code duplication percentage | Low % (minimize) | Duplicated code means duplicated bugs and duplicated maintenance effort. A fix in one copy must be replicated in all copies -- a process that is error-prone and often incomplete. |
| 4 | **Keep Unit Interfaces Small** | Number of parameters per method/function | <= 4 | Large parameter lists indicate that a method is doing too much or that related parameters should be grouped into objects. They also make method calls harder to read and more error-prone. |
| 5 | **Separate Concerns in Modules** | Module coupling (fan-in) | Low coupling between modules | Each module should have a single, well-defined responsibility. When concerns are separated, changes to one concern do not ripple through unrelated modules. |
| 6 | **Couple Architecture Components Loosely** | Component independence (% of hidden/internal code) | High % hidden | Components that expose minimal public interfaces are easier to replace, evolve, and test independently. The percentage of code that is "hidden" (not part of the public API) indicates encapsulation quality. |
| 7 | **Keep Architecture Components Balanced** | Component count (6-12 ideal) + Gini coefficient | Balanced distribution | A system with one massive component and many tiny ones is poorly decomposed. Balanced components indicate well-distributed responsibilities. The Gini coefficient measures inequality in component sizes. |
| 8 | **Keep Your Codebase Small** | Total lines of code / rebuild value | Minimize | Larger codebases require more effort to understand, navigate, and maintain. Every line of code is a liability that must be read, understood, and potentially modified. |
| 9 | **Automate Tests** | Test coverage percentage | >= 80% | Automated tests provide a safety net for modifications. Without sufficient coverage, developers cannot confidently change code because they have no way to verify that existing behavior is preserved. |
| 10 | **Write Clean Code** | Number of code smells / static analysis findings | Minimize | Code smells (long methods, duplicated code, dead code, commented-out code) reduce readability and signal structural problems. Clean code communicates intent clearly. |

### The Star Rating System

The SIG model uses a 1-5 star rating system calibrated against a benchmark of hundreds of real-world systems:

| Stars | Percentile | Interpretation |
|-------|-----------|----------------|
| 5 stars | Top 5% | Best in class -- the system is among the most maintainable in the benchmark |
| 4 stars | Top 30% | Above average -- the system meets industry standards for maintainability |
| 3 stars | Average (30-70%) | Average -- typical for the industry but with clear improvement opportunities |
| 2 stars | Bottom 30% | Below average -- maintainability issues are likely causing visible productivity problems |
| 1 star | Bottom 5% | Worst in class -- the system likely has severe maintainability problems |

The practical significance of these ratings is backed by empirical data. SIG's benchmarking found that issue resolution is approximately **2x faster in 4-star systems compared to 2-star systems** [@visser2016maintainable]. This means that a team working on a well-maintained codebase can fix bugs and deliver features in roughly half the time of a team working on a poorly maintained one.

### Mapping Guidelines to ISO 25010 and Metrics

Each of Visser's guidelines contributes to one or more ISO 25010 maintainability sub-characteristics. Understanding this mapping is essential for connecting practical coding guidelines to the formal quality framework:

| # | Guideline | Primary ISO 25010 Sub-characteristic | Secondary Sub-characteristic | Measurable Metric | Tool |
|---|-----------|--------------------------------------|-----------------------------|--------------------|------|
| 1 | Write Short Units | Analysability | Modifiability | Unit LOC | Radon (raw metrics) |
| 2 | Write Simple Units | Analysability, Testability | Modifiability | Cyclomatic Complexity | Radon (`radon cc`) |
| 3 | Write Code Once (DRY) | Modifiability | Reusability | Duplication % | SonarQube, PMD/CPD |
| 4 | Keep Unit Interfaces Small | Modifiability | Reusability | Parameter count | Radon, pylint |
| 5 | Separate Concerns | Modularity | Analysability | Module fan-in/fan-out | pydeps, import-linter |
| 6 | Loose Coupling | Modularity | Testability | Hidden code %, CBO | SonarQube, custom |
| 7 | Balanced Components | Modularity | Analysability | Component Gini coefficient | Custom analysis |
| 8 | Small Codebase | Analysability | All | Total LOC | cloc, Radon |
| 9 | Automate Tests | Testability | Modifiability | Coverage % | coverage.py, pytest-cov |
| 10 | Write Clean Code | Analysability | Modifiability | Code smell count | SonarQube, flake8, pylint |

### Connecting SIG Guidelines to Architectural Tactics

A key insight, noted by Visser and confirmed by mapping his guidelines to the Bass taxonomy, is that **unit-level code quality aggregates upward to determine architecture-level maintainability** [@visser2016maintainable]. The 10 guidelines map directly onto the three categories of modifiability tactics defined by Bass et al. [@bass2021software]:

| Visser Guideline(s) | Bass Tactic Category | Specific Tactics |
|---------------------|---------------------|------------------|
| Short Units (1), Simple Units (2), Separate Concerns (5) | **Increase Cohesion** | Split Module, Increase Semantic Coherence |
| Loose Coupling at module level (5) and architecture level (6) | **Reduce Coupling** | Restrict Dependencies, Use Encapsulation |
| Write Code Once (3), Small Interfaces (4) | **Abstract Common Functionality** | Abstract Common Services, Generalize Module |
| Write Clean Code (10) -- incremental cleanup | Evolutionary maintenance | Boy Scout Rule (continuous small improvements) |

This mapping demonstrates that the gap between "good coding practices" and "architectural tactics" is smaller than it might appear. Many architectural tactics are, at their core, disciplined applications of coding guidelines at the module and system level. This observation is important for the thesis because it suggests that LLMs, which have demonstrated competence at code-level refactoring tasks, may be able to implement architectural tactics if given appropriate context about the system's structure and the tactic's intent.

### A Critical Caveat

It is important to note that while the SIG model provides excellent operationalization of maintainability, its benchmark thresholds are proprietary and recalibrated yearly. For the thesis, we use open-source equivalents (Radon for complexity metrics, SonarQube Community Edition for technical debt analysis, coverage.py for test coverage) with transparent thresholds. The SIG thresholds serve as reference guidelines, not as absolute standards. What matters for evaluating LLM-implemented tactics is the **direction and magnitude of metric change**, not whether a specific threshold is crossed.

## Summary

This chapter established the theoretical and practical foundation for measuring maintainability. The key takeaways are:

1. **Quality models have converged** on ISO/IEC 25010, which decomposes maintainability into five measurable sub-characteristics: modularity, reusability, analysability, modifiability, and testability.

2. **Maintainability dominates lifecycle costs** (60-80%), making even small improvements economically significant, especially when compounded over a system's lifespan.

3. **SQALE/Technical Debt Ratio** is the most reliable system-level maintainability metric, while the Maintainability Index remains useful at the class/method level for fine-grained assessment [@molnar2020study].

4. **Maintenance effort concentrates in hotspots** -- a small fraction of modules contains the majority of maintainability issues, suggesting that targeted architectural interventions can yield disproportionate improvements.

5. **The SIG model's 10 guidelines** provide concrete, metric-backed coding practices that map directly to the modifiability tactics discussed in the next chapter [@visser2016maintainable].

6. **The connection between code-level metrics and architectural tactics** creates a measurable bridge: tactics define *what* architectural change to make, metrics define *how* to evaluate whether it improved maintainability.

The next chapter introduces architectural tactics in detail -- the specific design decisions that, when applied systematically, target and improve these measurable quality attributes.
