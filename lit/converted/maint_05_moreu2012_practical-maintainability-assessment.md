(This is a sample cover image for this issue. The actual cover is not yet available at this time.)

This article appeared in a journal published by Elsevier. The attached
copy is furnished to the author for internal non-commercial research
and education use, including for instruction at the authors institution
and sharing with colleagues.

Other uses, including reproduction and distribution, or selling or
licensing copies, or posting to personal, institutional or third party
websites are prohibited.

In most cases authors are permitted to post their version of the
article (e.g. in Word or Tex form) to their personal website or
institutional repository. Authors requiring further information
regarding Elsevier’s archiving and manuscript policies are
encouraged to visit:

http://www.elsevier.com/copyright

Author's personal copy

Reliability Engineering and System Safety 100 (2012) 84–92

Contents lists available at SciVerse ScienceDirect

Reliability Engineering and System Safety

journal homepage: www.elsevier.com/locate/ress

A practical method for the maintainability assessment in industrial devices
using indicators and speciﬁc attributes

Pedro Moreu De Leon, Vicente Gonza´ lez-Prida Dı´az, Luis Barbera´ Martı´nez, Adolfo Crespo Ma´ rquez n

Department Industrial Management, Escuela Superior de Ingenieros de Sevilla, Camino de los Descubrimientos s/n, 41092 Sevilla, Spain

a r t i c l e i n f o

a b s t r a c t

Article history:
Received 3 March 2011
Received in revised form
27 December 2011
Accepted 29 December 2011
Available online 8 January 2012

Keywords:
Maintainability
Maintainability assessment and indicators
Maintenance
Dependability

The objective of this paper is to describe a procedure to obtain maintainability indicators for industrial
devices. This analysis can be helpful, among other cases, to compare systems, to achieve a better design
regarding maintainability requirements, to improve this maintainability under speciﬁc industrial
environment and to foresee maintainability problems due to eventual changes in a device operation
conditions. This maintainability assessment can be carried out at any stage of the industrial asset
life cycle.

With this purpose, this work ﬁrst introduces the notion of maintainability and the implementation
of assessment indicators, including some important requirements to perform that. Then, a brief
literature review is presented, including the deﬁnition of the main concepts, which are later used in the
paper. After studying the maintenance levels and the maintainability attributes, both terms are linked,
leading all this analysis to the assessment of the maintainability indicators. It follows a discussion
about the information obtained through the maintainability assessment process and its computation
into several maintainability indicators. The paper includes a case study, which implements the deﬁned
assessment into a practical scenario. Finally, the work concludes summarizing the more signiﬁcant
aspects and suggesting future researches.

& 2012 Elsevier Ltd. All rights reserved.

1.

Introduction

The purpose of this paper is to describe a procedure for obtaining
maintainability indicators applied to industrial devices and to
discuss how the indicators compiles the technical information in a
suitable and useful manner. According to the European Standard EN
13306:2010 [3], the maintainability is deﬁned as ‘‘ability of an item
under given conditions of use, to be retained in or restored to, a state
in which it can perform a required function, when maintenance is
performed under given conditions and using stated procedures and
resources.’’ This deﬁnition is completed with the following note:
‘‘Maintainability may be quantiﬁed using appropriate measures or
indicators and is then referred to as maintainability performance’’.
This paper presents a method to accomplish that note, that is to say,
to obtain the maintainability performance of an industrial asset, at
any time within its life cycle, including the original design (‘‘intrinsic
or inherent maintainability’’, EN 13306:2010 [3]). In order to do so,
the ﬁrst problem is to ﬁnd a way, a suitable procedure, to measure
maintainability in an easy and practical way. Once that procedure
is determined, a second problem is to decide precisely what needs
to be measured and for which type of maintenance operation

n Corresponding author. Tel.: þ34 610540222; fax: þ 34 954 486112.

E-mail address: adolfo@esi.us.es (A. Crespo Ma´ rquez).

0951-8320/$ - see front matter & 2012 Elsevier Ltd. All rights reserved.
doi:10.1016/j.ress.2011.12.018

(UNE 20654: 1992 [8]). The ﬁrst purpose of this paper is to deal
with these two problems.

In this work, the maintenance operations to accomplish on a
certain industrial device are divided into ﬁve groups, named
maintenance levels (related to the complexity of the maintenance
tasks) and two sets of features/attributes to measure maintain-
ability are proposed (only one of these sets will be maintenance
level dependent). Finally, six maintainability indicators will be
deﬁned and their values calculated by combining the scores
assigned to the maintainability attributes.

All this process requires the observation of ﬁve important
considerations if we want our set of ‘‘standardized’’ indicators to
allow future comparisons:

(cid:2) Capturing the operating conditions of the item. The description
of the device operational conditions/context, previously to the
assessment process, is a must. These conditions involve the
way that the item operates, its location within the plant layout
and relevant environmental aspects.

(cid:2) Capturing the maintenance level for which the maintainability
is assessed. The maintainability deﬁnition also includes
‘‘ywhen maintenance is performed under given conditions
and using stated procedures and resources’’.

(cid:2) Acknowledging the evaluators’ skills. In order to obtain objec-
tive and comparable measures for maintainability indicators,

Author's personal copy

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

85

the training of the evaluators will be another key aspect to
consider in this procedure.

(cid:2) Describing the item lifecycle stage where the maintainability

assessment is carried out.

Avoiding to take into consideration the existing maintenance
organization. When the maintainability indicator assessment is
performed during the device operational stage, it is important to
take into account that the assessments are on the device cap-
abilities, and not on the maintenance organization.

In the sequel this paper is organized as follows. After intro-
duction, in the second part a brief literature review is presented,
including the deﬁnition of the main concepts, which are later
used in the paper. Afterwards, in Section 3, the maintainability
indicators and maintenance levels are presented. Then, Section 4
presents a classiﬁcation of maintainability attributes from device
design perspective, maintenance staff and work conditions per-
spective and logistics support perspective. Consequently,
in
Section 5, maintainability attributes and maintenance levels are
described and evaluated to discuss and justify the indicators set in
Section 6. Moreover, the paper includes a case study, which
implements the deﬁned assessment into a practical scenario.
Finally, the work concludes summarizing the more signiﬁcant
aspects and suggesting future researches.

2. Brief literature review

It is not the aim of this section to present a comprehensive and
exhaustive study of the methods proposed for measuring the
maintainability performance, which could be the purpose of a
different paper, but to offer a quick overview of the main
approaches found in the technical literature dealing with this
issue. By doing so, we also contextualize the method that we
introduce in this paper.

The most referred contributions that we could ﬁnd in this area

in our literature review were the following:

– Goulden [4] uses MTTR as maintainability indicator (involving,
in that MTTR, all the times related with the repair, from the
fault location, to the ﬁnal checking after repair and set up
again). This MTTR is calculated throughout statistical infer-
ence, using historical data. The MTTR of a complex device can
be calculated by combining the MTTR, individually determined
for each of its components.

– Houshyar and Ghahramani [5], presents a software tool for the
operators of a device to record data from the device in order to
later calculate the performance and the maintainability, based
on that information.

– Wani and Gandhi [9], in Tribology (for mechanical devices),
assesses the tribo-maintainability, that is, the maintainability
from the tribology viewpoint. The tribology features are
assessed by a table in which qualitative (expert assessment)
assessment corresponds to a numerical value. Using those
values, the tribo-maintainability is obtained throughout an
algorithm

– Guo et al. [2], calculates MTTR from historical data and validate
statistically the result. Although MTTR is related with maintain-
ability, the author makes no considerations about that.

– Liu et al. [6], mainly considers the maintainability dependency on
the human factors required for maintaining the device, in order
to be taken into account in the device designing process. The
author groups those factors in four main categories: maintenance
operations safety, accessibility, comfort and practicability

– Lu and Sun [7], presents an expert-based assessment proce-
dure. The expert assesses a set of factors, from which, the

author considers the maintainability is depending on (such as
identiﬁcation, ergonomics,
testability, simplicity, etc. and
other experience evaluated factors). The evaluation of each
factor is made by verbal scale, which is translated into
numbers by fuzzy logic.

– Barabady [1] determines the reparation time by statistical
methods (using Relex software) in a case study. He considers
also some environmental and operational conditions to com-
pute with the time to repair data in order to better describe
the maintainability with such statistical-based indicator.

These contributions can be grouped, regarding the methods
being used, into two main basic approaches, according to the
source of the input information and the nature of it as follows:

J Expert based methods using the experience and insights of
maintenance experts combined with historical data and objec-
tive assessments.

J Statistics based methods applied to historical data recorded

from trials.

The method presented in this paper can be classiﬁed within
the expert-based approach. By its use, a comprehensive assess-
ment and updated maintainability can be achieved, in a very
practical, easy to understand and apply way.

With regards to the type of indicators being used, the con-
tributions reviewed above can be classiﬁed into three main
groups:

J Multiple maintainability factors stimation without the obten-
tion of a maintainability index or global or partial maintain-
ability indicator [6,7].

J Single maintainability performance indicator based on statis-
tical analysis of historical data and mainly on the estimation of
MTTR [4,1,5,2].

J Single maintainability global indicator based on an algorithm
involving the different scores in deﬁned maintainability
factors.

In this paper we present multiple maintainability indicators,
which are both general (for all maintenance levels) and speciﬁc
(related to each maintenance level). These indicators are not
based on statistical inference but on maintainability attributes/
factors evaluation and on the utilization of different algorithms to
use these factors’ scores and to obtain the ﬁnal indicators values
(general and speciﬁc).

3. Maintainability indicators and maintenance levels
description

The maintainability indicators are assessed according to two

kinds of attributes or characteristics of the device:

(cid:2) General attributes: those affecting any device maintenance
level. That is to say, they are maintenance level independent.
(cid:2) Speciﬁc attributes: those depending on the maintenance level.
That means they are functions of all the maintenance actions
to be performed on a speciﬁed maintenance indenture level.

The assessment of the maintainability speciﬁc attributes for a
device requires, therefore, the classiﬁcation of the maintenance
In this paper we
actions within speciﬁc maintenance levels.
propose ﬁve maintenance levels. For each level, the device
maintainability performance will be assessed, checking whether
the maintainability speciﬁc attributes have been taken into

Author's personal copy

86

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

account for the development of maintenance actions at that level.
The attributes ranking is done using a ﬁve values scale from
0 to 4 points, trying to reduce subjectivity and to obtain fair
values easily to manipulate.

The maintenance levels are here established, based on the
complexity of the tasks to be performed and the complexity of
the human and material resources needed for its performance.
The required unavailability time on the device is here also taken
into account. In any case, these levels are due to common criteria
accepted worldwide and are the following ones:

(cid:2) Level 1: simple maintenance actions performed in the up state
of the device. At this level, the operator performs preventive or
corrective activities, which do not require setting the device
into a down state. They are, for instance, simple adjustments
foreseen by the manufacturer, without assembling or disas-
sembling the device. Another example is the simple replace-
ment of easily accessible components.

(cid:2) Level 2: maintenance actions with replacement of functional
components. These actions set the device into a down state. In
this period the operator performs preventive and/or corrective
maintenance actions, usually considering functional compo-
nents of the device for their replacement.

(cid:2) Level 3: failures identiﬁcation and diagnosis. In these main-
tenance actions the operator, after setting the device into a
down state, identiﬁes and locates the causes of the failures.
(cid:2) Level 4: inspections. The inspections refer to an extensive
amount of
tests and preventive/corrective maintenance
actions that may require full or partial disassembly of the
device. The purpose of the inspection is to maintain, on a
device, the required availability and safety level over the time.
Revisions are usually performed at prescribed time intervals or
after determined amount of operations.

(cid:2) Level 5: updating, reconstruction and/or overhaul. These
operations are under the maintenance service responsibility
of the plant or manufacturer. They are very important opera-
tions, which may include modiﬁcations and/or improvements.
It is therefore possible that these operations increase the
lifetime of the original device.

4. Classiﬁcation of maintainability attributes

The maintainability indicators assessment shall be performed
taking into account attributes from the device. These attributes
are classiﬁed into three groups according to their nature: attri-
butes related to the design, related to work conditions and staff
requirements and attributes related to the needs of logistic
support. It is important to observe here how these attributes are
connected to capabilities of the device under assessment, and not
to the actual capabilities of the maintenance organization already
existing, where the device is being used.

4.1. Attributes related to the device design

Inside this group, we consider eight attributes as follows:

(cid:2) Simplicity: existing reduction in the amount of elements and

unnecessary assemblies.

(cid:2) Identiﬁcation: clearly location and signs from those compo-
nents that are going to be mainly maintained, and from those
existing points for inspection and test.

(cid:2) Modularity: device design in separated parts, functional assem-
bly units, thus, it is not necessary to disassemble the whole
equipment in case of failure, but only the part(s) where the
problem is located.

(cid:2) Tribology: right use of materials with appropriated quality in
order to increase the use life of fragile elements, and to
improve the lubrication of pieces wearing out quickly.

(cid:2) Standardization: spare parts compatibility to other similar
materials when it is necessary to replace a device component.
This attribute is conditioned by the standards choice during
the design of elements like bearings, gaskets, etc. and their
dimensional and functional tolerances.

(cid:2) Failure watch: indications in the device about critical para-

meters and alarms to foresee failures.

(cid:2) Accessibility: schedule for accesses to all those elements to be

maintained through gates, sliding doors, etc.

(cid:2) Assembly/disassembly: easiness to remove or replace elements
in the different subsystems. This easiness shall be emphasized
by gaskets, joints, welding, etc. inﬂuencing also the elements
size and volume.

4.2. Attributes related to the maintenance staff and work conditions

Inside this group, we consider three attributes:

(cid:2) Ergonomics: space requirements in order to set up the proper
working conditions for the development of maintenance
activities. This attribute also assesses requirements in loca-
tions and spaces where materials to manipulate can be placed
when it is necessary to perform interventions on the physical
system.

(cid:2) Training: skill required in the maintenance staff for the kind of

work to perform.

(cid:2) Environment: requirements on the environmental conditions
are referred in order to enable the maintenance under proper
conditions and complete safety.

4.3. Attributes related to the necessity of logistics support

Inside this group, we consider ﬁve attributes:

(cid:2) Relation with the manufacturer: requirements related to the
coordination among the people responsible for the plant
maintenance and the manufacturer: common language, same
system for machines management, geographical remoteness,
same working hours, same jurisdiction, etc.

(cid:2) Personnel organization: amount of people required to carry out
the maintenance operation and possibilities of dividing the
work into parallel tasks.

(cid:2) Spare parts: requirements in terms of spare parts for their use
in the maintenance activity where the acquisition easiness
shall be observed.

(cid:2) Maintenance tools and equipments: requirements in terms of
tools and instruments for performing the maintenance activ-
ity. Functionality, ergonomics as well as the acquisition easi-
ness will be observed.

(cid:2) Interdepartmental coordination: complexity in the task envir-
onment: requirements for handling of hazardous parts or
elements, for the permit application, for the communication
among different departments, etc.

(cid:2) Documentation: indications given by the manufacturer for the
device maintenance or prepared for the maintenance service,
explaining how to perform the maintenance action.

5. Maintainability attributes and maintenance level

The 17 attributes commented in the paragraph above, are
grouped into two sets, according to Section 4. The ﬁrst group

Author's personal copy

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

87

concerns those attributes, which inﬂuence the device maintain-
ability at any maintenance levels (General attributes), that is, a
type of maintainability, which is independent of the maintenance
level. The second group of attributes could inﬂuence the device
maintainability in a different way and degree, deepening on
the level of maintenance, which is being considered (Speciﬁc
attributes).

5.1. General attributes and their assessment

They are considered eight general attributes, which are main-
tenance level independent. The general attributes are simplicity,
identiﬁcation, modularity, tribology, ergonomics, standardization,
failure watch and relationship with the manufacturer. For their
assessment, the expert will consider each one of them independently.
The result of their assessment is an integer number within the range
from ‘‘0’’ to ‘‘4’’. Hereafter some examples are presented as follows:
G1. Simplicity: the use of a minimal amount of components
and assemblies in the devices will be checked, even those
components that are redundant.

(cid:2) 0: Very high number of components with redundant elements,

easily visible.

(cid:2) 4: Optimized, reduced and without redundancy number of

components.

G2. Identiﬁcation: the identiﬁcation of elements to be main-
tained and the points for testing will be checked, considering
whether they are clearly indicated or not. It will be also observed
that connectors are identiﬁed as well as danger areas, places
where technicians have to position themselves for working, etc.

(cid:2) 0: No identiﬁcation
(cid:2) 4: Complete identiﬁcation, everything can be seen in front of

the device

G6. Standardization: for those components, which could be
replaced at any moment during their life cycle, their compatibility
with other ones out of the shelves of the market are checked out.
It will result in a minimum storage of components, and minimum
amount of adjustments.

(cid:2) 0: Very bad standardization. High difﬁculty to ﬁnd a spare part

in the market. High need of spare parts storage.

(cid:2) 4: Good standardization. High easiness to ﬁnd spare parts in
the market and with competitive prices. There is no need to
store spare parts.

Table 1
Accessibility (S1) and Assembly/disassembly (S2).

Level Watching this attribute

Assessment scale

will have as a target

S1. Accessibility
1

Checking the proper access for ﬁrst
maintenance level tasks, for
instance basic inspections,
consumable changes (lubricants),
etc.
Checking the proper access for
second maintenance level tasks,
easy repairs by replacement of
functional elements, etc.
Checking the proper access for third
maintenance level tasks, for
instance on the diagnosis and
ﬁnding out of failures causes in the
device, or the replacement or repair
of minor components.
Checking the proper access for forth
maintenance level tasks, which
involve important revisions on the
device, test performances, etc.
Checking the proper access in order
to perform reconstructions,
updating or overhauls in the device.

S2. Assembly/disassembly
1
2

Checking the easiness for the
assembly/disassembly (open, close,
connect, disconnect, adjust, etc.)
of those subsystems or elements,
which are involved in the device
ﬁrst maintenance level tasks.

2

3

4

5

3

4
5

In the range (0–4) where
0: Very difﬁcult access, it is
needed to move things and the
technician himself, etc.
4: Very good access

In the range (0–4) where
0: Many difﬁculties: many tools
are needed. Material weight,
volume and size are too
important.
4: Very easy to assemble and
disassemble.

6. Maintainability indicators assessment

In order to apply this methodology, it is required to calculate
six indicators, based on the value of the attributes assessed at
general level and at each maintenance level

(cid:2) One general maintainability indicator (GMI), which results from

the device general attributes assessment.

(cid:2) Five speciﬁc maintainability indicators, one for each mainte-
nance level, named ‘‘maintainability indicator of maintenance
level i’’ (where ‘‘i’’ takes the integer value from 1 to 5) or LMIi,
as a result of assessing the speciﬁc attributes of the device.

5.2. Speciﬁc attributes (maintenance level dependents) and their
assessment

6.1. Discussion and justiﬁcation of the indicators set

These attributes will be applied in the place where the device
maintenance is performed (which can be different from its usual
location), especially in the case of the last two maintenance levels.
We consider nine maintainability attributes, such as accessibility,
assembly/disassembly, training, personnel organization, environ-
ment, spare parts, maintenance tools and equipments,
inter-
departmental co-ordination and documentation. These attributes
should be assessed by an expert, at each maintenance level, by
assigning an integer number, ranging from ‘‘0’’ to ‘‘4’’. Hereafter,
there are two of those attributes, as examples (see Table 1 with
S1: Accessibility and S2: Assembly/Disassembly).

There are similar tables for other seven speciﬁc attributes

(they are nine in total)

The maintainability degree of an industrial asset can be
understood by studying the scores obtained for each one of the
eight general attributes and for those of the nine speciﬁc attri-
butes (per maintenance level,
i.e. 45 values considering ﬁve
possible levels). However it is obvious that such an amount of
information is not practical to be managed (especially for com-
parison purposes). Moreover, the relevance of the different
attributes could not be the same, for a device in particular.
Additionally, an attribute could be very important for a device
in a certain operating conditions while the same attribute could
be negligible for the asset in a different operating condition, or for
a different asset in the same conditions.

For the ﬁrst reasons (the big amount of heterogeneous
information concerning the maintainability of an asset), it would

Author's personal copy

88

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

to aggregate all

this information in a few
be convenient
indicators, leaving the whole attributes information for an in-
depth analysis. For the second consideration (the different
importance of the attributes, depending on the kind of asset
and/or its operating conditions), it is recommended to assess also
the relevance of each attribute. That means that we have to
consider two ﬁgures for each attribute (the score for each
attribute and the attribute relative importance within the set of
attributes), instead of only one (the score of the attribute), as it
has been considered until now. But this consideration drives to a
new problem: to assess the relative importance for each attribute.
Note that the complexity related to the large amount of informa-
tion to deal with the maintainability performance results now
even increased when considering the relative importance of each
attribute.

For all previous reasons, the aggregation of the information
becomes an absolute need, and in order to carry out such
aggregation,
in each case, the maintainability indicators are
obtained by the weighted average of the values achieved in the
attributes assessment.
Let consider that

pAi ¼ 0,1f

g with

pAi ¼ 1

n

X
i ¼ 1

where pAi is the relative weight of attribute Ai. The treatment is
similar for general attributes (Gi), as well as for speciﬁc ones (Si)
concerning a maintenance level;
the ordinal number of
each attribute, n the number of attributes, which conﬁgure the
indicator under calculation (n ¼8 for the general maintainability
indicator, based on the eight general attributes; n¼9 for any of
the maintainability indicators of any maintenance level, based on
the nine speciﬁc attributes).

i

To determine the contribution of each attribute to the main-

tainability indicator, we propone the following procedure:

(cid:2) To estimate PAi¼{0,4}: the importance of each attribute for the
maintainability calculation. The expert who is assessing the

maintainability should answer how important each attribute
(general or speciﬁc for a maintenance level) is, concerning the
maintenance of the device under evaluation, in its operation
conditions (notice that this PAi is different from pAi, which is a
value between 0 and 1).

(cid:2) The weight of each attribute (relative importance of each

attribute within the set of them) will be

n

pAi ¼ PAi(cid:2) X

i ¼ 1

PAi

6.2. General maintainability indicator

It is deﬁned as follows:

8

GMI ¼

GipGi

X
i ¼ 1

ð1Þ

ð2Þ

where i is the ordinal number of each of the eight maintainability
general attributes; Gi the integer value in the range from 0 to 4,
for each of the eight maintainability general attributes; pGi the
decimal value in the range from 0 to 1, weight of each of the eight
maintainability general attributes. These weights have been
previously calculated (Formula (1)) from the importance of the
attributes for the maintainability performance.

6.3. Maintainability indicator of maintenance level j

It is deﬁned as follows:

LMIj ¼

9

X
i ¼ 1

Sijpsij with j ¼ 1. . .5

ð3Þ

where j is the ordinal number of each of the ﬁve maintenance
levels; i the ordinal number of each of the nine maintainability
speciﬁc attributes; Sij the integer value in the range from 0 to 4,
for each of the nine maintainability speciﬁc attributes, for each of
the ﬁve maintenance levels; pVij the decimal value within the

Weight system

Control screen

Black box for crane

Load limit devices

Crane
remote
control

Weigh hook:
200 kg–50 ton

Weigh crane pin

Weigh pulley

Electro magnetics

Fig. 1. Bridge crane components.

Author's personal copy

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

89

range from 0 to 1, weight of each of the nine maintainability
speciﬁc attributes, for each of the ﬁve maintenance levels. These
weights have been previously calculated (Formula (1)),
in a
similar way to what we did for the case of GMI.

7. Case study

Here, we present a case of practical application for character-
ization of maintainability indicators in a bridge crane (see Fig. 1),
which is a traveling overhead hoisting machine that spans ﬁxed
side rails that are part of a building structure. The hoisting unit
also travels laterally between the rails used to handle materials in
such a manufacturing plant.

For the evaluation of maintainability indicators, we have taken
into account the general attributes and the speciﬁc attributes.
However,
in this case study, we have considered the same
importance for all the attributes (PG1 to PG8¼ 1 and PS1 to
PS9¼1; consequently the weights are the same for all the general
attributes and for all speciﬁc ones). The indicators in this case are
the corresponding average of the attributes ﬁgures (as an exam-
ple, Table 2 shows the general attributes and Table 3 the
maintainability indicator for maintenance levels 1–5). After the

tables, a graphical representation illustrates the maintainability
indicators (see Figs. 2 and 3).

As a brief discussion of results, we can point out that the
general maintainability indicator and those indicators for the
three ﬁrst maintenance levels are over the two third parts of
the maximum possible indicator level (71% for the general
indicator, and 72.25%, 77.75% and 66.75% for the three ﬁrst
maintenance levels maintainability indicators). Only for those
more complex maintenance operations, big complex general
maintenance operations and overhauls, the maintainability goes
down to 64% and 52.75%. To understand the reasons for those
ﬁgures, the attributes could be analyzed. As an example, con-
cerning the maintenance levels 4 and 5, those indicators with
values lower than 3 (i.e., those ones very badly scored) should be
specially followed up. They are summarized in Tables 4 and 5.

8. Conclusions

The objective of this paper has been to deﬁne a calcula-
tion method for a set of indicators, which assesses the maintain-
ability of industrial devices. The purpose of this assessment can
be the comparison of devices according to established criteria,

Table 2
General maintainability indicator.

Code Attribute

Criteria

Scale (0–4)

Value

General attributes
Simplicity
G1

The use of a minimal amount of components and assemblies
in the devices will be checked, even those components that
are redundant.

0: very high number of components with redundant
elements, easily visible.
4: Optimized, reduced and without redundancy number of
components.

G2

Identiﬁcation

The identiﬁcation of elements to be maintained and the
locations for testing will be checked. It will be also observed
that connectors are identiﬁed as well as danger areas, places
where technicians have to position themselves for working, etc.

0: No identiﬁcation.
4: Perfect equipment identiﬁcation.

It will be checked if there are different functional assembly
units in the device, which allow to minimize the parts of the
device to be touched in case of maintenance operations.

0: The change of units is complex and requires the
movement of other units.
4: Excellent modularization.

G3 Modularity

G4

Tribology

G5

Ergonomics

Appropriate choice of device materials that are subjected to
friction, lubrication and wear will be checked, with the aim
of maximizing their life.

It will be checked how easy it is the development of
maintenance tasks, analyzing the weight, size and shape of
components to be handled. Those areas allocated for the task
completion will be also reviewed, checking their suitability in
terms of lighting, volume, etc.

G6

Standardization It will be checked the components compatibility to be replaced

with others found in the market. It will result in a minimum
storage of components, and minimum amount of adjustments
especially in elements to replace at low maintenance levels.

G7

Failure watch

The existence of failures indicators on the device will be
checked, as well as the possibility of monitoring parameters
useful for maintenance.

G8

Relation with
the
manufacturer

The coordination necessity will be checked for the development
of maintenance activities, as well as those requirements on
communications and management, which are in common to
other parts.

0: 0–10% of properly selected items.
4: 80–100% of properly selected items.

0: Maintenance tasks with complex implementation. Weight,
size and shape of the elements to manipulate extremely
uncomfortable causing fatigue to the operator. Inadequate
working space.
4: Excellent ergonomics of the device, maintenance is very
comfortable and agile.

0: Poor standardization. High difﬁculty to ﬁnd spare parts
on the market. High need for storage of spare parts.
4: Good standardization. Very easy to ﬁnd spare parts on the
market at competitive prices. It is not necessary to store spare
parts.

0: Poor failure watch and diagnosis. There are not indicators
of the condition of equipment and is impossible to make any
diagnosis on its condition.
4: Good failure watch and diagnosis. There are indicators to
know the status of the device and indicators are easily
monitored in the device.

0: Poor coordination. The maintenance worker is far, use
different languages, etc.
4: Good coordination. The maintenance worker is near, use the
same language, there are no communication problems, use
standard communication technologies, etc.

General maintainability indicator

2.875

3

2

3

1

3

3

4

4

Author's personal copy

90

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

Table 3
Maintainability indicators for maintenance level 1 to 5.

COD. Attribute

Criteria

Scale (0–4)

VALUE at mainten. level

Speciﬁc attributes
S1

Accessibility

S2

Assembly/disassembly

– Hinges
– Doors
– Removable shelves

– Lock
– Welding
– Joints
– Connections
– Edge connectors

S3

Training

– Presence of people trained according to work type
– Operators training

S4

Personnel organization

– Amount of people per maintenance operation
– Active preventive maintenance time
– Logistic cost

S5

Environment

– Isolation
– Leak detection system
– Presence of high voltage cables

S6

Spare parts

Requirements concerning their storing and handling,
concerning tasks of maintenance level 1.

S7

Maintenance tools and
equipments

– Components and tools with weight and volume

that allow an easily use

– Standard components and tools

S8

Inter-departmental
co-ordination

– Possibility of performing simultaneous

maintenance tasks

– Permission to perform operations

S9

Documentation

– Appropriate manuals for maintenance and

procedures instructions

0: very difﬁcult access
1: Quite difﬁcult access
2: Difﬁcult access
3: Normal access
4: Very good access

0: Many difﬁculties
1: Quite a lot of difﬁculties
2: Some difﬁculties
3: Good manipulation
4: Very good manipulation

0: Very bad
1: Bad
2: Somewhat bad
3: Regular
4: Good

0: 5/6 people, no coordination
1: 4/5 people
2: 3/4 people
3: 2/3 people
4: 1 person

0: Very dangerous
1: Dangerous
2: Somewhat dangerous
3: Safety
4: Very safety

0: Many different spare parts in
stock and difﬁcult for handling
4: Few number of spare parts in
stock and very easy for handling

0: Many strange things
1: Many things
2: Quite a lot of things
3: Few things
4: Very few things

0: Very complicated
1: Complicated
2: A bit complicated
3: Regular
4: Very well organized

0: No documentation
1: Incomplete
2: Complete but difﬁcult
3: Regular
4: Very good

1

3

2

3

3

2

4

2

5

1

4

2

2

2

2

1

4

4

3

3

3

3

3

3

2

3

3

3

3

3

4

4

4

4

4

3

4

3

2

1

3

3

3

2

1

2

2

2

2

2

Maintainability indicators for
maintenance levels 1–5

2.89 3.11 2.67 2.56 2.11

the design improvement
regarding maintainability require-
ments or, simply, the maintenance improvement in a speciﬁc
item.

In order to describe the maintainability indicators, maintain-
ability attributes have been deﬁned and classiﬁed, ﬁrst of all,
according to its general and speciﬁc scope (in relation to the
maintenance level). Maintenance levels refer to the complexity of
the maintenance tasks, which are performed at an indenture
level. The attributes ranking is performed with a 0 to 4 scale, in
order to reduce subjectivity and to obtain reasonable values, easy
to be manipulated. Once deﬁned the maintenance level of the

item, each attribute is assessed, making a weighted average for
each maintenance level.

The method allows considering different importance factors
for each of the attributes, according to the characteristics of the
item or its operation. In such cases, the evaluator should also
assess that factor in order to estimate the weighted average.
Consequently, they are six measures obtained, one for the general
indicator and ﬁve for each maintenance level maintainability
indicator.

Results for each indicator can be presented in a table contain-
ing the assigned value for each attribute, the remarks of the

Author's personal copy

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

91

MAINTAINABILITY GENERAL INDICATOR

Simplicity

Relation with the manufacturer

Failure watch

4

3

2

1

0

Identification

Modularity

Standardization

Tribology

Ergonomics

General Attributes

Fig. 2. Graphical representation of general maintainability indicator.

MAINTAINABILITY INDICATOR
FOR MAINTENANCE LEVEL 1

MAINTAINABILITY INDICATOR
FOR MAINTENANCE LEVEL 2

Accesibility

4
3
2
1
0

Documentation

Inter-departamental
coordination

Maintenance tools and
equipments

Assembly / Disassembly

Documentation

Trainning

Personnel organisation

Inter-departamental
coordination

Maintenance tools and
equipments

Accesibility

4
3
2
1
0

Assembly / Disassembly

Trainning

Personnel organisation

Spare parts

Environment

Spare parts

Environment

Level 1 Attributes

Level 2 Attributes

MAINTAINABILITY INDICATOR
FOR MAINTENANCE LEVEL 3

MAINTAINABILITY INDICATOR
FOR MAINTENANCE LEVEL 4

Accesibility

4
3
2
1
0

Documentation

Inter-departamental
coordination

Maintenance tools and
equipments

Assembly / Disassembly

Documentation

Trainning

Inter-departamental
coordination

Personnel or ganisation

Maintenance tools and
equipments

Accesibility

4
3
2
1
0

Assembly / Disassembly

Trainning

Personnel organisation

Spare parts

Environment

Spare parts

Environment

Level 3 Attributes

Level 4 Attributes

MAINTAINABILITY INDICATOR
FOR MAINTENANCE LEVEL 5

Documentation

Inter-departamental
coordination

Maintenance tools and
equipments

Accesibility
4
3
2
1
0

Assembly / Disassembly

Trainning

Personnel organisation

Spare parts

Environment

Level 5 Attributes

Fig. 3. Graphical representation of maintainability indicators.

Author's personal copy

92

P. Moreu De Leon et al. / Reliability Engineering and System Safety 100 (2012) 84–92

Table 4
Poorly scored indicators from Maintenance Level 4.

Code

Attribute

Value

Comments

S1
S2
S7

S8

S9

Accesibility
Assembly/disassembly
Maintenance tools and
equipments
Inter-departmental co-ordination 2

2
2
2

Documentation

2

There is a difﬁcult access to the area where the maintenance tasks are carried out.
The manipulation of components and subcomponents presents some difﬁculties.
In order to proceed with the maintenance task, several tools and equipment are
needed.
Permission and coordination to perform operations and maintenance tasks are a bit
complicated
Technical manuals are complete but difﬁcult to deal with.

Table 5
Poorly scored indicators from Maintenance Level 5.

Code

Attribute

Value

Comments

S1

S2
S4
S7

S8

S9

Accesibility

1

Assembly/disassembly
Personnel organization
Maintenance tools and
equipments
Inter-departmental co-ordination 1

2
2
1

Documentation

2

There is a quite difﬁcult access to the area where the maintenance tasks are carried
out.
The manipulation of components and subcomponents presents some difﬁculties.
The maintenance task requires 3/4 people for its performance.
In order to proceed with the maintenance task, quite a lot of tools and equipment are
needed.
Permission and coordination to perform operations and maintenance tasks are really
complicated.
Technical manuals are complete but difﬁcult to deal with.

assessment staff and the value for the maintainability indicator.
It is also very useful to represent all these results in a graphical
way (radar-graphic), with the measurement for each level of
maintenance.

This simple process may help us to improve maintainability

along the different stages of an item life cycle.

Finally, the application of this method in a case study has
shown how important is, for instance, the training of the person
who performs the assessment. In fact, the indicator deﬁnition is
quite simple and applicable to any device. Nevertheless,
it
requires an adaptation and interpretation of attributes, as well
as those maintenance levels in agreement with each item
peculiarities.

Further research on this interesting ﬁeld can be addressed,
for instance, to the application of this practical method, not just
for industrial devices but also to products already released into
the market. In this context, the intervention of the after sales
department as well as the experience of the warranty technicians
will be crucial for the maintainability assessment. In addition to
this, and in a similar way to the concept of maintainability, it is
possible to redeﬁne that indicator to a certain speciﬁc warranty
case study.

References

[1] Barabadi A, Barabady J, Markeset T. Maintainability analysis considering time-
dependent and time-independent covariates. Reliability Engineering and
System Safety 2011;96:210–7.

[2] Guo Bo, Jiang Ping, Xing Yun-Yan. A censored sequential posterior odd test
(spot) method for veriﬁcation of the mean time to repair. IEEE Transactions on
Reliability 2008;57(2):243–7.

[3] CEN/TC 319. EN 13306:2010, Maintenance—maintenance terminology.

European standard, Bruxelles; 2010.

[4] Goulden Eldon C. An analytic approach to performing a maintainability
demonstration. IEEE Tansactions on Reliability 1990;39(1). (19–22, 25).
[5] Houshyar A, Ghahramani B. A practical reliability and maintainability data
collection and processing software. Computers & Industrial Engineering
1997;33(1–2):133–6.

[6] Liu R, Lv C, Zou Y, Zhou D. The preliminary study on the human-factor
evaluation system for maintainability design. In: Proceedings of the 2009
international conference on intelligent human–machine systems and cyber-
netics, IHMSC 2009, vol. 2, art. no. 5336031; 2009. p. 107–12.

[7] Lu Z, Sun YC. Maintainability virtual evaluation method based on fuzzy
multiple attribute decision making theory for civil aircraft system.
In:
Proceedings of the eighth international conference on reliability, maintain-
ability and safety, ICRMS 2009, art. no. 5270100; 2009. p. 684–9.

[8] UNE 20654:1992. Maintainability requirements. AENOR, Madrid; 1992.
[9] Wani MF, Gandhi OP. Maintainability design and evaluation of mechanical
systems based on tribology. Reliability Engineering and System Safety
2002;77(2):181–8.


