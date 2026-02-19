1

Introduction to the

Special Issue on Software Architecture

David Garlan and Dewayne Perry

I. What is software architecture?

For example, the box and line diagrams and explanatory

A critical aspect of the design for any large software sys-

tem is its gross structure represented as a high-level organi-

zation of computational elements and interactions between

those elements. Broadly speaking, this is the software ar-

chitectural level of design [1], [2]. The structure of software

has long been recognized as an important issue of concern

(e.g., [3], [4]). However, recently software architecture has

begun to emerge as an explicit (cid:12)eld of study for software

engineering practitioners and researchers. Evidence of this

prose that typically accompany a high-level system descrip-

tion often refer to such organizations as a \pipeline," a

\blackboard-oriented design," or a \client-server system."

Although these terms are rarely assigned precise de(cid:12)ni-

tions, they permit designers to describe complex systems

using abstractions that make the overall system intelligi-

ble. Moreover, they provide signi(cid:12)cant semantic content

that informs others about the kinds of properties that the

system will have: the expected paths of evolution, its over-

all computational paradigm, and its relationship to similar

trend is apparent in a large body of recent work in ar-

systems.

eas such as module interface languages, domain speci(cid:12)c

architectures, architectural description languages, design

patterns and handbooks, formal underpinnings for archi-

tectural design, and architectural design environments.

The second trend is the concern with exploiting speci(cid:12)c

domains to provide reusable frameworks for product fam-

ilies. Such exploitation is based on the idea that common

aspects of a collection of related systems can be extracted

What exactly do we mean by the term \software archi-

so that each new system can be built at relatively low cost

tecture?" As one might expect of a (cid:12)eld that has only

by \instantiating" the shared design. Familiar examples

recently emerged as an explicit focus for research and de-

include the standard decomposition of a compiler (which

velopment, there is currently no universally-accepted def-

permits undergraduates to construct a new compiler in a

inition. Moreover, if we look at the common uses of the

semester), standardized communication protocols (which

term \architecture" in software, we (cid:12)nd that it is used in

allow vendors to interoperate by providing services at dif-

quite di(cid:11)erent ways, often making it di(cid:14)cult to understand

ferent layers of abstraction), fourth-generation languages

what aspect is being addressed. Among the various uses

(which exploit the common patterns of business informa-

are (a) the architecture of a particular system, as in \the

tion processing), and user interface toolkits and frame-

architecture of this system consists of the following compo-

works (which provide both a reusable framework for de-

nents," (b) an architectural style, as in \this system adopts

veloping interfaces and sets of reusable components, such

a client-server architecture," and (c) the general study of

as menus, and dialogue boxes).

architecture, as in \the papers in this journal are about

Generalizing from these trends, it is possible to identify

architecture."

four salient distinctions:

Within software engineering, most uses of the term \soft-

(cid:15)

Focus of Concern:

The (cid:12)rst distinction is between

ware architecture" focus on the (cid:12)rst of these interpreta-

traditional concerns about design of algorithms and

tions. Typical of these is the following de(cid:12)nition (which

data structures, on the one hand, and architectural

was developed in a a software architecture discussion group

concerns about the organization of a large system, on

at the SEI in 1994).

the other. The former has been the traditional focus of

The structure of the components of a pro-

much of computer science, while the latter is emerging

gram/system, their interrelationships, and prin-

as a signi(cid:12)cant and di(cid:11)erent design level that requires

ciples and guidelines governing their design and

its own notations, theories, and tools. In particular,

evolution over time.

software architectural design is concerned less with the

As de(cid:12)nitions go, this is not a bad starting point. But

algorithms and data structures used within modules

de(cid:12)nitions such as this tell only a small part of the story.

than with issues such as gross organization and global

More important than such explicit de(cid:12)nitions, is the locus

control structure; protocols for communication, syn-

of e(cid:11)ort in research and development that implicitly has

chronization, and data access; assignment of function-

come to de(cid:12)ne the (cid:12)eld of software architecture.

ality to design elements; physical distribution; com-

To clarify the nature of this e(cid:11)ort it is helpful to observe

position of design elements; scaling and performance;

that the recent emergence of interest in software architec-

and selection among design alternatives.

ture has been prompted by two distinct trends. The (cid:12)rst

The second distinc-

Nature of Representation:

(cid:15)

is the recognition that over the years designers have begun

tion is between system description based on de(cid:12)nition-

to develop a shared repertoire of methods, techniques, pat-

use structure and architectural description based on

terns and idioms for structuring complex software systems.

graphs of interacting components [5]. The former

2

Requirements

Any way
that works

Implementations

Requirements

Requirements

Methods

Software Architecture

Implementations

Implementations

Figure 1a

Figure 1b

Figure 1c

Fig. 1. Design Methods versus Software Architecture

modularizes a system in terms of source code, usually

in their scopes of concern. Figure 1 illustrates this

making explicit the dependencies between use sites of

di(cid:11)erence. Without either software design methods

the code and corresponding de(cid:12)nition sites. The latter

or a discipline of software architecture design, the im-

modularizes a system as a graph, or con(cid:12)guration, of

plementor is typically left to develop a solution using

\components" and \connectors." Components de(cid:12)ne

whatever ad hoc techniques may be at hand (Figure

the application-level computations and data stores of

1a). Design methods improve the situation by provid-

a system. Examples include clients, servers, (cid:12)lters,

ing a path between some class of system requirements

databases, and ob jects. Connectors de(cid:12)ne the inter-

and some class of system implementations (Figure 1b).

actions between those components. These interactions

Ideally, a design method de(cid:12)nes each of the steps that

can be as simple as procedure calls, pipes, and event

take a system designer from the requirements to a solu-

broadcast, or much more complex, including client-

tion. The extent to which such methods are successful

server protocols, database accessing protocols, etc.

often depends on their ability to exploit constraints

(cid:15)

Instance versus Style:

The third distinction is be-

on the class of problems they address and the class

tween architectural instance and architectural style.

of solutions they provide. One of the ways they do

An architectural instance refers to the architecture of

this is to focus on certain styles of architectural de-

a speci(cid:12)c system. Box and line diagrams that accom-

sign. For example, ob ject-oriented methods usually

pany system documentation describe architectural in-

lead to systems formed out of ob jects, while others

stances, since they apply to individual systems. An

may lead more naturally to systems with an emphasis

architectural style, however, de(cid:12)nes constraints on the

on data(cid:13)ow. In contrast, the (cid:12)eld of software archi-

form and structure of a family of architectural in-

tecture is concerned with the space of architectural

stances [2], [6]. For example, a \pipe and (cid:12)lter" ar-

designs (Figure 1c). Within this space ob ject-oriented

chitectural style might de(cid:12)ne the family of system

and data(cid:13)ow structures are but two of the many pos-

architectures that are constructed as a graph of in-

sibilities. Architecture is concerned with the trade-

cremental stream transformers. Architectural styles

o(cid:11)s between the choices in this space|the properties

prescribe such things as a vocabulary of components

of di(cid:11)erent architectural designs and their ability to

and connectors (for example, (cid:12)lters and pipes), topo-

solve certain kinds of problems. Thus design meth-

logical constraints (for example, the graph must be

ods and architectures complement each other: behind

acyclic), and semantic constraints (for example, (cid:12)lters

most design methods are preferred architectural styles,

cannot share state). Styles range from abstract archi-

and di(cid:11)erent architectural styles can lead to new de-

tectural patterns and idioms (such as \client-server" or

sign methods that exploit them.

\layered" organizations), to concrete \reference archi-

tectures" (such as the ISO OSI communication model

II. Why is Software Architecture Important?

or the traditional linear decomposition of a compiler).

(cid:15)

Design Methods versus Architectures:

A fourth

Architectural design of large systems has always played

distinction is between software design methods|such

a signi(cid:12)cant role in determining the success of a system:

as ob ject-oriented design, structured analysis, and

choosing an inappropriate architecture can have a disas-

JSD|and software architecture. Although both de-

trous e(cid:11)ect. The current recognition of the importance

sign methods and architectures are concerned with

of software architecture would appear to signal the emer-

the problem of bridging the gap between requirements

gence of a more disciplined basis for architectural design

and implementations, there is a signi(cid:12)cant di(cid:11)erence

that has the potential to signi(cid:12)cantly improve our ability

to construct e(cid:11)ective software systems.

3

Speci(cid:12)cally, a principled use of software architecture can

been on the market for some time, there is a broad base of

have a positive impact on at least (cid:12)ve aspects of software

existing software. This base represents a signi(cid:12)cant invest-

development.

ment of capital, and as such should be considered as capital

1.

Software architecture simpli(cid:12)es

Understanding:

assets. The ability to use these assets is of important to

our ability to comprehend large systems by present-

the (cid:12)nancial health of software producers. Software archi-

ing them at a level of abstraction at which a system’s

tecture, to the extent that it focuses on domain-speci(cid:12)c

high-level design can be understood [1], [2]. More-

abstractions and the use of various granularities of existing

over, at its best, architectural description exposes the

architectural elements, supports the exploitation of these

high-level constraints on system design, as well as the

assets.

rationale for making speci(cid:12)c architectural choices.

Interoperability is another market driver that contribute

2.

Architectural descriptions support reuse at

Reuse:

to the successful exploitation of a company’s software as-

multiple levels. Current work on reuse generally fo-

sets, since it promotes sharing across product lines. Soft-

cuses on component libraries. Architectural design

ware architecture, to the extent that it is an e(cid:11)ective means

supports, in addition, both reuse of large components

of establishing a common architectural framework across

and also frameworks into which components can be

various domain-related products, represents a signi(cid:12)cant

integrated. Existing work on domain-speci(cid:12)c soft-

means for achieving interoperability.

ware architectures, reference frameworks, and design

As the research and development costs of software in-

patterns have already begun to provide evidence for

crease, there is increasing market pressure to procure,

this [7], [8].

rather than produce, signi(cid:12)cant portions of software sys-

3.

Software architecture can expose the di-

Evolution:

tems, either by third party production or by the purchase

mensions along which a system is expected to evolve.

of software commodities. The result of this shift to

con-

By making explicit the \load-bearing walls" of a sys-

suming

producing

rather than

software places an increased

tem, system maintainers can better understand the

importance on the resulting integration of the developed

rami(cid:12)cations of changes, and thereby more accurately

and purchased components. Software architecture, to the

estimate costs of modi(cid:12)cations [2]. Moreover, architec-

extent that it provides accessible codi(cid:12)cation of design ele-

tural descriptions can separate concerns of the func-

ments and their correct use in the context of speci(cid:12)c archi-

tionality of a component from the ways in which that

tectural styles, can be critically important in assuring that

component is connected to (interacts with) other com-

these various components are integrated e(cid:11)ectively.

ponents. This allows one to change the connection

An important software development driving factor is that

mechanism to handle evolving concerns about perfor-

of \interval reduction." In many segments of software-

mance, interoperability, prototyping, and reuse.

dependent businesses, market forces call for reduced costs

4.

Architectural descriptions provide new

Analysis:

and release cycles.

If a company can maintain cost and

opportunities for analysis, including high-level forms

quality levels while reducing production cycles,

it can

of system consistency checking [9], conformance to

achieve signi(cid:12)cant overall reductions in costs, while at the

an architectural style [6], conformance to quality at-

same time improving time-to-market. Software architec-

tributes [10], and domain-speci(cid:12)c analyses for archi-

ture, to the extent that it is able to reduce production

tectures that conform to speci(cid:12)c styles [11].

time by using existing assets, exploit common architectural

5.

There is a strong rationale for mak-

Management:

frameworks, and establish more e(cid:11)ective integration and

ing the achievement of a viable software architecture

generation mechanisms, may be able to achieve these time

a key milestone in an industrial software development

reductions.

process. Achieving this milestone involves specify-

ing a software system’s initial operational capabil-

III. The State of the Practice

ity requirements,

its the dimensions of anticipated

Much of architectural description in practice is largely in-

growth, the software architecture, and a rationale,

formal: drawings in which boxes represent processing com-

which demonstrates that the architecture,

if imple-

ponents, and arrows represent interactions among those

mented, would satisfy the system’s initial requirements

components. At best, these pictures present high-level

and anticipated directions of growth. If one proceeds

overviews of the software identifying ma jor design compo-

to develop a software product without satisfying these

nents and data/control (cid:13)ows, but they usually provide little

conditions, there is signi(cid:12)cant risk that the system

insight into the role that the data plays in the computation

will be either inadequate or unable to accommodate

or the details of the interactions between the components.

change.

However, the growing recognition of the importance of

The importance of software architecture can also be seen

software architecture is leading to much more explicit use

in terms of its broad impact on market drivers that are

of architectural design as currently manifested in the fol-

important for software-intensive businesses. These drivers

lowing approaches:

a(cid:11)ect the way businesses plan their software pro jects and,

ultimately, the way they build their software systems.

standardized components

product families

(cid:15)

(cid:15)

(cid:15)

Given that software has become an integral part of a wide

platforms

variety of products, and that many of these products have

domain-speci(cid:12)c architectures

(cid:15)

4

Product Line Manager

*

sponsors

sponsors

incentivizes

incentivizes

Researcher

*

collab

Product Line
Analyst

collab

*

*

Component
Producer

collab or
identity

Component
Assembler

*

produces

produces

Software
Architecture
Principles

used in

Product Line
Structure &
Strategy

used in

produces,
verifies

Product Line
Components,
Specifications,
Verifn Info

queries/
supplies

*

receives feedback
from other
participants

submitted to

Certification

Library

enters

items into

Brokerage

produces

Software
Products
for Users

provides
brokerage
feedback

Broker

*
operates

Fig. 2. Boehm-Scherlis Megaprogramming Enterprise Model

The use of

standardized components

arises where soft-

domain, these companies can combine the best aspects of

ware producers recognize that there is a common set of

standard platforms and standardized components to create

components that are used across a set of products. An

and specialize their domain-related product families. The

example of this is BaseWorx [12], a set of standard com-

platforms are tailored to their domains and the standard

ponents that forms the basis for a set of related operations

components are built to provide both the domain-speci(cid:12)c

support systems. Speci(cid:12)c systems are produced by adding

processing and structures, and the necessary glue to weld

the specialized components to the standard ones.

the many di(cid:11)erent architectural elements together.

Product families

are one means of capitalizing product

A good example of this approach is the oscilloscope

assets and using that asset base to create a family of closely

architecture developed at Tektronix, Inc. Product engi-

related product architectures. While the instances of a

neers in collaboration with researchers developed a reusable

product family all tend to be in the same domain, it is the

product architecture that provided a customizable frame-

sharing of components amongst those instances and the

work for instrumentation systems, based on a specialized

generation of those instances that is the driving force in

data(cid:13)ow model [1], [13]. Other more recent examples in-

product family architecture.

clude a number of DoD-sponsored pro jects in domains such

One approach that is gaining in popularity among many

as avionics, command and control, and mobile robotics.

software producers is that of a software

. A plat-

platform

This trend towards reuse of architecture-based, product-

form is a general set of components that form the basis of

line assets is leading to new roles, artifacts and relation-

a variety of related products. These components are usu-

ships in software development organizations. An example

ally generic capabilities, such as databases, graphical user

of a new organizational model based on architectural reuse

interface generators, etc. The components provide means

is provided by Boehm and Scherlis in their \Megaprogram-

of specialization by either special declarative languages or

ming Enterprise Model." As illustrated in Figure 2, some

special-purpose scripting languages. A platform is similar

of new roles introduced in the model include

to a set of standardized components, but it is populated

(cid:15)

product line managers

, who oversee the human,

with large-granularity components that need to be tailored

(cid:12)nancial, and software resources needed for success-

for the speci(cid:12)c software system.

ful development and exploitation of software product

Finally, there is a movement towards

domain-speci(cid:12)c

lines;

architectures

[8]. Most software intensive businesses have

, who are concerned with do-

product line analysts

(cid:15)

domain-speci(cid:12)c systems that are vital to their (cid:12)nancial

main analysis, and engineering and evolution of soft-

pro(cid:12)tability. By concentrating on those domains and cre-

ware product line architectures;

ating architectural abstractions that are speci(cid:12)c to their

, who develop,

test, cus-

component producers

(cid:15)

5

tomize, and adapt components;

ing issues of interoperability: techniques for detecting

(cid:15)

component assemblers

, who identify, assess, and

component mismatch and bridging those mismatches.

compose components to produce software systems;

6.

Architectural Codi(cid:12)cation and Guidance:

and

While expertise in architectural design is currently the

(cid:15)

\brokers"

, who manage and help populate a library

province of virtuoso designers, there is on-going work

of components and architectures.

on codifying this expertise so that others can use it.

IV. The State of Research

selection of architectural styles, handbooks of patterns

This has led to an interest in rules and techniques for

While the application of good architectural design is

and elements, and curricula for educating software ar-

becoming increasingly important to software engineering

chitects.

practice, the fact remains that much of common practice

7.

Tools and Environments for Architectural De-

leads to architectural designs that are informal, ad hoc, un-

sign:

Given notations and models for characteriz-

analyzable, unmaintainable, and handcrafted. This has the

ing software architectures, it becomes possible to sup-

consequences that architectural designs are only vaguely

port architectural design with new tools and environ-

understood by developers; that architectural choices are

ments. Current work is addressing architectural anal-

based more on default than solid engineering principles;

ysis tools, architectural design environments, and ap-

that architectural designs cannot be analyzed for consis-

plication generators.

tency or completeness; that architectures are not enforced

8.

Finally, we are beginning to see the

Case Studies:

as a system evolves; and that there are virtually no tools

emergence of good published case studies of architec-

to help the architectural designers with their tasks.

tural design including retrospective analyses of suc-

Current research in software architecture is attempting

cessful (and sometimes unsuccessful) architectural de-

to address all of these issues. Among the more active areas

velopment. These serve both to increase our under-

are:

standing of what it takes to carry out architectural

1.

This area

Architecture Description Languages:

design, as well as providing model problems against

addresses the need to (cid:12)nd expressive notations for

which other researchers can gauge the e(cid:11)ectiveness of

representing architectural designs and architectural

their techniques and tools.

styles. In particular, much of the focus of this research

V. This Issue

is on providing precise descriptions of the \glue" for

combining components into larger systems.

In this special

issue on software architecture we are

2.

Formal Underpinnings of Software Architec-

pleased to present seven papers that illustrate many of

ture:

This area addresses the current imprecision of

these emerging research areas.

architectural description by providing formal models

The (cid:12)rst paper, \Architectural Tradeo(cid:11)s for a Meaning-

of architectures, mathematical foundations for modu-

Preserving Program Restructuring Tool," by William Gris-

larization and system composition, formal characteri-

wold and David Notkin, presents a case study of the archi-

zations of extra-functional properties (such as perfor-

tectural design of a tool for program analysis and trans-

mance, maintainability, etc.), and theories of architec-

formation. It nicely illustrates how an architectural view

tural connection.

of a system helps clarify system issues, and highlights the

3.

Researchers

Architectural Analysis Techniques:

challenges of combining multiple architectural paradigms

in this area are developing new techniques for deter-

in a single design.

mining and predicting properties of architectures. In

The second paper, \A Domain-Speci(cid:12)c Software Ar-

particular, progress is being made to understand the

chitecture for Adaptive Intelligent Systems," by Barbara

relationships between architectural constraints and the

Hayes-Roth, Karl P(cid:13)eger, Phillippe Lalanda, Phillippe

ability to perform specialized analyses, as well as ab-

Morignot, and Marko Balabanovic, describes a hierarchi-

straction techniques that make analysis practical for

cal domain-speci(cid:12)c architecture based on a combination of

large systems.

layering, data streams, and blackboards. It shows how a

4.

As archi-

Architectural Development Methods:

common architectural framework, together with a rich set

tectural design becomes better understood, it becomes

of building blocks, can provide a powerful tool for system

imperative to (cid:12)nd ways to integrate architectural ac-

construction.

tivities smoothly into the broader methods and pro-

The next three papers deal with architectural descrip-

cesses of software development.

tion. \A Syntactic Theory of Software Architecture," by

5.

Architecture Recovery and Re-Engineering:

Thomas R. Dean and James R. Cordy, presents a notation

The ability to handle legacy code is critical for large

that focuses on the syntactic, graphical aspects of architec-

systems with long lifetimes. Research is beginning

tural patterns.

to address extraction of architectural design from ex-

\Abstractions for Software Architecture and Tools to

isting systems, uni(cid:12)cation of related architectural de-

Support Them," by Mary Shaw, Robert DeLine, Daniel

signs, abstraction, generalization, and instantiation of

V. Klien, Theodore L. Ross, David M. Young, and Gre-

domain-speci(cid:12)c components and frameworks. In ad-

gory Zelesnik, describes a language and set of supporting

dition, there is increasing research activity address-

tools for architectural description. One of the more inno-

6

vative aspects of this work is its support for the explicit

[13] D. Garlan, \The role of formal reusable frameworks," in

Pro-

de(cid:12)nition of architectural connectors.

ceedings of the First ACM/SIGSOFT International Workshop

on Formal Methods in Software Development

, (Napa, CA), 1990.

\Speci(cid:12)cation and Analysis of System Architecture Us-

ing Rapide," by David C. Luckham, Larry M. Augustin,

John J. Kenney, James Vera, Doug Bryan, and Walter

Mann, also de(cid:12)nes an architectural description language.

David Garlan

is an Assistant Professor of

In this language, interactions between components can be

Computer Science in the School of Computer

characterized in terms of event patterns. These can fur-

Science at Carnegie Mellon University. His re-

ther be used to analyze a running system for conformance

search interests include software architecture,

the application of formal methods to the con-

to more global rules about legal event interleavings.

struction of reusable designs, and software de-

The (cid:12)nal two papers are concerned with formal ap-

velopment environments. Professor Garlan

proaches to architectural modelling. \A Formal Approach

heads the ABLE pro ject, which focuses on the

development of languages and environments to

to Correct Re(cid:12)nement of Software Architectures," by R.A.

support the construction of software system

Riemenschneider, Mark Moriconi, and Xiaolei Qian, con-

architectures. Before joining the CMU faculty,

siders the problem of architectural re(cid:12)nement. The au-

Tektronix, Inc., where he developed formal, architectural models of

Professor Garlan worked in the Computer Research Laboratory of

thors argue that re(cid:12)nement should preserve certain struc-

instrumentation software.

tural and semantic properties, and show how this notion

leads to the use of conservative extension as a re(cid:12)nement

criterion.

\Formal Speci(cid:12)cation and Analysis of Software Archi-

Dewayne E. Perry

is a Member of Techni-

tecture Using the Chemical Abstract Machine Model," by

cal Sta(cid:11) in the Software and Systems Research

Center at AT&T Bell Laboratories. He spent

Paola Inverardi and Alexander L. Wolf, explores ways to

the (cid:12)rst part of his computing career as a pro-

characterize architectures as reactive models inspired by

fessional programmer, then combined both re-

recent formal work on the Chemical Abstract Machine.

search (as a visiting research faculty member

in Computer Science at Carnegie Mellon Uni-

Acknowledgements

versity) and consulting in software architecture

We would like to thank Barry Boehm, Paul Clements, Robert Mon-

in software engineering for the past 10 years.

and design, and has concentrated on research

roe, Mary Shaw, and Jeannette Wing for their insightful comments

His research interests (in the context of build-

on earlier drafts of this guest introduction.

ing and evolving large software systems) include: software architec-

References

ture, software process descriptions, analysis, modeling, visualization,

and environmental support; software development environments; and

[1] D. Garlan and M. Shaw, \An introduction to software archi-

the practical use of formal speci(cid:12)cations and techniques,

tecture," in

Advances in Software Engineering and Know ledge

Dr. Perry is a member of ACM and IEEE, a member of the ed-

Engineering, Volume I

, World Scienti(cid:12)c Publishing Company,

itorial board for IEEE Transactions on Software Engineering, and

1993.

Co-Editor in Chief of Software Process: Improvement and Practice.

[2] D. E. Perry and A. L. Wolf, \Foundations for the study of

software architecture,"

ACM SIGSOFT Software Engineering

Notes

, vol. 17, no. 4, 1992.

[3] E. W. Dijkstra, \The structure of the \THE"-multiprogramming

system,"

, vol. 11, no. 5, pp. 341{

Communications of the ACM

346, 1968.

[4] D. L. Parnas, P. C. Clements, and D. M. Weiss, \The modular

structure of complex systems,"

IEEE Transactions on Software

Engineering

, vol. SE-11, pp. 259{266, March 1985.

[5] R. Allen and D. Garlan, \Beyond de(cid:12)nition/use: Architectural

interconnection," in

Proceedings of the ACM Interface De(cid:12)ni-

tion Language Workshop

, vol. 29(8), SIGPLAN Notices, August

1994.

[6] G. Abowd, R. Allen, and D. Garlan, \Using style to give mean-

ing to software architecture," in

Proc. of SIGSOFT’93: Foun-

dations of Software Engineering

, Software Engineering Notes

18(5), pp. 9{20, December 1993.

[7] E. Gamma, R. Helm, R. Johnson, and J. Vlissides,

Design Pat-

terns: Elements of Reusable Object-Oriented Design

. Addison-

Wesley, 1994.

[8] E. Mettala and M. H. Graham, \The domain-speci(cid:12)c software

architecture program," Tech. Rep. CMU/SEI-92-SR-9, CMU

Software Engineering Institute, June 1992.

[9] R. Allen and D. Garlan, \Formalizing architectural connection,"

in

, May 1994.

Proc. of ICSE’16

[10] P. Clements, L. Bass, R. Kazman, and G. Abowd, \Predicting

software quality by architecture-level evaluation," in

To appear

in Proceedings of the Fifth International Conference on Software

Quality

, (Austin, Texas), October 1995.

[11] D. Garlan, R. Allen, and J. Ockerbloom, \Exploiting style

in architectural design environments," in

Proceedings of SIG-

SOFT’94: Foundations of Software Engineering

, ACM Press,

December 1994.

[12] R. P. Beck

, \Architectures for large-scale reuse,"

et al.

AT&T

Technical Journal

, vol. 71, pp. 34{45, November-December 1992.


