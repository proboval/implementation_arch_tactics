A Critical Comparison on Six Static Analysis Tools:
Detection, Agreement, and Precision

Valentina Lenarduzzia, Fabiano Pecorellib, Nyyti Saarimakib, Savanna Lujanb, Fabio Palombac

aM3S Research Unit - University of Oulu, Finland
bClowee Research group - Tampere University, Finland
cSeSa Lab - University of Salerno, Italy

Abstract

Background. Developers use Static Analysis Tools (SATs) to control for potential quality issues in source code, including
defects and technical debt. Tool vendors have devised quite a number of tools, which makes it harder for practitioners
to select the most suitable one for their needs. To better support developers, researchers have been conducting several
studies on SATs to favor the understanding of their actual capabilities.
Aims. Despite the work done so far, there is still a lack of knowledge regarding (1) what is their agreement, and (2)
what is the precision of their recommendations. We aim at bridging this gap by proposing a large-scale comparison of
six popular SATs for Java projects: Better Code Hub, CheckStyle, Coverity Scan, FindBugs, PMD, and SonarQube.
Method. We analyze 47 Java projects applying 6 SATs. To assess their agreement, we compared them by manually
analyzing - at line- and class-level - whether they identify the same issues. Finally, we evaluate the precision of the tools
against a manually-defined ground truth.
Results. The key results show little to no agreement among the tools and a low degree of precision.
Conclusions. Our study provides the first overview on the agreement among different tools as well as an extensive analysis
of their precision that can be used by researchers, practitioners, and tool vendors to map the current capabilities of the
tools and envision possible improvements.

1. Introduction

Static analysis tools (SATs) are instruments that ana-
lyze source code without executing it, in an effort to dis-
cover potential source code quality issues [1]. These tools
are getting more popular as they are becoming easier to
use—especially in continuous integration pipelines [2]—
and there is a wide range to choose from [3]. However, as
the number of available tools grows, it becomes harder for
practitioners to choose the tool (or combination thereof)
that is most suitable for their needs [4].

To help practitioners with this selection process, re-
searchers have been conducting empirical studies to com-
pare the capabilities of existing SATs [5, 6]. Most of these
investigations have focused on (1) the features provided
by the tools, e.g., which maintainability dimensions can
be tracked by current SATs, (2) comparing specific as-
pects considered by the tools, such as security [7, 8] or
concurrency defects [9], and (3) assessing the number of
false positives given by the available SATs [10].

Recognizing the effort spent by the research commu-
nity, which led to notable advances in the way tool ven-

dors develop SATs, we herein notice that our knowledge
on the capabilities of the existing SATs is still limited.
More specifically, in the context of our research we point
out that three specific aspects are under-investigated: (1)
which source quality problems can actually be detected
by static analysis tools, (2) what is the agreement among
different tools with respect to source code marked as po-
tentially problematic, and (3) what is the precision with
which a large variety of the available tools provide rec-
ommendations. An improved knowledge of these aspects
would not only allow practitioners to take informed deci-
sions when selecting the tool(s) to use, but also researcher-
s/tool vendors to enhance the tool and improve the level
of support provided to developers.

In this paper, we propose a large-scale empirical inves-
tigation into the detection capabilities of six of the most
widely used SATs, namely SonarQube, Better Code Hub,
Coverity Scan, FindBugs, PMD, and CheckStyle.1 Specif-
ically, we run the considered tools against a corpus of 47
projects from the Qualitas Corpus dataset, (1) showcasing
the functionalities and distribution of source code quality

Email addresses: valentina.lenarduzzi@oulu.fi (Valentina

Lenarduzzi), fabiano.pecorelli@tuni.fi (Fabiano Pecorelli),
nyyti.saarimaki@tuni.fi (Nyyti Saarimaki),
savanna.lujan@tuni.fi (Savanna Lujan), fpalomba@unisa.it
(Fabio Palomba)

1SATs verify code compliance with a specific set of rules that,
if violated, can introduce an issue in the code. This issue can be
accounted for as “source code quality issue”: as such, in the remain-
ing the paper we use this term when referring to the output of the
considered tools.

Preprint submitted to Journal of Systems and Software

December 5, 2022

issues detected by the tools; (2) computing the agreement
among the recommendations given by them at line-level;
and (3) manually computing the precision of the tools.

The key results of the study shows that, among the con-
sidered tools, SonarQube is the one able to detect most of
the quality issues that can be detected by the other SATs.
However, when considering the specific quality issues de-
tected, there is little to no agreement among the tools,
indicating that different tools are able to identify differ-
ent forms of quality problems. Finally, the precision of
the considered tools ranges between 18% and 86%, mean-
ing that the practical accuracy of some tools is seriously
threatened by the presence of false positives—this result
corroborates and enlarges previous findings [10] on a larger
scale and considering a broader set of tools.

To sum up, the main contribution of our work is rep-
resented by the largest empirical analysis up to date on
the capabilities of existing static analysis tools—a more
detailed description of how our work compares to previous
studies in the field is reported in the next section. Specif-
ically, we advance the current state of the art in three
different manners:

1. By providing an overview of the features and types of
source code quality concerns detectable by six pop-
ular static analyzers, which may be used by practi-
tioners as a way to select the most suitable tool(s)
based on the specific needs of a project;

2. By investigating the agreement among the consid-
ered tools, which can inform tool vendors about the
limitations of the current solutions available the mar-
ket, other than making practitioners aware of how to
benefit more from the combined capabilities of exist-
ing static analysis tool;

3. By providing a quantification of the precision of six
static analysis tools, which may used to describe
their accuracy in practice, hence alerting developers
on the actual effectiveness of those tools.

Structure of the paper. Section 2 discusses the related
work in the field of empirical studies on static analysis
tools, highlighting how our work advances the state of the
art. Section 3 reports on the tools selected for the em-
pirical investigation, while Section 4 presents the specific
research questions targeted by our study and the methods
employed to address them. The results are presented in
Section 5 and further elaborated in Section 6. Section 7
identifies the threats to the validity of our study. Finally,
in Section 8 we draw conclusions and provide an outlook
on our future research agenda.

2. Related Work

Static analysis tools (SATs) are getting more popu-
lar [3, 11] as they are becoming easier to use [2]. The

use of static analysis tools has been studied by several re-
searchers in the last years [12, 13, 14, 15]. In this section,
we report the relevant work on static analysis tools fo-
cusing on their usage [16, 17, 18], rules and the detected
problems [19, 20, 21].

SATs has been investigating considering which tools
are being used, which types of issues are detected [22, 2],
and the effective solving time [23], considering projects
developed in different language [24]. Results showed that
the most violated rules are related to adherence to coding
standards and missing licenses [2]. Looking at the which
issues is fixed and the related fixing time in average 13%
of the issues have been solved in the systems [23].

Developers can use SATs, such as SonarQube3.6 and
CheckStyle2, to evaluate software source code, finding
anomalies of various kinds in the code [25, 26]. More-
over, SATs are widely adopted in many research studies
in order to evaluate the code quality [10, 27, 23] and iden-
tify issues in the code [16, 17, 18]. Some studies demon-
strated that some rules detected by SATs can be effective
for identifying issues in the code [14, 28, 18]. However,
evaluating the performance in defect prediction, results
are discordant comparing different tools (e.g. FindBugs3.4
and PMD3.5) [29].

Rutar et al. [25] compared five bug-finding tools for
Java (Bandera3, ESC/Java24, FindBugs5, JLint6, and
PMD7), that use syntactic bug pattern detection, on
five projects, including JBoss 3.2.38 and Apache Tomcat
5.0199. They focused on the different rules (also called
rules) provided by each tool, and their results demonstrate
some overlaps among the types of errors detected, which
may be due to the fact that each tool applies different
trade-offs to generate false positives and false negatives.
Overall, they stated that rules provided by the different
tools are not correlated with each other. Complementing
the work by Rutar et al. [25], we calculated the agreement
of SATs on TD identification. In addition, we investigated
the precision with which these tools output rules. Finally,
we also investigated the types of TD items that can actu-
ally be detected by existing SATs.

Tomas et al. [26] performed a comparative analysis by
In total, they
means of a systematic literature review.
compared 16 Java code SATs, including JDepend10, Find-
Bugs3.4, PMD3.5, and SonarQube??. They focused on in-
ternal quality metrics of a software product and software
tools of static code analysis that automate measurement
of these metrics. As results, they reported the tools’ detec-
tion strategies and what they detect. For instance, most of

2 https://checkstyle.sourceforge.io/
3http://bandera.projects.cs.ksu.edu/
4https://kindsoftware.com/products/opensource/ESCJava2/
5 http://findbugs.sourceforge.net/
6 http://jlint.sourceforge.net/
7 https://pmd.github.io/
8http://www.jboss.org/
9http://jakarta.apache.org/tomcat
10https://github.com/clarkware/jdepend

2

them automate the calculation of internal quality metrics,
the most common ones being code smells, complexity, and
code size [26]. However, they did not investigate agree-
ment between the tools’ detection rules.

Avgeriou et al. [30] identified the available SATs for the
Technical Debt detection. They compared features and
popularity of nine tools investigating also the empirical
evidence on their validity. Results can help practitioners
and developers to select the suitable tool against the other
ones according to the measured information that satisfied
better their needs. However, they did not evaluate their
agreement and precision in the detection.

Focusing on developers’ perception on the SATs usage,
they can help to find bugs [10]. However, developers are
not sure about the usefulness of the rules [31, 32, 33], they
do pay attention to different rules categories and priori-
ties and remove violations related to rules with high sever-
ity [32] to avoid the possible risk of faults [31]. Moreover,
false positives and the way in which the rules are presented
are barriers to their wider adoption [10]. Some studies
highlighted the need to reduce the number of detectable
rules [34, 35] or summarize them based on similarities [32].
SATs are able to detect many defects in the code. How-
ever, some tools do not capture all the possible defect even
if they could be detected by the tools [36]. Even if some
studies since the beginning of 2010 highlighted the need
to better clarify the precision of the tools, differentiating
false positives from actionable rules [37, 38], many studies
deal with the many false positives produced by different
tools, such as FindBugs3.4 [36, 39, 40], JLint6, PMD3.5,
CheckStyle3.2, and JCSC11 [36].

The two closest works with respect to ours are those
by Mantere et al.
[5] and Wilander et al [6]. Both of
them investigated and compared existing security vulner-
ability SATs. More specifically, Mantere et al.
[5] exe-
cuted three SATs (Fortify SCA, Splint, and Frama-C) on
a project reporting the amount of violated security rules
without comparing their detection agreement. Wilander
et al [6] compared five SATs (Flawfinder, ITS4, RATS,
Splint, and BOON) and verified their detection capability
of four security vulnerabilities (Changing the flaw of con-
trol, Bugger overflow attacks, Buffer overflow vulnerabili-
ties, and Format string attacks) on 20 vulnerable functions
selected from ITS4’s vulnerability database. Differently
from our work, the two papers just discussed only focused
on security vulnerabilities. In addition, none of them per-
formed additional analyses aiming at shedding lights on
their detection agreement and precision. As such, our work
represents the first attempt to investigate the capabilities
of a large amount of static analysis tools under multiple
perspectives, providing researchers, practitioners, and tool
vendors with insights into (1) the features and types of is-
sues they detect; (2) the potential usefulness given by their
combination; and (3) the limitations in terms of precision.

11http://jcsc.sourceforge.net

3. Selection of the Static Analysis Tools

In this section, we describe the SATs we selected for
this work and their code quality issues detection capability.
In particular, we selected six SATs based on two main
observations. First and foremost, we selected the tools
that have been previously investigated by researchers in
the field with respect to their adoption [3, 32, 30] and
were found to be the most widely employed in practice [3].
In the second place, the selected tools were familiar to
the authors: such a familiarity allowed us to (1) use/run
them better (e.g., by running them without errors) and
(2) analyze their results better, for instance by providing
qualitative insights able to explain the reasons behind the
achieved results. The analysis of other tools is already
part of our future research agenda. Table 1 reports the
detection capability of each tool in terms of how many
rules can be detected, and the classification of internal
rules (e.g., type and severity). Moreover, we report the
diffusion of the rule in the selected projects.

3.1. Better Code Hub

Better Code Hub12 is a commonly used static analy-
sis tool that assesses code quality. The analysis is done
through the website’s API, which analyzes the repository
from GitHub. The default configuration file can be modi-
fied for customization purposes. Code quality is generally
measured based on structure, organization, modifiability,
and comprehensibility.

This is done by assessing the code against ten guide-
lines: write short units of code, write simple units of code,
write code once, keep unit interfaces small, separate con-
cern in modules, couple architecture components loosely,
keep architecture components balanced, keep your code
base small, automate tests, and write clean code. Out of
the ten guidelines, eight guidelines are grouped based on
type of severity: medium, high, and very high. Compli-
ance is rated on a scale from 1-10 based on the results13.
Better Code Hub static analysis is based on the anal-
ysis of the source code against heuristics and commonly
adopted coding conventions. This gives a holistic view of
the health of the code from a macroscopic perspective.

It detects a total of 10 rules, of which 8 are grouped
based on type and severity. Better Code Hub categorizes
the 8 rules under 3 types: RefactoringFileCandidateWith-
LocationList, RefactoringFileCandidate, and Refactoring-
FileCandidateWithCategory. Of these 8 rules, one is of
RefactoringFileCandidateWithLocationList type, six are of
RefactoringFileCandidate type, and one is of Refactor-
In addition to the
ingFileCandidateWithCategory type.
types, Better Code Hub assigns three possible severities
to the rules: Medium, High, and Very High. Of these eight
rules, four were classified as Medium severity, four as High

12https://bettercodehub.com/
13https://pybit.es/bettercodehub.html

3

Table 1: Detection capability of the six selected SATs. For each tool, the number of supported rules, the number of rules categories, the
number of severity levels and the description of severity levels are reported.

Tool

Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube

Detection Capability

Severity levels
# rule #Type group #Severity levels
Medium, High, and Very High
3
Error, Ignore, Info, and Rule
4
3
Low, Medium, and High
4 Of concern, Troubling, Scary, and Scariest
from 1 (most severe) to 5 (least severe)
5
Info, Minor, Major, Critical, and Blocker
5

10
173
130
424
305
413

3
14
-
9
8
3

severity, and eight as Very High severity. Some of the rules
have more than one severity possibly assigned to them.

3.2. Checkstyle

Checkstyle14 is an open-source tool that evaluates Java
code quality. The analysis is done either by using it as a
side feature in Ant or as a command line tool. Check-
style assesses code according to a certain coding standard,
which is configured according to a set of checks. Checkstyle
has two sets of style configurations for standard checks:
Google Java Style15 and Sun Java Style16. In addition to
standard checks provided by Checkstyle, customized con-
figuration files are also possible according to user pref-
erence.17 These checks are classified under 14 different
categories: annotations, block checks, class design, cod-
ing, headers, imports, javadoc comments, metrics, miscel-
laneous, modifiers, naming conventions, regexp, size vio-
lations, and whitespace. Moreover, the violation of the
checks are grouped under two severity levels: error and
rule18, with the first reporting actual problems and the
second possible issues to be verified.

It detects a total of 173 rules which are grouped based
on type and severity. Checkstyle categorizes the 173 rules
under 14 types: Annotations, Block Checks, Class Design,
Coding, Headers, Imports, Javac Comments, Metrics, Mis-
cellaneous, Modifiers, Naming Conventions, Regexp, Size
Violations, and Whitespace. Of these 173 rules, 8 are of
Annotations type, 6 are of Block Checks type, 9 are of
Class Design type, 52 are of Coding type, 1 is of Headers
type, 8 are of Imports type, 19 are of Javac Comments
type, 6 are of Metrics type, 16 are of Miscellaneous type,
4 are of Modifiers type, 16 are of Naming Conventions
type, 4 are of Regexp type, 8 are of Size Violations type,
and 16 are of Whitespace type. In addition to these types,
Checkstyle groups these checks under four different sever-
ity levels: Error, Ignore, Info, and rule. The distribution
of the checks with respect to the severity levels is not pro-
vided in the documentation.

14https://checkstyle.org
15https://checkstyle.sourceforge.io/google_style.html
16https://checkstyle.sourceforge.io/sun_style.html
17https://checkstyle.sourceforge.io/index.html
18https://checkstyle.sourceforge.io/checks.html

3.3. Coverity Scan

Coverity Scan19 is another common open-source static
analysis tool. The code build is analyzed by submitting
the build to the server through the public API. The tool
detects defects and vulnerabilities that are grouped by
categories such as: resource leaks, dereferences of NULL
pointers, incorrect usage of APIs, use of uninitialized data,
memory corruptions, buffer overruns, control flow issues,
error handling issues, incorrect expressions, concurrency
issues, insecure data handling, unsafe use of signed val-
ues, and use of resources that have been freed20. For each
of these categories, there are various issue types that ex-
plain more details about the defect. In addition to issue
types, issues are grouped based on impact: low, medium,
and high. The static analysis applied by Coverity Scan is
based on the examination of the source code by determin-
ing all possible paths the program may take. This gives a
better understanding of the control and data flow of the
code21. Coverity Scan’s total scope of detectable rules as
well as the classification is not known, since its documen-
tation requires being a client. However, within the scope
of our results, Coverity Scan detected a total of 130 rules.
These rules were classified under three severity levels: Low,
Medium, and High. Of these 130 rules, 48 were classified
as Low severity, 87 as Medium severity, and 12 as High
severity. Like Better Code Hub, some of Coverity Scan’s
rules have more than one severity type assigned to them.

3.4. FindBugs

FindBugs22 is a static analysis tool for evaluating Java
code, more precisely Java bytecode. Despite analyzing
bytecode, the tool is able to highlight the exact posi-
tion of an issue if also the source code is provided to the
tool 23. The analysis is done using the GUI, which is en-
gaged through the command line. The analysis applied
by the tool is based on detecting bug patterns. Accord-
ing to FindBugs, the bug patterns arise for the following
main reasons: difficult language features, misunderstood
API features, misunderstood invariants when code is mod-
ified during maintenance, and garden variety mistakes.24

19https://scan.coverity.com/
20https://scan.coverity.com/faq\#what-is-coverity-scan
21https://devguide.python.org/coverity
22http://findbugs.sourceforge.net
23http://findbugs.sourceforge.net/manual/gui.html
24http://findbugs.sourceforge.net/findbugs2.html

4

25 Such bug patterns are classified under 9 different cat-
egories: bad practice, correctness, experimental, interna-
tionalization, malicious code vulnerability, multithreaded
correctness, performance, security, and dodgy code. More-
over, the bug patterns are ranked from 1-20. Rank 1-4 is
the scariest group, rank 5-9 is the scary group, rank 10-
14 is the troubling group, and rank 15-20 is the concern
group26. It detects a total of 424 rules grouped based on
It categorizes the 424 rules under 9
type and severity.
types: Bad practice, Correctness, Experimental, Interna-
tionalization, Malicious code vulnerability, Multithreaded
correctness, Performance, Security, and Dodgy code. Of
these 424 rules, 88 are of Bad practice type, 149 are of
Correctness, 3 are of Experimental, 2 are of Internation-
alization, 17 are of Malicious code vulnerability, 46 are
of Multithreaded correctness, 29 are of Performance, 11
are of Security, and 79 are of Dodgy code. In addition to
these types, FindBugs ranks these ’bug patterns’ from 1-
20. Rank 1-4 is the scariest group, rank 5-9 is the scary
group, rank 10-14 is the troubling group, and rank 15-20
is the concern group.

3.5. PMD

PMD27 is a static analysis tool mainly used to evalu-
ate Java and Apex, even though it can also be applied
to six other programming languages. The analysis is
done through the command line using the tool’s binary
distributions. PMD uses a set of rules to assess code
quality according to the main focus areas: unused vari-
ables, empty catch blocks, unnecessary object creation,
and more. There are a total of 33 different rule set con-
figurations28 for Java projects. The rule sets can also
be customized according to the user preference29. These
rules are classified under 8 different categories: best prac-
tices, code style, design, documentation, error prone, multi
threading, performance, and security. Moreover, the vio-
lations of rules are measured on a priority scale from 1-5,
with 1 being the most severe and 5 being the least30.

PMD detects a total of 305 rules which are grouped
based on type and severity. PMD categorizes the 305 rules
under 8 types: Best Practices, Code Style, Design, Docu-
mentation, Error Prone, Multithreading, Performance, and
Security. Of these 305 rules, 51 are of Best Practices, 62
are of Code Style, 46 are of Design, 5 are of Documenta-
tion, 98 are of Error Prone, 11 are of Multithreading, 30
are of Performance, and 2 are of Security type. In addition
to the types, PMD categorizes the rules according to five
priority levels (from P1 “Change absolutely required” to
P5 “Change highly optional”). Rule priority guidelines for

25http://findbugs.sourceforge.net/factSheet.html
26http://findbugs.sourceforge.net/bugDescriptions.html
27https://pmd.github.io/latest/
28https://github.com/pmd/pmd/tree/master/pmd-java/src/

main/resources/rulesets/java

29https://pmd.github.io/latest/index.html
30https://pmd.github.io/latest/pmd$_$rules$_$java.html

default and custom-made rules can be found in the PMD
project documentation.31

3.6. SonarQube

SonarQube32 is one of the most popular open-source
static code analysis tools for measuring code quality is-
sues.
It is provided as a service by the sonarcloud.io
platform or it can be downloaded and executed on a pri-
vate server. SonarQube computes several metrics such as
number of lines of code and code complexity, and veri-
fies code compliance with a specific set of “coding rules”
defined for most common development languages. If the
analyzed source code violates a coding rule, the tool re-
ports an “issue”. The time needed to remove these issues
is called remediation effort.

SonarQube includes reliability, maintainability, and se-
curity rules. Reliability rules, also named Bugs, create
quality issues that “represent something wrong in the
code” and that will soon be reflected in a bug. Code smells
are considered “maintainability-related issues” in the code
that decrease code readability and code modifiability. It
is important to note that in the category “code smells”,
SonarQube actually includes some of the code smells pro-
posed by Fowler et al. [41].

SonarQube LTS 6.7.7 detects a total of 413 rules which
are grouped based on type and severity. SonarQube cat-
egorizes the 413 rules under 3 types: Bugs, Code Smells,
and Vulnerabilities. Of these 413 rules, 107 rules are classi-
fied as Bugs, 272 as Code Smells, and 34 as Vulnerabilities.
In addition to the types, SonarQube groups the rules un-
der 5 severity typers: Blocker, Critical, Major, Minor, and
Info. Considering the assigned severity levels, SonarQube
detects 36 Blocker, 61 Critical, 170 Major, 141 Minor, and
5 Info rules. Unlike Better Code Hub and Coverity Scan,
SonarQube has only one severity and classification type
assigned to each rule.

4. Empirical Study Design

We designed our empirical study according to the
guidelines defined by Wohlin [42]. The following section
describes the goals and specific research questions driv-
ing our empirical study as well as the data collection and
analysis procedures.

4.1. Goal and Research Questions

The goal of our empirical study is to compare state-
of-the-practice SATs with the aim of assessing their ca-
pabilities when detecting source code quality issues with
respect to (1) the types of problems they can actually iden-
tify; (2) the agreement among them, and (3) their preci-
sion. Our ultimate purpose is to enlarge the knowledge

31https://pmd.github.io/latest/
32http://www.sonarsource.org/

5

available on the identification of source code quality issues
with SATs from the perspective of both researchers and
tool vendors. The former are interested in identifying ar-
eas where the state-of-the-art tools can be improved, thus
setting up future research directions, while the latter are
instead concerned with assessing their current capabilities
and possibly the limitations that should be addressed in
the future to better support developers.

It is important to remark that the goal of the empiri-
cal study is to show and compare the capabilities of exist-
ing, widely used static analysis tools independently from
the types of analyses they perform while detecting poten-
tial concerns in source code. Indeed, we are interested in
benchmarking the most popular static analysis tools with
respect to their practical support provided by developers,
i.e., with respect to the issues they are able to uncover, the
potential gain provided by their combination, and their
overall precision. Our results are meant to inform prac-
titioners on how to benefit more from the capabilities of
existing static analysis tools, other than alerting them on
the potential drawbacks of blindly relying on these tools.
In addition, our findings might raise limitations that re-
searchers and tool vendors should consider to provide bet-
ter tools. More specifically, our goal can be structured
around three main research questions (RQs). As a first
step, we conducted a preliminary investigation aiming at
posing the basis for the additional analyses. The goal of
our first research question is to (i) analyze the features
the various tools make available, and (ii) determine how
many issues can be detected on the selected dataset—this
is important to understand whether the selected dataset
is actually useful to address the other research questions.

RQ1. How do the considered static analysis tools
compare in terms of functionalities and distribution of
source code quality issues?

Once we had characterized the tools with respect to
what they are able to identify, we proceeded with a finer-
grained investigation aimed at measuring the extent to
which SATs agree with each other. Regarding this aspect,
further investigation would not only benefit tool vendors
who want to better understand the capabilities of their
tools compared to others, but would also benefit practi-
tioners who would like to know whether it is worth using
multiple tools within their code base. Moreover, we were
interested in how the issues from different tools overlap
with each other. We wanted to determine the type and
number of overlapping issues, but also whether the over-
lapping is between all tools or just a subset.

RQ2. What is the agreement among different Static
Analysis Tools when detecting source code quality is-
sues?

Finally, we focused on investigating the potential ac-
curacy of the tools in practice. While they could output
numerous rules that alert developers of the presence of
potential quality problems, it is still possible that some
of these rules might represent false positive instances, i.e.,
that they wrongly recommend source code entities to be
refactored/investigated. Previous studies have highlighted
the presence of false positives as one of the main problems
of the tools currently available [10]; our study aims at cor-
roborating and extending the available findings, as further
remarked in Section 4.4.

RQ3. What is the precision of Static Analysis Tools?

All in all, our goal was to provide an updated view on
this matter and understand whether, and to what extent,
this problem has been mitigated in recent years or whether
there is still room for improvement.

4.2. Context of the Study

We selected projects from the Qualitas Corpus col-
lection of software systems (Release 20130901), using the
compiled version of the Qualitas Corpus [43]. There are
two main reasons leading to the selection of the Qualitas
Corpus dataset. First, it provides compiled versions of
software systems. This is a key requirement in our case,
as most of the static analysis tools considered in our study
require compiled code to be executed - the build phase
would have been extremely time-consuming and error-
prone, should have we relied on different datasets [44]. In
addition, the Qualitas Corpus dataset allowed us to per-
form analyses on a publicly available and well-established
source, which has been often used as a benchmark for soft-
ware quality studies [45, 46, 47]. As such, we preferred to
conduct the study on this dataset to provide researchers
with insights and findings that can be challenged by other
researchers by using the same dataset.

The dataset contains 112 Java systems with 754 ver-
sions, more than 18 million LOCs, 16,000 packages, and
200,000 classes. Moreover, the dataset includes projects
from different contexts such as IDEs, databases, and pro-
gramming language compilers. More information is avail-
able in [43]. In our study, we considered the recent (“r”)
release of each of the 112 available systems. Since two of
SATs considered, i.e., Coverity Scan and Better Code Hub,
require permissions in the GitHub project or the upload of
a configuration file, we privately uploaded all 112 projects
to our GitHub account in order to enable the analysis33.

4.3. Data Collection

This section describes the data collection from each
tool and the data collection process. We analyzed a single

33The GitHub projects, with the related configuration adopted
for executing the tools, will be made public in the case of acceptance
of this paper.

6

snapshot of each project, considering the release available
in the dataset for each of 112 systems.

SonarQube. We first installed SonarQube LTS 6.7.7
on a private server having 128 GB RAM and 4 processors.
However, because of the limitations of the open-source ver-
sion of SonarQube, we are allowed to use only one core,
therefore more cores would have not been beneficial for our
scope. We decided to adopt the LTS version (Long-Time
Support) since this is the most stable and best-supported
version of the tool.

Coverity Scan. The projects were registered in
Coverity Scan (version 2017.07) by linking the GitHub ac-
count and adding all the projects to the profile. Cover-
ity Scan was set up by downloading the tarball file from
https://scan.coverity.com/download and adding the
bin directory of the installation folder to the path in the
.bash profile. Afterwards the building process began,
which was dependent on the type of project in question.
Coverity Scan requires to compile the sources with a spe-
cial command. Therefore, we had to compile them, instead
of using the original binaries.

Better Code Hub.

The .bettercodehub.yml
files were configured by defining the component depth,
languages, and exclusions. The exclusions were de-
fined so that they would exclude all directories that were
not source code, since Better Code Hub only analyzes
source code.

Checkstyle. The JAR file for the Checkstyle anal-
ysis was downloaded directly from Checkstyle’s web-
site34 in order to engage the analysis from the com-
mand line. The executable JAR file used in this case was
checkstyle-8.30-all.jar. In addition to downloading
the JAR executable, Checkstlye offers two different types
of rule sets for the analysis34.

FindBugs. FindBugs 3.0.1 was installed by running
brew install findbugs in the command line. Once in-
stalled, the GUI was then engaged by writing spotbugs.
From the GUI, the analysis was executed through File →
New Project. The classpath for the analysis was identified
to be the location of the project directory.

PMD. PMD 6.23.0 was downloaded from GitHub35
as a zip file. After unzipping, the analysis was engaged by
identifying several parameters: project directory, export
file format, rule set, and export file name.

More details about the how install and ran the tools

are available in our replication package36.

4.4. Data Analysis

In this section, we describe the analysis methods em-

ployed to address our research questions (RQs).

34https://checkstyle.org/#Download
35https://github.com/pmd/pmd/releases/download/pmd$_

$releases\%2F6.23.0/pmd-bin-6.23.0.zip

Source code quality issues identified by the tools
(RQ1). To address this RQ, we first provide an overview
of the features and the issues detected by the tools. To
this aim, we consulted the tools’ documentation in order
to extract their main features. Specifically, we collected
the list of programming languages supported by each tool
and the typologies of issues they cover. As for the for-
mer, we simply reported programming language support
according to the documentation. For the latter case, in-
stead, we had to perform a qualitative analysis process [48]
by applying descriptive and pattern coding [49]. First, the
documentation of each tool was analyzed in order to ex-
tract the categories of issues covered. Then, two of the
authors performed a standardization of the categories to
ensure consistency and completeness of the coding process.
Finally, the categories referring to the same or similar con-
cept were grouped together.

Once having provided an overview of the tools features,
in order to determine the tool detection capabilities over-
laps, we also calculated how many issues are generated by
the rules violated in the reference dataset.

In the reminder of the paper, we will refer to all the
categories and types of rules and analysis checks performed
by SATs as “rule” and to the instances of rules violated in
the code as “issue”.

Agreement among the tools (RQ2).

In this re-
search question the goal is to inspect whether the tools are
similar in terms of the issues they detect. The assumption
is similar tools to have similar rules and, further, we ex-
pect similar rules to affect the same classes, and the same
lines of the code.

Tool similarity. Similar tools were identified by com-
paring all six tools with each other, meaning (cid:0)6
(cid:1) = 15 tool
pair comparisons. To determine the similarity of a tool
pair t1 and t2, we calculated the percentage of detected
issues that in both tools highlighted the same position in
the source code. The agreement value for tools t1 and t2
is defined below:

2

tool agreement(t1, t2) = #issues in the same position from t1 and t2

min (#issues from t1, #issues from t2)

(1)

The numerator is the number of times issues from t1
and t2 were detected in the same code position. The max-
imum of this number achieved when all issues generated
from one tool are always present with an issue from the
other tool, which is possible only for the tool that gen-
erated less issues. Therefore, the formula uses minimum
in the denominator. In the equation, #issues for t is the
total number of issues the tool has identified, therefore, it
is the sum of issues generated by all rules in tool t.

The overlap of the detected issues was determined by
analyzing all possible rule pairs from each tool pair. For
each rule pair (rm, rn), we iterated through all detected
instances of rm and checked whether an instance of rn
was affecting the same position. For calculating the tool
similarity, this data was aggregated to the tool level. For

7

example, in the data set used in this paper, SonarQube
had 275 rules and which generated issues while PMD had
180, resulting in 275·180 = 49, 500 possible rule pairs from
that tool pair. In total, we analyzed 339,169 rule pairs as
similar comparison was made for each tool pair (Table 5).
Rule similarity. In addition to tool similarity, we in-
vestigated the similarity of the individual rules from the
tools. The similarity of two rules is determined using the
percentage of the instances of a rule occurring together
with another rule. The agreement value for rule rm when
compared to rule rn is defined as below:

rule agreement(rm, rn) = #times rm and rn violated in the same position

#total violations of rm

(2)

The data for the numerator was obtained during the
data analysis for the tool agreement, and it has been de-
scribed there.
Note,

that the value is calculated separately for
both rules in a rule pair,
it is possible that
i.e.,
rule agreement(r1,r2) ̸= rule agreement(r2,r1). Therefore,
the perfect overlap is obtained if the agreement for both
rules is equal to one. This means that all the issues gen-
erated by s and r are always detected in the same classes
or position, and no issues are detected separately in a dif-
ferent class. Such measure was used as the granularity
of the rules differs greatly between the tools. For exam-
ple, BCH has only few wide rules like ”write clean code”
where as SonarQube has several smaller rules falling under
that rule. The lower granularity rules might always exist
with the wider rule as they both are meant to detect the
smaller issues but the wider rule exists also without the
smaller rule as it catches other issues as well.

Naturally, most of these rule pairs are not even meant
to be similar, they might never occur together or they
could be defined for a different level of granularity. How-
ever, we decided to inspect all possible rule pairs to make
the comparison as objective as possible. This would have
not been true, had we manually selected the inspected rule
pairs based on their description. We believe similar rules
should be found also by comparing all rules as similar rules
should consistently highlight the same positions of code.

In

the

comparisons.

both
of
Granularity
and tool agreement we have used
rule agreement
In
the term ”in the same position” in their definition.
this paper,
the comparisons were performed on two
granularity levels: class level and line level. On class level
the requirement was for the issues to be found in the
same class, regardless where in the class the issues were
located. Practically, we checked for each issue from one
tool whether the other tool had a issue in the same class.
However, on line level, in addition the issues being in the
same class, the lines affected by the issues had to overlap.
A third granularity option would have been method level
but, as several of the tools did not report it, it was not
used in the paper.

As the granularity of the rules varies between the tools,
we checked what fraction of the affected lines are over-

8

lapping between the issues, instead of requiring sufficient
overlap between both issues. To quantify the degree of
overlapping, we used the percentage of the lines inside the
comparison range. The results were grouped based on four
percentage thresholds: 100%, 90%, 80%, and 70%.

The concept is illustrated in Figure 1. The lines repre-
sent issues in a code file, indicating the start and end of the
affected code lines. issue BCH1 is the comparison issue to
which other issues are compared to. Depending on the
used threshold, different issues are selected based on the
overlapping percentage, as shown in the table associated
with the figure. For example, SQ1 would be always consid-
ered as a similar issue as it is completely ”inside” BCH1.
90% of P M D1 is within the comparison issue BCH1 and,
therefore, if the selected threshold is 90% or less it is listed
as a similar issue, otherwise it is discarded. However, as
less than 70% of CS1 and CS2 are overlapping with the
comparison issue, they will not be listed as a similar issue
regardless of the threshold.

As a final step, we manually inspected all the rules
with agreement 100 % to verify if they were related to
the same type of problem. For this purpose, two authors
having high expertise with SAT tools manually checked
all the 100 % matching rules applying open coding.
In
the case of disagreements, a third author helped to solve
the inconsistencies. The whole process lasted around three
hours.

⇓

Threshold
Comparison issue

Issues overlapping with
the comparison issue

100 % 90 %
BCH1
SQ1

SQ1
P M D1

80 %

70 %

SQ1
P M D1

SQ1
P M D1
SQ2

Figure 1: Determining issues in the same position as BCH1 at “line-
level” for thresholds 100%, 90 %, 80%, and 70%. (RQ2)

Precision of the tools (RQ3). In our last research
question, we aimed at assessing the precision of the con-
sidered tools. Since previous work already assessed the
accuracy of static analysis tools [10], with this analysis we
aimed at corroborating or contrasting the findings previ-
ously achieved.
In any case, it is worth remarking im-
mediately that, in the context of our study, we did not
consider the conventions used by the considered projects:
as such, we could not know if certain issues output by the
tools were actually relevant for developers or if they were
considered meaningless. Since the individual conventions
used by the projects are not always explicitly established
or easy to mine, we can only estimate the false positive rate
by looking at the precision of the tools, being aware of the

potential bias of this analysis. Nonetheless, we still believe
that an analysis of this type might be useful to researchers
and tool vendors to understand the extent to which the
issues output by tools can be considered reliable.st

From a theoretical point of view, precision is defined
as the ratio between the true positive issues identified by
a tool and the total number of issues it detects, i.e., true
positives plus false positive items (TPs + FPs). Formally,
for each tool we computed precision as follows:

precision =

T P s
T P s + F P s

(3)

It is worth remarking that our focus on precision is
driven by recent findings in the field that showed that the
presence of false positives is among the most critical bar-
riers to the adoption of static analysis tools in practice
[10, 3]. Hence, our analysis provides research community,
practitioners, and tool vendors with indications on the ac-
tual precision of the currently available tools—and aims
at possibly highlighting limitations that can be addressed
It is also important to remark that
by further studies.
we do not assess recall, i.e., the number of true positive
items identified over the total number of issues present in
a software project, because of the lack of a comprehensive
ground truth. We plan to create a similar dataset and per-
form such an additional evaluation as part of our future
research agenda.

When assessing precision, a crucial detail is related to
the computation of the set of true positive issues identified
by each tool. In the context of our work, we conducted a
manual analysis of the rules highlighted by the six con-
sidered tools, thus marking each of them as true or false
positive based on our analysis of (1) the issue identified
and (2) the source code of the system where the issue
was detected. Given the expensive amount of work re-
quired for a manual inspection, we could not consider all
the rules output by each tool, but rather focused on sta-
tistically significant samples. Specifically, we took into ac-
count a 95% statistically significant stratified sample with
a 5% confidence interval [50] of the 65,133, 8,828, 62,293,
402,409, 33,704, and 467,583 items given by Better Code
Hub, Coverity Scan, SonarQube, Checkstyle, FindBugs,
and PMD respectively: This step led to the selection of a
set of 375 items from Better Code Hub, 367 from Coverity
Scan, 384 from SonarQube, 384 from Checkstyle, 379 from
FindBugs, and 380 from PMD.

Using stratified sampling, the components of the tar-
get samples are separated into distinct groups or strata,
and within each stratum, they are similar to one another
and respect key relevant criteria of the initial sample (in-
cluding weights, in our case) [51]. Therefore, the selection
of a stratified sample already resolves the problem of hav-
ing different weights.
Indeed, this strategy intrinsically
ensures that the weights in the selected sample are consis-
tent with the ones in the original superset.

To increase the reliability of this manual analysis, two
of the authors of this paper having a high expertise with

Table 2: The selected samples to compute the Precision of the six
static analysis tools (RQ3)

SATs
Better Code Hub
Checkstyle
Coverity Scan
FindBugs
PMD
SonarQube

# samples
375
384
367
379
380
384

SAT tools (henceforth called the inspectors) first indepen-
dently analyzed the rule samples. They were provided
with a spreadsheet containing six columns: (1) the name
of the static analysis tool the row refers to, i.e., Better
Code Hub, Coverity Scan, Sonarqube, Checkstyle, Find-
Bugs, and PMD; (2) the full path of the rule identified by
the tool that the inspectors had to verify manually; and
(3) the rule type and specification, e.g., the code smell.
The inspectors’ task was to go over each of the rules and
add a seventh column in the spreadsheet that indicated
whether the rule was a true or a false positive. During
this analysis, the inspectors had to first understand the
context of the issue, namely the class or the project of in-
terest. As such, before analyzing a issue, they inspected
the project with the aim of having a general understand-
ing of the functionalities implemented. Afterwards, they
analyzed the specific class affected by a potential problem
raised by the issue and analyzed the content of the class
and, if needed, the content of the other classes called by
the class. This last step, namely the analysis of the class
dependencies, was required in just five cases; in the others,
the inspectors were able to assess the validity of a issue just
by looking at the source code of the affected class. Both
the inspectors were able to complete the entire process in
one week.

After this analysis, the two inspectors had a four-hour
meeting where they discussed their work and resolved any
disagreements: All the items marked as true or false pos-
itive by both inspectors were considered as actual true or
false positives; in the case of a disagreement, the inspec-
tors re-analyzed the rule in order to provide a common as-
sessment. Overall, after the first phase of inspection, the
inspectors reached an agreement of 0.84—which we com-
puted using Krippendorff’s alpha Krα [52] and which is
higher than 0.80, which has been reported to be the stan-
dard reference score for Krα [53]. Overall, the inspectors
individually spent, approximately, 160 person/hours.

In Section 5.3, we report the precision values obtained
for each of the considered tools and discuss some qualita-
tive examples that emerged from the manual analysis of
the sample dataset.

4.5. Replicability

In order to allow the replication of our study, we have

published the raw data in a replication package36.

36 https://figshare.com/s/5df8c271baa0368cd695

9

Table 3: Support for the top 15 programming languages according to the PYPL index. Results for all the programming languages supported
by the tools are reported in Appendix A.

Tool
Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube

Python Java Javascript C# C/C++ PHP R TypeScript Objective C Swift Go Matlab Kotlin Rust VBA

x

x

x

x
x
x
x
x
x

x

x

x
x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

x

Table 4: Typologies of issues spotted by the tools.

Tool
Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube

Syntax Bugs Security Design Bad practices

x
x

x

x
x
x

x

x
x

x
x
x
x
x
x

x

x
x
x
x

5. Analysis of the Results

In this section, we report and discuss the results ob-

tained when addressing our research questions (RQs).

5.1. Static Analysis Tools detected issues (RQ1)

Table 3 reports information about the tools’ support
for the top 15 programming languages, according to PYPL
classification37. The complete results, including all the
programming languages supported by the six tools are re-
ported in our Appendix A. As we can observe, the most
popular programming language is Java, which is the only
one supported by all the considered tools—this is one of
the reasons for the dataset selection in Section 4.2.

Other languages having high support by the selected
tools are Javascript, C/C#/C++, Objective C,
Swift, Go, and Kotlin, that are supported by Better
Code Hub, Coverity, and SonarQube (and also PMD for
Javascript).

Turning to the tools perspective, we can observe that
SonarQube is the one providing the best support for the
top 15 programming languages, covering 11 of them. Al-
most the same set of languages are also supported by Bet-
ter Code Hub and Coverity which support respectively 10
and 9 out of the top 15 programming languages.

The remaining three tools only focus on a very nar-
row set of programming languages. Specifically, Check-
style and Findbugs only support Java source code while
PMD provides support only for Java and Javascript.

Table 4 shows the categories of issues covered by the
subject tools. As a result of the coding process described
in Section 4.4, we came out with 5 categories, namely Syn-
tax, Bugs, Security, Design, Bad practices.

Results of our classification show that the selected tools
mainly deal with design concerns. They all capture design
issues and bad practices (excluding Checkstyle for the lat-
ter). Some of the tools also check for other characteristics

37https://pypl.github.io/PYPL.html

10

such as syntactic violations, and indicators of bugs/secu-
rity flaws.

As an overall observation, we can conclude that the
selected tools are mainly focused on the same characteris-
tics, hence justifying the empirical comparison subject of
our next two research questions.

We obtained results only for 47 projects out of the 112
contained in the Qualitas Corpus dataset, applying the
rules defined by Better Code Hub, Checkstyle, Coverity
Scan, FindBugs, PMD, and SonarQube. Unfortunately,
the used versions of Better Code Hub and Coverity Scan
were not able to analyze all the dataset. So, we considered
only the projects analyzed by all the six tools.

Table 5: Issues detected by the six SATs in the 47 projects (RQ1)

Tool

Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube

Detected rule
# rule # occurrences # type # severity
3
2
3
3
5
5

27,888
9,686,813
7,431
33,704
3,380,493
418,433

8
88
130
255
275
180

3
12
26
9
7
3

In total, the projects were infected by 936 rules vio-
lated 13,554,762 times (number of total issues). 8 (out
of 10) rules were detected by Better Code Hub 27,888
times, 88 (out of 173) rules were detected by Checkstyle
9,686,813 times, 130 rules were detected by Coverity Scan
7,431 times, 255 (out of 424) rules were detected by Find-
Bugs 33,704 time, 275 (out of 305) rules were detected by
PMD 3,380,493 times, and 180 (out of 413) rules were de-
tected by SonarQube 418.433 times (Table 6 and Table 5).
It is important to note that in Table 5, the detection capa-
bility is empty for Coverity. As mentioned earlier, the full
detection capability is only provided to clients and not on
the public API. We also computed how often rules were vi-
olated by grouping them based on type and severity. The
full results of this additional analysis are reported in our
replication package36.

Given the scope of rules that were detected, our
projects were affected by all rules that are detectable by
Better Code Hub and by some rules that are detectable
by Coverity Scan and SonarQube (Table 7). For the sake
of readability, we report only the Top-10 rules detected in
our projects by the six tools. The complete list is available
in the replication package36.

Table 6: Rule diffusion across the 47 projects (RQ1)

Project Name #Classes #Methods
2568
AOI
2019
Collections
1482
Colt
2941
Columba
683
DisplayTag
1079
Drawswf
962
Emma
4691
FindBugs
4857
Freecol
3460
Freemind
2404
Ganttproject
10701
Hadoop
5459
HSQLDB
9061
Htmlunit
644
Informa
1926
Jag
2197
James
4699
Jasperreports
689
Javacc
18239
JBoss
4918
JEdit
2804
JExt
3534
JFreechart
1350
JGraph
916
JGgraphPad
696
JGgraphT
4029
JGroups
455
JMoney
443
Jpf
5132
JRefactory
1028
Log4J
Lucene
10332
777
Marauroa
4455
Maven
Megamek
8754
5097
Myfaces core
269
Nekohtml
3116
PMD
8648
POI
1815
Proguard
Quilt
638
886
Sablecc
6719
Struts
670
Sunflow
477
Trove
6286
Weka
Xalan
4758
169,763
Total

865
646
627
1288
337
1031
509
1396
1569
1773
1093
3880
1284
3767
260
1234
4138
2380
269
7650
2410
2798
1152
314
433
330
1370
183
143
4210
674
4454
266
1730
3225
1922
82
1263
2276
1043
394
251
2598
227
421
2147
2174
74,486

SQ
10865
4545
7452
7030
853
3493
4451
12496
5963
5698
12349
24125
14139
5176
992
6091
6091
17575
3693
42190
15464
7185
6708
2577
2550
922
14497
575
522
18165
2042
11332
1228
3110
14974
22247
623
8818
19463
3203
1075
4385
8878
1549
454
32258
18362
418,433

BCH Coverity Checkstyle
250201
123
85501
25
172034
62
166062
70
32033
22
368052
65
68838
55
320087
134
127363
337
128590
112
71872
64
284315
665
192010
178
92998
141
11276
56
24643
56
336107
82
643076
226
24936
29
1084739
51
434183
134
276503
339
154064
88
98119
128
62230
10
23808
35
265886
391
15377
52
14736
21
207911
129
40206
125
627683
85
53616
33
225017
121
346070
321
619072
121
12987
13
109519
50
476488
771
115466
23
16840
13
30840
25
231912
57
32251
46
15507
78
365535
1437
232
330254
9,686,813
7,431

924
584
560
662
452
559
648
600
607
662
642
682
620
924
594
301
656
702
504
415
630
585
660
666
599
562
602
426
558
580
625
707
547
642
600
312
460
616
903
646
386
520
616
478
216
604
844
27,888

PMD FindBugs
1979
108458
185
39893
4
47843
1345
49068
32
10137
69
22264
16524
172
1068
90309
704
79588
1536
50873
898
36689
1547
228966
182
109625
467
59807
217
9364
408
19818
29253
25
1420
96000
39
17784
1158
377357
74
93605
125
42693
849
89284
41
22516
75
18777
11147
15
1560
89601
118
5639
20
7054
2633
116452
162
15463
585
233379
10681
148
1242
46620
3430
174680
790
174790
56
3979
543
47664
792
162045
6
37221
170
7488
101
19756
253
106513
63
20937
416
5430
4118
195774
1864
121685
33,704
3,380,493

Total
372550
130733
227955
224237
43529
394502
90688
424694
214562
187471
122514
540300
316754
159513
22499
51317
372214
758999
46985
1505910
544090
327430
251653
124047
84241
36489
372537
22187
22911
345870
58623
873771
66253
276752
540075
817332
18118
167210
660462
156565
25972
55627
348229
55324
22101
599726
473241
13,554,762

Finding 1. The selected tools share the same main
features. The amount of rules detected by the six
static analysis tools is significant (936 rules de-
tected 13,554,762 times); hence, we can proceed
with the analysis of the remaining RQs.

5.2. Static Analysis Tools Agreement (RQ2)

Our second research question focused on the analysis

of the agreement between the SATs.

Agreement based on the overlapping at “class-
level”. In order to include Coverity Scan in this analysis,
we first evaluated the detection agreement at “class-level”,
considering each class where the rule detected by the other
five tools overlapped at 100% and where at least one rule
of Coverity Scan was violated in the same class.

To calculate T ool similarity (column “%”, Table 8),
we checked the occurrences of the rules of both tools in
our projects, then we considered only the minimum value.
For example, in Table 8, calculating the percentage be-
tween Checkstyle - PMD rule pairs, we have 9,686,813
rules Checkstyle detected and 3,380,493 PMD ones de-
tected. The combination of these rule should be max-
imum 3,380,493 (the minimum value between the two).
We calculated the percentage considering the column “#
occurrences” and the column “# possible occurrences”.

The T ool similarity on the “class-level” is always low,
as reported in Table 8. This means that a piece of
code violated by a rule detected by one tool is almost
never violated by another rule detected by another tool.
In the best case (Table 8), only 9.378% of the possible
rule (FindBugs-PMD). Moreover, we did not investigate
T ool similarity at “class-level” considering more that two
tools (e.g. Checkstyle-FindBugs-PMD).

11

Table 7: The top-10 issues detected by Better Code Hub, Checkstyle, Coverity Scan, FindBugs, PMD, and SonarQube (RQ1)

Id

Id

Id

Id

Id

Better Code Hub Detected Rule
WRITE CLEAN CODE
WRITE CODE ONCE
WRITE SHORT UNITS
AUTOMATE TESTS
WRITE SIMPLE UNITS
SMALL UNIT INTERFACES
SEPARATE CONCERNS IN MODULES
COUPLE ARCHITECTURE COMPONENTS LOOSELY
Checkstyle Detected Rule
IndentationCheck
FileTabCharacterCheck
WhitespaceAroundCheck
LeftCurlyCheck
LineLengthCheck
RegexpSinglelineCheck
FinalParametersCheck
ParenPadCheck
NeedBracesCheck
MagicNumberCheck
Coverty Scan Detected Rule
Dereference null return value
Dm: Dubious method used
Unguarded read
Explicit null dereferenced
Resource leak on an exceptional path
Dereference after null check
Resource leak
DLS: Dead local store
Missing call to superclass
Se: Incorrect definition of serializable class
FindBugs Detected Rule
BC UNCONFIRMED CAST
DM NUMBER CTOR
BC UNCONFIRMED CAST OF RETURN VALUE
DM DEFAULT ENCODING
RCN REDUNDANT NULLCHECK OF NONNULL VALUE
DLS DEAD LOCAL STORE
DM FP NUMBER CTOR
SE NO SERIALVERSIONID
REC CATCH EXCEPTION
SE BAD FIELD
PMD Detected Rule
LawOfDemeter
MethodArgumentCouldBeFinal
CommentRequired
LocalVariableCouldBeFinal
CommentSize
DataflowAnomalyAnalysis
ShortVariable
UselessParentheses
BeanMembersShouldSerialize
ControlStatementBraces
SonarQube Detected Rule
The members of an interface declaration or class should appear in a pre-defined order
Sections of code should not be ”commented out”
Statements should be on separate lines

Id
S1213
S125
S00122
S00116 Field names should comply with a naming convention
S00117 Local variable and method parameter names should comply with a naming convention
S1166
S106
S1192
S134
S1132

Exception handlers should preserve the original exceptions
Standard outputs should not be used directly to log anything
String literals should not be duplicated
Control flow statements ”if”,”for”,”while”,”switch” and ”try” should not be nested too deeply
Strings literals should be placed on the left side when checking for equality

#
16,055
14,692
6,510
6,475
6,362
6,352
5,880
2,807
#
3,997,581
2,406,876
865,339
757,512
703,429
590,020
406,331
333,007
245,110
223,398
#
1,360
689
556
514
494
334
301
293
242
224
#
2,840
2,557
2,424
1,946
1,544
1,281
959
944
887
878
#
505,947
374,159
368,177
341,240
153,464
152,681
136,162
128,682
111,400
110,241
#
30,888
30,336
26,072
25,449
23,497
21,150
19,713
19,508
17,654
13,576

12

Table 8: Issue pairs that overlap at the “class-level” (RQ2)
%

occur-

issue pairs

Checkstyle - PMD
SonarQube - PMD
FindBugs - PMD
SonarQube - Checkstyle
FindBugs - Checkstyle
BCH-PMD
SonarQube - FindBugs
BCH-SonarQube
BCH-Checkstyle
BCH-FindBugs
Coverity - BCH
Coverity - Checkstyle
Coverity - FindBugs
Coverity - PMD
Coverity - SonarQube
Total

Checkstyle - PMD
SonarQube - PMD
FindBugs - PMD
SonarQube - Checkstyle
FindBugs - Checkstyle
BCH-PMD
SonarQube - FindBugs
BCH-SonarQube
BCH-CheckSyle
BCH-FindBugs
Total

#
rences
4,872
4,126
3,161
1,495
1,265
1,017
849
517
440
235
117
128
120
128
128
18,598

#
rences
4,872
4,126
3,161
1,495
1,265
1,017
849
517
440
235
17,977

# possible oc-
currences
3,380,493
418,433
33,704
418,433
33,704
27,888
33,704
27,888
27,888
27,888
7,431
7,431
7,431
7,431
7,431
4,457,178

0.144
0.98
9.378
0.357
3.753
3.646
2.518
1.853
1.577
0.842
1.574
1.723
1.615
1.723
1.723
0.417

# possible occur-
rences
3,380,493
418,433
33,704
418,433
33,704
27,888
33,704
27,888
27,888
27,888
4,430,023

0.144
0.98
9.378
0.357
3.753
3.646
2.518
1.853
1.577
0.842
0.4%

Table 9: Issue pairs that overlap at the 100% threshold considering
the “line-level” (RQ2)
issue pairs

occur-

%

For each rule pair we computed the detection agree-
ment at class level. For the sake of readability, we report
these results in Appendix A. Specifically, the three tables
(Table .13, Table .14, and Table .15) overview the detec-
tion agreement of each rule pair, according to the pro-
cedure described in Section 4.4. As further explained in
the appendix, for reasoning of space we only showed the
10 most recurrent pairs, putting the full set of results in
our replication package 36. In these tables, the third and
fourth columns (eg. “#BCH pairs” and “# CHS pairs”,
Table .13) report how many times a rule instance from a
tool exists with another one. The remaining two columns
report the agreement of each tool considered in the rule
pairs (eg. “#BCH Agr.” and “# CHS Agr.”, Table .13).
Results showed for all the rule pairs that the agreement at
“class-level” is very low, as none of the most recurrent rule
pairs agree well. The results also highlighted the difference
in the granularity of the rules.

Agreement based on the overlapping at the
“line-level”. Since we cannot compare at “line-level” the
rules detected by Coverity Scan, we could only consider the
remaining five SATs. Several rule pairs were found accord-
ing to the 100%, 90%, 80%, and 70% thresholds (Figure 1).
Using the threshold of 100% which indicates that a rule
completely resides within the comparison rule, we found
17,977 rule pairs, as reported in Table 9. Using the
thresholds of 90%, 80%, and 70% the following rule pairs

13

were found respectively: 17,985, 18,004, and 18,025 (Ta-
ble 10). These rules resided partially within the reference
rule.

Similarly to what happened with the agreement at
“class-level”, it is important to note that the overlap at
the “line-level” is always low. Results show that, also in
this case, only 9.378% of the possible rule occurrences are
detected in the same line by the same two tools (FindBugs
and PMD). In addition, also in this case we did find no
pair rules at “line-level” considering more that two tools
(e.g. Checkstyle-FindBugs-PMD).

When considering the agreement for each rule pair at
“line-level‘, we could not obtain any result because of com-
putational reasons.
Indeed, the analysis at line-level of
936 rule types that have been violated 13,554,762 times
would have required a prohibitively expensive amount of
time/space—according to our estimations, it would have
been taken up to 1.5 years—and, therefore, we preferred
excluding it.

Manual validation of the agreement based on
the overlapping at “class-level”. The manual inspec-
tion of the 66 rules with 100% agreement resulted into six
couples of rules from Checkstyle and PMD. It is interest-
ing to note that for all the other tools, rules with 100%
agreement were referred to totally different concepts. As
an example, none of the rules agreeing with 100% between
BCH and Coverity Scan were considered to be related to
the same quality issue. An example of a rule pair is BCH
“automate tests” that matches with Coverity Scan rule
“dead default in swich”. Table 11 reports the rules that
resulted to be related to the same quality issue.

Finding 2. The detection agreement among the
different tools is very low (less than 0.4%). The
rule pairs Checkstyle - PMD as the lowest over-
lap (0.144%) and FindBugs - PMD the highest one
(9.378%). Consequently also the detection agree-
ment is very low.

Finding 3. Among the 66 rules with 100% de-
tection agreement, only six are related to the same
quality issues.

5.3. Static Analysis Tools precision (RQ3)

In the context of our last research question, we focused
on the precision of the SATs when employed for potential
quality rules detection. Table 12 reports the results of our
manual analyses. As shown, the precision of most tools
is quite low, e.g., SonarQube has a precision of 18%, with
the only exception of CheckStyle whose precision is equal
to 86%.

Table 10: Issue pairs that overlap at the different thresholds, i.e., 90/80/70%, considering the “line-level” (RQ2)

issue pairs

Checkstyle - PMD
SonarQube - PMD
FindBugs - PMD
SonarQube - Checkstyle
FindBugs - Checkstyle
BCH-PMD
SonarQube - FindBugs
BCH-SonarQube
BCH-CheckSyle
BCH-FindBugs
Total

90%
#(%)
4,872 (0.144)
4,126 (0.986)
3,167 (9.39)
1,495 (0.357)
1,265 (3.753)
1,017 (3.646)
849 (2.519)
517 (1.853)
440 (1.577)
237 (0.849)
18,004 (0.4)

# occurrences
70%
#(%)
4,876 (0.144)
4,139 (0.989)
3,173 (9.41)
1,496 (0.357)
1,265 (3.753)
1,024 (3.647)
849 (2.519)
522 (1.868)
441 (1.578)
240 (0.860)
18,025 (0.4)

80%
#(%)
4,874 (0.144)
4,130 (0.987)
3,173 (9.41)
1,496 (0.357)
1,265 (3.753)
1,019 (3.646)
849 (2.519)
521 (1.868)
440 (1.577)
237 (0.849)
18,004 (0.4)

possible

3,380,493
418,433
33,704
418,433
33,704
27,888
33,704
27,888
27,888
27,888
4,430,023

Table 11: Rules with 100% agreement related to similar quality issue (RQ2)

Checkstyle
JavadocVariableCheck

PMD
CommentRequired

MissingJavadocMethodCheck

CommentRequired

StaticVariableNameCheck

VariableNamingConventions

NeedBracesCheck

ControlStatementBraces

ParameterNameCheck

FormalParameterNamingConventions

EmptyStatementCheck

EmptyIfStmt / EmptyWhileStmt

Manually validation
PMD Rule is more generic. Checkstyle refers to variables while
PMD to all elements.
PMD Rule is more generic. Checkstyle refers to methods while
PMD to all elements.
PMD Rule is more generic. Checkstyle only refers to static
variables. PMD to all variables.
Checkstyle rule is more generic. PMD only refers to control
statements. Checkstyle to all blocks.
PMD defines one rule for both local variables and formal pa-
rameters. Checkstyle and PMD define two separate rules.
PMD and Checkstyle define one rule for both if and while
statements. PMD defines two separate rules.

Table 12: Precision of the considered SATs over the manually vali-
dated sample set of rules (RQ3)

SAT
Better Code Hub
Checkstyle
Coverity Scan
FindBugs
PMD
SonarQube

# rules # True Positives Precision
29%
86%
37%
57%
52%
18%

375
384
367
379
384
384

109
330
136
217
199
69

In general, based on our findings, we can first corrobo-
rate previous findings in the field [7, 10, 8] and the observa-
tions reported by Johnson et al. [10], who found through
semi-structured interviews with developers that the pres-
ence of false positives represents one of the main issues that
developers face when using SATs in practice. With respect
to the qualitative insights obtained by interviewing devel-
opers [10], our work concretely quantifies the capabilities
of the considered SATs.

Looking deeper into the results, we could delineate
some interesting discussion points. First, we found that
for Better Code Hub and Coverity Scan almost two thirds
of the recommendations represented false alarms, while the
lowest performance was achieved by SonarQube. The poor
precision of the tools is likely due to the high sensitivity
of the rules adopted to search for potential issues in the
source code, e.g., threshold values that are too low lead
to the identification of false positive TD items. This is
especially true in the case of SonarQube: In our dataset,
it outputs an average of 47.4 violations per source code

14

class, often detecting potential TD in the code too hastily.
A slightly different discussion is the one related to the
other three SATs, namely PMD, FindBugs, and Check-
style.

As for the former, we noticed that it typically fails
when raising rules related to naming conventions. For
instance, this is the case of the ’AbstractName’ rule:
it
suggests the developer that an abstract class should con-
tain the term Abstract in the name. In our validation,
we discovered that in several cases the recommendation
was wrong because the contribution guidelines established
by developers explicitly indicated alternative naming con-
ventions. A similar problem was found when considering
FindBugs. The precision of the tool is 57% and, hence,
almost half of the rules were labeled as false positives. In
this case, one of the most problematic cases was related to
the ’BC UNCONFIRMED CAST’ rules: these are raised
when a cast is unchecked and not all instances of the type
casted from can be cast to the type it is being cast to. In
most cases, these rules have been labeled as false positives
because, despite casts were formally unchecked, they were
still correct by design, i.e., the casts could not fail any-
way because developers have implicitly ensured that all of
them were correct.

Finally, Checkstyle was the SAT having the highest
precision, i.e., 86%. When validating the instances out-
put by the tool, we realized that the rules raised are re-
lated to pretty simple checks in source code that cannot be
considered false positives, yet do not influence too much

the functioning of the source code. To make the reason-
ing clearer, let consider the case of the ’IndentationCheck’
rule: as the name suggests, it is raised when the inden-
tation of the code does not respect the standards of the
project. In our sample, these rules were all true positives,
hence contributing to the increase of the precision value.
However, the implementation of these recommendations
would improve the documentation of the source code but
not dealing with possible defects or vulnerabilities. As
such, we claim that the adoption of Checkstyle would be
ideal when used in combination with additional SATs.

To broaden the scope of the discussion, the poor per-
formance achieved by the considered tools reinforces the
preliminary research efforts to devise approaches for the
automatic/adaptive configuration of SATs [54, 55] as well
as for the automatic derivation of proper thresholds to
use when locating the presence of design issues in source
code [56, 57]. It might indeed be possible that the inte-
gration of those approaches into the inner workings of the
currently available SATs could lead to a reduction of the
number of false positive. In addition, our findings also sug-
gest that the current SATs should not limit themselves to
the analysis of source code but, for instance, complement-
ing it with additional resources like naming conventions
actually in place in the target software system.

Finding 4. Most of the considered SATs suf-
fer from a high number of false positive rules, and
their precision ranges between 18% and 57%. The
only expection is Checkstyle (precision=86%), even
though most of the rules it raises are related to doc-
umentation issues rather than functional problems
and, as such, its adoption should be complemented
with other SATs.

6. Discussion and Implications

The results of our study provide a number of insights
that can be used by researchers and tool vendors to im-
prove SATs. Specifically, these are:

There is no silver bullet. According to the results
obtained in our study, and specifically for RQ2, differ-
ent SAT rules are able to cover different issues, and can
therefore find different forms of source code quality prob-
lems: Hence, we can claim that there is no silver bullet that
is able to guarantee source code quality assessment on its
own. On the one hand, this finding highlights that practi-
tioners interested in detecting quality issues in their source
code might want to combine multiple SATs to find a larger
variety of problems. On the other hand, and perhaps more
importantly, our results suggest that the research commu-
nity should have an interest in and be willing to devise
more advanced algorithms and techniques that can im-
prove the detection capabilities of currently available tools.
As an example, we can envision a wider adoption of more

complex static analysis methods, e.g., taint tracking and
typestate, other than ensemble methods or meta-models
[58, 59, 60, 61], that can (1) combine the results from dif-
ferent SATs and (2) account for possible overlaps among
the rules of different SATs. This would allow the presen-
tation of more complete reports about the code quality
status of the software systems to their developers.

Learning to deal with false positives. One of the
main findings of our study concerns with the low per-
formance achieved by all SATs in terms of precision of
the recommendations provided to developers (RQ3). Our
findings represent the first attempt to concretely quantify
the capabilities of the considered SATs in the field. More-
over, our study provides two practical implications: (1) It
corroborates and triangulates the qualitative observations
provided by Johnson et al. [10], hence confirming that the
real accuracy of SATs is threatened by the presence of false
positives; (2) it supports the need for more research on how
to deal with false positives, and particularly on how to fil-
ter likely false alarms [62] and how to select/prioritize the
rules to be presented to developers [? 37, 28]. While some
preliminary research efforts on the matter have been made,
we believe that more research should be devoted to these
aspects. Finally, our findings may potentially suggest the
need for further investigation into the effects of false pos-
itives in practice: For example, it may be worthwhile for
researchers to study what the maximum number of false
positive instances is that developers can deal with, e.g.,
they should devise a critical mass theory for false positive
ASAT rules [63] in order to augment the design of existing
tools and the way they present rules to developers.

Complementing static analysis tools. The find-
ings from our RQ2 highlight that most of the issues re-
ported by the static analysis tools are related to rather
simple problems, like the writing of shorter units or the au-
tomation of software tests. These specific problems could
possibly be avoided if current SATs tools would be comple-
mented with effective tools targeting (1) automated refac-
toring and (2) automatic test case generation.
In other
words, our findings support and strongly reinforce the need
for a joint research effort among the communities of source
code quality improvement and testing, which are called to
study possible synergies between them as well as to devise
novel approaches and tools that could help practitioners
complement the outcome provided by SATs with that of
other refactoring and testing tools. For instance, with ef-
fective refactoring tools, the number of violations output
by SATs would be notably reduced, possibly enabling prac-
titioners to focus on the most serious issues. At the same
time, the opposite is true as well. Running a static ana-
lyzer on large projects might lead to have too many poten-
tial issues to address and this would make the resolution
of problems infeasible in practice. Yet, most projects still
employ static analyzers in a continuous integration con-
text [2] to adhere to the rules they care about.
In this
sense, static analyzers might be used to identify possible

15

refactoring opportunities and guide developers toward the
improvement of source code quality [64]. This point fur-
ther reinforces the need for a joint research effort toward
a better integration of static analysis tools and other soft-
ware engineering methods.

be an underestimation of the accuracy of the static anal-
ysis tools. We are aware of this limitation, yet we still
believe that the reported results might be interesting for
both developers and tool vendors, since they represent a
lower-bound validity of the tools in practice.

7. Threats to Validity

A number of factors might have influenced the results
reported in our study. This section discusses the main
threats to validity and how we mitigated them.

Construct Validity. Threats in this category con-
cern the relationship between theory and observation. A
first aspect is related to the dataset used.
In our work,
we selected 112 projects from the Qualitas Corpus [43],
which is one of the most reliable data sources in soft-
ware engineering research [65]. We are aware of the fact
that this dataset contains data collected in 2013, hence we
could have missed some newly introduced constructs (e.g.,
lambda expressions). This is a limitation of the study,
which we could not address because of time and compu-
tation constraints. Replications of our study on newer
systems might address this limitation and highlight new
insights on how static analysis tools work in practice.

Another possible threat relates to the configuration of
the SATs employed. None of the considered projects had
all the SATs configured and so we had to manually intro-
duce them; in doing so, we adopted the default configura-
tion of the tools. However, we are aware that different con-
figurations given directly by the developers of the projects
could affect the results.

Nevertheless,

it is important to point out that this
indeed, we were
choice did not influence our analyses:
interested in comparing the capabilities of existing tools
independently from their practical usage in the considered
systems. The problem of configuring the tools therefore
does not change the answers to our research questions.

Internal Validity. As for potential confounding fac-
tors that may have influenced our findings, it is worth
mentioning that some issues detected by SonarQube were
duplicated: in particular, in some cases the tool reported
the same issue violated in the same class multiple times.
To mitigate this issue, we manually excluded those cases
to avoid interpretation bias; we also went over the rules
output by the other SATs employed to check for the pres-
ence of duplicates, but we did not find any. Another rele-
vant threat concerns with the analysis of the precision of
the static analysis tools (RQ3). By design, we did not
analyze whether the considered projects established con-
ventions or internal policies to ignore some of the violated
rules raised by static analysis tools. This may have influ-
enced our findings because the reported precision might
not be consistent with the developer’s perception of the
accuracy of the tools. Nonetheless, mining conventions is
not always possible, since some of them are not explicitly
reported by developer. As such, the results of RQ3 might

16

External Validity. Threats in this category are con-
cerned with the generalization of the results. While we
cannot claim that our results fully represent every Java
project, we considered a large set of projects with differ-
ent characteristics, domains, sizes, and architectures. This
makes us confident of the validity of our results in the field,
yet replications conducted in other contexts would be de-
sirable to corroborate the reported findings.

Another discussion point is related to our decision to
focus only on open-source projects.
In our case, this
was a requirement: we needed to access the code base
of the projects in order to configure the SATs. Never-
theless, open-source projects are comparable—in terms of
source code quality—to closed-source or industrial appli-
cations [66]; hence, we are confident that we might have
obtained similar results by analyzing different projects.
Nevertheless, additional replications would provide further
complementary insights and are, therefore, still desirable.
Finally, we limited ourselves to the analysis of Java
projects, hence we cannot generalize our results to projects
in different programming languages. Therefore, further
replications would be useful to corroborate our results.

Conclusion Validity. With respect to the correct-
ness of the conclusions reached in this study, this has
mainly to do with the data analysis processes used. In the
context of RQ3, we conducted iterative manual analyses
in order to study the precision of the tools, respectively.
While we cannot exclude possible imprecision, we miti-
gated this threat by involving more than one inspector in
each phase, who first conducted independent evaluations
that were later merged and discussed. Perhaps more im-
portantly, we made all data used in the study publicly
available with the aim of encouraging replicability, other
than a further assessment of our results.

In RQ2 we proceeded with an automatic mechanism
to study the agreement among the tools. As explained in
Section 4.3, different SATs might possibly output the same
rules in slightly different positions of the source code, e.g.,
highlighting the violation of a rule at two subsequent lines
of code. To account for this aspect, we defined thresh-
olds with which we could manage those cases where the
same rules were presented in different locations.
In this
case, too, we cannot exclude possible imprecision; how-
ever, we extensively tested our automated data analysis
script. More specifically, we manually validated a subset
of rules for which the script indicated an overlap between
two tools with the aim of assessing whether it was correct
or not. This manual validation was conducted by one of
the authors of this paper, who took into account a random
sample of 300 candidate overlapping rules. In this sample,
the author could not find any false positives, meaning that

our script correctly identified the agreement among tools.
This further analysis makes us confident of the validity of
the findings reported for RQ2.

8. Conclusion

We performed a large-scale comparison of six popu-
lar static analysis tools (Better Code Hub, CheckStyle,
Coverity Scan, FindBugs, PMD, and SonarQube) with re-
spect to the detection of static analysis rules. We ana-
lyzed 47 Java projects from the Qualitas Corpus dataset,
and derived similar rules that can be detected by the tools.
We also compared their detection agreement at “line-level”
and “class-level”, and manually analyzed their precision.
Our future work includes an extension of this study
with the evaluation of the recall, and the in-vivo assess-
ment of the tools. Furthermore, we plan to conduct ad-
ditional investigations into how different types of static
analyses, e.g., taint tracking or typestate, can impact the
detection capabilities observed in our study.

Acknowledgments

The authors would like to thank the Associate Edi-
tor and anonymous reviewers for the feedback provided
during the review process. Fabio is partially supported
by the Swiss National Science Foundation - SNF Project
No. PZ00P2 186090. Furthermore, this work has been
partially supported by the EMELIOT national research
project, which has been funded by the MUR under the
PRIN 2020 program (Contract No. 2020W3A5FY).

References

[1] N. A. Ernst, S. Bellomo, I. Ozkaya, R. L. Nord, I. Gorton,
Measure it? Manage it? Ignore it? Software practitioners and
technical debt, Symposium on the Foundations of Software En-
gineering (2015) 50–60.

[2] F. Zampetti,

S. Scalabrino, R. Oliveto, G. Canfora,
M. Di Penta, How open source projects use static code analy-
sis tools in continuous integration pipelines,
in: Int. Conf. on
Mining Software Repositories (2017), pp. 334–344.

[3] C. Vassallo, S. Panichella, F. Palomba, S. Proksch, H. C. Gall,
A. Zaidman, How developers engage with static analysis tools
in different contexts, Empirical Software Engineering (2019)
1–39.

[4] T. W. Thomas, H. Lipford, B. Chu, J. Smith, E. Murphy-Hill,
What questions remain? an examination of how developers un-
derstand an interactive static analysis tool, in: Symposium on
Usable Privacy and Security (2016).

[5] M. Mantere, I. Uusitalo, J. Roning, Comparison of static code
analysis tools, in: Int. Conf. on Emerging Security Information,
Systems and Technologies (2009), pp. 15–22.

[6] J. Wilander, M. Kamkar, A comparison of publicly available
in: Workshop on Secure

tools for static intrusion prevention,
IT Systems (2002).

[7] N. Antunes, M. Vieira, Comparing the effectiveness of pene-
tration testing and static code analysis on the detection of sql
injection vulnerabilities in web services, in: International Sym-
posium on Dependable Computing (2009).

[8] R. K. McLean, Comparing static security analysis tools using
in: Int. Conf. on Software Security and

open source software,
Reliability (2012), pp. 68–74.

17

[9] M. A. Al Mamun, A. Khanam, H. Grahn, R. Feldt, Comparing
in: Third

four static analysis tools for java concurrency bugs,
Swedish Workshop on Multi-Core Computing (2010).

[10] B. Johnson, Y. Song, E. Murphy-Hill, R. Bowdidge, Why don’t
software developers use static analysis tools to find bugs?,
in:
2013 35th International Conference on Software Engineering
(ICSE 2013), IEEE, pp. 672–681.

[11] V. Lenarduzzi, A. Sillitti, D. Taibi, A survey on code anal-
ysis tools for software maintenance prediction,
in: Software
Engineering for Defence Applications - SEDA 2018, volume
925 of Advances in Intelligent Systems and Computing (AISC),
Springer-Verlag, 2019.

[12] S. Wagner, J. J¨urjens, C. Koller, P. Trischberger, Comparing
bug finding tools with reviews and tests, in: International Con-
ference on Testing of Communicating Systems (2005), p. 40–55.
[13] N. Nagappan, T. Ball, Static analysis tools as early indicators
of pre-release defect density, in: 27th International Conference
on Software Engineering (ICSE 2005), pp. 580–586.

[14] J. Zheng, L. Williams, N. Nagappan, W. Snipes, J. P. Hudepohl,
M. A. Vouk, On the value of static analysis for fault detection in
software, IEEE Transactions on Software Engineering 32 (2006)
240–253.

[15] M. G. Nanda, M. Gupta, S. Sinha, S. Chandra, D. Schmidt,
P. Balachandran, Making defect-finding tools work for you, in:
32nd ACM/IEEE International Conference on Software Engi-
neering - Volume 2 (ICSE 2010), p. 99–108.

[16] N. Saarim¨aki, V. Lenarduzzi, D. Taibi, On the diffuseness of
in: International

code technical debt in open source projects,
Conference on Technical Debt (TechDebt 2019).

[17] V. Lenarduzzi, A. Martini, D. Taibi, D. A. Tamburri, Towards
surgically-precise technical debt estimation: Early results and
International Workshop on Machine
research roadmap,
Learning Techniques for Software Quality Evaluation (2019),
MaLTeSQuE 2019, pp. 37–42.

in:

[18] V. Lenarduzzi, N. Saarim¨aki, D. Taibi, Some sonarqube issues
have a significant but smalleffect on faults and changes. a large-
scale empirical study, Journal of Systems and Software 170
(2020).

[19] C. Flanagan, K. R. M. Leino, M. Lillibridge, G. Nelson, J. B.
Saxe, R. Stata, Extended static checking for java,
in: Con-
ference on Programming Language Design and Implementation
(2002), p. 234–245.

[20] S. Heckman, L. Williams, A systematic literature review of
actionable alert identification techniques for automated static
code analysis, Information and Software Technology 53 (2011)
363 – 387. Special section: Software Engineering track of the
24th Annual Symposium on Applied Computing.

[21] M. Beller, R. Bholanath, S. McIntosh, A. Zaidman, Analyzing
the state of static analysis: A large-scale evaluation in open
source software,
in: 23rd International Conference on Soft-
ware Analysis, Evolution, and Reengineering (SANER 2016),
volume 1, pp. 470–481.

[22] D. Kong, Q. Zheng, C. Chen, J. Shuai, M. Zhu, Isa: A source
code static vulnerability detection system based on data fusion,
in: International Conference on Scalable Information Systems,
ICST (Institute for Computer Sciences, Social-Informatics and
Telecommunications Engineering), 2007.

[23] D. Marcilio, R. Bonif´acio, E. Monteiro, E. Canedo, W. Luz,
G. Pinto, Are static analysis violations really fixed? a closer
look at realistic usage of sonarqube, in: 27th International Con-
ference on Program Comprehension (ICPC 2019), p. 209–219.
[24] B. Lu, W. Dong, L. Yin, L. Zhang, Evaluating and integrating
diverse bug finders for effective program analysis,
in: L. Bu,
Y. Xiong (Eds.), Software Analysis, Testing, and Evolution
(2018), Cham, pp. 51–67.

[25] N. Rutar, C. B. Almazan, J. S. Foster, A comparison of bug
in: Symposium on Software Reliability

finding tools for java,
Engineering (2004), pp. 245–256.

[26] P. Tomas, M. J. Escalona, M. Mejias, Open source tools for
measuring the Internal Quality of Java software products. A
survey, Computer Standards and Interfaces 36 (2013) 244–255.

[27] M. Schnappinger, M. H. Osman, A. Pretschner, A. Fietzke,
Learning a classifier for prediction of maintainability based on
static analysis tools, in: 27th International Conference on Pro-
gram Comprehension (ICPC 2019), p. 243–248.

[28] V. Lenarduzzi, F. Lomio, H. Huttunen, D. Taibi, Are sonar-
International Conference on Soft-
qube rules inducing bugs?,
ware Analysis, Evolution and Reengineering (SANER) Preprint:
arXiv:1907.00376 (2019).

[29] F. Rahman, S. Khatri, E. T. Barr, P. Devanbu, Comparing
static bug finders and statistical prediction,
in: 36th Inter-
national Conference on Software Engineering (ICSE 2014), p.
424–434.

[30] P. Avgeriou, D. Taibi, A. Ampatzoglou, F. Arcelli Fontana,
T. Besker, A. Chatzigeorgiou, V. Lenarduzzi, A. Martini,
N. Moschou, I. Pigazzini, N. Saarim¨aki, D. Sas, S. Soares de
Toledo, A. Tsintzira, An overview and comparison of technical
debt measurement tools, IEEE Software (2021).

[31] D. Taibi, A. Janes, V. Lenarduzzi, How developers perceive
Information and

smells in source code: A replicated study,
Software Technology 92 (2017) 223 – 235.

[32] C. Vassallo, S. Panichella, F. Palomba, S. Proksch, A. Zaidman,
H. C. Gall, Context is king: The developer perspective on the
usage of static analysis tools, in: 25th International Conference
on Software Analysis, Evolution and Reengineering (SANER
2018), pp. 38–49.

[33] C. Sadowski, E. Aftandilian, A. Eagle, L. Miller-Cushon, C. Jas-
pan, Lessons from building static analysis tools at google, Com-
mun. ACM 61 (2018) 58–66.

[34] T. Muske, R. Talluri, A. Serebrenik, Repositioning of static
analysis alarms, in: 27th International Symposium on Software
Testing and Analysis (2018), p. 187–197.

[35] E. Bodden, Self-adaptive static analysis, in: 40th International
Conference on Software Engineering: New Ideas and Emerging
Results (ICSE 2018), p. 45–48.

[36] F. Thung, Lucia, D. Lo, L. Jiang, F. Rahman, P. T. Devanbu,
To what extent could we detect field defects? an extended em-
pirical study of false negatives in static bug-finding tools, Au-
tomated Software Engg. 22 (2015) 561–602.

[37] G. Liang, L. Wu, Q. Wu, Q. Wang, T. Xie, H. Mei, Auto-
matic construction of an effective training set for prioritizing
static analysis warnings, in: Int. Conf. on Automated software
engineering (ASE 2010), pp. 93–102.

[38] J. R. Ruthruff, J. Penix, J. D. Morgenthaler, S. Elbaum,
G. Rothermel, Predicting accurate and actionable static analy-
sis warnings: An experimental approach, in: 30th International
Conference on Software Engineering (ICSE 2008), p. 341–350.
[39] N. Ayewah, W. Pugh, The google findbugs fixit, in: 19th Inter-
national Symposium on Software Testing and Analysis (2010),
p. 241–252.

[40] N. Ayewah, D. Hovemeyer, J. D. Morgenthaler, J. Penix,
W. Pugh, Using static analysis to find bugs, IEEE Software 25
(2008) 22–29.

[41] M. Fowler, K. Beck, Refactoring: Improving the design of exist-
ing code, Addison-Wesley Longman Publishing Co., Inc. (1999).
[42] C. Wohlin, P. Runeson, M. H¨ost, M. Ohlsson, A. W. B. Reg-
nell, Experimentation in Software Engineering: An Introduc-
tion, 2000.

[43] R. M. Terra, L. F. Miranda, M. T. Valente, R. da Silva Bigonha,
Qualitas.class corpus: a compiled version of the qualitas corpus,
ACM SIGSOFT Software Engineering Notes 38 (2013) 1–4.
[44] M. Tufano, F. Palomba, G. Bavota, M. Di Penta, R. Oliveto,
A. De Lucia, D. Poshyvanyk, There and back again: Can you
compile that snapshot?, Journal of Software: Evolution and
Process 29 (2017) e1838.

[45] T. Lewowski, L. Madeyski, How far are we from reproducible
research on code smell detection? a systematic literature review,
Information and Software Technology 144 (2022) 106783.
[46] A. Singh, R. Bhatia, A. Singhrova, Taxonomy of machine learn-
ing algorithms in software fault prediction using object oriented
metrics, Procedia computer science 132 (2018) 993–1001.
[47] C. Tavares, M. Bigonha, E. Figueiredo, Analyzing the impact of

refactoring on bad smells, in: Proceedings of the 34th Brazilian
Symposium on Software Engineering (2020), pp. 97–101.
[48] C. Wohlin, P. Runeson, M. H¨ost, M. C. Ohlsson, B. Regnell,
A. Wessl´en, Experimentation in software engineering, Springer
Science & Business Media, 2012.

[49] J. Salda˜na, The coding manual for qualitative researchers, sage,

2021.

[50] M. Sandelowski, Sample size in qualitative research, Research

in nursing & health 18 (1995) 179–183.

[51] J. Neyman, On the two different aspects of the representative
method: the method of stratified sampling and the method of
purposive selection,
in: Breakthroughs in statistics, Springer,
1992, pp. 123–150.

[52] K. Krippendorff, Content analysis: An introduction to its

methodology, Sage publications, 2018.

[53] J.-Y. Antoine, J. Villaneau, A. Lefeuvre, Weighted krippen-
dorff’s alpha is a more reliable metrics for multi-coders or-
dinal annotations: experimental studies on emotion, opinion
and coreference annotation.,
in: 14th Conference of the Euro-
pean Chapter of the Association for Computational Linguistics
(2014), pp. 550–559.

[54] S. Nadi, T. Berger, C. K¨astner, K. Czarnecki, Mining config-
uration constraints: Static analyses and empirical results,
in:
International Conference on Software Engineering (ICSE 2014),
ACM, pp. 140–151.

[55] D. Di Nucci, F. Palomba, R. Oliveto, A. De Lucia, Dynamic
selection of classifiers in bug prediction: An adaptive method,
Transactions on Emerging Topics in Computational Intelligence
1 (2017) 202–212.

[56] M. Aniche, C. Treude, A. Zaidman, A. Van Deursen, M. A.
Gerosa, Satt: Tailoring code metric thresholds for different
in: International Working Conference
software architectures,
on Source Code Analysis and Manipulation (SCAM 2016), pp.
41–50.

[57] F. Fontana Arcelli, V. Ferme, M. Zanoni, A. Yamashita, Auto-
matic metric thresholds derivation for code smell detection, in:
International workshop on emerging trends in software metrics
(2015), pp. 44–53.

[58] G. Catolino, F. Ferrucci, An extensive evaluation of ensemble
techniques for software change prediction, Journal of Software:
Evolution and Process (2019) e2156.

[59] G. Catolino, F. Palomba, F. Fontana Arcelli, A. De Lu-
Improving change prediction
arXiv preprint

cia, A. Zaidman, F. Ferrucci,
models with code smell-related information,
arXiv:1905.10889 (2019).

[60] G. Catolino, F. Palomba, A. De Lucia, F. Ferrucci, A. Zaid-
man, Enhancing change prediction models using developer-
related factors, Journal of Systems and Software 143 (2018)
14–28.

[61] F. Palomba, M. Zanoni, F. Fontana Arcelli, A. De Lucia,
R. Oliveto, Toward a smell-aware bug prediction model, Trans-
actions on Software Engineering 45 (2017) 194–218.

[62] F. Fontana Arcelli, V. Ferme, M. Zanoni, Filtering code smells
International Conference on Software

detection results,
Engineering-Volume 2 (ICSE 2015), pp. 803–804.

in:

[63] P. E. Oliver, G. Marwell, Whatever happened to critical mass
theory? a retrospective and assessment, Sociological Theory 19
(2001) 292–311.

[64] N. Imtiaz, B. Murphy, L. Williams, How do developers act on
static analysis alerts? an empirical study of coverity usage, in:
2019 IEEE 30th International Symposium on Software Reliabil-
ity Engineering (ISSRE 2019), IEEE, pp. 323–333.

[65] E. Tempero, C. Anslow, J. Dietrich, T. Han, J. Li, M. Lumpe,
H. Melton, J. Noble, The qualitas corpus: A curated collec-
tion of java code for empirical studies, Asia Pacific Software
Engineering Conference (2010) 336–345.

[66] V. Lenarduzzi, D. Tosi, L. Lavazza, S. Morasca, Why do devel-
opers adopt open source software? past, present and future, in:
Open Source Systems, Springer International Publishing, 2019,
pp. 104–115.

18

Appendix A

In the following, we report more results achieved in
the context of RQ2. For each rules pair we computed
the detection agreement at class level as reported in Ta-
ble .13, Table .14, and Table .15, according to the process
described in Section 4.4. It is worth remarking that, for
the sake of readability, we only show the 10 most recur-
rent pairs. The results for the remaining thresholds are
reported in the replication package36.

19

Table .13: The 10 most recurrent rule pairs detected in the same class by the considered SATs and their corresponding agreement values
(RQ2)

SonarQube

FindBugs

#
SQ
pairs

#
FB
pairs

SQ
Agr.

FB
Agr.

CommentedOutCodeLine
S1155
S1186
S135
S1312
complex class
S1195
S1195
S1301
S1148

RV RETURN VALUE OF PUTIFABSENT IGNORED
RV RETURN VALUE OF PUTIFABSENT IGNORED
RV RETURN VALUE OF PUTIFABSENT IGNORED
RV RETURN VALUE OF PUTIFABSENT IGNORED
RV RETURN VALUE OF PUTIFABSENT IGNORED
RV RETURN VALUE OF PUTIFABSENT IGNORED
DM DEFAULT ENCODING
EI EXPOSE REP
LG LOST LOGGER DUE TO WEAK REFERENCE
FI NULLIFY SUPER

SonarQube

PMD

S1192
S2110
S2110
S2110
S2110
S2110
S2110
S2110
S2110
S2110

FinalizeOnlyCallsSuperFinalize
JUnit4SuitesShouldUseSuiteAnnotation
AvoidCatchingGenericException
AvoidCatchingNPE
AvoidPrintStackTrace
CloseResource
CommentSize
DataflowAnomalyAnalysis
JUnit4TestShouldUseBeforeAnnotation
ShortVariable

SonarQube

CheckStyle

S2252
S2200
S2123
S2123
S2123
S2123
S2200
S2200
S2200
S2200

CommentsIndentationCheck
NeedBracesCheck
RedundantModifierCheck
InvalidJavadocPositionCheck
RegexpSinglelineCheck
WhitespaceAroundCheck
EqualsHashCodeCheck
FileTabCharacterCheck
FinalParametersCheck
IndentationCheck

SonarQube

CoverityScan

S1244
S00105
S1125
S1126
S1132
S1149
S1151
S1172
S1213
S1226

Unexpected control flow
Use of hard-coded cryptographic key
Dead default in switch
Dead default in switch
Dead default in switch
Dead default in switch
Dead default in switch
Dead default in switch
Dead default in switch
Dead default in switch

CheckStyle

FindBugs

2
1
1
3
1
1
1
1
1
1

1
1
1
1
1
1
1
1
1
1

#
SQ
pairs

#
PMD
pairs

1
1
1
1
1
1
1
1
1
1

1
1
5
4
1
2
2
5
1
25

#
SQ
pairs

#
CHS
pairs

1
2
2
2
2
2
2
2
2
2

1
12
56
4
42
22
1
8
9
1

#

SQ
pairs

#
CS
pairs

2
1
4
2
1
1
8
4
26
7

2
1
1
1
1
1
1
1
1
1

#
CHS
pairs

#
FB
pairs

AvoidStarImportCheck
FinalParametersCheck

RedundantModifierCheck

DesignForExtensionCheck
NeedBracesCheck

JavadocVariableCheck
JavadocVariableCheck

WhitespaceAroundCheck
JavadocPackageCheck

MissingJavadocMethodCheck

Agr. means Agreement

SA FIELD SELF COMPUTATION
NP NONNULL FIELD NOT INITIALIZED IN CONSTRUC-
TOR
IC SUPERCLASS USES SUBCLASS DURING INITIALIZA-
TION
RV RETURN VALUE OF PUTIFABSENT IGNORED
TQ EXPLICIT UNKNOWN SOURCE VALUE REACHES -
NEVER...
RV RETURN VALUE OF PUTIFABSENT IGNORED
IC SUPERCLASS USES SUBCLASS DURING INITIALIZA-
TION
BIT IOR
IC SUPERCLASS USES SUBCLASS DURING INITIALIZA-
TION
FI MISSING SUPER CALL

8
3

1

8
28

8
1

10
1

149

2
1

1

1
1

1
1

1
1

1

1.000
1.000
1.000
1.000
1.000
1.000
0.001
0.001
1.000
1.000

PMD
Agr.

1.000
0.001
0.000
0.011
0.000
0.000
0.000
0.000
0.001
0.000

0.000
0.000
0.000
0.001
0.000
0.000
1.000
1.000
0.001
0.000

SQ
Agr.

0.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

SQ

Agr. CHS
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

SQ
Agr.

0.001
0.000
0.001
0.001
0.000
0.000
0.001
0.002
0.001
0.001

CHS
Agr.

0.000
0.000
0.002
0.000
0.000
0.000
0.002
0.000
0.000
0.000

CS
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

FB
Agr.

0.000
0.000

1.000
1.000

0.000

1.000

0.000
0.000

1.000
1.000

0.000
0.000

1.000
1.000

0.000
0.000

1.000
1.000

0.001

1.000

20

Table .14: The 10 most recurrent rule pairs detected in the same class by the considered SATs and their corresponding agreement values
(RQ2)

BetterCodeHub

CheckStyle

WRITE SIMPLE UNITS
WRITE SHORT UNITS
WRITE CODE ONCE
WRITE SIMPLE UNITS
WRITE SHORT UNITS
WRITE CODE ONCE
WRITE SHORT UNITS
WRITE SIMPLE UNITS
AUTOMATE TESTS
WRITE CODE ONCE

BetterCodeHub

AvoidEscapedUnicodeCharactersCheck
AvoidEscapedUnicodeCharactersCheck
AvoidEscapedUnicodeCharactersCheck
OperatorWrapCheck
OperatorWrapCheck
OperatorWrapCheck
IllegalTokenTextCheck
IllegalTokenTextCheck
IllegalTokenTextCheck
AtclauseOrderCheck

CoverityScan

AUTOMATE TESTS
SEPARATE CONCERNS IN MODULES
COUPLE ARCHITECTURE COMPONENTS LOOSELY
WRITE CLEAN CODE
WRITE SIMPLE UNITS
WRITE SHORT UNITS
WRITE CODE ONCE
WRITE SHORT UNITS
WRITE SIMPLE UNITS
AUTOMATE TESTS

Exception leaked to user interface
Unsafe reflection
AT: Possible atomicity violation
Use of hard-coded cryptographic key
Exception leaked to user interface
Exception leaked to user interface
Exception leaked to user interface
Unsafe reflection
Unsafe reflection
Dead default in switch

BetterCodeHub

FindBugs

#
BCH
pairs

1
1
1
1
1
1
4
4
2
30

#
BCH
pairs

2
2
2
20
2
2
2
2
2
2

#
CHS
pairs

29859
29859
29859
60694
60694
60694
418
418
418
210

#
CS
pairs

1
2
1
1
1
1
1
2
2
1

#
BCH
pairs

#
FB
pairs

WRITE CODE ONCE
WRITE SIMPLE UNITS
AUTOMATE TESTS
SMALL UNIT INTERFACES
WRITE SHORT UNITS
WRITE SHORT UNITS
SEPARATE CONCERNS IN MODULES
AUTOMATE TESTS
WRITE CLEAN CODE
AUTOMATE TESTS

ICAST BAD SHIFT AMOUNT
SA LOCAL SELF ASSIGNMENT INSTEAD OF FIELD
FI MISSING SUPER CALL
ICAST BAD SHIFT AMOUNT
INT VACUOUS BIT OPERATION
RV RETURN VALUE OF PUTIFABSENT IGNORED
EQ COMPARING CLASS NAMES
NP ALWAYS NULL EXCEPTION
RV RETURN VALUE OF PUTIFABSENT IGNORED
ICAST BAD SHIFT AMOUNT

12
2
3
12
6
4
2
2
4
3

8
1
1
8
1
1
1
1
1
8

BCH
Agr.

CHS
Agr.

0.000
0.000
0.000
0.000
0.000
0.000
0.001
0.001
0.000
0.002

BCH
Agr.

0.000
0.000
0.001
0.001
0.000
0.000
0.000
0.000
0.000
0.000

BCH
Agr.

0.001
0.000
0.000
0.002
0.001
0.001
0.000
0.000
0.000
0.000

0.529
0.529
0.529
0.312
0.312
0.312
0.306
0.306
0.306
0.306

CS
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

FB
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

BetterCodeHub

PMD

SEPARATE CONCERNS IN MODULES
WRITE CODE ONCE
SEPARATE CONCERNS IN MODULES
COUPLE ARCHITECTURE COMPONENTS LOOSELY
SMALL UNIT INTERFACES
WRITE CLEAN CODE
AUTOMATE TESTS
AUTOMATE TESTS
WRITE SHORT UNITS
WRITE SIMPLE UNITS

CheckStyle

FinalizeOnlyCallsSuperFinalize
FinalizeOnlyCallsSuperFinalize
AvoidMultipleUnaryOperators
AvoidMultipleUnaryOperators
FinalizeOnlyCallsSuperFinalize
InvalidLogMessageFormat
FinalizeOnlyCallsSuperFinalize
EmptyStatementBlock
EmptyStatementBlock
EmptyStatementBlock

CoverityScan

FinalParametersCheck
InvalidJavadocPositionCheck
NoWhitespaceAfterCheck
MissingJavadocMethodCheck
MagicNumberCheck
LineLengthCheck
JavadocVariableCheck
JavadocStyleCheck
JavadocMethodCheck
IndentationCheck

Agr. means Agreement

Unsafe reflection
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter
IP: Ignored parameter

#
BCH
pairs

#
PMD
pairs

BCH
Agr.

PMD
Agr.

2
4
3
3
4
2
2
2
2
4

1
1
2
2
1
1
1
160
160
160

#
CHS
pairs

#
CS
pairs

313
4
1
112
50
6
36
84
66
1152

2
2
2
2
2
2
2
2
2
2

0.000
0.000
0.001
0.001
0.001
0.000
0.000
0.000
0.000
0.001

CHS
Agr.

0.001
0.000
0.000
0.001
0.000
0.000
0.000
0.001
0.001
0.000

1.000
1.000
1.000
1.000
1.000
1.000
1.000
0.748
0.748
0.748

CS
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

21

0.000
0.000
0.015
0.000
0.000
0.000
0.001
0.000
0.000
0.000

CS
Agr.

1.000
1.000
0.010
1.000
1.000
1.000
1.000
0.500
0.013
0.250

CS
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

FB
Agr.

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

SQ
Agr.

1.000
1.000
0.667
0.667
0.667
0.667
0.667
0.500
0.500
0.500

1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000
1.000

FB
Agr.

0.001
0.004
1.000
0.000
0.012
0.011
0.001
1.000
1.000
1.000

PMD
Agr.

0.000
0.000
0.010
0.002
0.000
0.000
0.000
0.001
0.000
0.001

PMD
Agr.

0.000
0.002
0.001
0.000
0.000
0.000
0.000
0.000
0.000
0.000

BCH
Agr.

0.001
0.000
0.001
0.001
0.002
0.000
0.000
0.000
0.000
0.000

Table .15: The 10 most recurrent rule pairs detected in the same class by the considered SATs and their corresponding agreement values
(RQ2)

CheckStyle

PMD

FinalParametersCheck
RegexpSinglelineCheck
NoFinalizerCheck
VisibilityModifierCheck
AbbreviationAsWordInNameCheck
NoWhitespaceAfterCheck
VariableDeclarationUsageDistanceCheck
NeedBracesCheck
JavadocParagraphCheck
NonEmptyAtclauseDescriptionCheck

CoverityScan

AvoidMultipleUnaryOperators
AvoidMultipleUnaryOperators
FinalizeOnlyCallsSuperFinalize
InvalidLogMessageFormat
FinalizeOnlyCallsSuperFinalize
AvoidMultipleUnaryOperators
AvoidMultipleUnaryOperators
AvoidMultipleUnaryOperators
FinalizeOnlyCallsSuperFinalize
FinalizeOnlyCallsSuperFinalize

FindBugs

#
CHS
pairs

#
PMD
pairs

CHS
Agr.

PMD
Agr.

51
75
1
15
1
7
7
90
1
10

2
2
1
1
1
2
2
2
1
1

#CS
pairs

#FB
pairs

UCF: Useless control flow
Dead default in switch
DLS: Dead local store
UCF: Useless control flow
Unsafe reflection
UCF: Useless control flow
OGNL injection
Failure to call super.finalize()
REC: RuntimeException capture
USELESS STRING: Useless/non-informative string...

BC UNCONFIRMED CAST OF RETURN VALUE
DLS DEAD LOCAL STORE
NP ALWAYS NULL EXCEPTION
BC UNCONFIRMED CAST
NP LOAD OF KNOWN NULL VALUE
UCF USELESS CONTROL FLOW
RCN REDUNDANT NULLCHECK OF NONNULL VALUE
FI NULLIFY SUPER
RV RETURN VALUE OF PUTIFABSENT IGNORED
FI MISSING SUPER CALL

1
1
3
1
2
1
1
1
1
5

2
5
1
1
2
1
1
1
1
1

CoverityScan

PMD

Dead default in switch
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held
TLW: Wait with two locks held

FindBugs

DMI EMPTY DB PASSWORD
TESTING
ICAST BAD SHIFT AMOUNT
BIT IOR
BC IMPOSSIBLE DOWNCAST OF TOARRAY
LG LOST LOGGER DUE TO WEAK REFERENCE
QF QUESTIONABLE FOR LOOP
HRS REQUEST PARAMETER TO HTTP HEADER
ICAST BAD SHIFT AMOUNT
BIT IOR

SonarQube

S2275
S2275
S888
S888
S888
S888
S888
ObjectFinalizeOverridenCalls SuperFinalizeCheck
S2232
S2232

Agr. means Agreement

AvoidInstantiatingObjectsInLoops
ShortVariable
UseCorrectExceptionLogging
UseConcurrentHashMap
UnusedImports
UnnecessaryFullyQualifiedName
TooManyMethods
TooManyFields
StdCyclomaticComplexity
ProperLogger

PMD

LawOfDemeter
OnlyOneReturn
DataflowAnomalyAnalysis
SignatureDeclareThrowsException
ForLoopCanBeForeach
MethodArgumentCouldBeFinal
MethodArgumentCouldBeFinal
MethodArgumentCouldBeFinal
ConfusingTernary
ConfusingTernary

BetterCodeHub

COUPLE ARCHITECTURE COMPONENTS LOOSELY
AUTOMATE TESTS
COUPLE ARCHITECTURE COMPONENTS LOOSELY
WRITE CLEAN CODE
WRITE CODE ONCE
AUTOMATE TESTS
SEPARATE CONCERNS IN MODULES
AUTOMATE TESTS
SEPARATE CONCERNS IN MODULES
AUTOMATE TESTS

#
CS
pairs

#
PMD
pairs

1
1
1
1
1
1
1
1
1
1

1
10
3
5
21
2
1
1
2
2

#
FB
pairs

#
PMD
pairs

1
1
8
1
1
1
1
1
8
1

9
169
100
14
6
62
6
6
4
3

#
SQ
pairs

#
BCH
pairs

1
1
2
2
2
2
2
1
1
1

2
2
4
10
26
2
2
3
1
1

Table .16: Programming languages supported by the tools.

Tool
Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube
Tool
Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube
Tool
Better Code Hub
Checkstyle
Coverity
FindBugs
PMD
SonarQube

C
x

x

x

C
x

x

x

Shell Script Solidity

x

x

C++
x

x

x
Swift
x

x

x

Groovy
x

Go
x

x

Java
x
x
x
x
x
x

Javascript
x

Objective C
x

Perl
x

x

x
x

x

x

x
TypeScript
x

x

Kotlin VB.NET Salesforce.com Visualforce Modelica

x

x

x

x

x

x

x

x

XML

XSL

Terraform CloudFormation ABAP COBOL

CSS

Flex

HTML5

Python Ruby

x

x

x
PL

x

x

x
PL

Scala
x

x
x
Apache Velocity

x
x
RPG

x
T-SQL

x

VB6

x
x

x

x

x

x

x

x

x

x

x

x

x

22


