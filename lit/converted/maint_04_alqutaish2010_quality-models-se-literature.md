Journal of American Science                                                                                                                            2010; 6(3)

Quality Models in Software Engineering Literature:
An Analytical and Comparative Study

Rafa E. Al-Qutaish, PhD

Al Ain University of Science and Technology – Abu Dhabi Campus, PO Box: 112612, Abu Dhabi, UAE.
rafa@ieee.org

Abstract: The quality of the software is critical and essential in different types of organizations. In some types of
software, poor quality of the software product in sensitive systems (such as: real-time systems, control systems, etc.)
may  lead  to  loss  of  human  life,  permanent  injury,  mission  failure,  or  financial  loss.  In  software  engineering
literature, there are a number of quality models in which they contain a number of quality characteristics (or factors,
as called in some models). These quality characteristics could be used to reflect the quality of the software product
from  the  view  of  that  characteristic.  Selecting  which  one  of  the  quality  models  to  use  is  a  real  challenge.  In  this
paper,  we  will  discuss  the  contents  of  the  following  quality  models:  McCall’s  quality  model,  Boehm’s  quality
model, Dromey's quality model, FURPS quality model and ISO 9126 quality model. In addition, we will focus on a
comparison between these quality models, and find the key differences between them. [Journal of American Science
2010; 6(3):166-175]. (ISSN: 1545-1003).

Keywords: Software Quality; Quality Models; Quality Engineering; ISO 9126; McCall’s Quality Model; Boehm’s
Quality Model; Dromey's Quality Model; FURPS Quality Model

1. Introduction

is

critical

Software

in  providing

a
competitive  edge  to  many  organizations,  and  is
progressively becoming a key component of business
systems,  products  and  services.  The  quality  of
software  products  is  now  considered  to  be  an
essential  element  in  business  success  [Veenendaal
and  McMullan,  1997].  Furthermore,  the  quality  of
software product is very important and essential since
for  example  in  some  sensitive  systems  –  such  as,
real-time  systems,  control  systems,  etc.  –  the  poor
quality  may  lead  to  financial  loss,  mission  failure,
permanent injury or even loss of human life.

There  are  several  definitions  for  “software
Quality” term, for examples, it is defined by the IEEE
[1990]  as  the  degree  to  which  a  system,  component
or  process  meets  specified
requirements  and
customer  (user)  needs  (expectations).  Pressman
[2004] defines it as “conformance to explicitly stated
functional  and  performance  requirements,  explicitly
documented  development  standards,  and  implicit
characteristics that are expected of  all  professionally
developed  software.”  The  ISO,  by  contrast,  defines
“quality” in ISO 14598-1 [ISO, 1999] as “the totality
of  characteristics  of  an  entity  that  bear  on  its  ability
to  satisfy  stated  and  implied  needs,”  and  Petrasch
[1999]  defines  it  as  “the  existence  of  characteristics
of a product which can be assigned to requirements.”
There  are  a  number  of  quality  models  in
software  engineering  literature,  each  one  of  these
quality  models  consists  of  a  number  of  quality
characteristics (or factors, as called in some models).
These quality characteristics could be used to reflect

the quality  of the software product from the view of
that characteristic. Selecting which one of the quality
models  to  use  is  a  real  challenge.  In  this  paper,  we
will  discuss  the  contents  of  the  following  quality
models:
1.  McCall’s Quality Model.
2.  Boehm’s Quality Model.
3.  Dromey's Quality Model.
4.  FURPS Quality Model.
5.  ISO 9126 Quality Model.

In  addition,  we  will  focus  on  a  comparison
between  these  quality  models,  and  find  the  key
differences between them.

quality  models

The  rest  of  this  paper  is  structured  as
follows:  Section  2  presents  an  overview  of  the  five
common
software
engineering.  Section  3  contains  a  detailed  analysis
and  comparison  between  the  five  quality  models.
Finally,  Section  4  concludes  the  paper  with  some
comments.

used

in

2. An Overview of the Software Quality Models

2.1 McCall’s Quality Model
McCall’s

is  one  of

known  as
1977)
models
literature.
McCall
originates
primarily
developers

the

Model

Quality

software

(also
the  General  Electrics  Model  of
the  most  known  quality
engineering
Jim
model
is
system
development

This
the  US  military
the

aimed
and

presented

has
al.

towards

[1977].

system

in
It
et
from

been

and

the

by

http://www.americanscience.org

166

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

et

al,  1977].  Using
to  bridge
and  developers  by

process
[McCall
model,  McCall  attempts
between  users
on
that
developers’ priorities [McCall et al, 1977].

software  quality
the  users’  views  and

a  number  of
reflect  both

this
the  gap
focusing
factors
the

The structure of the McCall’s quality model
consists of three major perspectives (types of quality

characteristics)  for  defining  and  identifying  the
quality of a software product, and each of these major
perspectives  consists  of  a  number  of  quality  factors.
Each  of  these  quality  factors  has  a  set  of  quality
criteria,  and  each  quality  criteria  could  be  reflected
by one or more metrics, see Figure 1 for the details of
the McCall’s quality model structure. The contents of
the three major perspectives are the following:

McCall’s Quality Model

Major Perspective 1

Major Perspective 2

Major Perspective 3

Quality Factor 1

Quality Factor 2

.  .  .

Quality Factor N

Quality Criteria 1

Quality Criteria 2

.  .  .

Quality Criteria M

Metric 1

Metric 2

.  .  .

Metric L

Figure 1. The structure of McCall’s quality model

1.  Product  Revision:  it  is  about  the  ability  of  the

product to undergo changes, and it includes:
a.  Maintainability:  the  effort  required  to  locate
and  fix  a  fault  in  the  program  within  its
operating environment.

b.  Flexibility:

the  ease  of  making  changes
the  operating

in

required  by  changes
environment.

c.  Testability: the ease of testing the program, to
ensure  that  it  is  error-free  and  meets  its
specification.

2.  Product Operations: it is about the characteristics
of  the  product  operation.  The  quality  of  the
product operations depends on:
a.  Correctness:  the  extent  to  which  a  program

fulfils its specification.

b.  Reliability: the system ability not to fail.
categorized
c.  Efficiency:

into
execution  efficiency  and  storage  efficiency
and  generally  meaning  the  use  of  resources,
e.g. processor time, storage.

further

it

d.  Integrity:  the  protection  of  the  program  from

unauthorized access.

e.  Usability: the ease of the use of the software.

3.  Product Transition:  it is about  the adaptability of
the product to new environments. It is all about:
a.  Portability:  the  effort  required  to  transfer  a
program from one environment to another.
b.  Reusability:  the  ease  of  reusing  software  in  a

different context.

c.  Interoperability:  the  effort  required  to  couple

the system to another system.

In  more  details,  McCall’s  Quality  Model
consists of 11 quality factors to describe the external
view  of  the  software  (from  the  users’  view),  23
quality  criteria  to  describe  the  internal  view  of  the
software  (from  the  developer’s  view)  and  a  set  of
Metrics which are defined and used to provide a scale
and method for measurement. Table 1 presents two of
the three major perspectives  and  their  corresponding
quality factors and quality criteria.

The main objective of the McCall’s Quality
Model  is  that  the  quality  factors  structure  should
software  quality  picture
provide  a  complete
[Kitchenham,  1996].  The  actual  quality  metric  is
computed  by  answering  “yes”  and  “no”  questions.
However,  if  answering  equally  amount  of  “yes”  and

http://www.americanscience.org

167

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

“no”  on  the  questions  measuring  a  quality  criteria,
then you will achieve 50% on that quality criteria.

Table 1.  The contents of McCall’s quality model -
product revision and product operations

Major
Perspectives

Quality
Factors

Quality
Criteria

Product
revision

Maintainability  Simplicity

Conciseness

Self-descriptiveness

Modularity

 Flexibility

Self-descriptiveness

Expandability

Generality

 Testability

Simplicity

Instrumentation

Self-descriptiveness

Modularity

Product
operations

 Correctness

Traceability

Completeness

Consistency

 Efficiency

Execution efficiency

Storage efficiency

 Reliability

Consistency

Accuracy

Error tolerance

 Integrity

Access control

Access audit

characteristics which contribute to the overall quality
level (see Figure 2).

In  this  model,  the  high-level  characteristics
represent basic high-level requirements  of actual use
to which evaluation of software quality could be put.
In its high-level, there are three characteristics, that is
[Boehm et al, 1976, Boehm et al, 1978]:
1.  As-is utility: to address how well, easily, reliably
and efficiently can I use the software product as-
is?

2.  Maintainability:  to  address  how  easy  is  it  to
the  software

understand,  modify  and  retest
product?

3.  Portability:  to  address  if  can  I  still  use  the
software product when the environment has been
changed?

in

the

three

Table 2 shows the  contents  of  the  Boehm’s
quality  model
levels,  high-level,
intermediate-level and lowest-level characteristics. In
addition,  it  is  noted  that  there  is  a  number  of  the
lowest-level  characteristics  which  can  be  related  to
more  than  one  intermediate-level  characteristics,  for
example,
‘Self  Contentedness’  primitive
characteristic could be related to the ‘reliability’ and
‘portability’ primitive characteristics.

the

In the intermediate level characteristic, there
are  seven  quality  characteristics
together
represent  the  qualities  expected  from  a  software
system [Boehm et al, 1976, Boehm et al, 1978]:
1.  Portability:  the  software  can  be  operated  easily
and  well  on  computer  configurations  other  than
its current one.

that

2.  Reliability:  the  software  can  be  expected  to

perform its intended functions satisfactorily.

3.  Efficiency:

the  software  fulfills

its  purpose

without waste of resources.

4.  Usability:  the  software  is  reliable,  efficient  and

human-engineered.
the

5.  Testability:

the
software
establishment of verification criteria and supports
evaluation of its performance.

facilitates

 Usability

Operability

6.  Understandability: the software purpose is clear to

Training

Communicativeness

2.2 Boehm’s Quality Model

Boehm  [1976,  1978]  introduced  his  quality
model  to  automatically  and  quantitatively  evaluate
the  quality  of  software.  This  model  attempts  to
qualitatively  define  the  quality  of  software  by  a
predefined set of attributes and metrics. It consists of
intermediate-level
high-level
(primitive)
characteristics

characteristics,

lowest-level

and

the inspector.

7.  Flexibility:

the

the
software
incorporation  of  changes,  once  the  nature  of  the
desired change has been determined.

facilitates

The primitive characteristics can be  used to
provide  the  foundation  for  defining  quality  metrics,
this use is one of the most important goals established
by  Boehm  when  he  constructed  his  quality  model.
One or more metrics are supposed to measure a given
primitive  characteristic.  Boehm  [1978]  defined  the
‘metric’ as “a measure of extent or degree to which a
product  possesses  and  exhibits  a  certain  (quality)
characteristic.”

http://www.americanscience.org

168

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

Boehm’s Quality Model

High-Level Characteristic 1

High-Level Characteristic 2

High-Level Characteristic 3

Intermediate-Level
Characteristic 1

Intermediate-Level
Characteristic 2

    .  .  .

Intermediate-Level
Characteristic N

Lowest-Level
Characteristic 1

Lowest-Level
Characteristic 2

.  .  .

Lowest-Level
Characteristic M

Metric 1

Metric 2

.  .  .

Metric L

Figure 2. The structure of Boehm’s quality model

Table 2. The contents of Boehm’s quality model

High-Level Characteristics

Intermediate-Level Characteristics

Primitive Characteristics

As-is Utility

  Reliability

  Efficiency

  Human
  Engineering

  Portability

Maintainability

  Testability

  Understandability

  Modifiability

Self Containedness
Accuracy
Completeness
Robustness/Integrity
Consistency
Accountability
Device Efficiency
Accessibility
Robustness/Integrity
Accessibility
Communicativeness
Device Independence
Self Containedness
Accountability
Communicativeness
Self Descriptiveness
Structuredness
Consistency
Structuredness
Conciseness
Legibility
Structuredness
Augmentability

3
High-Level
Characteristics

7
Intermediate-Level
Characteristics

15
Distinct Primitive
Characteristics

http://www.americanscience.org

169

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

2.3 Dromey’s Quality Model

This  quality  model  has  been  presented  by
Dromey  [1995,  1996].  It  is  a  product  based  quality
model  that  recognizes  that  quality  evaluation  differs
for  each  product  and  that  a  more  dynamic  idea  for
modeling the process is needed to be wide enough to

systems

for  different

apply
[Dromey,  195].
Furthermore,  Figure  3  shows  that  it  consists  of  four
software  product  properties  and  for  each  property
there  is  a  number  of  quality  attributes.  In  addition,
figure  4  shows  the  contents  of  the  Dromey's  quality
model.

Dromey’s Quality Model

Software Product

Product Property 1

Product Property 2

.  .  .

Product Property 4

Quality Attribute 1

Quality Attribute 2

Quality Attribute N

.  .  .

Figure 3. The structure of Dromey’s quality model

Implementation

Correctness

Internal

Contextual

Descriptive

Functionality

Maintainability

Maintainability

Maintainability

Reliability

Efficiency

Reusability

Efficiency

Reliability

Portability

Reliability

Reliability

Usability

Figure 4. The contents of Dromey’s quality model

2.4 FURPS Quality Model

The  FURPS  model  originally  presented  by
Robert  Grady[1992],  then  it  has  been  extended  by
IBM  Rational  Software  [Jacobson  et  al,  1999,
the  ‘+’
Kruchten,  2000]
indicates  such  requirements  as  design  constraints,
implementation  requirements,  interface  requirements
and physical requirements [Jacobson et al, 1999].

into  FURPS+,  where

In this quality model, the FURPS stands for
[Grady,  1992]  -  as  in  Figure  5  -  the  following  five
characteristics:
1.  Functionality:

feature  sets,

include

it  may
capabilities, and security.

2.  Usability:

it  may

factors,
aesthetics,  consistency  in  the  user  interface,
online  and  context  sensitive  help,  wizards  and

include  human

http://www.americanscience.org

170

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

agents,  user  documentation,
materials.

and

training

3.  Reliability: it may include frequency and severity
of failure, recoverability, predictability, accuracy,
and mean time between failures (MTBF).

4.  Performance: it imposes conditions on functional
efficiency,
as
requirements
availability,  accuracy,  throughput,  response  time,
recovery time, and resource usage.

speed,

such

5.  Supportability:
it  may
extensibility,
adaptability,
configurability,
compatibility,
installability, and localizability.

include

testability,
maintainability,
serviceability,

Supportability

Functionality

Performance

 FURPS

Usability

Reliability

Figure 5. The contents of FURPS quality model

2.5 ISO 9126 Quality Model
In  1991,

first
international  consensus  on  the  terminology  for  the

ISO  published

the

its

for

software

characteristics

quality
product
evaluation;  this  standard  was  called  as  Software
Product  Evaluation  -  Quality  Characteristics  and
Guidelines  for  Their  Use  (ISO  9126)  [ISO,  1991].
From  2001 to  2004, the  ISO published  an  expanded
version, containing both the ISO quality models and
inventories  of  proposed  measures  for  these  models.
The  current  version  of  the  ISO  9126  series  now
consists of  one  International Standard  (IS)  and  three
Technical Reports (TRs):
1.  ISO IS 9126-1: Quality Model [ISO, 2001].
2.  ISO TR 9126-2: External Metrics [ISO, 2003].
3.  ISO TR 9126-3: Internal Metrics [ISO, 2003].
4.  ISO  TR  9126-4:  Quality  in  Use  Metrics  [ISO,

2004].

The first document of the ISO 9126 series –
Quality Model – contains two-parts quality model for
software product quality [ISO, 2001]:
1.  Internal and external quality model.
2.  Quality in use model.

The first part of the two-parts quality model
determines  six  characteristics  in  which  they  are
subdivided  into  twenty-seven  sub-characteristics  for
internal  and  external  quality,  as  in  Figure  6  [ISO,
2001].  These  sub-characteristics  are  a  result  of
internal  software  attributes  and  are  noticeable
externally  when  the  software  is  used  as  a  part  of  a
computer  system.  The  second  part  of  the  two-part
model indicates four quality in use characteristics, as
in Figure 7 [ISO, 2001].

External and Internal Quality

Functionality

   Reliability

  Usability

   Efficiency

Maintainability

Portability

 - Suitability
 - Accuracy
 - Interoperability
 - Security
 - Functionality
   Compliance

 - Maturity
 - Fault Tolerance
 - Recoverability
 - Reliability
   Compliance

 - Understandability
 - Learnability
 - Operability
 - Attractiveness
 - Usability

Compliance

 - Time

Behavior
 - Resource
Utilization
 - Efficiency
Compliance

 - Analyzability
 - Changeability
 - Stability
 - Testability
 - Maintainability
Compliance

 - Adaptability
 - Installability
 - Co-existence
 - Replaceability
 - Portability
Compliance

Figure 6. ISO 9126 quality model for external and internal quality (characteristics/sub-characteristics) [ISO, 2001]

Quality in use

Effectiveness

Productivity

Safety

Satisfaction

Figure 7. ISO 9126 quality model for quality in use (characteristics) [ISO, 2001]

http://www.americanscience.org

171

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

Figure 8 shows the ISO view of the expected
relationships  between  internal,  external,  and  quality
in  use  attributes.  The  internal  quality  attributes
influence on the  external  quality  attributes  while  the
external  attributes  influences  on  the  quality  in  use
attributes. Furthermore, the quality in use depends on

the  external  quality  while
depends on the internal quality [ISO, 2001].

the  external  quality

the

For

internal  and  external  software
products,  each  quality  characteristics  and
its
corresponding  sub-characteristics  are  defined  in  ISO
9126-1 [ISO, 2001] as follows:

Process

        influences

Process
Quality

Software Product

Effect of Software Product

        influences

      influences

Internal
Quality
 Attributes

External
Quality
   Attributes

Quality in
use
   Attributes

      depends on

    depends on

  depends on

Context of use

Process Measures

  Internal Measures

External Measures  Quality in use Measures

Figure 8. Quality in the lifecycle [ISO, 2001]

1.  Functionality:  “the  capability  of  the  software
product  to  provide  functions  which  meet  stated
and  implied  needs  when  the  software  is  used
under  specified  conditions”.  It  contains
the
following sub-characteristics:
a.  Suitability:  “the  capability  of  the  software
product  to  provide  an  appropriate  set  of
functions
tasks  and  user
objectives”.

specified

for

b.  Accuracy:  “the  capability  of  the  software
product  to  provide  the  right  or  agreed  results
or  effects  with
the  needed  degree  of
precision”.

c.  Security:  “the  capability  of  the  software
product to protect information and data so that
unauthorised  persons  or  systems  cannot  read
or  modify  them  and  authorised  persons  or
systems are not denied access to them”.

d.  Interoperability:

the
software product to interact with one or more
specified systems”.

capability  of

“the

e.  Functionality  Compliance:  “the  capability  of
the  software  product  to  adhere  to  standards,
conventions or regulations in laws and similar
prescriptions relating to functionality”.

2.  Reliability:  “The  capability  of

the  software
level  of
specified
following  sub-

to  maintain  a  specified
under

product
performance  when
conditions”.
It
characteristics:
a.  Maturity:  “the  capability  of  the  software
product to avoid failure as a result of faults in

includes

used

the

the software”.

b.  Fault tolerance: “the capability of the software
product  to  maintain  a  specified  level  of
performance  in  cases  of  software  faults  or  of
infringement of its specified interface”.

c.  Recoverability: “the capability of the software
product  to  re-establish  a  specified  level  of
performance  and  recover  the  data  directly
affected in the case of a failure”.

d.  Reliability  Compliance:  “the capability  of the
software  product  to  adhere  to  standards,
conventions  or
to
reliability”.

regulations

relating

3.  Usability: “the capability of the software product
to  be  understood,  learned,  used,  and  attractive  to
the  user,  when  used  under  specified  conditions”.
It contains the following sub-characteristics:
a.  Understandability:  “the  capability  of

the
to
software  product
understand  whether  the  software  is  suitable,
and how it can be used for particular tasks and
conditions of use”.

to  enable

the  user

b.  Learnability:  “the  capability  of  the  software
to  learn  its

product  to  enable  the  user
application”.

c.  Operability:  “the  capability  of  the  software
product  to  enable  the  user  to  operate  and
control it”.

d.  Attractiveness: “the capability of the software

product to be attractive to the user”.

e.  Usability  Compliance:  “the  capability  of  the
software  product  to  adhere  to  standards,

http://www.americanscience.org

172

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

conventions,  style  guides  or
relating to usability”.

regulations

environment”.

includes

4.  Efficiency: “the capability of the software product
to  provide  appropriate  performance,  relative  to
the  amount  of  resources  used,  under  stated
conditions”.
following  sub-
It
characteristics:
a.  Time  behaviour:  “the  capability  of

the
software  product
to  provide  appropriate
response and processing times and throughput
rates  when  performing  its  function,  under
stated conditions”.

the

b.  Resource  behaviour:  “the  capability  of  the
software  product  to  use  appropriate  amounts
and  types  of  resources  when  the  software
performs its function under stated conditions”.
c.  Efficiency  Compliance:  “the capability  of  the
software  product  to  adhere  to  standards  or
conventions relating to efficiency”.

5.  Maintainability:  “the  capability  of  the  software
product  to  be  modified.    Modifications  may
include  corrections,  improvements  or  adaptation
of the software to changes in environment, and in
requirements  and  functional  specifications”.  It
contains the following sub-characteristics:
a.  Analyzability:  “the  capability  of  the  software
product  to  be  diagnosed  for  deficiencies  or
causes  of  failures  in  the  software,  or  for  the
parts to be modified to be identified”.

b.  Changeability:  “the  capability  of  the  software
product  to  enable  a  specified  modification  to
be implemented”.

c.  Stability:  “the  capability  of  the  software
product  to  avoid  unexpected  effects  from
modifications of the software”.

d.  Testability:  “the  capability  of  the  software
product  to  enable  modified  software  to  be
validated”.

e.  Maintainability Compliance: “the capability of
the software product to adhere to standards or
conventions relating to maintainability”.
6.  Portability: “the capability of the software product
to
to  be  transferred  from  one  environment
another”.
sub-
characteristics:
a.  Adaptability:  “the  capability  of  the  software
product  to  be  adapted  for  different  specified
environments  without  applying  actions  or
means  other  than  those  provided  for  this
purpose for the software considered”.

following

includes

the

It

b.  Installability:  “the  capability  of  the  software
in  a  specified

installed

product

to  be

c.  Co-existence:  “the  capability  of  the  software
product  to  co-exist  with  other  independent
software  in  a  common  environment  sharing
common resources”.

d.  Replaceability: “the capability of the software
product  to  be  used  in  place  of  another
specified  software  product  for
the  same
purpose in the same environment”.

e.  Portability  Compliance:  “the capability  of the
software  product  to  adhere  to  standards  or
conventions relating to portability”.

3. Analysis of the Quality Models

(i.e.

In  this  section,  a  comparison  between  the
availability  of  the  characteristics  (called  factors  or
attributes  in  some  quality  models)  within  the  five
quality  models  will  be  presented.  Table  3  presents
this comparison, at the end this table you will find the
number of the corresponding characteristics for each
quality model.
From

the  17  characteristics,  only  one
characteristic  is  common  to  all  quality  models,  that
is,  the  ‘reliability’.  Also,  there  are  only  three
‘usability’  and
characteristics
‘portability’)  which  are  belonging  to  four  quality
models.  Two  characteristic  is  common  only  to  three
quality  models,  that  is,  the  ‘functionality’  and
‘maintainability’  characteristics.  Two  characteristic
belong to two quality models, that is, the ‘testability’
and
nine
characteristics
‘correctness’,
‘integrity’  and  ‘interoperability’  in  McCall’s  quality
model; ‘human engineering’, ‘understandability’ and
‘modifiability’
quality  model;
‘performance’ and ‘supportability’ in FURPS quality
model) are defined in only one quality model.

characteristics.  And,

in  Boehm’s

‘efficiency’,

‘reusability’

‘flexibility’,

(i.e.

Furthermore,

it  can  be  noted

that  the
‘testability’, ‘interoperability’ and ‘understandability’
are  used  as  factors/attributes/characteristics  in  some
quality  models.  However,  in  ISO  9126-1,  these
factors/attributes/characteristics  are  defined  as  sub-
characteristics.  More  specifically,  the  ‘testability’  is
belonging  to  the  ‘maintainability’  characteristic,  the
‘understandability’  is  belonging  to  the  ‘usability’
characteristic,  and  the  ‘interoperability’  is  belonging
to the ‘functionality’ characteristic.

From  our  point  of  view,  the  ISO  9126-1
quality model is the most useful one since it has been
built  based  on  an
international  consensus  and
agreement  from  all  the  country  members  of  the  ISO
organization.

http://www.americanscience.org

173

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

Table 3. A comparison between the five quality models

Factors/Attributes/Characteristics

McCall

Boehm

Dromey

FURPS

ISO 9126

Maintainability

Flexibility

Testability

Correctness

Efficiency

Reliability

Integrity

Usability

Portability

Reusability

Interoperability

Human Engineering

Understandability

Modifiability

Functionality

Performance

Supportability

(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)
(cid:1)

(cid:1)

(cid:1)
(cid:1)

(cid:1)

(cid:1)
(cid:1)
(cid:1)

(cid:1)

(cid:1)
(cid:1)

(cid:1)
(cid:1)
(cid:1)

(cid:1)

17

11

7

7

(cid:1)

(cid:1)
(cid:1)

(cid:1)
(cid:1)

(cid:1)

6

(cid:1)

(cid:1)

(cid:1)
(cid:1)
(cid:1)

5

4. Discussion

There  are  a  number  of  quality  models  in
software  engineering  literature,  each  one  of  these
quality  models  consists  of  a  number  of  quality
characteristics (or factors, as called in some models).
These quality characteristics could be used to reflect
the quality  of the software product from the view of
that characteristic. Selecting which one of the quality
models  to  use  is  a  real  challenge.  In  this  paper,  we
have  discussed  and  compared  the  following  quality
models:
1.  McCall’s Quality Mode.
2.  Boehm’s Quality Model.
3.  Dromey's Quality Model.
4.  FURPS Quality Model.
5.  ISO 9126 Quality Model.

Based  on  the  discussion  of  the  five  quality
models  and  on  the  comparison  between  them,  the
following comments could be written:
1.  In  McCall’s  quality  model,

is
subjectively  measured  based  on  the  judgment  on
the  person(s)  answering  the  questions  (‘yes’  or

the  quality

‘no’ questions).

2.  Three  of  the  characteristics  are  used  in  the  ISO
9126-1  quality  model  as  sub-characteristics  from
other characteristics.

3.  The  FURPS  quality  model  is  built  and  extended
to  be  used
the  IBM  Rational  Software
Company.  Therefore,  it  is  a  special-purpose
quality  model,  that  is,  for  the  benefits  of  that
company.

in

4.  The  metrics  in  the  lower  level  of  the  McCall’s,
Boehm’s, Doromey’s and FURPS quality models
are  neither  clearly  nor  completely  defined  and
connected  to  the  upper  level  of  the  quality
models. For example, in McCall’s quality model,
the  metrics  should  be  clearly  and  completely
defined  and  connected  to  the  corresponding
quality criteria, see Figure 1.

The  ISO  9126-1  quality  model  is  the  most
useful  one  since  it  has  been  build  based  on  an
international  consensus  and  agreement  from  all  the
country members of the ISO organization.

http://www.americanscience.org

174

           editor@americanscience.org

Journal of American Science                                                                                                                            2010; 6(3)

Corresponding Author:
Dr. Rafa E. Al-Qutaish
Al Ain University of Science and Technology – Abu
Dhabi Campus, P.O. Box: 112612, Abu Dhabi, UAE.
E-mail: rafa@ieee.org

References
1.  Boehm, B. W., Brown, J. R., Kaspar, H., Lipow,
M.,  McLeod,  G.,  Merritt,  M.  Characteristics  of
Software  Quality.  North  Holland  Publishing,
Amsterdam, The Netherlands, 1978.

2.  Boehm,  B.  W.,  Brown,  J.  R.,  Lipow,  M.
Quantitative  evaluation  of  software  quality.  In
Proceedings  of  the  2nd  international  conference
on  Software  engineering,
IEEE  Computer
Society,  Los  Alamitos  (CA),  USA,  1976;  592-
605.

3.  Dromey,  R.  G.  A  model  for  software  product
IEEE  Transactions  on  Software

quality.
Engineering, 1995; 21:146-162.
4.  Dromey,  R.  G.  Concerning

the  Chimera
[software quality].  IEEE Software,  1996; 13:33-
43.

7.

6.

5.  Grady,  R.  B.  Practical  Software  Metrics  for
Project  Management  and  Process  Improvement.
Prentice Hall, Englewood Cliffs, NJ, USA, 1992.
IEEE.  IEEE  Std.  610.12:  Standard  Glossary  of
Software  Engineering  Terminology.  The
Institute of Electrical and Electronics Engineers,
New York, NY, USA, 1990.
ISO.
Evaluation
Guidelines
Organization
Switzerland, 1991.
ISO/IEC  14598-1:  Software  product
ISO.
evaluation
-  Part  1:  General  overview.
International  Organization  for  Standardization,
Geneva, Switzerland, 1999.

IS  9126:  Software  Product
and
International
for  Standardization,  Geneva,

-  Quality  Characteristics
for

their  Use.

ISO/IEC

8.

9.

ISO.  ISO/IEC  9126-1:  Software  Engineering  -
Product  Quality  -  Part  1:  Quality  Model.
International  Organization  for  Standardization,
Geneva, Switzerland, 2001.

10.  ISO. ISO/IEC TR 9126-2: Software Engineering
-  Product  Quality  -  Part  2:  External  Metrics.
International  Organization  for  Standardization,
Geneva, Switzerland, 2003.

11.  ISO. ISO/IEC TR 9126-3: Software Engineering
-  Product  Quality  -  Part  3:  Internal  Metrics,
International  Organization  for  Standardization,
Geneva, Switzerland, 2003.

12.  ISO. ISO/IEC TR 9126-4: Software Engineering
-  Product  Quality  -  Part  4:  Quality  in  Use
Metrics.
for
Switzerland.
Standardization,
Switzerland, 2004.

International  Organization
Geneva,

13.  Jacobson,  I.,  Booch,  G.,  Rumbaugh,  J.  The
Unified Software Development Process. Addison
Wesley, 1999.

14.  Kitchenham,  B.,  Pfleeger,  S.  L.  Software
Quality:  the  Elusive  Target.  IEEE  Software,
1996; 13: 12-21.

15.  Kruchten,  P.  The  Rational  Unified  Process:  An

Introduction. Addison Wesley, 2000.

16.  McCall,  J.  A.,  Richards,  P.  K.,  Walters,  G.  F.
Factors  in  Software  Quality,  Volumes  I,  II,  and
III.  US  Rome  Air  Development  Center  Reports,
US Department of Commerce, USA, 1977.
17.  Pressman,  R.  S.  Software  Engineering:  A
Practitioner’s  Approach.  McGraw-Hill,  New
York, NY, USA, 2004.

18.  Petrasch, R. The Definition of Software Quality:
A Practical Approach. In Proceedings of the 10th
International Symposium on Software Reliability
Engineering, 1999; 33-34.

19.  Veenendaal,  E.  V.,  McMullan,  J.  Achieving
Software  Product  Quality,  Den  Bosch,  UTN
Publishers, Amsterdam, The Netherlands, 1997.

Submitted on 12/9/2009

http://www.americanscience.org

175

           editor@americanscience.org


