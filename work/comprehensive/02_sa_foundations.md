# Software Architecture Foundations

> **Learning objectives.** After reading this chapter you should be able to (1) state and compare the two foundational definitions of software architecture, (2) explain the role of design rationale as a first-class architectural element, (3) describe the major architectural styles and their quality trade-offs, (4) analyze the KWIC case study as an illustration of style-driven quality differences, and (5) explain how quality attribute scenarios connect styles to architectural tactics.

---

## 2.1 What Is Software Architecture?

Before we can discuss *improving* software architecture with automated tactics, we need a precise understanding of what software architecture *is*. Two foundational definitions, published within a year of each other in the early 1990s, established the vocabulary that the entire field still uses today. Each emphasizes different aspects of the same underlying reality, and understanding both provides a richer conceptual foundation.

### 2.1.1 Perry and Wolf (1992): Elements, Form, and Rationale

Perry and Wolf proposed the first formal model of software architecture in their seminal 1992 paper [@perry1992foundations]. Their definition takes the form of a triple:

$$\text{Software Architecture} = \{\text{Elements}, \text{Form}, \text{Rationale}\}$$

Each component of this triple captures a distinct concern.

**Elements** are the building blocks of an architecture. Perry and Wolf distinguish three classes:

- **Processing elements** perform transformations on data. In a web application, a request handler that validates input and produces a response is a processing element. In a compiler, the lexer, parser, and code generator are each processing elements.
- **Data elements** contain and represent information. The abstract syntax tree passed between compiler phases, the database schema behind a web service, or the message payload in a queue are all data elements.
- **Connecting elements** glue processing and data elements together. A REST API endpoint, a message broker, a shared database, or even a simple function call can serve as a connecting element. Perry and Wolf emphasize that connecting elements are "often overlooked but have a profound impact on the resulting architecture" --- systems with identical processing and data elements can have radically different properties depending on how they are connected.

**Form** comprises two sub-aspects:

- **Properties** constrain which elements may be chosen. For example, a "real-time" property constrains processing elements to those with bounded execution time. Properties are *weighted* --- some are mandatory (hard constraints), others desirable (soft constraints).
- **Relationships** constrain how elements may be placed relative to each other. A layered architecture imposes the relationship "layer N may only call layer N-1." A pipes-and-filters architecture imposes "each filter reads from exactly one input pipe and writes to exactly one output pipe."

**Rationale** captures *why* these elements, properties, and relationships were chosen. It explicates the satisfaction of system constraints including economics, performance, reliability, and organizational factors. Rationale is what distinguishes architecture from mere structure: two systems may have identical elements and form, but different rationale --- meaning they were designed to optimize different qualities and should be evolved according to different principles.

**A concrete example.** Consider a multi-phase compiler:

| Element class | Example | Role |
|---------------|---------|------|
| Processing | Lexer, Parser, Type Checker, Code Generator | Transform source code through successive representations |
| Data | Token stream, AST, Symbol table, IR | Intermediate representations passed between phases |
| Connecting | Function calls (sequential), Shared symbol table (repository) | Link phases together |

The *form* might specify: "Each phase must be invocable independently" (property) and "phases execute in a fixed linear sequence" (relationship). The *rationale* explains: "This decomposition was chosen to maximize modifiability --- a new optimization pass can be inserted between existing phases without modifying them."

### 2.1.2 Garlan and Shaw (1993): Components, Connectors, and Configuration

One year later, Garlan and Shaw proposed an alternative formulation that has become equally canonical [@garlan1993introduction]:

> "Software architecture [is] a collection of computational **components** together with **connectors** describing their interactions, composed into a graph with topological **constraints**."

- **Components** are the computational units that perform the work of the system. They range in granularity from individual objects or modules to entire services or subsystems. A microservice handling user authentication, a database engine, or a JavaScript front-end module are all components. What distinguishes a component from arbitrary code is that it has a well-defined interface through which it communicates with the rest of the system.

- **Connectors** are the interaction mechanisms through which components communicate. Unlike Perry and Wolf's "connecting elements," Garlan and Shaw treat connectors as first-class architectural entities with their own properties and semantics. An HTTP REST call, a message queue, a shared-memory region, a remote procedure call, or a Unix pipe are all connectors. The choice of connector deeply influences the system's quality attributes: a synchronous RPC connector creates tight temporal coupling; an asynchronous message queue provides loose coupling but introduces eventual consistency.

- **Configuration** is the topology --- the graph structure describing how components are wired together through connectors. Two systems using the same components and connectors can have very different configurations. A client-server configuration centralizes state in one component; a peer-to-peer configuration distributes it. The configuration determines the system's overall properties: scalability, fault tolerance, modifiability.

**A concrete example.** Consider a web-based e-commerce system:

| Concept | Example | Notes |
|---------|---------|-------|
| Component | Product Catalog Service, Order Service, Payment Gateway, PostgreSQL database | Each has a defined API |
| Connector | REST/HTTP between services, SQL connection to database, Message queue (RabbitMQ) for async order processing | Each has distinct quality implications |
| Configuration | Services communicate via REST; Order Service publishes events to RabbitMQ; Payment Gateway is called synchronously during checkout | Topology determines coupling and change propagation |

### 2.1.3 Comparing the Two Definitions

Both definitions describe the same phenomenon, but they emphasize different facets. The following table highlights the key differences and commonalities:

| Dimension | Perry & Wolf (1992) | Garlan & Shaw (1993) |
|-----------|---------------------|----------------------|
| **Core formula** | {Elements, Form, Rationale} | Components + Connectors + Configuration |
| **Building blocks** | Three element classes (processing, data, connecting) | Two first-class entities (components, connectors) |
| **Data treatment** | Data elements are a separate, explicit class | Data is implicit --- flows through connectors or resides in components |
| **Connectors** | "Connecting elements" --- one of three element classes | First-class entities with their own properties; elevated status |
| **Constraints** | Form = weighted properties + relationships | Configuration = topological constraints on the component-connector graph |
| **Design motivation** | Rationale is a first-class triple member | Not explicitly modeled (implicit in style choice) |
| **Style concept** | Architectural style as an abstraction over specific architectures | Styles defined by component/connector types and configuration rules |
| **Emphasis** | Formal model; why decisions were made | Taxonomic vocabulary; what structures exist |
| **Origin discipline** | Analogy to building, hardware, and network architecture | Emerged from practical SE case studies (KWIC, compilers, etc.) |

The two definitions are complementary. Perry and Wolf give us a framework for reasoning about *why* an architecture is the way it is (rationale) and *what constraints* it satisfies (form). Garlan and Shaw give us a concrete vocabulary for describing *what* an architecture looks like (components, connectors, configuration) and *which patterns* recur across systems (styles). A complete understanding of software architecture draws on both.

### 2.1.4 The "Load-Bearing Walls" Metaphor

Garlan and Perry, writing together in 1995, introduced a metaphor that crystallizes why architecture matters for maintainability [@garlan1995editorial]:

> "By making explicit the **load-bearing walls** of a system, system maintainers can better understand the ramifications of changes, and thereby more accurately estimate costs of modifications."

In a building, a load-bearing wall supports the structure above it. You can repaint it, hang pictures on it, even change its material --- but you cannot remove it without risking collapse. Non-load-bearing partition walls, by contrast, can be moved freely to reconfigure floor plans.

Software architecture works the same way. Some architectural decisions are *load-bearing*:

- The choice to use a relational database (changing to a document store later affects every query in the system)
- The decision to communicate between services via synchronous REST (switching to asynchronous messaging requires rethinking error handling, transaction boundaries, and user experience)
- The decomposition of a monolith into specific service boundaries (merging or splitting services later propagates changes through APIs, deployment pipelines, and team structures)

Other decisions are *partition walls* --- easily changed:

- The specific HTTP framework used within a service (Flask vs. FastAPI can be swapped with modest effort if endpoints are well-isolated)
- The serialization format for internal messages (JSON vs. MessagePack, if abstracted behind a serializer interface)

The critical insight for maintainability: **architectural tactics operate on the load-bearing walls.** When we apply "Use an Intermediary" to decouple a database dependency, we are modifying a load-bearing structural decision. When we "Split Module" to separate concerns, we are redefining the structural partitions of the system. These are exactly the changes that are most impactful for long-term maintainability --- and exactly the changes that are hardest to get right, which is why automating them is both valuable and challenging.

---

## 2.2 Architectural Styles

An *architectural style* defines a family of systems in terms of a pattern of structural organization [@garlan1993introduction]. Each style specifies the types of components and connectors that may be used, how they may be combined, and what constraints govern their composition. Choosing an architectural style is one of the earliest and most consequential decisions in a system's lifecycle, because it determines the system's strengths and weaknesses across multiple quality attributes.

### 2.2.1 Major Styles Overview

| Style | Structure | Quality Strengths | Quality Weaknesses | Example |
|-------|-----------|-------------------|-------------------|---------|
| **Pipes-and-Filters** | Linear chain of filters connected by pipes; each filter reads input, transforms it, writes output | Reusability (filters are independent), modifiability (add/replace/reorder filters), concurrency (filters can run in parallel) | Poor for interactive systems, overhead from data format conversion between filters, no shared state | Unix shell pipelines (`cat file | grep pattern | sort | uniq`), ETL data pipelines |
| **Layered** | Hierarchical layers; each layer provides services to the layer above and consumes services from the layer below | Abstraction (each layer hides complexity), modifiability (change in one layer affects at most adjacent layers), portability (replace a layer implementation) | Performance overhead from indirection, not all systems decompose naturally into layers, "layer bridging" temptation undermines the style | OSI network model, three-tier web applications (presentation / business logic / data) |
| **Event-Driven (Publish-Subscribe)** | Components publish events; other components subscribe to event types and react when events occur | Loose coupling (publishers do not know subscribers), extensibility (new subscribers added without changing publishers), evolution (components replaced without interface changes) | Loss of control over processing order, difficulty reasoning about correctness, challenges with data exchange between decoupled components | GUI frameworks (event listeners), microservice event buses, IoT sensor networks |
| **Repository (Blackboard)** | Central data store (repository) accessed by independent processing components; in the Blackboard variant, components are triggered by changes to the shared data | Data integration (single source of truth), tool independence (components interact only through the repository) | Bottleneck at the central store, tight coupling to the data schema, concurrency challenges | Database-centric applications, IDE environments (shared AST), Blackboard AI systems |
| **Client-Server** | Clients request services; servers provide them. Clear separation of concerns between request initiation and service provision | Centralized data management, clear security boundaries, shared resource efficiency | Server is a single point of failure, network latency, scalability limited by server capacity | Web applications, email (SMTP/IMAP), databases (client query / server response) |
| **Microservices** | System decomposed into small, independently deployable services, each owning its data and communicating via lightweight protocols (typically HTTP/REST or messaging) | Independent deployment, technology heterogeneity, team autonomy, fine-grained scalability | Distributed system complexity (network failures, eventual consistency), operational overhead (monitoring, tracing), data duplication across service boundaries | Netflix, Amazon, modern cloud-native applications |

### 2.2.2 The KWIC Case Study

One of the most influential demonstrations of how architectural style choice impacts quality attributes is the **Key Word In Context (KWIC)** case study, introduced by Parnas in 1972 and elaborated by Garlan and Shaw in 1993 [@garlan1993introduction].

**The problem.** A KWIC index system takes a set of lines (e.g., paper titles), generates all circular shifts of each line (moving each word to the front in turn), sorts the shifts alphabetically, and outputs the sorted result. For example, given the title "Software Architecture in Practice," the circular shifts are:

```
Software Architecture in Practice
Architecture in Practice Software
in Practice Software Architecture
Practice Software Architecture in
```

**Four architectural decompositions.** Garlan and Shaw show how the same KWIC functionality can be implemented using four different styles, each producing a different set of quality trade-offs:

1. **Shared Data (Repository).** All modules access a shared in-memory data structure. The input module stores lines in a shared array; the shift module reads lines and writes shifts to another shared structure; the sort module operates on the shifts in place; the output module reads the sorted shifts.

2. **Abstract Data Types (ADT / Object-Oriented).** Each module encapsulates its own data behind a well-defined interface. The Lines module provides `add_line()`, `get_line()`, `get_char()` operations; the Shifts module provides `shift()`, `get_shift_char()` operations that internally reference the Lines module; and so on.

3. **Implicit Invocation (Event-Driven).** Modules register interest in events. When the Input module finishes reading a line, it publishes a "line-added" event. The Shift module, subscribed to this event, automatically generates shifts. The Sort module is triggered when shifts are complete.

4. **Pipes and Filters.** The system is a pipeline: `Input | CircularShift | Sort | Output`. Each stage reads from standard input, processes, and writes to standard output. Filters are independent processes with no shared state.

**Quality trade-off comparison.** The following table, adapted from Garlan and Shaw's analysis, compares the four decompositions across five quality dimensions:

| Quality dimension | Shared Data | ADT / OO | Implicit Invocation | Pipes and Filters |
|-------------------|:-----------:|:--------:|:-------------------:|:-----------------:|
| **Algorithm change** (e.g., replace sort algorithm) | Poor --- sort is tangled with shared data structure | Good --- encapsulated behind interface | Good --- replace subscriber | Best --- replace a filter |
| **Data representation change** (e.g., change from array to linked list) | Poor --- all modules depend on shared structure | Best --- hidden behind ADT interface | Good --- data is local to components | Good --- filter-internal data is private |
| **Functional enhancement** (e.g., add "stop words" filtering) | Poor --- requires modifying shared data structures | Good --- add a new ADT module | Best --- add a new subscriber | Best --- insert a new filter |
| **Performance** (minimize memory, maximize speed) | Best --- direct memory access, no overhead | Good --- some overhead from interface calls | Poor --- event dispatch overhead | Poor --- data copying between filters |
| **Reusability** (use components in other systems) | Poor --- tightly coupled to shared data | Good --- modules are self-contained | Good --- event-based components are portable | Best --- filters are fully independent |

**Key insight.** No single style dominates all dimensions. The Shared Data style wins on performance but loses on modifiability. Pipes and Filters excels at reusability and functional enhancement but pays a performance cost. The ADT style balances most dimensions but does not achieve the best score in any single one. This is why architectural design involves *trade-offs* --- and why the concept of *architectural tactics* (fine-grained decisions targeting specific qualities) is essential.

### 2.2.3 Heterogeneous Architectures

Real-world systems rarely conform to a single pure architectural style. Garlan and Shaw explicitly note that practical architectures are **heterogeneous**, combining multiple styles through several mechanisms [@garlan1993introduction]:

- **Hierarchical composition.** A system may be organized as a layered architecture at the top level, but within a specific layer, use a pipes-and-filters decomposition. For example, a data processing layer might internally use an ETL pipeline, while the overall system follows a client-server pattern.
- **Mixed connectors.** A single system may use REST calls between services, message queues for asynchronous operations, and shared databases for batch processing --- combining client-server, event-driven, and repository connectors.
- **Multi-level elaboration.** A high-level "microservices" style decomposes into individual services, each of which internally follows a layered (controller / service / repository) pattern.

This heterogeneity is important for the thesis because it means that automated tactic implementation cannot assume a single style. An LLM-based tool must recognize the local style context of the code it is modifying and select tactics that are compatible with that context. As Harrison and Avgeriou demonstrated, the same tactic can be a "Good Fit" in one style and a "Poor Fit" in another [@harrison2010how].

---

## 2.3 Design Rationale

### 2.3.1 Rationale as a First-Class Element

Perry and Wolf's inclusion of *rationale* in the architecture triple is one of their most important and most overlooked contributions [@perry1992foundations]. Rationale answers the question: **Why was this architecture chosen?**

Consider two systems with identical structure: both use a layered architecture with three tiers. But the rationale differs:

- **System A** was layered to maximize *portability*: the data layer abstracts the database engine so the system can run on PostgreSQL, MySQL, or SQLite.
- **System B** was layered to maximize *team autonomy*: the presentation layer is owned by the front-end team, the business layer by the back-end team, and the data layer by the DBA team.

These systems look the same in a class diagram, but they should be *evolved differently*. In System A, changes to the data layer interface are extremely costly (they compromise portability). In System B, changes to the data layer interface may be acceptable if they improve the back-end team's velocity, as long as the inter-team API contract is maintained.

Without rationale, a maintainer looking at either system sees only the structure and might make changes that violate the original design intent --- contributing to architectural erosion.

### 2.3.2 The Documentation Problem

In practice, design rationale is rarely documented and even more rarely traced from architecture decisions to code [@perry1992foundations; @garlan1995editorial]. This creates a persistent problem:

1. The original architects understand *why* the system is structured as it is.
2. As team members rotate, this knowledge dissipates --- Perry and Wolf's concept of **knowledge vaporization** [@perry1992foundations]. Li et al. confirmed this as a top non-technical cause of architecture erosion, cited in 15.1% of the studies they surveyed [@li2021understanding].
3. New developers, lacking rationale, make changes that seem locally reasonable but violate architectural constraints.
4. The architecture erodes. Erosion increases the cost of future changes. The maintenance crisis deepens.

This documentation gap is part of what makes automated tactic implementation so valuable: if the tactic catalog explicitly encodes design rationale (e.g., "Use an Intermediary *because* direct coupling between modules increases change propagation cost"), then the LLM pipeline preserves and propagates that rationale through the code changes it generates.

### 2.3.3 Connecting Rationale to Tactics

Architectural tactics are, in essence, the **operational expression of rationale**. When a quality attribute requirement states "the system must accommodate new data sources without modifying existing processing modules," the rationale for choosing the "Generalize Module" tactic is directly embedded in that requirement. The relationship is:

```
Quality Attribute Requirement (WHY)
    -> Tactic Selection (WHAT design decision)
        -> Code Transformation (HOW it is implemented)
```

Perry and Wolf's model tells us that the *rationale* motivates the *form* (properties and relationships), and the form constrains the *elements*. Tactics are the mechanism by which we translate rationale into form: each tactic imposes specific properties ("modules must be decoupled") and relationships ("communication must go through an intermediary") that shape the architecture.

---

## 2.4 From Styles to Tactics

### 2.4.1 The Granularity Gap

Architectural styles provide the *big picture*: the overall structural organization of a system. But styles alone do not prescribe how to handle specific quality attribute requirements. Knowing that a system uses a layered architecture does not tell you:

- How to ensure that a change to the payment processing logic does not cascade into the presentation layer.
- How to reduce the coupling between the authentication module and every service that requires authorization.
- How to make the logging infrastructure replaceable at deployment time.

These are finer-grained design decisions that operate *within* a chosen style. They are **architectural tactics** --- a concept introduced and systematically cataloged by Bass, Clements, and Kazman [@bass2021software].

### 2.4.2 Quality Attribute Scenarios

Bass et al. define a formal structure for reasoning about quality requirements called a **quality attribute scenario** [@bass2021software]. Each scenario has six parts:

| Part | Description | Example |
|------|-------------|---------|
| **Source of stimulus** | An entity (human, system, environment) that generates the stimulus | A developer on the maintenance team |
| **Stimulus** | A condition that the architecture must respond to | Wants to add support for a new payment provider |
| **Environment** | The conditions under which the stimulus occurs | During normal development, system is in production |
| **Artifact** | The part of the system that is stimulated | The payment processing module |
| **Response** | The activity that results from the stimulus | The change is made, tested, and deployed |
| **Response measure** | How the response is measured | Change is confined to 1 module, completed in < 4 hours, no regression failures |

A modifiability scenario might read: "A developer (source) wants to add a new payment provider (stimulus) during normal development (environment). The change should affect only the payment module (artifact), be completed within 4 person-hours (response measure), and introduce no regressions (response measure)."

This scenario *motivates* the selection of specific tactics. To confine the change to one module, we might apply "Use Encapsulation" (hide the payment provider behind a stable interface) and "Generalize Module" (make the payment module parameterized by provider). To avoid regressions, we might apply "Maintain Existing Interface" (ensure the new provider conforms to the existing contract).

### 2.4.3 Bridging to the Next Chapter

Quality attribute scenarios are the bridge between architectural styles (Chapter 2) and architectural tactics (Chapter 4). Styles determine the overall playing field; scenarios define the specific quality goals; and tactics are the design moves that achieve those goals within the constraints of the chosen style.

In the next chapter, we examine the quality model that gives us a precise vocabulary for *what* we mean by "maintainability" --- the ISO/IEC 25010 standard and its sub-characteristics. In Chapter 4, we then present the complete catalog of modifiability tactics and show how each one addresses specific maintainability concerns.

---

**Review questions.**

1. In Perry and Wolf's model, what is the difference between *form* and *rationale*? Why is rationale important for long-term maintenance?
2. Using Garlan and Shaw's vocabulary, describe the components, connectors, and configuration of a system you have worked on or studied.
3. In the KWIC case study, why does the Pipes-and-Filters style excel at functional enhancement but perform poorly on raw execution speed?
4. Give an example of a "load-bearing" architectural decision and a "partition wall" decision in a web application you are familiar with.
5. How does the concept of *design rationale* connect to the problem of *architecture erosion*?
6. Write a quality attribute scenario (source, stimulus, environment, artifact, response, response measure) for a modifiability requirement in a system you know.
