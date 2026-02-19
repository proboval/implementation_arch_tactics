ACM SIGSOFT

SOFTWARE ENGINEERING  NOTES vol 17 no 4

Oct 1992 Page 40

F o u n d a t i o n s   for  t h e   S t u d y   of  Software  A r c h i t e c t u r e

Dewayne E.  Perry

Alexander  L. Wolf

AT&T Bell Laboratories
600  Mountain  Avenue
Murray Hill, New Jersey 07974
dep@research.att.com

Department  of Computer  Science
University of Colorado
Boulder,  Colorado 80309
alw@cs.colorado.edu

(~) 1989,1991,1992  Dewayne  E.  Perry and  Alexander  L.  Wolf

A B S T R A C T

The  purpose  of this  paper  is  to  build  the  foundation
for software  architecture.  We  first  develop  an  intuition
for  software  architecture  by  appealing  to  several  well-
established  architectural  disciplines.  On  the  basis  of
this  intuition,  we  present  a  model  of software  architec-
ture  that  consists  of three  components:  elements,  form,
and  rationale.  Elements  are  either  processing,  data,  or
connecting  elements.  Form  is  defined  in  terms  of  the
properties of, and the  relationships  among, the  elements
- -   that  is,  the  constraints  on  the  elements.  The  ratio-
nale provides the underlying basis for the  architecture in
terms of the  system constraints,  which most often derive
from  the  system  :requirements.  We  discuss  the  compo-
nents  of the  model  in  the  context  of both  architectures
and  architectural  styles  and  present  an  extended  exam-
ple  to  illustrate  some  important  architecture  and  style
considerations.  We  conclude  by  presenting  some  of the
benefits  of our  approach  to  software  architecture,  sum-
marizing  our  contributions,  and  relating  our  approach
to  other  current  work.

1

I n t r o d u c t i o n

Software design received  a  great  deal  of attention  by
researchers  in the  1970s.  This research  arose in response
to  the  unique  problems  of  developing  large-scale  soft-
ware  systems  first  recognized  in  the  1960s  5.
The
premise  of  the  research  was  that  design  is  an  activity
separate  from  implementation,  requiring  special  nota-
tions,  techniques:,  and  tools  3,  9,  17.  The  results  of
this  software design  research  has now begun  to make in-
roads  into  the  marketplace  as  computer-aided  software
engineering  (CASE)  tools  7.

In  the  1980s,  the  focus  of  software  engineering  re-
search moved away from software design specifically and

more toward  integrating  designs  and  the  design  process
into  the  broader  context  of  the  software  process  and
its  management.  One  result of this  integration was  that
many of the notations and techniques developed for soft-
ware design  have been  absorbed  by implementation lan-
guages.  Consider,  for example,  the  concept  of support-
ing  "programmming-in-the-large".  This  integration  has
tended  to  blur,  if not  confuse,  the  distinction  between
design  and  implementation.

The  1980s  also  saw  great  advances  in  our  ability  to
describe  and  analyze software systems.  We refer here to
such  things  as formal descriptive techniques  and  sophis-
ticated  notions  of typing  that  enable  us  to  reason  more
effectively about  software systems.  For example,  we  are
able  to reason  about  "consistency"  and  "inconsistency"
more  effectively  and  we  are  able  to  talk  about  "type
conformance" 1 rather  than  just  "type equivalence".

The  1990s,  we  believe,  will  be  the  decade  of software
architecture.  We  use  the  term  "architecture",  in  con-
trast  to  "design",  to  evoke  notions  of  codification,  of
abstraction,  of  standards,  of  formal  training  (of  soft-
ware  architects),  and  of  style.  While  there  has  been
some  work  in  defining  particular  software  architectures
(e.g.,  19,  22),  and  even  some  work  in  developing  gen-
eral  support  for  the  process  of developing architectures
it is time to reexamine the role of ar-
(notably SARA 8),
chitecture in  the  broader  context of the  software 15rocess
and software process  management,  as well as to  marshal
the  various  new  techniques  that  have  been  developed.

Some of the  benefits  we expect to gain from the  emer-
gence  of software architecture  as  a  major  discipline  are:
1)  architecture  as  the  framework for satisfying  require-
ments;  2)  architecture  as  the  technical  basis  for  design

1 Conformance  is  used  to  describe  the  relationship  between

types and subtypes.

A C M   SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol  17  no 4

Oct  1992  Page 41

and  as the  managerial basis  for cost estimation and  pro-
cess  managment;  3)  architecture  as  an effective basis for
reuse;  and  4)  architecture  as  the  basis  for  dependency
and  consistency  analysis.

Thus,  the  primary  object  of our  research  is  support
for  the  development  and  use  of  software  architecture
specifications.  This  paper  is  intended  to build  the  foun-
dation  for future  research  in  software  architecture.  We
begin  in  Section  2  by  developing  an  intuition  about
software  architecture  against  the  background  of  well-
established  disciplines  such  as  hardware,  network,  and
building  architecture,  establish  the  context  of software
architecture,  and  provide  the  motivation  for  our  ap-
proach.  In  Section  3,  we  propose  a  model  for,  and  a
characterization  of,  software  architecture  and  software
architectural  styles.  Next,  in Section  4,  we  discuss  an
easily  understood  example  to  elicit  some  important  as-
pects  of software  architecture  and  to  delineate  require-
ments for a software-architecture notation.  In Section 5,
we  elaborate  on  two  of  the  major  benefits  of  our  ap-
proach  to  software  architecture.  We  conclude,  in  Sec-
tion  6,  by  summarizing  the  major  points  made  in  this
paper  and  considering  related  work.

2

I n t u i t i o n ,

C o n t e x t ,

a n d   M o t i v a t i o n

Before presenting  our  model of software architecture,
we lay the  philosophical foundations for it  by:  1)  devel-
oping  an  intuition  about  software  architecture  through
analogies  to  existing  disciplines;  2)  proposing  a  con-
text  for  software  architecture  in  a  multi-level  product
paradigm;  and  3)  providing  some  motivation  for  soft-
ware  architecture  as  a  separate  discipline.

2 . 1

D e v e l o p i n g
w a r e   A r c h i t e c t u r e

a n   I n t u i t i o n

a b o u t   S o f t -

It  is  interesting  to  note  that  we  do  not  have  named
software  architectures.  We  have  some  intuition  that
there  are  different  kinds  of software  architectures,  but
we  have not  formalized, or institutionalized,  them.  It  is
our  claim that  it  is  because  there  are  so  many  software
architectures,  not  because  there  are  so  few,  that  the
present  state  of affairs exists.  In  this  section  we  look at
several  architectural  disciplines  in  order  to  develop our
intuition  about  software  architecture.  We  look at  hard-
ware  and  network  architecture  because  they  have  tra-
ditionally  been  considered  sources  of ideas  for software
architecture;  we look at  building  architecture because  it
is  the  "classical"  architectural  discipline.

2.1.1  Computing  Hardware  Architecture

There  are  several  different  approaches  to  hardware
architecture  that  are  distinguished  by the  aspect  of the
hardware  that  is  emphasized.  RISC  machines  are  ex-
amples  of a  hardware  architecture  that  emphasizes  the
instruction  set  as  the  important  feature.  Pipelined  ma-
chines  and  multi-processor  machines  are  examples  of
hardware  architectures  that  emphasize  the  configura-
tion  of architectural  pieces  of the  hardware.

There  are  two  interesting  features  of the  second  ap-
proach  to  hardware  architecture  that  are  important  in
our  consideration  of software  architecture:

•  there  are  a  relatively  small  number  of  design  ele-

ments;  and

•  scale  is  achieved  by  replication  of these  design  ele-

ments.

This contrasts with software architecture,  where there  is
an exceedingly large number of possible design elements.
Further,  scale  is  achieved  not  by  replicating  design  el-
ements,  but  by  adding  more  distinct  design  elements.
However,  there  are  some  similarities:  we  often  organize
and  configure software  architectures  in  ways  analogous
to the  h ~ d w a r e   architectures  mentioned  above.  For ex-
ample, we create multi-process software systems and use
pipelined  processing.

Thus,  the  important  insight  from  this  discussion  is
that  there  are  fundamental  and  important  differences
between  the  two  kinds  of architecture.  Because  of these
differences,  it  is  somewhat  ironic  that  we  often  present
software  architecture  in  hardware-like  terms.

2.1.2  N e t w o r k   A r c h i t e c t u r e

Network architectures  are achieved by abstracting  the
design  elements  of  a  network  into  nodes  and  connec-
tions,  and  by  naming  the  kinds  of  relationships  that
these  two  elements  have  to  each  other.  Thus  we  get
star networks,  ring  networks,  and  manhattan  street net-
works  as  examples  of named  network  architectures.

The  two  interesting  architectural  points  about  net-

work  architecture  are:

•  there  are  two  components  - -   nodes  and  connec-

tions;  and

•  there  are  only a few topologies that  are  considered.

It  is certainly the  case  that  we  can  abstract  to  a  similar
level  in  software  architecture  - -   for example,  processes
and  inteprocess  communication.  However,  rather  than
a  few  topologies  to  consider,  there  are  an  exceedingly

ACM SIGSOFT

SOFTWARE ENGINEERING NOTES vol 17 no 4

Oct 1992 Page 42

large  number  of  possible  topologies  and  those  topolo-
gies  generally go  without  names.  Moreover,  we  empha-
size aspects  different from the  topology of the nodes  and
connections.  We  consider  instead  such  matters  as  the
placement  of  processes  (e.g.,  dislribuled  architectures)
or  the  kinds  of interprocess  communication  (e.g.,  mes-
sage  passing  architectures).

Thus,  we  do  not  benefit  much  from  using  networks
as  an  analogy for software architecture,  even though  we
can  look  at  architectural  elements  from  a  similar  level
of abstraction.

2.1.3  Building Architecture

The  classical  field  of  architecture  provides  some  of
the  more  interesting  insights  for  software  architecture.
While  the  subject  matter  for  the  two  is  quite  different,
there  are  a  number  of  interesting  architectural  points
in building  architecture  that  are  suggestive  for software
architecture:

•  multiple  views;

•  architectural  styles;

•  style  and  engineering;  and

•  style  and  materials.

A  building  architect  works  with  the  customer  by
means  of  a  number  of  different  views  in  which  some
particular  aspect  of  the  building  is  emphasized.  For
example,  there  are  elevations  and  floor  plans  that  give
the  exterior  views  and  "top-down"  views,  respectively.
The elevation views may be supplemented by contextual
drawings  or  even  scale  models  to  provide  the  customer
with  the  look  of  the  building  in  its  context.  For  the
builder,  the  archite.ct  provides  the  same floor plans  plus
additional  structural  views  that  provide  an  immense
amount  Q£detail  about  various  explicit  design  consider-
ations  such  as  electrical  wiring,  plumbing,  heating,  and
air-conditioning.

Analogously, the  software architect  needs a  number of
different  views  of the  software  architecture  for  the  var-
ious  uses  and  users.  At  present  we  make  do  with  only
one  view:  the  implementation.  In  a  real  sense,  the  im-
plementation  is  like  a  builders  detailed  view - -   that  is,
like  a  building  with  no  skin  in  which  all  the  details  are
visible.  It  is  very difficult to  abstract  the  design  and  ar-
chitecture  of the  system  from  all  the  details.  (Consider
the  Pompidou  Center  in  Paris  as  an  example.)

The  notion  of architectural  style  is  particularly  use-
ful  from  both  descriptive  and  prescriptive  points  of

view.  Descriptively, architectural  style  defines  a  partic-
ular  codification of design elements  and  formal arrange-
ments.  Prescriptively,  style  limits  the  kinds  of  design
elements  and  their  formal  arrangements.  T h a t   is,  an
architectural  style  constrains  both  the  design  elements
and  the formal relationships  among the  design elements.
Analogously,  we  shall  find  this  a  most  useful  concept  in
software  architecture.

Of  extreme  importance  is  the  relationship  between
engineering  principles  and  architectural  style  (and,  of
course,  architecture  itself).  For  example,  one  does  not
get  the  light,  airy  feel  of the  perpendicular  style  as  ex-
emplified  in  the  chapel  at  King's  College,  Cambridge,
from  romanesque  engineering.  Different  engineering
principles  are  needed  to  move  from  the  massiveness  of
the  romanesque  to  lightness  of the  perpendicular.  It  is
not  just  a  m a t t e r   of  aesthetics.  This  relationship  be-
tween  engineering  principles  and  software  architecture
is  also  of fundamental  importance.

Finally,  the  relationship  between  architectural  style
and  materials  is  of  critical  importance.  The  materi-
als  have  certain  properties  that  are  exploited  in  pro-
viding  a  particular  style.  One  may  combine  structural
with  aesthetic  uses  of materials,  such  as  that  found  in
the  post  and  beam  construction  of  tudor-style  houses.
However,  one  does  not  build  a  skyscraper  with  wooden
posts  and  beams.  The  material  aspects  of  the  design
elements  provide  both  aesthetic  and  engineering  bases
for an  architecture.  Again,  this  relationship  is of critical
importance  in  software  architecture.

Thus,  we  find  in  building  architecture  some  funda-
mental  insights  about  software  architecture:  multiple
views  are  needed  to  emphasize  and  to  understand  dif-
ferent  aspects  of  the  architecture;  styles  are  a  cogent
and  important  form  of  codification  that  can  be  used
both  descriptively  and  prescriptively;  and,  engineering
principles  and  material  properties  are  of  fundamental
importance  in  the  development and  support  of a  partic-
ular  architecture  and  architectural  style.

2.2

T h e   C o n t e x t

o f   A r c h i t e c t u r e

Before  discussing  our  motivation  for  software  archi-
tecture  specifications,  we  posi t  a  characterization  of ar-
chitecture  in  the  context  of the  entire  software product.
Note  that  we  do  not  mean  to  imply  anything  about  the
particular  process  by  which  this  product  is  created  - -
though  of  course  there  may  be  implications  about  the
process  that  are  inherent  in  our  view.  Our  purpose  is
primarily  to  provide  a  context  for  architecture  in  what
would  be  considered  a fairly standard  software product.
We  characterize  the  different  parts  of  the  software

ACM  SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol 17 no 4

Oct 1992 Page 43

product  by  the  kinds  of  things  that  are  important  for
that  part  - -   the  kinds  of entities,  their  properties  and
relationships  that  are  important  at  that  level,  and  the
kinds  of  decision  and  evaluation  criteria  that  are  rele-
vant  at  that  level:

requirements  are  concerned with  the  determination
of  the  information,  processing,  and  the  character-
istics  of that  information and  processing  needed  by
the  user  of the  system; 2

architecture  is concerned with the selection of archi-
tectural  elements,  their  interactions,  and  the  con-
straints  on  those  elements  and  their  interactions
necessary  to  provide  a  framework  in  which  to  sat-
isfy  the  requirements  and  serve  as  a  basis  for  the
design;

design  is  concerned  with  the  modularization  and
their
detailed  interfaces  of  the  design  elements,
algorithms  and  procedures,  and  the  data  types
needed  to  support  the  architecture  and  to  satisfy
the  requirements;  and

implementation  is" concerned  with  the  representa-
tions  of the  algorithms  and  data  types  that  satisfy
the  design,  architecture,  and  requirements.

The  different  parts  of  a  particular  product  are  by  no
means  as  simple  as  this  characterization.  There  is  a
continuum  of possible  choices  of models,  abstractions,
transformations,  and  representations.  We  simplify this
continuum  into  four  discrete  parts  primarily to  provide
an  intuition  about  how  architecture  is  related  to  the
requirements  and  design  of a  software  system.

It  should  be  noted  that  there  are  some  development
paradigms  to  which  our  characterization  will not  apply
- -   for example,  the  exploratory programming paradigm
often  found  in  AI  research.  However,  our  characteriza-
tion  represents  a  wide  variety  of development  and  evo-
lutionary  paradigms  used  in  the  creation  of production
software,  and  delineates  an  important,  and  hitherto un-
derconsidered,  part  of a  unified  software  product  15.

2 . 3   M o t i v a t i o n

f o r   A r c h i t e c t u r a l

S p e c i -

f i c a t i o n s

There  are  a  number  of factors  that  contribute  to  the
high  cost  of software.  Two  factors  that  are  important

2 N o t e   t h a t   t h e  n o t i o n  of r e q u i r e m e n t s  p r e s e n t e d  h e r e  is a n   ide-

a i i s t i c  one.  I n  p r a c t i c e ,  r e q u i r e m e n t s  are n o t   so  " p u r e "  ; t h e y  o f t e n

c o n t a i n  c o n s t r a i n t s  on  t h e   a r c h i t e c t u r e  of a  s y s t e m ,  c o n s t r a i n t s  on
the system design, a n d   e v e n   c o n s t r a i n t s  on  t h e   i m p l e m e n t a t i o n .

to  software  architecture  are  evolution  and  customiza-
tion.  Systems  evolve and  are  adapted  to  new  uses,  just
as  buildings  change  over  time  and  are  adapted  to  new
uses.  One  frequently  accompanying  property  of evolu-
tion is an  increasing  brittleness  of the  system  - -   that  is,
an  increasing  resistance  to  change,  or  at  least  to  chang-
ing  gracefully  5.  This  is  due  in  part  to  two  architec-
tural  problems:  architectural  erosion  and  architectural
drift.  Architectural erosion is due to violations of the  ar-
chitecture.  These  violations often lead  to  an  increase  in
problems in the  system  and  contribute  to the  increasing
brittleness  of a  system  - -   for  example,  removing  load-
bearing walls often leads to  disastrous  results.  Architec-
tural  drift is  due to insensitivity  about  the  architecture.
This  insensitivity  leads  more  to  inadaptability  than  to
disasters  and  results  in  a  lack  of coherence  and  clarity
of form,  which  in  turn  makes  it  much  easier  to  violate
the  architecture  that  has  now  become  more  obscured.

Customization  is  an  important  factor  in  software  ar-
chitecture,  not  because  of problems  that  it  causes,  but
because  of the  lack  of architectural  maturity  that  it  in-
dicates.
In  building  software  systems,  we  are  still  at
the  stage  of  recreating  every  design  element  for  each
new  architecture.  We  have  not  yet  arrived  at  the  stage
where  we  have  a  standard  set  of  architectural  styles
with  their  accompanying  design  elements  and  formal
arrangements.  Each  system  is,  in  essence,  a  new  ar-
chitecture,  a  new  architectural  style.  The  presense  of
ubiquitous  customization  indicates  that  there  is  a  gen-
eral  need  for  codification - -   that  is,  there  is  a  need  for
architectural  templates  for  various  architectural  styles.
For the  standard  parts  of a  system  in  a  particular  style,
the  architect  can  select  from  a  set  of  well-known  and
understood  elements  and  use  them  in  ways  appropriate
to  the  desired  architecture.  This  use  of standard  tem-
plates  for architectural  elements then frees the  architect
to  concentrate  on  those  elements  where  customization
is  crucial.

Given  our  characterization  of architecture  and  moti-
vating  problems,  there  are  a  number  of things  that  we
want  to be able to do with an  architectural  specification:

*  Prescribe the  architectural  constraints  rid the  desired
level  - -   that  is,  indicate  the  desired  restrictiveness
or  permissiveness,  determine  the  desired  level  of
generality or  particularity,  define  what  is  necessity
and  what  is luxury,  and  pin-point  the  degree of rel-
ativeness  and  absoluteness.  We  want  a  means  of
supporting  a  "principle  of  least  constraint"  to  be
able  to  to  express  only  those  constraints  in  the  ar-
chitecture  that  are  necessary  at  the  architectural
level  of the  system  description.  This  is  an  impor-

ACM SIGSOFT

SOFTWARE ENGINEERING NOTES vol 17 no 4

Oct 1992  Page 44

tant  departure  from  current  practice  that,  instead
of specifying 1;he constraints,  supplies  specific solu-
tions  that  embody  those  desired  constraints.

•  Separate  aest~ietics from  engineering  - -   that  is,  in-
dicate  what  is  "load-bearing"  from  what  is  "dec-
oration".  This  separation  enables  us  to  avoid  the
kinds of changes that  result in architectural erosion.

•  Express  different  aspects  of  the  architecture  in  an
appropriate  manner  - -   that  is,  describe  different
parts  of the  architecture  in  an  appropriate  view.

•  Perform  dependency  and  consistency  analysis  - -
that  is,  determine  the  interdependencies  between
architecture,  requirements  and  design;  determine
interdependencies  between  various  parts  of the  ar-
chitecture;  and  determine  the  consistency,  or  lack
of  it,  between  architectural  styles,  between  styles
and  architecture,  and  between  architectural  ele-
ments.

3  M o d e l

o f   S o f t w a r e   A r c h i t e c t u r e

In  Section  2  we  use  the  field  of building  architecture
to  provide  a  number  of insights  into  what  software  ar-
chitecture  might  be.  The  concept  of building  architec-
ture  that  we appeal  to is that  of the standard  definition:
"The  art  or science  of building:  especially  designing  and
building  habital structures"  11.  Perhaps  more  relevant
to  our  needs  here  is  a  secondary  definition:  "A  unifying
It  is  this  sense  of
or  coherent  form  or  structure"  11.
architecture  - -   providing  a  unifying  or  coherent  form
or structure  - -   that  infuses our  model of software archi-
tecture.

We  first  present  our  model  of  software  architecture,
introduce  the  notion of software architectural style,  and
discuss  the  interdependence  of  processing,  data,  and
connector  views.

3 . 1

T h e   M o d e l

By  anMogy  to  building  architecture,  we  propose  the

following model  of software  architecture:

Software Architecture  =
{  Elements,  Form,  Rationale  }

T h a t   is,  a  software  architecture  is  a  set  of architectural
(or,  if you  will,  design)  elements  that  have  a  particular
form.

We  distinguish  three  different  classes  of architectural

elements:

•  processing  elements;

•  data  elements;  and

•  connecting  elements.

The processing elements are those.components that  sup-
ply  the  transformation  on  the  data  elements;  the  data
elements  are  those  that  contain  the  information that  is
used  and  transformed;  the  connecting  elements  (which
at  times  may  be  either  processing  or  data  elements,
or  both)  are  the  glue  that  holds  the  different  pieces
of  the  architecture  together.  For  example,  procedure
calls,  shared  data,  and  messages  are  different  examples
of connecting elements that  serve to  "glue"  architectural
elements  together.

Consider the  example of water  polo as a  metaphor for
the  different  classes  of elements:  the  swimmers  are  the
processing  elements,  the  ball  is  the  data  element,  and
water  is  the  primary  connecting  element  (the  "glue").
Consider further the  similarities of water polo, polo, and
soccer.  They  all  have  a  similar  "architecture"  but  dif-
fer  in  the  "glue"  - -   that  is,  they  have  similar  elements,
shapes  and  forms,  but  differ  mainly  in  the  context  in
which  they  are  played  and  in  the  way  that  the  elements
are  connected  together.  We  shall  see  below  that  these
connecting  elements  play  a  fundamental  part  in  distin-
guishing  one  architecture  from  another  and  may  have
an  important  effect  on  the  characteristics  of a  particu-
lar  architecture  or  architectural  style.

The  architectural  form  consists  of  weighted  proper-
ties  and  relationships.  The  weighting  indicates  one  of
two things:  either  the  importance of the  property or the
relationship,  or the  necessity of selecting among alterna-
tives,  some  of which  may be  preferred  over others.  The
use  of weighting  to  indicate  importance  enables  the  ar-
chitect  to  distinguish  between  "load-bearing"  and  "dec-
orative"  formal aspects;  the  use of weighting  to indicate
alternatives enables the  architect to constrain  the  choice
while  giving  a  degree  of latitude  to  the  designers  who
must  satisfy  and  implement  the  architecture.

Properties  are  used  to  constrain  the  choice  of archi-
tectural  elements  - -   that  is,  the  properties  are  used  to
define  constraints  on  the  elements to  the  degree  desired
by  the  architect.  Properties  define  the  minimum  de-
sired  constraints  unless  otherwise  stated  - -   that  is,  the
default  on  constraints  defined  by  properties  is:  "what
is  not  constrained  by  the  architect  may  take  any  form
desired  by  the  designer  or  implementer".

Relationships  are  used  to  constrain  the  "placement"
of architectural  elements - -   that  is,  they  constrain  how
the  different  elements  may  interact  and  how  they  are
organized with respect  to each other  in the  architecture.

ACM SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol 17 no 4

Oct 1992  Page 45

As  with  properties,  relationships  define  the  minimum
desired  constraints  unless  otherwise  stated.

An  underlying,  but  integral,  part  of an  architecture  is
the  rationale  for the  various choices made in  defining an
architecture.  The  rationale  captures  the  motivation for
the  choice of architectural  style,  the  choice of elements,
and  the  form.  In  building  architecture,  the  rationale
explicates  the  underlying  philosophical  aesthetics  that
motivate  the  architect.
In  software  architecture,  the
rationale  instead  explicates  the  satisfaction  of  the  sys-
tem  constraints.  These  constraints  are  determined  by
considerations  ranging  from  basic  functional  aspects  to
various  non-functional  aspects  such  as  economics  4,
performance  2  and  reliability  13.

3 . 2

A r c h i t e c t u r a l

S t y l e

If  architecture  is  a  formal  arrangement  of  architec-
tural  elements,  then  architectural  style  is  that  which
abstracts  elements and  formal aspects  from various spe-
cific  architectures.  An  architectural  style  is  less  con-
strained  and  less  complete  than  a  specific  architecture.
For  example,  we  might  talk  about  a  distributed  style  or
a  multi-process  style.  In  these  cases,  we  concentrate  on
only  certain  aspects  of a  specific  architecture:  relation-
ships  between  processing  elements  and  hardware  pro-
cessors,  and  constraints  on  the  elements,  respectively.

Given this  definition of architecture  and  architectural
style,  there  is  no  hard  dividing  line  between  where  ar-
chitectural  style  leaves  off and  architecture  begins.  We
have  a  continuum  in  which  one  person's  architecture
may  be  another's  architectural  style.  Whether  it  is  an
architecture  or  a  style  depends  in  some  sense  on  the
use.  For example,  we  propose  in  Section  2.3  that  archi-
tectural styles be used  as constraints  on an  architecture.
Given that  we want  the  architectural  specification to be
constrained  only  to  the  level  desired  by  the  architect,
it  could  easily  happen  that  one  person's  architecture
might  well  be  less  constrained  than  another's  architec-
tural  style.

The  important  thing  about  an  architectural  style
is  that  it  encapsulates  important  decisions  about  the
architectural  elements  and  emphasizes  important  con-
straints  on  the  elements  and  their  relationships.  The
useful  thing  about  style  is  that  we  can  use  it  both  to
constrain  the  architecture  and  to  coordinate  cooperat-
ing architects.  Moreover, style embodies those decisions
that  suffer  erosion  and  drift.  An  emphasis  on  style  as
a  constraint  on  the  architecture  provides  a  visibility to
certain  aspects  of the  architecture  so  that  violations of
those  aspects  and  insensitivity  to  them  will  be  more
obvious.

3 . 3

P r o c e s s / D a t a / C o n n e c t o r

I n t e r d e p e n d e n c e

As mentioned above, an  important insight from build-
ing  architecture  is  that  Of multiple  views.  Three  im-
portant  views  in  software  architecture  are  those  of pro-
cessing,  data,  and  connections.  We  observe  that  if  a
process  view 3 of an  architecture  is  provided,  the  result-
ing  emphasis  is  on  the  data  flow though  the  processing
elements  and  on  some  aspects  of  the  connections  be-
tween  the  processing  elements  with  respect  to  the  data
elements.  Conversely,  if a  data  view  of an  architecture
is  provided,  the  resulting  emphasis  is  on  the  process-
ing  flow,  but  with  less  an  emphasis  on  the  connecting
elements  than  we  have  in  the  process  view.  While  the
current  common wisdom  seems  to  put  the  emphasis  on
object-oriented  (that  is,  data-oriented)  approaches,  we
believe  that  all  three  views  are  necessary  and  useful  at
the  architectural  level.

We  argue  informally, in  the  following way, that  there

is  a  process  and  data  interdependence:

•  there  are some properties  that  distinguish  one state

of the  data  from  another;  and

•  those  properties  are  the  result  of some  transforma-

tion  produced  by some  processing  element.

These two views are thus  intertwined - -   each dependent
on  the  other  for  at  least  some  of the  important  charac-
teristics  of both  data  and  processing.  (For  a  more  gen-
eral  discussion  of process  and  data  interdependence,  see
10.)

The interdependence  of processing  and  data upon  the
connections  is  more  obvious:  the  connecting  elements
are  the  mechanisms  for  moving  data  around  from  pro-
cessor  to  processor.  Because  of  this  activity  upon  the
data,  the  connecting elements will necessarily have some
of the  properties  required  by  the  data  elements  in  pre-
cisely the  same  way that  processing elements have some
of the  properties  required  by  the  data  elements.

At  the  architectural  level,  we  need  all  three  views
and  the  ability  to  move freely  and  easily  among  them.
Our  example  in  the  next  section  provides  illustrations
of this  interdependence  and  how we might provide three
different,  but  overlapping,  views.

3 We use the  d i c h o t o m y  of process  a n d   data  i n s t e a d  of.functi0n
a n d   object  b e c a u s e   these  t e r m s   s e e m   to  be  m o r e   n e u t r a l .   T h e
l a t t e r   t e r m s   seem  to  suggest  s o m e t h i n g  m o r e   specific in  t e r m s   of
p r o g r a m m i n g  t h a n   the  former.

ACM SIGSOFT

SOFTWARE ENGINEERING  NOTES voi 17 no 4

Oct 1992 Page 46

4  Examples

One  of the  few  software  architectural  styles  that  has
achieved  widespread  acceptance  is  that  of  the  multi-
phase  compiler.
It  is  practically  the  only  style  in
which  every software  engineer  is  expected  to  have  been
trained.  We  rely  on  this  familiarity  to  illustrate  some
of the  insights  that  we  have  gained  into  software  archi-
tectures  and  their  descriptions.

In  this  section  we  look  at  two  compiler  architectures

of the  multi-phase  style:

•  a  compiler that  is  organized  sequentially;  and

•  a  compiler that  is organized as  a  set  of parallel pro-
cesses  connected  by means of a  shared  internal  rep-
resentation.

Because  of space  limitations  and  for  presentation  pur-
poses,  our  examples  are  somewhat  simplified and  ideal-
ized,  with  many details  ignored.  Moreover, we use exist-
ing notations because they are convenient for illustrative
purposes;  proposals  for  specific  architectural  notations
are beyond the scope of this paper.  In each case we focus
on  the  architectural  considerations  that  seem  to  be  the
most  interesting to  derive from that  particular  example.
(Of  course,  other  examples  of multi-phase  compiler  ar-
chitectures  exist  and  we  make  no  claims  of exhaustive
coverage of this  architectural  landscape.)  Before explor-
ing  these  examples,  we  provide  a  brief  review  of  their
common  architectural  style.

4.1

T h e   M u l t i - p h a s e
Style

A r c h i t e c t u r a l

Our  simplified model  of a  compiler  distinguishes  five
phases:
lexical  analysis,  syntactic  analysis,  semantic
analysis,  optimization,  and  code  generation.  Lexical
analysis  acts  on  ,characters  in  a  source  text  to  produce
tokens  for  syntactic  analysis.  Syntactic  analysis  pro-
duces  phrases  that  are  either  definition  phrases  or  use
phrases.  Semantic  analysis  correlates  use  phrases  with
definition phrases  - -   i.e.,  each  use of a  program element
such  as  an  identifier is  associated  with  the  definition for
that  element,  resulting  in  correlated phrases.  Optimiza-
tion  produces  annotations  on  correlated  phrases  that
are  hints  used  during  generation  of  object  code.  The
optimization  phase  is  considered  a  preferred,  but  not
necessary,  aspect  of  this  style.  Thus,  the  multi-phase
style  recognizes  the  following architectural  elements:

processing  elements:  lexer,  parser,  semantor,  op-
timizer,  and  code  generator;
and

data  elements:

characters,
tokens,  phrases,
correlated phrases,  annotated
phrases,  and  object  code.

Notice  that  we  have  not  specified  connecting  elements.
It  is  simply  the  case  that  this  style  does  not  dictate
what  connecting elements  are to be used.  Of course,  the
choice of connecting elements  has  a  profound  impact  on
the  resulting  architecture,  as  shown  below.

The  form  of  the  architectural  style  is  expressed  by
weighted  properties  and  relationships  among  the  archi-
tectural  elements.  For  example,  the  optimizer  and  an-
notated  phrases  must  be  found  together,  but  they  are
both  only  preferred  elements,  not  necessary.  As  an-
other  example,  there  are  linear  relationships  between
the  characters  constituting  the  text  of the  program,  the
tokens produced  by the  lexer,  and  the  phrases  produced
by the parser.  In particular,  tokens consist of a sequence
of characters,  and  phrases  consist  of  a  sequence  of  to-
kens.  However,  there  exists  a  non-linear  relationship
between phrases  and correlated phrases.  These relation-
ships  are  depicted  in  Figure  1.  As  a  final example,  each
of the  processing  elements  has  a  set  of  properties  that
defines the  constraints  on those  elements.  The  lexer, for
instance,  takes  as  input  the" characters  that  represent
the  program  text  and  produces  as  output  a  sequence  of
tokens.  Moreover,  there  is  an  ordering  correspondence
between  the  tokens  and  the  characters  that  must  be
preserved  by  the  lexer.  A  good  architectural  descrip-
tion  would  capture  these  and  other  such  properties  and
relationships.

Let  us  illustrate  this  by  formally describing  the  rela-
tionship  between  characters  and  tokens  and  describing
the  order-preserving  property  of  the  lexer.  We  begin
the  description  with  a  data  view  stated  in  terms  of se-
quences  and  disjoint  subsequences.

Let  C  =  {cl,c2,...,Cm}  be  a  sequence  of  char-
acters  representing  a  source  text,  C~  i  _~ j  be  a
subsequence  of  C  whose  elements  are  all  the  el-
ements  in  C  between  ci  and  cj  inclusive,  T  ----
{ t l , t 2 , . . . , t n }   be  a  sequence  of tokens,  and  "~"
indicate  the correspondence between  a  token in  T
and  a  subsequence  of C.  T  is  said  to preserve  C
ff  there  exists  an  i,  j,  k,  q,  r,  and  s  such  that
1 _ < i < j _ < m ,   1 <   k  <  n,  1 <  q  ~_ r  <  m,  and
for all  t  E T  there  exists  a  C~  such  that:

  C~
C~

if t  =  tl
if t  =  tn

l _ < u _ < q - 1

Cr q

if $ =  t~,  where  S u,

V

tk-1  =  C~-1

u

tk+l  --~ C~ +1

ACM  SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol  17 no 4

Oct  1992  Page 47

Characters

Tokens

Phrases

L ~ I

L

~

I

L

L

l

I

I

l

L _ _ I

I

L

Correlated Phrases

i  ..............

•
÷  ...............................

L ~ J

I

I

L

J

I

I

I

I

I

I

,

F i g u r e   1:  D a t a   E l e m e n t   Relationships.

The  lexer is now constrained  from a  processing  perspec-
tive  to  accept  a  sequence  of  characters  C,  produce  a
sequence  of tokens  T,  and  to  preserve  the  ordering  cor-
respondence  between  characters  and  tokens:

lexer:  C  ---+ T,  where  T  preserves  C

Finally,  it  is  interesting  to  note  that  the  connec-
tor  view  reveals  additional  constraints  that  should  be
placed  on  the  architectural  style.  These  constraints  are
illustrated  by  the  connection  between  the  lexer and  the
parser.  In  particular,  connecting  elements  must  ensure
that  the  tokens  produced  by  the  lexer are  preserved  for
the  parser,  such  that  the  order  remains  intact  and  that
there  are  no  losses,  duplicates,  or  spurious  additions.

4 . 2

S e q u e n t i a l   A r c h i t e c t u r e

If  there  is  a  "classical"  multi-phase  compiler  archi-
tecture,  then  it  is  the  sequential  one,  in  which  each
phase  performs  its  function  to  completion  before  the
next phase  begins and in which data elements are passed
directly from one processing element to the other.  Thus,
we  add  the  following  architectural  elements  to  those
characterizing  the  overall  style:

connecting  elements:  procedure  call  and  parame-

ters.

Furthermore,  we  refine  tokens  to  include  the  structur-
ing of the  identifier  tokens  into  a  name  table (NT),  and
refine  phrases  to  be  organized  into  an  abstract syntax
tree  (AST).  Correlation of phrases  results  in  an  abstract
syntax  graph (ASG)  and  optimization  in  an  annotated
abstract syntax graph (AASG).  Figure  2 gives a  process-
ing view of the sequential  architecture,  showing the flow
of data  through  the  system.  Notice  that  there  are  two
paths  from the semantor to the  code generator, only one
of which  passes  through  the  optimizer.  This reflects the
fact  that  a  separate  optimization phase  is not  necessary
in  this  architecture.  T h a t   is,  a  design  satisfying  this
architecture  need  not  provide  an  optimizer.

To  illustrate  the  interdependence  of  processing  and
data  views,  let  us  consider  the  data  as  a  whole  being

Characters

ObJect Code

Tokens
OVT)  , , , , , , , ~ @

I
Phrases
(NT+AST)

Y
G<  Correlated Phrases

(NT~ASG)

Annotated Cor. Phrases
(NT+AASG)

Correlated Phrases
(NT+ASG)

Figure  2:  Processing  View  o f   Se-
q u e n t i a l   C o m p i l e r   A r -
c h i t e c t u r e .

created  and  transformed  as  they  flow  through  the  sys-
tem.  We have found that  the  data view is best  captured
by  a  notion that  we  call  application-oriented properties.
Application-oriented  properties  describe  the  states  of a
data  structure  that  are  of  significance  to  the  process-
ing  elements manipulating  that  structure.  They  can  be
used  for such  things  as  controlling the  order  of process-
ing,  helping  to define  the  effects of a  processing element
on  a  data  structure,  and  even  helping  to  define  the  op-
erations  needed  by  the  processing  elements  to  achieve
those  effects.

For

this  example,

the

(simplified)  application-

oriented  properties  are  as  follows:

has-all-tokens:  a  state  produced  as  a  result  of lex-
ically  analyzing  the  program  text,
necessary  for  the  parser  to  begin
processing;

ACM SIGSOFT

SOFTWARE ENGINEERING NOTES vol 17 no 4

Oct 1992 Page 48

has-alLphrases:  a  state  produced  by  the  parser,
necessary  for  the  semantor  to  be-
gin processing;

has-all-correlated-phrases: a state  produced  by the
semantor,  necessary  for  the  opti-
mizer and  code generator to begin
processing;  and

has-all-optimizalion-annotations:  a state produced
by the optimizer, preferred for the
code  generator  to  begin  process-
ing.

Notice  again  that  the  last  property  is  only  preferred.
While in  this  example the  application-oriented proper-
ties  may appear  obvious and  almost trivial, in  the  next
example they are  crucial to the description of the archi-
tecture  and  in  guaranteeing the  compliance of designs
and implementations with that  architecture.

An  interesting  question  to  consider  is  why  we  evi-
dently  chose  to  use  a  property-based  scheme  for  de-
scribing architectural elements rather than a type-based
scheme.  The  rea~3on is  that  type  models,  as  they  cur-
rently exist,  are  essentially only able to  characterize  el-
ements  and  element  types  in  terms  of the  relationship
of one  element type  to  another  (e.g., subtyping and  in-
heritance  12),
in  terms  of the  relationships  that  par-
ticular  elements  :have with  other  elements  (e.g.,  as  in
Ortos  18),  and  in  terms  of  the  operations  that  can
be  performed  on  the  elements.  They  are  not  suited  to
descriptions  of  characteristics  of elements  such  as  the
application-oriented  properties  mentioned  above.  For
example, simply knowing that  there  is  an operation as-
sociated  with  abstract  syntax  graphs  to  connect  one
phrase  to  another  does  not  lead  to  an  understanding
that  the  abstract  syntax  graph  must  have  all  phrases
correlated  before  the  code  generator  can  access  the
graph.

Property-based  schemes,  on  the  other  hand,  can  be
used to capture easily all these characteristics; one prop-
erty  of an  element  could  be  the  set  of operations  with
which  it  is  associated.  It  seems  reasonable  to  consider
enhancing  type  models  in  this  regard  and  we  see  this
as  a  potentially  interesting  area  of future  work.  We
note,  however,  that  type-based schemes are  already ap-
propriately  used  at  the  design  level,  as  mentioned  in
Section  2.  Further,  we  note  that  application-oriented
properties  provide  a  good  vehicle  with  which  to  drive
the  design,  or justify the  suitability, of a  set  of opera-
tions for an  element type.

Returning  to  the  interdependence  between  the  pro-
cessing  and  data  views,  we  can  see  that  the  data

"(cid:127)xer

l~r'ser

1~'~CneO~tor

Code

, /

Optimizer m  C~r~a/~te~d.

F i g u r e   3:  Data  View  of  S e q u e n t i a l

C o m p i l e r   A r c h i t e c t u r e .

view concentrates on the particular application-oriented
properties  that  are  of  importance  in  describing  each
data  structure,  while  the  processing  view  concentrates
on the functional properties of each processing element.
These  views  are  actually complementary. In fact,  if we
depict  the  data  view,  as  is  done  in  Figure  3,  and  com-
pare  it  to  the  processing  view,  shown in  Figure 2,  then
the  correspondence  becomes fairly obvious.

The  important  architectural  considerations  that  de-

rive from this  example can  be summarized as follows:

•  the  form  descriptions  must  include  the  relation-
ships  and  constraints  among the  elements, includ-
ing relative weightings and  preferences;

•  current  type-based  schemes  for  characterizing  ele-

ments are  insufficient; and

•  there is a natural interdependence between the pro-
cessing  and  data  views  that  can  provide  comple-
mentary descriptions of an  architecture.

4 . 3

P a r a l l e l
S t r u c t u r e   A r c h i t e c t u r e

P r o c e s s ,

S h a r e d

D a t a

Suppose  that  performance  is  of  paramount  impor-
tance,  such  that  one  wants  to  optimize  the  speed  of
the compiler as much as possible.  One possible solution
is  to  adopt  an  architecture  that  treats  the  processing
elements  as  independent  processes  driven  by  a  shared
internal  representation  - -   that  is,  the  connecting  ele-
ment  is  the  shared  representation  and  each  processing
element  performs  eager  evaluation.  Figure  4  depicts  a

ACM  SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol  17 no 4

Oct 1992 Page 49

Characters

)

L

I n t e r n a l
Representation

F i g u r e   4:  P a r t i a l   P r o c e s s   V i e w   of
P a r a l l e l   P r o c e s s ,   S h a r e d
D a t a
S t r u c t u r e   C o m -
p i l e r   A r c h i t e c t u r e .

simplified and  partial  process  view of this  architecture,
showing  the  relationships  between  the  internal  repre-
sentation  and  the  lexer,  the  parser,  and  the  semantor.
(We only consider these three processing elements in the
remainder  of this example.)

The  application-oriented  properties  of the  shared  in-
ternal representation  in this architecture are much more
complicated,  and  interesting,  than  those  given  in  the
previous  example.  In  particular,  a  number  of process-
ing elements are affecting the state  of the internal repre-
sentation,  and  doing so  concurrently.  This  implies that
the  application-oriented properties  must provide for co-
ordination  and  synchronization  among  the  processing
elements.  We  begin  by  giving the  basic  properties  that
the  internal  representation  may exhibit:

J

sic  properties  must  be  explicitly  described.  A  num-
ber  of  notations  exist  that  are  suitable  for  making
such  descriptions,  including  parallel  path  expressions
6,  constrained  expressions  1,  and  petri  nets  16.
In
this  example  we  use  parallel  path  expressions,  where
a  comma  indicates  sequence,  a  plus  sign  indicates  one
or  more  repetitions,  an  asterisk  indicates  zero  or  more
repetitions,  and  subexpressions  are  enclosed  in  paren-
theses.  Synchronization  points  occur  where  names  of
application-oriented  properties  are  the  same  in  differ-
ent  parallel  path  expressions.  First,  the  path  expres-
sions  for  each  of the  data  elements  - -   tokens,  phrases,
and  correlated  phrases  - -   are  given:

(1)

(2)

(3)

(no-tokens,  has-token+) *,
will-be-no-more-tokens, has-token*,  no-tokens
(no-phrases,  has-phrase+) * ,
will-be-no-more-phrases,  has-phrase*,  no-phrases
no-correlated-phrases,  (have-correlated-phrases)*,
all-phrases-correlated

Next,  the  path  expressions  relating  the  application-
oriented  properties  are  given:

(4)  will-be-no-more-tokens, will-be-no-more-phrases,

all-plirases-correlated
has-token + , has-phrase
has-phrase +,  has-correlated-phrase

(5)
(6)

Thus,  tokens  are  consumed  to  produce  phrases,  and
phrases  are  correlated  until  they  are  all  processed.

What  we  have  given  so  far  is  essentially  a  connector
view  (and,  in  this  case,  effectively a  data  view  as  well).
Concentrating  instead  on  the  processing  view  allows us
to  describe  how each  processing  element transforms the
internal  representation  as  well  as  how  those  processing
elements  are  synchronized:

no-tokens
has-token
will-be-no-more-tokens
no-phrases
has-phrase
will-be-no-more-phrases
no- correlated-phrases
have- correlated-phrases
all-phrases- correlated

lexer:

parser:

semantor:

Notice  that  these  properties  imply  that  tokens  and
phrases  are  consumed,  but
that  correlated  phrases
are  accumulated  (consider  "has-phrase"  versus  "have-
correlated-phrases").

(no-tokens,  has-token +) ~,
will-be-no-more-tokens

no-phrases,  (has-token +,  has-phrase)*,
will-be-no-more-tokens,  (has-token + ,
has-phrase)*,  no-tokens,
will-be-no-more-phrases

(has-phrase + ,

no-correlated-phrases,
has-correlated-phrase)*,
will-be-no-more-phrases,
has-correlated-phrase)*,  no-phrases,
all-phrases- correlated

(has-phrase + ,

Because  of the  parallel  behavior  of the  processing  el-
ements,  the  interrelationships  among  the  various  ba-

An  interesting  question  to  ask  is  how  this  architec-
ture  relates  to  the  previous  one.  In  fact,  the  ability to

ACM SIGS OFT

SOFTWARE ENGINEERING NOTES vol 17 no 4

Oct 1992 Page 50

relate similar architectures is an important aspect of the
software process;  an  example is the evaluation of "com-
peting"  architectures.  Certainly, the  architectures both
being  of a  common style  captures  some  portion  of the
relationship.  More  can  be  said,  however,  given  the  use
of application-oriented properties.  In particular, we can
draw  correlation~3 among the  properties  of the  different
architectures.  The table below shows  some of these cor-
relations.

Sequential  A r c h i t e c t u r e
has-all-tokens
has-all-phrases
has-all-correlated-phrases

Parallel  A r c h i t e c t u r e
will-be-no-more-tokens
will-be-no-more-pharses
all-phrases-correlated

In  this  case,  the  correlations  indicate  common  points
of processing,  leading,  for  instance,  to  a  better  under-
standing  of  the  possible  reusability  of  the  processing
elements.

The important points of this example can be summa-

rized  as follows:

•  the  processing  elements  are  much  the  same  as  in
the previous architecture,  but  with different "locus
of control"  properties;

•  the  form  of  this  architecture  is  more  complex
than  that  of  the  previous  one  - -   there  are  more
application-oriented  properties  and  those  proper-
ties  require  a  richer  notation  to  express  them  and
their  interrelationships;

•  we still benefit from the processing/data/connector
view interdependence, albeit with more complexity;
and

5.1

S o f t w a r e   A r c h i t e c t u r e

a n d   A n a l y s i s

Aside  from  providing  clear  and  precise  documenta-
tion, the primary purpose  of specifications is  to provide
automated analysis of the documents and to expose var-
ious  kinds  of problems  that  would otherwise  go  unde-
tected.  There  are  two  primary  categories  of  analysis
that  we  wish  to  perform:  consistency  and  dependency
analysis.  Consistency occurs in several dimensions:  con-
sistency within the architecture and architectural styles,
consistency  of the  architecture  with  the  requirements,
and  consistency of the  design with the  architecture.  In
the  same  way that  Inscape  14  formally and  automat-
ically manages the  interdependencies  between  interface
specifications and  implementations, we  also want to  be
able  to  manage the  interdependencies  between  require-
ments,  architecture,  and  design.

Therefore,  we  want  to  provide  and  support  at  least

the following kinds of analysis:

•  consistency of architectural style constraints;

•  satisfaction  of architectural  styles  by  an  architec-

ture;

consistency of architectural  constraints;

satisfaction of the  architecture  by  the  design;

establishment  of  dependencies  between  architec-
ture  and  design,  and  architecture  and  require-
ments; and

determination of the implications of changes in  ar-
chitecture  or  architectural  style on  design  and  re-
quirements,  and  vice  versa.

•  application-oriented properties  are  useful in  relat-

5 . 2   A r c h i t e c t u r e

a n d

t h e   P r o b l e m s

o f

ing similar architectures.

U s e   a n d   R e u s e

5

S o m e   B e n e f i t s   D e r i v e d   f r o m   S o f t w a r e
A r c h i t e c t u r e

We have previously mentioned the use of software ar-
chitecture  in  the  context  of  requirements  and  design.
Software  architecture  provides  the  framework  within
which  to  satisfy the  system  requirements  and  provides
both  the  technical  and  managerial basis  for  the  design
and  implementation of the  system.  There  are  two fur-
ther benefits that. we wish to discuss  in detail:  the kinds
of analysis that  software architecture specifications will
enable us to perform and the kinds of reuse that we gain
from our  approach  to  software architecture.

An  important  aspect  in  improving the  productivity
of the  designers  and  the  programmers  is  that  of being
able  to  build  on  the  efforts  of others  - -   that  is,  using
and  reusing  components  whether  they  come  as  part  of
another  system  or  as  parts  from standard  components
catalogs.

There has  been  much attention given to the  problem
of finding  components  to  reuse.  Finding  components
may be  important  in  reducing  the  duplication of effort
and  code  within  a  system,  but  it  is  not  the  primary
issue  in  attaining effective use  of standardized  compo-
nents.  For example, finding the  components in  a  math
library  is  not  an  issue.  The  primary  issue  is  under-
standing  the  concepts  embodied in  the  library.  If they

ACM  SIGSOFT

SOFTWARE  ENGINEERING  NOTES  vol  17 no 4

Oct  1992 Page  51

are  understood,  then  there  is  usually no  problem find-
ing the  appropriate  component in  the  library to use.  If
they  are  ndt  understood,  then  browsing  will help  only
in  conjunction with  the  acquisition of the  appropriate
concepts.

The primary focus in architecture is the identification
of important properties  and relationships - -   constraints
on  the  kinds  of components that  are  necessary  for the
architecture,  design,  and  implementation of a  system.
Given this  as  the  basis for use  and  reuse,  the  architect,
designer,  or  implementer may be  able  to  select  the  ap-
propriate  architectural element,  design  element, or  im-
plemented  code  to  satisfy  the  specified  constraints  at
the  appropriate  level.

Moreover,

the  various  parts  of  previously  imple-
mented  software  may  be  teased  apart  to  select  that
which  is  useful from  that  which  is  not.  For  example,
the  design  of  a  component  from  another  system  may
have just  the  right  architectural  constraints  to  satisfy
a  particular architectural element, but  the implementa-
tion is constrained such that-it conflicts with other  sys-
tem  constraints.  The  solution  is  to  use  the  design  but
not the implementation: This becomes possible only by
indentifying the  architectural,  design,  and  implemen-
tation  constraints  and  use  them  to  satisfy the  desired
goals of the  architecture,  design,  and implementation.
The  important  lesson  in  reusing  components is  that
the possibilities for reuse  are the greatest where specifi-
cations for the components are  constrained the least - -
at  the  architectural  level.  Component reuse  at  the  im-
plementation level is usually too late because the imple-
mentation elements often embody too many constraints.
Moreover,  consideration  of  reuse  at  the  architectural
level  may  lead  development  down  a  different,  equally
valid solution path, but one that results in greater reuse.

6  C o n c l u s i o n s

Our efforts over the past few years have been  directed
toward  improving the  software process  associated  with
large,  complex software systems.  We have  come to  be-
lieve  that  software architecture  can  play a  vital role  in
this process,  but that it has been both underutilized and
underdeveloped.  We  have  begun  to  address  this  sit-
uation  by  establishing  an  intuition  about  and  context
for  software  architecture  and  architectural  style.  We
have formulated a  model of software architecture  that
emphasizes the  architectural elements of data,  process-
ing,  and  connection,  highlights their  relationships  and
properties,  and captures  constraints on their realization
or  satisfaction.  Moreover,  we  have  begun  to  delineate

the  necessary features of architectural description tech-
niques and their supporting infrastructure.  In so doing,
we have set  a  direction for future  research  that  should
establish the  primacy of software architecture.

Others  have  begun  to  look  at  soft'rare  architecture.
Three that are most relevant are Schwanke,  et al., Zach-
man, and Shaw.

Schwanke,  et  al.,  20  define  architecture  as  the  per-
mitted or allowed set of connections among components.
We agree that  that  aspect  of architecture  is important,
but  feel  that  there  is  much  more  to  architecture  than
simply components and  connections, as we demonstrate
in this paper.

Zachman 23  uses  the metaphor of building architec-
ture  to  advantage  in  constructing  an  architecture  for
information systems.  He  exploits  the  notion  of differ-
ent  architectural documents to provide a  vision of what
the  various  documents  ought  to  be  in  the  building  of
an  information system.  The  architect  is  the  mediator
between  the  user  and  the  builders  of the  system.  The
various documents provide the various views of different
parts  of the  product  - -   the  users  view,  the  contractors
views,  etc.  His  work  differs  from  ours  in  that  he  is
proposing  a  specific  architecture for  a  specific  applica-
tion domain while we are attempting to define the philo-
sophical underpinnings of the discipline, to determine a
notation for  expressing  the  specification of the  various
architectural documents, and determine how these doc-
uments can be  used  in  automated ways.

Shaw  21  comes  the  closest  in approach  to ours.  She
takes the view of a programming language designer and
abstracts  classes  of components,  methods  of composi-
tion, and schemas from a wide variety of systems.  These
correspond  somewhat to  our  notions of processing  and
data  elements,  connecting  elements,  and  architectural
style,  respectively.  One  major  difference  between  our
work and Shaw's is that she is taking a traditional type-
based  approach  to  describing  architecture,  while  we
are  taking  a  more expressive  property-based  approach.
Our  approach appears better  able to more directly cap-
ture  notions  of weighted  properties  and  relationships.
Shaw's  approach  of abstracting  the  various  properties
and relationships of existing architectures  and embody-
ing them in  a  small set  of component  and  composition
types  appears  rather  restrictive.  Indeed,  she  is  seeking
to  provide  a  fixed  set  of useful  architectural  elements
that  one  can  mix and  match to  create  an  architecture.
Shaw's approach is  clearly an important and useful one
and  does  much  to  promote  the  understanding of basic
and  important  architectural  concepts.  Our  approach,
on  the  other  hand,  emphasizes  the  importance  of the

ACM SIGSOFT

SOFTWARE ENGINEERING NOTES vol 17 no 4

Oct 1992  Page 52

14  D.E.

Perry,

lnscape
Environment,  Proc.  Eleventh  Inter.  Conf.  on  Soft-
ware  Engineering,  Pittsburgh,  PA,  IEEE  Computer
Society Press,  May  1989, pp.  2-12.

The

15  D.E.  Perry,  Industrial  Strength  Software  Development
Environments,  Proe.  I F I P   Congress  '89,  T h e   11th
W o r l d   C o m p u t e r   Congress,  San  Francisco,  CA,
Aug.  1989.

16

J.L.  Peterson,  Petri  Nets,  A C M   C o m p u t i n g   Sur-
veys,  Vol. 9,  No.  3,  Sept.  1977, pp.  223-252.

17  W.E.  Riddle and  J.C. Wileden,  T u t o r i a l   on  Software
System  Design:  Description  and  .Analysis,  Com-
puter  Society Press,  1980.

18  W.R.  Rosenblatt,  J.C.  Wfleden,  and A.L. Wolf,  OROS:
Towards  a  Type  Model  for  Software  Development
Environments,  Proe.  O O P S L A   ~89,  New  Orleans,
Louisiana,  October  1989.

19  E. Sandewall,  C. StrSmberg,  and  H. SSrensen, Software
Architecture  Based  on  Communicating  Residential  En-
vironments,  Proc.  F i f t h   Inter.  Conf.  on  Software
Engineering,  San  Diego,  CA, IEEE Computer Society
Press,  Mar.  1981, pp.  144-152.

20  R.W.  Schwanke,  R.Z.  Altucher,  and  M.A.  Platoff,  Dis-
covering,  Visualizing  and  Uontrolling  Software  Struc-
ture,  Proe.  Fifth
Inter.  W o r k s h o p   on  Soft-
ware  Specification  and  Design,  Pittsburgh,  PA,
May  1989,  appearing  in  A C M   S I G S O F T   Notes,
Vol.  14,  No.  3,  May  1989, pp.  147-150.

21  M.  Shaw,  Larger  Scale  Systems  R e q u i r e   Higher-
Level  Abstractions,  Proc.  Fifth  Inter.  Workshop  on
Software  Specification  and  Design,  Pittsburgh,  PA,
May  1989,  appearing  in  A C M   S I G S O F T   Notes,
Vol.  14,  No.  3,  May  1989, pp.  143-146.

22  A.Z.  Spector,  Moduar  Architectures  for  Distributed
P r o e .   E i g h t h   A C M

and  Database  Systems,
S I G A C T - S I G M O D - S I G A R T
ples of Database Systems, Philadelphia, PA, A C M
Press, Mar. 1989, pp. 217-224.

Symp.  on  Princi-

23

J.A.  Zachman,  A  Framework  for  Information  Sys-
tems  Architecture,  I B M   Systems  J o u r n a l ,   Vol.  26,
No.  3,  1987.

underlying  properties  and  relationships  as  a  more  gen-
eral  mechanism  that  can  be  used  to  describe  the  partic-
ular  types  of elements  and  compositions  in  such  a  way
that  provides  a  latitude  of choice.

In  conclusion,  we  offer the  following conjecture:  per-
haps  the  reason  for  such  slow  progress  in  the  develop-
ment  and  evolution of software systems  is  that  we  have
trained  carpenters  and  contractors,  but  no  architects.

R E F E R E N C E S

1  G.S.  Avrulfin,  L.K.  Dillon.,

J.C.  Wfleden,  and
W.E.  Riddle,  Constrained  Expressions:  Adding  Anal-
ysis  Capab~ties  to  Design  Methods  for  Concurrent
Systems,  I E E E   Trans.  on  Software  Engineering,
Vol.  SE-12,  No.  2,  Feb.  1986, pp.  278-292.

2

J.L.  Bentley, 'Writing  Efficient P r o g r a m s ,   Addison-
Wesley,  Reading,  MA,  1982.

3  G.D.  Bergland,  A  Guided  Tour  of  Program  Design
Methodologies,  I E E E   C o m p u t e r ,   Vol. 14,  No.  10,
Oct.  1981, pp.  13-37.

4  B.W.  Boehm,  Software  Engineering  Economics,

Prentice-Hail,  Englewood  Cliffs,  N J,  1981.

5  F.P.  Brooks,  Jr.,.  T h e   M y t h i c a l   M a n - M o n t h ,

Addison-Wesley,  Re~ding,  MA,  1972.

6  R.H.  Campbell  and  A.N.  Habermann,  The  Specifica-
tion  of  Process  Synchronization  by  Path  Expressions,
L e c t u r e   Notes
in  C o m p u t e r   Science,  No.  16,
Apr.  1974, pp.  89-102.

7  E.J.  Chikofsky  (ed.),  Software  D e v e l o p m e n t   - -
C o m p u t e r - a i d e d   Software  Engineering,  Technol-
ogy Series,  IEEE  Computer  Society Press,  1988.

8  G.  Estrin,  R.S.  Fenchel,  R.R.  Razouk,  and  M.K.  Ver-
non,  SARA  (System  ARchitects  Apprentice),  I E E E
Trans.  on  Software  Engineering,  Vol. SE-12,  No. 2,
Feb.  1986, pp.  293-277.

9  P.  Freeman  and  A.I.  Wasserma~,  Tutorial  on  Soft-
ware  Design  Techniques,  IEEE  Computer  Society
Press,  1976.

10  D.  Ja~ckson, Composing  Data  and  Process Descriptions
in  the  Design  of  Software  Systems,  LCS  Tech.  Re-
p o r t   419,  Massachusetts Institute of Technology, Cam-
bridge,  MA,  May  1988.

11  F.C.  Mish,  x~rebster~s  N i n t h   New  Collegiate  Die-
tlonary,  Merfiam  Webster,  Springfield,  MA,  1983.

12

13

J.E.B.  Moss  ~md  A.L.  Wolf,  Toward  Principles  of In-
heritance  and  Subtyping  for  Programming  Languages,
C O I N S   Tec~.  R e p o r t   88-95,  COINS  Dept.,  Univ.
of Mass.,  Amherst,  MA,  Nov.  1988.

J.D.  Musa,  Software  Reliability:  M e a s u r e m e n t ,
P r e d i c t i o n ,   Application,  McGraw-Hill,  New  York,
NY,  1990.


