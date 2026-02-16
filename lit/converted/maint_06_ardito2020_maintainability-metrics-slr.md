Hindawi
Scientiﬁc Programming
Volume 2020, Article ID 8840389, 26 pages
https://doi.org/10.1155/2020/8840389

Review Article
A Tool-Based Perspective on Software Code Maintainability
Metrics: A Systematic Literature Review

Luca Ardito ,1 Riccardo Coppola,1 Luca Barbato,2 and Diego Verga1

1Politecnico di Torino Department of Control and Computer Engineering Turin, Turin, Italy
2Luminem, Turin, Italy

Correspondence should be addressed to Luca Ardito; luca.ardito@polito.it

Received 19 March 2020; Accepted 17 July 2020; Published 4 August 2020

Academic Editor: Daniela Briola

Copyright © 2020 Luca Ardito et al. 'is is an open access article distributed under the Creative Commons Attribution License,
which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly cited.

Software maintainability is a crucial property of software projects. It can be deﬁned as the ease with which a software system or
component can be modiﬁed to be corrected, improved, or adapted to its environment. 'e software engineering literature
proposes many models and metrics to predict the maintainability of a software project statically. However, there is no common
accordance with the most dependable metrics or metric suites to evaluate such nonfunctional property. 'e goals of the present
manuscript are as follows: (i) providing an overview of the most popular maintainability metrics according to the related lit-
erature; (ii) ﬁnding what tools are available to evaluate software maintainability; and (iii) linking the most popular metrics with the
available tools and the most common programming languages. To this end, we performed a systematic literature review, following
Kitchenham’s SLR guidelines, on the most relevant scientiﬁc digital libraries. 'e SLR outcome provided us with 174 software
metrics, among which we identiﬁed a set of 15 most commonly mentioned ones, and 19 metric computation tools available to
practitioners. We found optimal sets of at most ﬁve tools to cover all the most commonly mentioned metrics. 'e results also
highlight missing tool coverage for some metrics on commonly used programming languages and minimal coverage of metrics for
newer or less popular programming languages. We consider these results valuable for researchers and practitioners who want to
ﬁnd the best selection of tools to evaluate the maintainability of their projects or to bridge the discussed coverage gaps for newer
programming languages.

1. Introduction

Nowadays, software security and resilience have become
increasingly important, given how pervasive the software is.
Eﬀective tools and programming languages can

(i) discover mistakes earlier
(ii) reduce the odds of their occurrence
(iii) make a large class of common errors impossible by
restricting at compile time what the programmer
can do

Several best practices are consolidated in software en-
gineering, e.g., continuous integration, testing with code
coverage measurement, and language sanitization. All these
techniques allow the application of code analysis tools au-
tomatically, which can provide a signiﬁcant enhancement of

the source code quality and allow software developers to
eﬃciently detect vulnerabilities and faults [1]. However, the
lack of comprehensive tooling may render it challenging to
apply the same code analysis strategies to software projects
developed with diﬀerent languages or for diﬀerent domains.
'e literature deﬁnes software maintainability as the ease
with which a software system or component can be modiﬁed
to correct faults, improve performance or other attributes, or
adapt to a changing environment [2]. 'us, maintainability
is a highly signiﬁcant factor in the economic success of
software products. Several studies have described models
and frameworks, based on software metrics, to predict or
infer the maintainability of a software project
[3–5].
However, although many diﬀerent metrics have been pro-
posed by the scientiﬁc literature over the course of the last 40
years, the available models are very language- and domain-

2

Scientiﬁc Programming

speciﬁc, and there is still no accordance in the industry and
academia about a universal set of metrics to adopt to
evaluate software maintainability [6].

'is work aims at answering the primary need of
identifying evaluation frameworks for diﬀerent program-
ming languages, either aﬃrmed or newly emerged, e.g., the
Rust programming language, developed by Mozilla Research
as a language similar in characteristics to C++, but with
better code maintainability, memory safety, and perfor-
mance [7, 8].

'us, the ﬁrst goal of this paper is to ﬁnd which are the
most commonly mentioned metrics in the state-of-the-art
literature. We focused on static metrics since the analysis of
dynamic metrics (i.e., metrics collected during the execution
of adequately instrumented software [9]) was out of the
scope of this work.

'e second goal of the paper is to determine which tools
are more commonly used in the literature to calculate source
code metrics. Based on the mostly used tools, we then deﬁne
an optimal selections able to compute the most popular
metrics for a set of programming languages.

To pursue both goals we

(i) applied the systematic literature review (SLR)

methodology on a set of scientiﬁc libraries

(ii) performed a thorough analysis of all the primary
studies, available in the literature, about the topic of
software metrics for maintainability

Hence, this manuscript provides the following contri-

butions to researchers and practitioners:

(i) 'e deﬁnition of the most mentioned metrics that
can be used to measure software maintainability for
software projects

(ii) Details about closed-source and open-source tools
that can be leveraged by practitioners to evaluate the
quality of their software projects

(iii) Optimal sets of open-source tools that can be lev-

eraged to

investigate the computation of software metrics for
maintainability
adopt them in evaluation frameworks
adapt them to other programming languages that
are currently not supported

'e remainder of the manuscript is structured as follows:

(i) Section 2 describes the approach we adopted to

conduct our SLR

(ii) Section 3 presents a discussion of the results ob-

tained by applying such approach

(iii) Section 4 discusses the threats to the validity of the

present study

(iv) Section 5 provides a comparison of this study with

existing related work in the literature

(v) Section 6 concludes the paper and provides direc-

tions for future research

2. Research Method

In this section, we outline the method that we utilized to
realize this study. We performed a systematic literature
review (from now on, SLR), following the guidelines pro-
vided by Barbara and Charters [10] to structure the work and
report it in an organized and replicable manner.

An SLR is considered one of the key research meth-
odologies of evidence-based software engineering (EBSE)
[11]. 'e methodology has gained signiﬁcant attention from
software engineering researchers in recent years [12]. SLRs
all include three fundamental phases: (i) planning the review
(which includes specifying its goals and research questions);
(ii) conducting the review (which includes querying article
repositories, selecting the studies, and performing data
extraction); and (iii) reporting the review.

All those steps have been undertaken during this re-
search and are detailed in the following sections of this
paper.

2.1. Planning. According to Barbara and Charters guide-
lines, the planning phase of an SLR involves the identiﬁ-
cation of the need for the review (hence the deﬁnition of its
goals), the deﬁnition of the research questions that will guide
the review, and the development of the review protocol we
will use.

2.1.1. Goals. 'e need for the review, as said in the intro-
duction section, came from the need to improve the software
maintainability, in terms of clarity of its source code, while
implementing complex algorithms. Our primary objective
was to identify a dependable set of metrics widely used in the
literature and computed for software usage with available
tools.

'e objectives of our research are deﬁned by using the
Goal-Question-Metric paradigm by van Solingen et al. [13].
Speciﬁcally, we based our research on the following goals:

(i) Goal 1: have an overview of the most used metrics in

the literature in the last few years

(ii) Goal 2: ﬁnd what tools have been used in (or de-
scribed by) the literature about maintainability
metrics

(iii) Goal 3: ﬁnd a mapping between the most common
metrics and the tools able to compute them

2.1.2. Research Questions. Based on the goals deﬁned above,
our study entailed answering the research questions deﬁned
in the following:

(i) RQ1.1: what are the metrics used to evaluate code

maintainability available in the literature?
Our aim for this research question is to determine
what metrics are present in the literature and how
popular
they are in manuscripts about code
maintainability.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

3

(ii) RQ1.2: which of the metrics we found are the most

(ii) Co-change, to avoid considering manuscripts more

popular in the literature?
'is research question aims at characterizing the
diﬀerent metrics obtained from answering RQ1.1
based on their popularity and adoption.

(iii) RQ2.1: what tools are available to perform code

evaluation?
'e expected result of this research question is a list
of tools, both closed source and open source, along
with the metrics they can calculate.

(iv) RQ2.2: what is the ideal selection of tools able to
apply the most popular metrics for the most sup-
ported programming languages?
'is research question entails measuring the cov-
erage provided by the set of the most popular
metrics for each language and providing the optimal
set of tools that can compute those metrics.

2.1.3. Selected Digital Libraries. 'e search strategy involves
the selection of the search resources and the identiﬁcation of
the search terms. For this SLR, we used the following digital
libraries:

(i) ACM Digital Library
(ii) IEEE Xplore
(iii) Scopus
(iv) Web of Science

2.1.4. Search Strings. 'e formulation of the search strings is
crucial for the deﬁnition of the search strategy of the SLR.
According to the guidelines deﬁned by Kitchenham et al.,
the ﬁrst operation in deﬁning the search string involved an
analysis of the main keywords used in the RQs, their syn-
onyms, and other possible spellings of such words.

In this phase, all the researchers collaboratively selected
several pilot studies. 'e selected pilot studies are presented
in Table 1 and are related to the target research domain.

'ese studies are selected to be used to verify the
goodness of the research queries: the researchers should
review the queries if the pilot studies are not present after the
reﬁning phase.

'e starting keywords identiﬁed were software, main-
tainability, and metrics. 'e search string “software main-
tainability metric” was hence used to perform the ﬁrst search
on the selected digital libraries. Our results include articles
published between 2000 and 2019.

'is ﬁrst search pointed out that adding the code syn-
onym of the keyword software added a large numbers of
papers to the results.

Also, the following keywords were excluded from the
search to reduce the number of unﬁtting papers from the
results:

(i) Defect and fault, to avoid considering manuscripts
more related to the topic of veriﬁcation and vali-
dation, error-proneness, and software reliability
prediction, than to code maintainability

related to the topic of code evolution

(iii) Policy-driven and design,

to avoid considering
manuscripts more related to the deﬁnition and
usage of metrics used to design software, instead of
evaluating existing code

Table 2 reports the search queries before and after ex-
cluding the keywords listed above, for each of the chosen
digital libraries.

2.1.5. Inclusion and Exclusion Criteria. 'e ﬁnal phase of the
study selection uses the studies obtained by applying the
ﬁnal search queries detailed below.

'e following are the inclusion criteria used for the study

selection:

IC1: studies written in a language comprehensible by
the authors
IC2: studies presenting a new metric accurately
IC3: studies that present, analyze, or compare known
metrics or tools
IC4: detailed primary studies

On the other hand, in the following are deﬁned the

exclusion criteria:

EC1: studies written in a language not directly com-
prehensible by the authors, i.e., not written in English,
Italian, Spanish, or Portuguese
EC2: studies that present a novel metric, but not do not
describe it accurately
EC3: studies that do not describe or use metrics or tools
EC4: secondary studies (e.g., systematic literature re-
views, surveys, and mappings)

2.2. Conducting. After deﬁning the review protocol in the
planning phase, the conducting phase involves its actual
application, the selection of papers by application of the
search strategy, and the extraction of relevant data from the
selected primary studies.

2.2.1. Study Search. 'is phase consisted of gathering all the
studies by applying the search strings formulated and dis-
cussed in Section 2.1.4 to the selected digital libraries. To this
end, we leveraged the Publish or Perish (PoP) tool [17]. To aid
the replicability of the study, we report that we performed
the last search iterations at the end of October 2019. After the
application of the queries and the removal of the duplicate
papers on the four considered digital libraries, 801 unique
papers were gathered (see Table 3). 'e result of this phase is
a list of possible papers that must be subject to the appli-
cation of exclusion and inclusion criteria. 'is action allows
having a ﬁnal verdict for their selection as primary studies
for our SLR. We exported the mined papers in a CSV ﬁle
with basic information about each extracted manuscript.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License4

Scientiﬁc Programming

Authors

ID
[14] Ostberg and Wagner
[15]
[5]
[6]
[16]

Ludwig et al.
Kaur et al.
Sarwar et al.
Liu et al.

Table 1: Pilot studies.

Title
On automatically collectable metrics for software maintainability evaluation
Compiling static software metrics for reliability and maintainability from GitHub repositories
Software maintainability prediction by data mining of software code metrics
A comparative study of MI tools: deﬁning the roadmap to MI tool standardization
Evaluate how cyclomatic complexity changes in the context of software evolution

Year
2014
2017
2014
2008
2018

Table 2: Search strings for the selected digital libraries.

Before reﬁnement

After reﬁnement

+(“software”
“code”)+(metrics)+(maintainability)

+(“software” “code”)+(metrics)+(maintainability)-(defect)-
(fault)-(co-change)-(policy-driven)

Library
ACM
Digital
Library

IEEE Xplore

(((code OR software) AND metrics) AND
maintainability)

Scopus

Web of
Science

(code OR software) AND metrics AND
maintainability

(code OR software) AND metrics AND
maintainability

((((((((code OR software) AND metrics) AND maintainability) NOT defect)
NOT fault) NOT co-change) NOT policy-driven) NOT design)
code OR software AND metrics AND maintainability AND NOT fault AND
NOT defect AND NOT co-change AND NOT policy-driven AND NOT
design
code OR software AND metrics AND maintainability NOT fault NOT defect
NOT co-change NOT policy-driven NOT design

Table 3: Number of manuscripts collected from the selected digital libraries.

Library
ACM Digital Library
IEEE Xplore
Scopus
Web of Science
Total

Before reﬁnement
497
443
848
599
2387

After reﬁnement
152
215
381
300
1048

Without duplicates
—
—
—
—
801

2.2.2. Study Selection. 'e authors of this SLR carried the
paper selection process independently. To analyze the pa-
pers, we used a 5-point Likert scale, instead of dividing them
between the ﬁtting and unﬁtting. We performed the fol-
lowing assignation:

During this phase, we also applied the process of
snowballing. Snowballing refers to using the reference list of
the included papers to identify additional papers [18]. 'e
application of snowballing, for this speciﬁc SLR, did not lead
to any additional paper to take into consideration.

(i) One point to the papers that matched exclusion
criteria and did not match any inclusion criteria
(ii) Two points to papers that matched some exclusion

criteria and some inclusion criteria

(iii) 'ree points to papers that did not match any

criteria (neither exclusion or inclusion)

(iv) Four points to papers that matched some, but not

all, inclusion criteria

(v) Five points to papers that matched all inclusion

2.2.3. Data Extraction. In this phase, we read each identiﬁed
primary studies again, to mine relevant data for addressing
the formulated RQs. We have created a spreadsheet form to
be compiled for each of the considered papers, and that
contained the data of interest subdivided by the RQ they
concurred to answer. 'e data extraction phase, again, was
performed by all the authors of the papers in an independent
manner.

For each paper, we collected some basic context

criteria

information:

We analyzed the studies in two diﬀerent steps: ﬁrst, the
title and abstract for ﬁnding immediate compliance of the
paper to the inclusion and exclusion criteria. For papers that
received 3 points after reading the title and abstract, the full
text was read, with particular attention to possible usage or
deﬁnition or metrics throughout the body of the article. At
the end of the second read, none of the uncertain studies
were evaluated as ﬁtting with our research needs, and hence,
no other primary study was added to our ﬁnal pool.

(i) Year of publication
(ii) Number of times the paper was viewed fully and

number of citations

(iii) Authors and location of the authors

To answer RQ1.1, we needed to inspect the set of primary
studies to understand which metrics they deﬁned or men-
tioned. Hence, for each paper, we extracted the following
data:

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

5

(i) 'e list of metrics and metric suites utilized in each

paper

(ii) 'e programming languages and the family of
programming language (e.g., C-like and object ori-
ented) for which the used or proposed metrics can be
computed

To answer RQ1.2, we wanted to give an additional
classiﬁcation of the metrics, other than the number of
mentions. We took in consideration the opinion of the
authors on each of the metrics studied in their papers. 'is
allowed us to evaluate if a metric is considered useful or not
in most papers. 'is analysis allowed us to take into con-
sideration the popularity of the metrics by counting the
diﬀerence between positive and negative citations by
authors.

To answer RQ2.1, we needed to inspect the primary
studies to understand which tools they presented or used to
compute the metrics that were adopted. For each paper that
following
mentioned tools, we hence gathered the
information:

(i) 'e list of tools described, used, or cited by each

paper

(ii) When possible, the list of metrics that can be cal-

culated by each tool

(iii) 'e list of programming languages on which the

tool can operate

(iv) 'e type of the tool, i.e., the fact that the tool is open

source or not

Finally, to answer RQ2.2, we had to correlate the in-
formation gathered for the previous research questions. We
achieved this by ﬁnding the tool or tools covering the metrics
that proved to be the most popular among selected primary
studies.

2.2.4. Data Synthesis and Reporting. In this phase, we
elaborated the data extracted and synthesized previously to
obtain a response for each of the research questions we had.
Having all the data we needed, in the shape of a form per
paper analyzed, we proceeded with the data synthesis.

We gathered all the metric suites and the metrics we
found in tables, keeping track of the papers mentioning
them. We computed aggregate measures on the popularity
value assigned to each metric.

3. Results

'is section describes the results obtained to answer the
research questions described in Section 2.1.2. 'e appen-
dices of this paper report the complete tables with the
extracted data to improve the readability of this manuscript.
At the end of this phase, we collected a ﬁnal set of 43
primary studies for the subsequent phase of our SLR. Fig-
ure 1 reports the distribution over the considered time frame
of the selected papers, and Figure 2 indicates the distribution
of authors of related studies over the world. We report the
selected papers in Table 4. 'e statistic seems to suggest that

the interest in software maintainability metrics had grown
since 2008 and has increased in the latest years since 2016
(see barplot in Figure 1).

3.1. RQ1.1: Available Metrics. 'e papers selected as primary
studies for our SLR cited a total of 174 diﬀerent metrics. We
report all the metrics in Table 5 in the appendix. 'e table
reports

(i) the metric suite (empty if the metric is not part of

any speciﬁc suite)

(ii) the metric name (acronym, if existing, and a full

explanation, if available)

(iii) the list of papers that mention the metric. 'e last

two columns, respectively, report

(iv) the total number of papers mentioning the metric
(i.e., the number of studies in the third column)

(v) the score we gave to each metric

We computed the score in the following way:

(i) +1 if the study used (or deﬁned) the metric or the
authors of the study expressed a positive opinion
about it

(ii) −1 if the paper criticized the metric

By examining the last two columns of the metrics table, it
can be seen that the last two columns are most of the times
identical. 'is is because the majority of the papers we found
just utilize the metrics without commenting them, neither
positively or negatively.

It is immediately evident that some suites and metrics are
taken into consideration much more often than others. More
than 75% of the metrics are mentioned by just a single paper.
'e boxplots in Figure 3 show, in red, the distribution of the
total number of mentions and the score for all the considered
metrics. It is evident, from the boxplots, that the diﬀerence
between the two distribution is rather limited, conﬁrming
the vast majority of neutral or positive opinions when the
metrics are referenced in a research paper. Since only 24.7%
of the metrics are used by more than one of our selected
studies, the median values of both the measured indicators,
“TOT” and “Score”, are equal to 1 if the whole set of metrics
is considered.

In general, however, it is worth underlining that a low
score does not necessarily mean that the metric is of lesser
quality but instead that it is less known in the related lit-
erature. Another interesting thing to point out is that we did
not ﬁnd a particular metric that received many negative
scores.

3.2. RQ1.2: Most Mentioned Metrics. Since our analysis was
aimed at ﬁnding the most popular metrics, to extract a set of
them to be declined to diﬀerent languages, we were inter-
ested in ﬁnding metrics mentioned by multiple papers. In
Table 6 we report metrics that were used by at least two
papers among the selected primary studies. 'is operation
allowed us to reduce the noise caused by metrics that were

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License6

Scientiﬁc Programming

Figure 1: Distribution of papers per year, between 2000 and 2019.

Figure 2: Number of authors per nationality of aﬀerence.

mentioned only once (possibly in the papers where they were
originally deﬁned). After applying this ﬁlter, only 43 metrics
(the 24.7% of the original set of 174) remained. 'e boxplots
in Figure 3 show, in green, the distributions of the total
number of mentions and the measured score for this set of
metrics. On these distributions, the rounded median value
for the total number of mention is 3, and for the score is 3.
Since our ﬁnal aim in answering RQ1.2 was to ﬁnd a set
of most popular metrics for the maintainability of source
code, we resorted on selecting, on the complete set of 43
metrics mentioned in at least two papers, those whose score
was above the median.

With this additional ﬁltering, we obtained a set of 13
metrics and 2 metric suites, which are reported in Table 7.
Two suites were included in their completeness (namely, the
Chidamber and Kemerer suite and the Halstead suite) be-
cause all of their metrics had a number of total mentions and
score higher or equal to the median. For them, the table
reports the lower number of mentions and score among
those of the contained metrics. Instead, for the Li and Henry
suite, only the MPC (message passing coupling) metric
obtained a number of mention and score above the median
and hence was included in our set of selected most popular

metrics. A brief description of the selected most popular
metrics is reported in the following. 'e metrics are listed in
alphabetical order:

(i) CC (McCabe’s Cyclomatic Complexity). It is de-
veloped by McCabe in 1976 [56] and is a metric
meant to calculate the complexity of code by ex-
amining the control ﬂow graph of the program, i.e.,
counting its independent execution paths based on
the ﬂow graph [14]. 'e assumption is that the
complexity of the code is correlated to the number
of execution paths of its ﬂow graph. It is also
proved that there exists a linear correlation be-
tween the CC and the LOC metrics, as found by Jay
and Hale. Such relationship is independent from
the used programming language and code para-
digms [57].
Each node in the ﬂow graph corresponds to a block
of code in the program where the ﬂow is se-
quential; the arcs correspond to branches that can
be taken by the control ﬂow during the execution
of the program. Based on those building blocks, the
CC of a source code is deﬁned as M � e n + 2p

Authors2122001200220032004200520062007200820092010201120122013201420152016201720182019200002468Number of selected manuscripts 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

ID
[19]
[6]
[9]
[20]

[21]

[22]
[23]
[24]
[25]
[26]
[27]

Authors
K´ad´ar et al.
Sarwar et al.
Tahir and Ahmad
Gil et al.

Jain et al.

Curtis et al.
Chhillar and Gahlot
Tian et al.
Kaur et al.
Barbosa and Hirama
Misra et al.

[28] Rongviriyapanish et al.

[29]
[30]

[15]

Arshad and Tjortjis
Pizka

Ludwig et al.

Mamun et al.
Alves et al.

[31]
[32]
[33] Matsushita and Sasano
[34]
[16]
[35]

Silva et al.
Liu et al.
Ch´avez et al.

[36]

Ma et al.

Wahler et al.
Kaur and Singh
Yan et al.
Chatzidimitriou et al.
Bohnet and ollner
Ostberg and Wagner

[37]
[38]
[39]
[40]
[41]
[14]
[42] Narayanan Prasanth et al.
[43]
[44]
[45]
[46]
[47]
[5]
[48] Vytovtov and Markov
[49]
[50]
[51]
[52]

Wang et al.
Sjøberg et al.
Hindle et al.
Lee and Chang
Sinha et al.
Kaur et al.

Gold et al.
Ludwig et al.
Saboe
Yamashita et al.

[53]

[54]
[55]

'rem et al.

Gon¸calves et al.
Jermakovics et al.

7

Year Score
2016
2008
2010
2012

4
4
4
4

Clustering software metric values extracted from C# code for maintainability assessment 2016
2005

Table 4: Selected studies.

Title
A code refactoring dataset and its assessment regarding software maintainability
A comparative study of MI tools: deﬁning the roadmap to MI tools standardization
An AOP-based approach for collecting software maintainability dynamic metrics
An empirical investigation of changes in some software properties over time
An empirical investigation of evolutionary algorithm for software maintainability
prediction
An evaluation of the internal quality of business applications: does size matter?
An evolution of software metrics: a review
AODE for source code metrics for improved software maintainability
A proposed new model for maintainability index of open-source software
Assessment of software maintainability evolution using C&K metrics
A suite of object-oriented cognitive complexity metrics
Changeability prediction model for Java class based on multiple layer perceptron neural
network

Code normal forms
Compiling static software metrics for reliability and maintainability from GitHub
repositories
Correlations of software code metrics: an empirical study
Deriving metric thresholds from benchmark data
Detecting code clones with gaps by function applications
Detecting modularity ﬂaws of evolving code: what the history can reveal?
Evaluate how cyclomatic complexity changes in the context of software evolution
How does refactoring aﬀect internal quality attributes? a multiproject study
How multiple-dependency structure of classes aﬀects their functions: a statistical
perspective
Improving code maintainability: A case study on the impact of refactoring
Improving the quality of software by refactoring
Learning to aggregate: an automated aggregation method for software quality model
npm-miner: an infrastructure for measuring the quality of the npm registry
Monitoring code quality and development activity by software maps
On automatically collectable metrics for software maintainability evaluation
Prediction of maintainability using software complexity analysis: an extended FRT
Predicting object-oriented software maintainability using projection pursuit regression
Questioning software maintenance metrics: a comparative case study
Reading beside the lines: indentation as a proxy for complexity metric
Reusability and maintainability metrics for object-oriented software
Software complexity measurement using multiple criteria
Software maintainability prediction by data mining of software code metrics
Source code quality classiﬁcation based on software metrics
Spatial complexity metrics: an investigation of utility
Static software metrics for reliability and maintainability
'e use of software quality metrics in the materiel release process experience report
Using concept mapping for maintainability assessments
Using normalized compression distance to measure the evolutionary stability of software
systems
Using TDD for developing object-oriented software—A Case study
Visualizing software evolution with Lagrein

2016

2011
2017
2008
2014
2013
2018

2016

2017

2017
2010
2017
2010
2018
2017

2010

2016
2017
2017
2018
2011
2014
2008
2009
2012
2008
2000
2013
2014
2017
2005
2018
2001
2009

2015

2015
2008

4

4
4
5
4
5
5

4

4
4

5

5
4
4
4
5
4

4

4
4
4
4
4
4
4
4
5
4
4
4
5
4
4
5
4
5

4

4
4

where n is the number of nodes of the graph, e is
the number of edges of the graph, and p is the
number of connected components, i.e., the num-
ber of exits from the program logic [6].

(ii) CE (Eﬀerent Coupling). It is a metric that measures
how many data types the analyzed class utilizes,
apart from itself. 'e metric takes into consider-
ation the known type inheritance, the interfaces
the
implemented by the class,

the types of

parameters of its methods, the types of the declared
attributes, and the types of the used exceptions.

(iii) CHANGE (Number of Lines Changed in the Class).
It is a change metric, which measures how many
lines of code are changed between two versions of
the same class of code. 'is metric is hence not
deﬁned on a single version of the software project,
but it is tailored to analyze the evolution of the
source code. 'e assumption between the usage of

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License8

Metric suite
—
—
Aspect-based
metrics
Aspect-based
metrics
Aspect-based
metrics
Aspect-based
metrics
Aspect-based
metrics
—
—
—
—
—
—
—
—
—
—

—

—
—
—
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
—
—
—
—
Code smells
Code smells
—
—
—
—
—
—
—
—
—
—
—
—
—
—
—

Table 5: Metric studies (complete).

Metric
Aggregate stability
AODE, aggregating one dependence estimators

DCP, degree of crosscutting per pointcut

NAA, number of advices per aspect

Number of aspects

NPA, number of pointcuts per aspect

RAD, response for advice

Avg CC, average cyclomatic complexity
Avg. LOC per method
Bandwidth
Base classes (IFANIN)
Branching complexity (Sneed Metric)
Branch stability
Bug patterns
CA, aﬀerent coupling
CAM, cohesion among methods of a class
CBM, coupling between methods

CC, McCabe’s cyclomatic complexity

CE, eﬀerent coupling
CHANGE, number changed in the class
CHC, class coupling complexity

CBO, coupling between objects

DIT, depth of inheritance tree

LCOM, lack of cohesion in methods

NOC, number of children

RFC, response for class

WMC, weighted methods per class

CI, clone instances
CLOC, comment lines of code
Clone coverage
Cocol’s metric
Feature Envy (# per KLOC of code)
God Class (# per KLOC of code)
Code-to-comment ratio
Complexity average by class
Complexity average by ﬁle
Complexity average by function
CONS, number of constructors
Coupling and cohesion
Coupling dispersion
Coupling intensity
CPC, class coupling complexity
CSA, class size (attributes)
CSO, class size (operations)
CSOA, class size (operations + attributes)
Cyclic, number of cyclic dependencies
Cyclomatic complexity in classes
Cyclomatic complexity in functions

Scientiﬁc Programming

TOT Score

Papers using it
[53]
[24]

[23]

[23]

[23]

[23]

[23]

[5, 54]
[54]
[24]
[35]
[35]
[53]
[14]
[5, 21]
[21]
[21]
[14, 24, 44, 51], [6, 16, 32, 44, 48],
[23, 29, 31, 35, 47]
[5, 21, 25]
[5, 25, 26, 43]
[46]
[5, 14, 15, 25, 26], [21, 27, 32, 44],
[20, 28, 36, 39], [23, 29, 35, 47, 50]
[5, 14, 26, 43, 44], [20, 21, 27, 32],
[23, 28, 29, 39], [35, 47]
[5, 14, 26, 43, 44], [20, 27, 28, 32],
[23, 36, 39, 46, 47]
[5, 14, 26, 43, 44], [20, 27, 32, 39],
[23, 29, 35, 47]
[5, 15, 19, 26, 43], [14, 21, 27, 44],
[20, 29, 32, 39], [23, 46, 47, 50]
[5, 21, 26, 43, 44], [16, 20, 27, 32],
[23, 29, 39, 47]
[19]
[5, 24, 25, 28, 44], [35]
[14]
[48]
[44]
[44]
[14, 15]
[31]
[31]
[31]
[5, 25]
[14]
[35]
[35]
[46]
[5, 25]
[5, 25]
[5, 25]
[25]
[31]
[31]

1
1

1

1

1

1

1

2
1
1
1
1
1
1
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

2
1
1
1
1
1
1
2
1
1

14

12

3
4
1

18

15

14

13

17

13

1
6
1
1
1
1
2
1
1
1
3
1
1
1
1
2
2
2
1
1
1

3
4
1

16

13

12

11

15

11

1
6
1
1
1
1
2
1
1
1
1
1
1
1
1
2
2
2
1
1
1

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

Table 5: Continued.

Metric suite
—
—
—
—
—
—
—
—
—
Dynamic metrics
Dynamic metrics
Dynamic metrics
—
—
—
—
Halstead
Halstead
Halstead
Halstead
Halstead
Halstead
History sensitive
metrics
History sensitive
metrics
History sensitive
metrics
History sensitive
metrics
History sensitive
metrics
History sensitive
metrics
—
—
—
—
—
—
—
—
—
—
—
—
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)

Metric
DAM, data access metric (Card Metric)
Data complexity (Chapin Metric)
Dataﬂow
Dcy, number of dependencies
Dcy∗, number of transitive dependencies
Decisional complexity (McClure)
Divergent change
Dominator tree metrics
Dpt, number of dependents
DCBO, dynamic coupling between objects
MTBF, mean time between failure
MTTF, the mean time to failure
ECC, external class complexity (CIC + ICP)
Essential complexity
Fan-in
Fan-out
Halstead bugs (B)
Halstead diﬃculty (D)
Halstead eﬀort (E)
Halstead length (N)
Halstead vocabulary (n)
Halstead volume (V)

Papers using it
[21, 47]
[35]
[14]
[5]
[5]
[35]
[34]
[20]
[5]
[9]
[9]
[9]
[46]
[35]
[35]
[35]
[5, 14, 23, 25, 48], [47]
[5, 14, 25, 44, 51], [23, 47, 48]
[5, 14, 25, 44, 51], [23, 47, 48]
[5, 14, 24, 25, 51], [23, 44, 47, 48]
[5, 14, 25, 44, 51], [23, 47, 48]
[5, 14, 25, 44, 51], [6, 23, 44, 47, 48]

pLOC

rdocLOC

rniLOC

rpdLOC

rpiLOC

TL

I, instability
IC, inheritance coupling
ICC, internal class complexity (CAC + CMC)
Indentation as proxy for complexity metric
Inner∗, number of inner classes
Jensen’s Nf
JLOC, JavaDoc lines of code
Kaur’s metric
LCOM2, lack of cohesion in methods
LCOM3, lack of cohesion of methods
Level, level order
Level∗, level order

DAC

DIT, depth of inheritance tree

LCOM, lack of cohesion in methods

[40]

[40]

[40]

[40]

[40]

[40]

[28]
[21]
[46]
[44]
[5]
[24]
[5, 25, 28]
[25]
[21, 29, 35]
[21, 35]
[5]
[5]

[39, 43]

[25]

[25]

MPC, message passing coupling

[25, 39, 43, 46]

NOC, number of children

NOM

RFC, response for a class

[25]

[39]

[25]

9

TOT Score

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
1
1
1
1
1
1
6
8
8
9
8
10

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
3
1
3
2
1
1

2

1

1

4

1

1

1

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
1
1
1
1
1
1
4
6
6
7
6
8

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
3
1
3
2
1
1

2

1

1

4

1

1

1

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License10

Metric suite
Li and Henry
(L&H)
Li and Henry
(L&H)
Li and Henry
(L&H)

—

—
—
—
—
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
Misra’s metrics
—
Mood’s metrics
Mood’s metrics
Mood’s metrics
Mood’s metrics
Mood’s metrics
Mood’s metrics
—
Narsimhan’s
metrics
Narsimhan’s
metrics
Narsimhan’s
metrics
—
—
—
—
—
—
—
—

—

—
—
—
—
—
—
—

—

—
—
—
—

Scientiﬁc Programming

Papers using it

TOT Score

Table 5: Continued.

Metric

SIZE2

SLOC, source lines of code

WMC, weighted method per class

LOC, lines of code

Logic
MC, method coupling
MFA, measure of functional abstraction
MI, maintainability index
AAC, average attributes per class
AC, attribute complexity
ACC, average class complexity
ACF, average coupling factor
AMC, average method complexity
AMCC, average method complexity per class
CLC, class complexity
CC, code complexity
CWC, coupling weight for a class
MC, method complexity
OMMIC, coupling
MOA, measure of aggregation
AHF, attribute hiding factor
AIF, attribute inheritance factor
CF, coupling factor
MHF, method hiding factor
MIF, method inheritance factor
PF, polymorphism factor
NAA, number of attributes added

AID, average interaction density

IID, incoming interaction density

OID, outgoing interaction density

Nesting depth
Nesting (Max Nest)
NIM, instance methods
NIV, instance variables
NOAC, number of operations added
NOI, number of outgoing invocations
NOOC, number of operations overridden
NOM, number of methods
Noncommenting lines of code (lines only containing
space, tab, and CR are ignored)
Noncommenting lines of new code
NOP, number of polymorphic methods
NOPA, number of public attributes
NPATH
NPM, number of public methods
Number of attributes added
Number of code characters
Number of classes (including nested classes, interfaces,
enums, and annotations)
Number of commands
Number of comment characters
Number of directories
Number of ﬁles

[39]

[25]

[25]

[15, 24–26], [14, 44, 51], [6, 21, 23, 31, 32],
[35, 50]
[14]
[46]
[21]
[6, 14, 25, 44, 51], [30]
[27]
[27]
[27]
[27]
[27]
[27]
[27]
[27]
[27]
[27]
[44]
[21, 28]
[23]
[23]
[23]
[23]
[23]
[23]
[25]

[23]

[23]

[23]

[14]
[35]
[35]
[35]
[5, 25]
[19]
[5]
[26, 28, 31, 43]

[31]

[31]
[28]
[35]
[32]
[5, 21, 28, 29]
[5]
[24]

[31, 35]

[5, 25]
[24]
[31]
[31, 33]

1

1

1

1

1

1

15

11

1
1
1
6
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

1

1
1
1
1
2
1
1
4

1

1
1
1
1
4
1
1

2

2
1
1
2

1
1
1
4
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

1

1
1
1
1
2
1
1
4

1

1
1
1
1
4
1
1

2

2
1
1
2

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

Table 5: Continued.

Metric suite
—
—
—
—
—
—
—
—
—
—
SM, structural
measures
SM, structural
Measures
SM, structural
Measures
—
—
—
—
—
—
—
—
—
—
—
—
—
—

—

—

Metric
Number of God Classes
Number of queries
Ocmax, maximum operation complexity
OSmax, maximum operation size
Override ratio
Paths
PDcy, number of package dependencies
RAM, RAM + CPU memory usage
RCI, ratio of cohesion interactions
Shotgun Surgery

OMMIC, coupling

TCC, tight class cohesion

WMC1, size of classes

Structure stability
Spatial complexity metrics
STAT, number of statements
TCLOC, total comment lines of code
Test results and coverage
TLLOC, total logical lines of code
TNOS, total number of statements
Token count
Total number of characters
Version distance
Version stability
Vytovtov’s metric
Welker and Oman
WMC, McCabe’s weighted method count
WMCU, McCabe’s weighted method count-
unweighted
WOC, weight of classes

Papers using it
[34]
[5, 25]
[25]
[25]
[35]
[35]
[5, 25]
[48]
[46]
[34]

[44]

[35, 44]

[44]

[53]
[49]
[5, 25, 31, 35]
[19]
[14]
[19]
[19]
[23]
[24]
[53]
[53]
[48]
[25]
[14, 15, 25, 38], [28, 36, 50]

[15, 50]

[35]

11

TOT Score

1
2
1
1
1
1
2
1
1
1

1

2

1

1
1
4
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
7

2

1

1
2
1
1
1
1
2
1
1
1

1

2

1

1
1
4
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
7

2

1

this metric is that if a class is continuously mod-
iﬁed, it can be a sign that it is hardly maintainable.
Generally, three types of changes can be made to a
line of code: additions, deletions, or modiﬁcations.
In the literature, there is typically accordance about
how to count the operations of modiﬁcations,
which typically counts two times as the additions
or deletions (the modiﬁcation is considered as a
deletion followed by an addition). Most of the
times, comments, and blanks are not considered in
the computation of the changed LOCs during the
evolution of software code.

(iv) C&K (Chidamber and Kemerer Suite). It is one of
the best-known sets of metrics, which was intro-
duced in 1994 [58]. 'is suite has been designed
keeping into consideration the object-oriented
approach. It is composed of 6 metrics, listed as
follows:

WMC, weighted method per class, deﬁned in the
same way as McCabe’s WMC (weighted method
count, described below) but applied to a class, i.e.,
it gives the complexity of that particular class by

Figure 3: Distributions of total number of mentions and the
measured score for the metrics.

MentionsScoresMeasure51015SetAll metricsWith 2 + mentions 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseMetric suite
—
—

—

—
—
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
Chidamber and
Kemerer
—
—
—
—
—
—
Halstead
Halstead
Halstead
Halstead
Halstead
Halstead
—
—
—
Li and Henry
(L&H)
Li and Henry
(L&H)
—
—
—
—
—
—

—

—
—
—
—
SM, structural
measures
—
—

—

12

Scientiﬁc Programming

Table 6: Metrics found in the selected set of primary studies, with the number of mentions and score higher or equal to 2.

Metric
Avg CC, average cyclomatic complexity
CA, aﬀerent coupling

CC, McCabe’s cyclomatic complexity

CE, eﬀerent coupling
CHANGE, number of lines changed in the class

CBO, coupling between objects

DIT, depth of inheritance tree

LCOM, lack of cohesion in methods

Mentioned by
[5, 54]
[5, 21]
[14, 24, 51], S13, [6, 16, 32, 45, 48],
[23, 29, 31, 35, 47]
[5, 21, 25]
[5, 25, 26, 43]
[5, 14, 15, 21, 25–27, 32, 44],
[20, 23, 28, 29, 35, 36, 39, 47, 50]
[5, 14, 26, 43], S13, [20, 21, 27, 32],
[23, 28, 29, 35, 39, 47]
[5, 14, 26, 43], S13, [20, 27, 28, 32],
[23, 36, 39, 46, 47]

TOT Score

2
2

14

3
4

18

15

14

NOC, number of children

[5, 14, 26, 43], S13, [20, 27, 32, 39], [23, 29, 35, 47]

13

RFC, response for class

[5, 14, 15, 19, 21, 26, 27, 43, 44],
[20, 23, 29, 32, 39, 46, 47, 50]

WMC, weighted methods per class

[5, 26, 43], S13, [16, 20, 21, 27, 32], [23, 29, 39, 47]

CLOC, comment lines of code
Code-to-comment ratio
CSA, class size (attributes)
CSO, class size (operations)
CSOA, class size (operations+attributes)
DAM, data access metric (card metric)
Halstead bugs (B)
Halstead diﬃculty (D)
Halstead eﬀort (E)
Halstead length (N)
Halstead vocabulary (n)
Halstead volume (V)
JLOC, JavaDoc lines of code
LCOM2, lack of cohesion of methods
LCOM3, lack of cohesion of methods

DAC

MPC, message passing coupling

LOC, lines of code
MI, maintainability index
MOA, measure of aggregation
NOAC, number of operations added
NOM, number of methods
NPM, number of public methods
Number of classes (including nested classes,
interfaces, enums, and annotations)
Number of commands
Number of ﬁles
Number of queries
PDcy, number of package dependencies

TCC, tight class cohesion

STAT, number of statements
WMC, McCabe’s weighted method count
WMCU, McCabe’s weighted method count-
unweighted

[5, 24, 25], S13, [28, 35]
[14, 15]
[5, 25]
[5, 25]
[5, 25]
[21, 47]
[5, 14, 23, 25, 47, 48]
[5, 14, 23, 25, 45, 47, 48, 51]
[5, 14, 23, 25, 45, 47, 48, 51]
[5, 14, 23–25, 45, 47, 48, 51]
[5, 14, 23, 25, 45, 47, 48, 51]
[5, 14, 25, 51], S13, [6, 23, 45, 48], [47]
[5, 25, 28]
[21, 29, 35]
[21, 35]

[39, 43]

[25, 39, 43, 46]

[14, 15, 21, 24–26, 44, 51], [6, 23, 31, 32, 35, 50]
[6, 14, 25, 30, 44, 51]
[21, 28]
[5, 25]
[26, 28, 31, 43]
[5, 21, 28, 29]

[31, 35]

[5, 25]
[31, 33]
[5, 25]
[5, 25]

S13, [35]

[5, 25, 31, 35]
[14, 15, 25, 28, 36, 38, 50]

[15, 50]

17

13

6
2
2
2
2
2
6
8
8
9
8
10
3
3
2

2

4

15
6
2
2
4
4

2

2
2
2
2

2

4
7

2

adding together the CC of all the methods within
that same class [58].
DIT, depth of inheritance tree, deﬁned as the
length of the maximal path from the leaf node to

the root of the inheritance tree of the classes of the
analyzed software.
Inheritance helps to reuse the code; therefore, it
increases the maintainability. 'e side eﬀect of

2
2

12

3
4

16

13

12

11

15

11

6
2
2
2
2
2
4
6
6
7
6
8
3
3
2

2

4

11
4
2
2
4
4

2

2
2
2
2

2

4
7

2

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

13

Table 7: Metrics (suites) with citation count and score above the
median.

Metric

CC, McCabe’s cyclomatic complexity
CE, eﬀerent coupling
CHANGE, number of lines changed in
class
C&K, Chidamber and Kemerer suite
CLOC, comment lines of code
Halstead’s suite
JLOC, JavaDoc lines of code
LOC, lines of code
LCOM2, lack of cohesion in methods
MI, maintainability index
MPC, message passing coupling
NOM, number of methods
NPM, number of public methods
STAT, number of statements
WMC, McCabe’s weighted method count

Total
mentions
14
3

4

13+
6
6+
3
14
3
6
4
4
4
4
7

Score

12
3

4

11+
6
4+
3
11
3
4
4
4
4
4
7

inheritance is that classes deeper within the hi-
erarchy tend to have increasingly complex be-
haviour, making them diﬃcult to maintain.
Having one, two, or even three levels of inheri-
tance can help the maintainability, but increasing
the value further is deemed detrimental.
NOC, number of children,
is the number of
immediate subclasses of the analyzed class. As the
NOC increases, maintainability of
the code
increases.
CBO, coupling between objects, is the number of
classes with which the analyzed class is coupled.
Two classes are
considered coupled when
methods declared in one class use methods or
instance variables deﬁned by the other class.
'us, this metric gives us an idea on how much
interlaced the classes are to each other and hence
how much inﬂuence the maintenance of a single
class has on other ones.
RFC, response for class, is deﬁned as the set of
methods that can potentially be executed in re-
sponse to a message received by an object of that
class. Also, in this case, the greater is the returned
value, the greater is the complexity of the class.
LCOM, lack of cohesion in methods, is deﬁned as
the subtraction between the number of method
pairs having no attributes in common, and the
number of method pairs having common attri-
butes. Several other versions of the metrics have
been provided in the literature. High values of
LCOM metric value provide a measure of the
relative disparate nature of methods in the class.

(v) CLOC (Comment Line of Code). It is the metric
which gives the number of lines of code which
contain textual comments. Empty lines of com-
ments are not counted. In contrast to the LOC
metric, the higher the value CLOC returns, the

more the comments there are in the analyzed code;
therefore, the code should be easier to understand
and to maintain.
'e literature has also proposed a metric that puts
in relation between CLOC and LOC, and it is called
the code-to-comment ratio.

(vi) 6e Halstead Suite. It is introduced in 1977 [59]
and is a set of statically computed metrics, which
tries to assess the eﬀorts required to maintain the
analyzed code, the quality of the program, and the
number of errors in the implementation.
To compute the metrics of the Halstead suite, the
following indicators must be computed from the
source code: n1, i.e., the number of distinct op-
erators; n2, i.e., the number of distinct operands;
N1, i.e., the total number of operators; and N2, i.e.,
the total number of operands. Operands are the
objects that are manipulated, and operators are all
the symbols that represent speciﬁc actions.
Operators and operands are the two types of
components that form all the expressions. 'e
following metrics are part of the Halstead suite:

Length (N): N � N1 + N2, i.e.,
where N1 is the total number of occurrences of
operators and N2 is the total number of occur-
rences of operands.
Vocabulary (n): n � n1 + n2, i.e., where n1 is the
total number of distinct operators and n2 is the
number of distinct operands in the program. By
deﬁnition, the Vocabulary constitutes a lower
bound for the Length, since each distinct operator
and operand has at least an occurrence.
Volume (V): V � N log2 n, i.e., the size, in bits, of
the space used to store the program (note that this
varies according to the speciﬁc implementation of
the program).
Diﬃculty (D): D � n1/2·N2/n2, which represents
the diﬃculty to understand the code.
Eﬀort (E): E � D V, which represents eﬀort nec-
essary to understand a class.
Bugs (B): B � E(2/3)/3000, which tries to give an
esteem of the number of bugs present during the
implementation of the code.
Time (T): T � E/18, which gives an esteem of the
time needed to implement that code.

(vii) JLOC, (JavaDoc Lines of Code). It is a metric
speciﬁc for Java code, which is deﬁned as the
number of lines of code to which JavaDoc com-
ments are associated. It is similar to other metrics
discussed in the literature that measure the
number of comments in the source code. In
general, a high value for the JLOC metrics is
deemed positive, since it suggests better docu-
mentation of
the code and hence a better
changeability and maintainability. 'is metric is
speciﬁc to the Java programming language. Similar

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License14

Scientiﬁc Programming

Table 8: All tools found in the selected set of primary studies.

Tool name
Columbus quality model
Analyst4j
Lachnesis
Metrics
CCEvaluator
Lagrein
Code Crawler
RAMOOS, reconﬁgurable automated metrics for object-
oriented software
Baker (Baker, 1993)
Kamiya (Kamiya et al., 2002)
Li (Li and 'ompson, 2010)
Baxter (Baxter et al., 1998)
Brown (Brown and 'ompson, 2010)
Koschke (Koschke et al., 2006)
Higo (Higo and Kusumoto, 2009)
Mayrand (Mayrand et al., 1996)
Elva (Elva and Leavens, 2012)
Murakami (Murakami et al., 2014)
Higo (Higo et al., 2007)
Closed-source tools
Codacy

Visual Studio

Understand
JHawk
CMT++/CMTJava

CAST’s Application Intelligence Platform

Open-source tools
CKJM
MetricsReloaded (IntelliJ IDEA plugin)
CodeMetrics (IntelliJ IDEA plugin)
Ref-Finder (Eclipse plugin)
Squale
Quamoco Benchmark for software quality
CBR Insight
Halstead Metrics Tool
SonarQube and CodeAnalyzers, by SonarSource
JSInspect
Escomplex
Eslint
CCFinder (code clones ﬁnder), now called CCFinderX

Papers using it
[15]
[6]
[6]
[6]
[16]
[55]
[55]

[46]

[33, 41]
[33]
[33]
[33]
[33]
[33]
[33]
[33]
[33]
[33]
[33]

[15]

[48]

[6, 50]
[6]
[6]

[22]

Source
Not found
Not found
Not found
Not found
Not found
Not found
Not clear what program they used

Reconﬁgurable

Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used
Not found/not clear what program they used

https://www.codacy.com
https://docs.microsoft.com/en-us/visualstudio/code-
quality/code-metrics-values
https://scitools.com/feature/metrics
http://www.virtualmachinery.com/jhawkprod.htm
https://www.verifysoft.com/en cmtx.html
https://www.castsoftware.com/products/application-
intelligence-platform

[5, 21, 25, 26, 43]
[5]
[5]
[19, 38]
[15]
[15]
[15]
[38]
[6, 15, 31]
[40]
[40]
[40]
[33]

https://www.spinellis.gr/sw/ckjm
https://github.com/BasLeijdekkers/MetricsReloaded
https://github.com/kisstkondoros/codemetrics-idea
https://sites.google.com/site/reﬃndertool
http://www.squale.org
https://github.com/wagnerst/quamoco
https://github.com/StottlerHenkeAssociates
https://sourceforge.net/p/halsteadmetricstool
https://www.sonarsource.com
https://www.npmjs.com/package/jsinspect
https://github.com/escomplex/escomplex
https://eslint.org
http://www.ccﬁnder.net/ccﬁnderxos.html

documentation generators are available for Java-
(JSDoc) and PHP (PHPDocumentor);
Script
however, we were not able to gather evidence from
the manuscripts about the applicability of the
JLOC metric to them, so we deemed it applicable
only for source code written in Java.

(viii) LOC (Lines of Code). It is a widely used metric
which is often used for its simplicity. It gives an
immediate measure of the size of the source code.
Among the most popular metrics, the LOC metric
was the only one to have two negative mentions in
other works in the literature. 'ese comments are
related to the fact that there appears to be no single,
universally adopted deﬁnition of how this metric is
computed [14]. Some works consider the count of

all the lines in a ﬁle, and others (the majority)
if
remove blank lines from such computation;
there is more than one instruction in a single line
or a single instruction is divided into diﬀerent
rows, there is ambiguity about considering the
number of lines (physical
lines) or the actual
lines).
number of instructions involved (logical
'us, it is of the utmost importance that the tools
to calculate the metrics specify exactly how they
calculate the values they return (or that they are
open source, hence allowing an analysis of the tool
source code for deriving such information).
Although LOC seems to be poorly related to the
maintenance eﬀort [14] and there is more than one
way to calculate it, this metric is used within the

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

15

maintainability index, and it seems to be correlated
with many of diﬀerent metric measures [60]. 'e
assumption is that the bigger the LOC metric, the
less maintainable the analyzed code is.

(ix) LCOM2 (Lack of Cohesion in Methods). It is an
evolution of the LCOM metric, which is part of the
Chidamber and Kemerer suite. LCOM2 equals the
percentage of methods that do not access a speciﬁc
attribute averaged over all attributes in the class. If
the number of methods or attributes is zero,
LCOM2 is undeﬁned and displayed as zero. A low
value of LCOM2 indicates high cohesion and a
well-designed class.

(x) MI (Maintainability Index). It

is a composite
metric, proposed as a way to assess the main-
tainability of a software system. 'ere are diﬀerent
deﬁnitions of this metric, which was ﬁrstly in-
troduced by Oman and Hagemeister in 1992 [61].
'ere are two diﬀerent formulae to calculate the
MI, one utilizing only three diﬀerent metrics,
Halstead volume (HV), cyclomatic complexity
(CC), and the number of lines of code (LOC), while
the other takes in consideration also the number of
comments. Despite being quite popular, Ostberg
and Wagner express their doubts about the ef-
fectiveness of this metric, claiming it does not give
information about the maintainability of the code,
since it is based on metrics considered not suited
for that task, and the result of the metric itself is not
intuitive [14]. In contrast, Sarwar et al. state that
MI proved to be very eﬃcient in improving soft-
ware maintainability and cost-eﬀectiveness [6].
'e 3-metric equation is as follows: MI � 171−5.2·ln
(avgV)−0.23·avgCC−16.2·ln (avgLOC).
'e 4-metric equation is as follows: MI √ � 171–5.2
ln (avgV) − 0.23 avgCC + − 16.2 ln (avgLOC) + 50
sin (2.4 perCM).
In both equations,
the following symbols are
adopted: avgV is the average Halstead volume for
the source code ﬁles; avgLOC is the average LOC
metric; avgCC is the average cyclomatic com-
plexity; perCM is the percentage of LOC con-
taining comments.
A returned value above 85 means that the code is
easily maintainable; a value from 85 to 65 indicates
that the code is not so easy to maintain; below 65,
the code is diﬃcult to maintain. 'e returned value
can reach zero, and even become negative, espe-
cially for large projects.

(xi) MPC (Message Passing Coupling). It is a metric
from the Li and Henry suite (the only metric of that
suite to have a score above the rounded median),
and it is deﬁned as the number of send statements
deﬁned in a class [62], i.e., the number of method
calls in a class.

(xii) NOM (Number of Methods Counts). It

is the
number of methods in a given class/source ﬁle,
with the assumption that the higher the number of
methods, the lower the maintainability of the code.
(xiii) NPM (Number of Public Methods). It returns the
number of all the methods in a class that are de-
clared as public.

(xiv) STAT (Number of Statements). It counts the
number of statements in a method. Diﬀerent
variations of the metric have been proposed in the
literature, which diﬀer on the decision of counting
statements also in named inner classes, interfaces,
and anonymous inner classes. For instance, Kaur
et al., in their study for software maintainability
prediction, count the number of statements only in
anonymous inner classes [5].

(xv) WMC (McCabe’s Weighted Method Count). It is a
measure of complexity that sums the complexity of
all the methods implemented in the analyzed code.
'e complexity of each method is calculated using
McCabe’s cyclomatic complexity, which is also
present among the most cited metrics and dis-
cussed above. A simpliﬁed variant of this metric,
called WMC-unweighted, simply counts each
method as if it had unitary complexity; this variant
corresponds to the NOM (number of methods)
metric.

3.3. RQ2.1: Available Tools. In Table 8, we report all the tools
that were identiﬁed while reading the papers. 'e columns
report, respectively, as follows: the name of the tool, as it is
presented in the studies; the studies using it; a web source
where the tool can be downloaded. In the upmost section of
the table, we reported papers from which we cannot ﬁnd the
used tool (i.e., a tool was mentioned but no download
pointer was provided, indicating that the tool has never been
made public and/or it had been discontinued), or for which
no information about the used tool was provided. For the
latter, we have indicated the studies in the table with the
respective author’s name.

In the second and third section of the table, we have
divided the tools according to their release nature, i.e., we
discriminated between open-source and commercial tools.
'e table reports information about a total of 38 tools: 19
were not found; 6 were closed source; and 13 were open
source.

'e majority of the tools we found are mentioned by
only one study; three are cited by two studies, and only one,
CKJM, is quoted by ﬁve papers.

It is immediately evident that the open-source tools are
more than two times in number than the closed-source ones.
'is result may be unrelated to the quality of the tools
themselves but instead be justiﬁed by the fact that open-
source tools are better suited for academic usage since they
provide the possibility of checking the algorithms and pos-
sibly modify or integrate them to analyze their performance.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License16

Scientiﬁc Programming

Figure 4: Programming languages supported by each tool.

For each of the tools that we were able to identify, we give
a brief description in the following; the details about their
supported languages and metrics can be found after the
descriptions of the tools.

3.3.1. Closed-Source Tools. Six closed-source tools can be
found in the analyzed primary studies, three of which are
mentioned in the same paper. 'e tools described hereafter
are listed in alphabetical order and not in any order of
importance.

(i) CAST’s Application Intelligence Platform. 'is tool
analyzes all the source code of an application, to
measure a set of nonfunctional properties such as
performance, robustness, security, transferability,
and changeability (which is strictly tied to main-
tainability). 'is last nonfunctional property is
measured based on cyclomatic complexity, cou-
pling, duplicated code, and modiﬁcation of indexes
in groups [63]. 'e tool produces as output a set of
violation of typical architectural and design patterns
and best practices, which are aggregated in formats
speciﬁc
and the
for both the management
developers.

(ii) CMT++/CMTJava. CMT is a tool speciﬁcally made
to estimate the overall maintainability of code done
in C, C++, C#, or Java, and to identify the less
maintainable parts of it. It is possible to compute
many of
the discussed metrics with the tool:
McCabe’s cyclomatic number, Halstead’s software
science metrics, lines of code, and others. CMT also
allows computing the maintainability index (MI).
'e tool can work in command line mode or with a
GUI.

(iii) Codacy. It is a free tool for open-source projects and
can be self-hosted, otherwise a license must be
purchased to use it. 'is tool aims at improving the
code quality, to augment the code coverage and to
prevent security issues. Its main focus is on iden-
tifying bugs and undeﬁned behaviours rather than
calculating metrics. It provides a set of statistics
about the analyzed code: error-proneness, code
style, code complexity, unused code, and security.
(iv) JHawk. 'e tool is tailored to only analyze code
written in Java, but it can calculate a vast variety of
diﬀerent metrics. JHawk is not new on the market
since its ﬁrst release was introduced more than ten
years ago. At the time of writing this article, the last

XRef-finder toolCCFinderXEslintEscomplexJsinspectSonarQube - codeAnalyzerHalstead metrics toolCBR insightQuamoco benchmarkSqualeCodeMetricsMetricsReloadedCKJMVisual studioUnderstandJhawkCMT++/CMTJavaCodacyCAST’s AIPAdaAPABApexXXXXXX XAssemblyXXCXXXXXXXXXXXC++XXXXXXXXXXC#XXXXXXXCobolXXXXXXCSSXFortranXXXGOXHTMLXJavaXXXXXXXXXXXXXJavaScriptXXXXXXXXJovialXXJsonXXXJSPXXXXKotlinXXXXMarkdownXXXObjective CXPHPXXXXXPythonXXXXXRPGXRubyXXXXScalaXXXXSQLXSwitfXT-SQLXTypeScriptXVB6XXXXVB.NETXXXXVelocityXXXVisualForceXXXXMLXXXX 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

17

Figure 5: Number of tools (closed or open source) per language.

Figure 6: Tool support to the metrics found in primary studies.

available version is 6.1.3, from 2017. It is used and
cited in more than twenty of the selected primary
studies. JHawk aids the empirical evaluation of
software metrics with the possibility of reporting the
computed measures in various formats, including
XML and CSV, and it supports a CLI interface.

(v) Understand. Developed by SciTools, it can calculate
several metrics, and the results can be extracted
automatically via command line, graphical inter-
face, or through their AIP. Most of the metrics
supported by this program are complexity metrics
(e.g., McCabe’s CC), volume metrics (e.g., LOC),

CCCECHANGEC&KCLOCHalstead’sJLOCLOCLCOM2MIMPCNOMNPMSTATWMCXXXXXXXX XXXX XXXXXXXXXXXXXXXXXXXXXXXXXX XX XXX XXX XX XX XXX XXXXXX XX X XXXXXXX XXXXXXAvgCCCACBOCode SmellsEssential ComplexityMNDMood’sNIVNOCN. ClassesN. CommandsN. DirectoriesN. FilesN. QueriesRFCTest ResultsOthersXXX XXXXX XXXX XXXXX XXXXXXXXXXX XXXX XXXXXXXXXXXXXXXXXRef-ﬁnder toolCCFinderXEslintEscomplexJsinspectSonarQube-codeAnalyzerHalstead metrics toolCBR insightQuamoco benchmarkSqualeCodeMetricsMetricsReloadedCKJMVisual studioUnderstandJhawkCMT++/CMTJavaCodacyCAST’s AIP14121086420CApexAssemblyT-SQLMarkdownVelocityJavaScriptVisualForceRubySwiHTMLJavaCSSCobolJsonJSPVB6C#C++PHPPythonRPGAPABScalaSQLFortanXMLAdaobjective CVB NETKotlinJovialGOTypeScriptCS toolsOS tools 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License18

Scientiﬁc Programming

Figure 7: Number of tools (closed or open source) per metric.

Table 9: Tools available for computing the most popular metrics for the most supported programming languages (open-source tools in
bold).

Metric

CC

CE

CHANGE

C&K

CLOC

C
CAST’S AIP
Codacy
CMT++
Understand
Visual Studio
MetricsReloaded
Squale
CodeAnalyzers
CCFinderX
CAST’S AIP
Understand
Visual Studio
MetricsReloaded
Squale
CCFinderX

Understand
Visual Studio
MetricsReloaded
Codacy
Understand
CBR Insight
CodeAnalyzers

C++
CAST’S AIP
Codacy
CMT++
Understand
Visual Studio
Squale
CodeAnalyzers
CCFinderX

CAST’S AIP
Understand
Visual Studio
Squale

C#
CAST’S AIP
Codacy
CMT++
Understand
CodeAnalyzers
CCFinderX

CAST’S AIP
Understand

CCFinderX

CCFinderX

Understand
Visual Studio

Codacy
Understand
CBR Insight
CodeAnalyzers

Understand

Codacy
Understand
CBR Insight
CodeAnalyzers

Halstead’s

CMT++
Halstead Metrics Tool

CMT++
Halstead Metrics Tool

CMT++

JLOC

—

—

—

Java
CAST’S AIP
Codacy
CMTJava
JHawk
Understand
MetricsReloaded
CodeMetrics
CodeAnalyzers
CCFinderX
CAST’S AIP
JHawk
Understand
MetricsReloaded

CCFinderX
Ref-Finder
Understand
CKJM
MetricsReloaded
Codacy
JHawk
Understand
CBR Insight
CodeAnalyzers
CMTJava
JHawk
Halstead Metrics Tool
Codacy
MetricsReloaded
Squale

JavaScript
CAST’S AIP
Codacy
Understand
CodeAnalyzers
Escomplex
Eslint

CAST’S AIP
Understand

Understand

Codacy
Understand
CBR Insight
CodeAnalyzers
Eslint
Escomplex

—

CCCECHANGEC&KCLOCHalsteadJLOCLOCLCOM2MIMPCNOMNPMSTATWMCAvgCCCACBOSmellsECMNDMoodNIVNOC#Classes#Commands#Directions#Files#QueriesRFCTestsOthers14121086420CS toolsOS tools 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

Metric

LOC

LCOM2

MI

MPC

NOM

NPM

STAT

WMC

C
CAST’S AIP
Codacy
CMT++
Understand
Visual Studio
MetricsReloaded
Squale
CBR Insight
CodeAnalyzers
CCFinderX
CAST’S AIP
Understand
CMT++
Visual Studio
CodeAnalyzers
CAST’S AIP

Understand
Squale
CodeAnalyzers
Understand
Squale
CodeAnalyzers
Understand
CodeAnalyzers

Understand
CBR Insight

Table 9: Continued.

C++
CAST’S AIP
Codacy
CMT++
Understand
Visual Studio
Squale
CBR Insight
CodeAnalyzers
CCFinderX

CAST’S AIP
Understand
CMT++
Visual Studio
CodeAnalyzers
CAST’S AIP

Understand
Squale
CodeAnalyzers
Understand
Squale
CodeAnalyzers
Understand
CodeAnalyzers

C#
CAST’S AIP
Codacy
CMT++
Understand
CBR Insight
CodeAnalyzers
CCFinderX

CAST’S AIP
Understand
CMT++
CodeAnalyzers

CAST’S AIP

Understand
CodeAnalyzers

Understand
CodeAnalyzers

Understand
CodeAnalyzers

Understand
CBR Insight

Understand
CBR Insight

Java
CAST’S AIP
Codacy
CMTJava
JHawk
Understand
MetricsReloaded
Quamoco Benchmark
CBR Insight
CodeAnalyzers
CCFinderX
CAST’S AIP
Understand
CMTJava
JHawk
CodeAnalyzers
CAST’S AIP
JHawk
Understand
CodeAnalyzers

Understand
CKJM
CodeAnalyzers
JHawk
Understand
CodeAnalyzers
Understand
CKJM
CBR Insight

19

JavaScript
CAST’S AIP
Codacy
Understand
CBR Insight
CodeAnalyzers
JSInspect
Eslint

CAST’S AIP
Understand
CodeAnalyzers
Eslint

CAST’S AIP

Understand
CodeAnalyzers

Understand
CodeAnalyzers

Understand
CodeAnalyzers
Eslint
Understand
CBR Insight

and object-oriented metrics. 'e correlation be-
tween the supported metrics and the inferred
maintainability of software projects is not explicitly
mentioned in the tool’s documentation.

(v) Visual Studio. It is a very well-known IDE developed
by Microsoft. It comes embedded with modules for
the computation of code quality metrics, in addition
to all its other functions. Among the maintainability
metrics listed in the previous section, it supports MI,
CC, DIT, class coupling, and LOC. 'e main lim-
itation for the Visual Studio tool is that these metrics
can be computed only for projects written in the C
and C++ languages, and not for projects in any
other of the many languages supported by the IDE.
Also, from the Visual Studio documentation, it can
be seen that the IDE makes some assumptions about
the metrics that are diﬀerent from the standard
ones. As an example, the MI metric used in Visual
Studio is an integer between 0 and 100, with dif-
ferent thresholds from the standard ones deﬁned for
MI (MI 20 indicates a code easy to maintain, a rating
from 10 to 19 indicates that the code is relatively

maintainable, and a value below 10 indicates low
maintainability).

3.3.2. Open-Source Tools. Fourteen open-source tools could
be found in the analyzed primary studies. Most of them,
however, require a license to be used in not open-source
projects or to be used without limitations. 'e tools de-
scribed hereafter are listed in alphabetical order and not in
any order of importance:

(i) CBR Insight. It is a tool built on top of Understand
(see the previous section about closed-source
tools), and it uses it to calculate the metrics. 'e
tool calculates metrics that are highly related to
software reliability, maintainability, and prevent-
able technical debt. It provides a dashboard to
present the data to developers/maintainers. It is
worth noting that the tool, although open source,
needs a license for the Understand tool to be used.
(ii) CCFinderX (Code Clones Finder). Previously
known as CCFinder, it is a tool able to detect
duplicate code fragments in source codes written
in Java, C, C++, C#, COBOL, and VB. At the time

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License20

Programming
Language
C
C++
C#

Java

JavaScript

Scientiﬁc Programming

Table 10: Optimal set of tools for most supported programming languages.

Optimal set of tools

Metrics covered

CAST’s AIP, Understand, CCFinderX, CMT++
CAST’s AIP, Understand, CCFinderX, CMT++
CAST’s AIP, Understand, CCFinderX, CMT++
(CAST’s or JHawk), (CCFinderX or Ref-Finder), Understand, CMTJava, (MetricsReloaded,
Squale, or Codacy)
CAST’S AIP, Understand, escomplex, (CodeAnalyzers or eslint)

14/14
14/14
14/14

15/15

14/14

Table 11: Optimal set of open-source tools for most supported programming languages.

Programming Language
C
C++
C#
Java
JavaScript

Optimal set of tools
CBR Insight, CCFinderX, CodeAnalyzers, Halstead Metrics Tool, MetricsReloaded
CBR Insight, CCFinderX, CodeAnalyzers, Halstead Metrics Tool, Squale
CBR Insight, CCFinderX, CodeAnalyzers
(CCFinderX or Ref-Finder), CKJM, CodeAnalyzers, Halstead Metrics Tool, MetricsReloaded
CBR Insight, CodeAnalyzers

Metrics covered
12/14
11/14
9/14
13/15
8/14

of writing this SLR, the project appears to be not
maintained, and the last version dates back to May
2010.

(iii) CKJM. 'e tool [64], cited in ﬁve of our selected
studies, supports only the Java programming
language. It can calculate the six metrics of the
C&K suite, plus the aﬀerent coupling (CA), and the
number of public methods (NPM). 'e results can
be exported in XML format, and the program can
be integrated with Ant. 'e tool appears to have
been discontinued, since its last release at the time
of the writing of this manuscript, i.e., the 1.9, was
released in 2008.

(iv) CodeMetrics (IntelliJ IDEA Plugin). 'e tool is
released under the MIT license. It can compute the
complexity of each method and the total for each
class of the source code. It does not calculate the
standard cyclomatic complexity, but an approxi-
mation of that. At the time of writing this article,
the project is still maintained.

(v) Escomplex. It is a tool that performs a software
complexity analysis of JavaScript abstract syntax
trees. It can compute several metrics among those
previously identiﬁed, e.g., the maintainability in-
dex, the Halstead suite, McCabe’s CC, and LOC.
'e results are returned in JSON format so that
they can be used by front-end programs. At the
time of writing this SLR, the last version of the tool
dates back to the end of 2015.

(vi) Eslint. 'e tool is a linting (i.e., running a program
to analyze code to automatically verify the pres-
ence of potential errors) utility for JavaScript. 'e
tool allows using a set of built-in linting rules and
also allows adding custom ones as plugins that are
dynamically loaded. 'e tool also allows ﬁxing
automatically some of the issues that it ﬁnds. At the

time of writing the SLR, the project’s last available
release is v6.5.1, released in September 2019.
(vii) Halstead Metrics Tool. A software metrics analyzer
for C, C++, and Java programs. It provides a
computation of the Halstead metric suite only. It is
written in Java and can export the results in HTML
and PDF. At the time of writing this SLR, no
development of the tools has been performed after
2016.

(viii) JSInspect. It is a program to analyze JavaScript code
in search of code smells, such as duplicate code and
repeated logic. 'e basic aim of the tool is to
identify separate portions of code with a similar
structure in a software project, based on the AST
node types, e.g., BlockStatement, VariableDecla-
ration, and ObjectExpression. At the moment of
writing this SLR, the tool seems to have been
discontinued, since the last commit on the re-
pository dates back to August 2017.

(ix) MetricsReloaded (IntelliJ IDEA Plugin). 'e tool, in
addition to being available as a plugin for the
popular IDE IntelliJ IDEA, can also be used stand-
alone from the command line. 'e project seems to
be discontinued since September 2017.

(x) Quamoco Benchmark for Software Quality. It is a
Java-based tool aimed to analyze code written in
Java. It is based on the Quamoco model, aimed at
integrating abstract code quality attributes and
concrete software quality assessments [65]. 'e
tool is mentioned in several academic studies se-
lected in this SLR, and its code repository is
available on GitHub. From the repository, it can be
seen that the development has been discontinued,
and the last commit dates back to July 2013.
(xi) Ref-Finder (Eclipse Plugin). A tool whose principal
aim is to detect refactorings occurred between two

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

21

program versions and helping the developers to
better understand code changes. 'e plugin can
recognize even complex refactoring with high
precision, and it supports 65 of the 72 refactoring
types in Fowler’s catalogue [66].

(xii) SonarQube. Along with CodeAnalyzers,

it is a
product by SonarSource. 'e two products are
provided in two diﬀerent editions: the community
one, which is open source, and a commercial one.
'e community edition features fewer metrics and
less programming languages and does not provide
the security reports that are a main feature of the
commercial versions. 'ey support more than 25
programming languages (15 in the OS editions)
and hundreds of rules, among which code smells
and maintainability metrics.

(xiii) Squale (Software QUALity Enhancement). It is
based on third party technologies (commercial or
open source) that produce raw quality information
(such as metrics for instance) and uses quality
models (such as ISO-9126) to aggregate the raw
information into high-level quality factors. Re-
leased under the LGPLv3 license, it is a program to
help to assess the software quality, giving as output
information to be used from both the development
and the management team, dealing with both
technical and economic aspects of software quality.
It targets diﬀerent programming languages (in-
cluding Java, C/C++,.NET, PHP, and Cobol) and
utilizes code metrics and quality models to assess
the grade of the code. 'e tool appears to be
discontinued, and the last version of the program,
v7.1, released in May 2011.

3.3.3. Correspondence between Tools and Languages.
Figure 4 shows which languages are supported by each tool.
Some of the considered tools support a wide variety of
languages, such as Understand, Codacy, and the tools by
SonarSource (SonarQube and CodeAnalyzers). CBR Insight,
as stated before, is based on Understand; hence, it supports
the same set of programming languages. 'e majority of
tools, however, support a limited number of programming
languages or also just one. For instance, JHawk, CKJM,
CodeMetrics, and Ref-Finder all support only Java; JSIns-
pect, escomplex, and eslint are tailored to work only with
JavaScript.

From the table, it is evident that the closed-source tools
support more programming languages (an average of 10.5)
compared to open-source tools (an average of 4.85). By
analyzing the primary studies selected for this SLR, it is also
reported that closed-source tools tend to support some
metrics better than open-source counterparts: for instance, a
comparative study between diﬀerent tools capable of MI
reports a higher dependability of such metric when com-
puted using closed-source tools rather than open-source
alternatives [6].

Figure 5 shows how many closed-source and open-
source tools have been found for each language. From that

chart, it is evident that some languages are better supported
than others. Java, C, and C++, followed closely by JavaScript
and C#, are supported by at least half of the tools we
considered in our study. More speciﬁcally, Java, C, C++, and
C# are supported by almost all the closed-source programs
we found. Some less widespread languages (e.g., APAB, GO,
RPG, and T-SQL) are supported only by open-source tools,
among the set of tools that we gathered from analyzing the
primary studies used for the SLR.

between Tools

3.3.4. Correspondence
and Metrics.
Figure 6 (CS tools and metrics) shows what metrics are
calculated by each of the considered tools. For conciseness,
only the metrics that are computed by at least one tool are
reported in the table. In the upper section of the table, the
most popular metrics identiﬁed in the answer to RQ1 are
reported. Instead, the lower section of the table includes
other metrics belonging to the complete set of metrics found
in the set of primary studies mined from the literature. 'e
table features a mark for a tool and a metric only in cases
when an explicit reference to such metric has been found in
the documentation of the tool.

Also, a suite was considered as supported if at least one of

its metrics was supported by a given tool.

In the case of the closed-source tools, the metrics have
been most of the times inferred from limited documenta-
tion. Most of the times, in fact, closed-source tools provide
dashboards with custom-deﬁned evaluations of the code, for
which the linkage with widespread software metrics is un-
clear. For instance, the Codacy tool provides a single, overall
grade for a software project, between A and F. 'is grade
depends on a set of tool-speciﬁc parameters: error-prone-
ness, code complexity, code style, unused code, security,
compatibility, documentation, and performance. In addition
to some metrics whose usage was explicitly mentioned by the
tool’s creators (e.g., number of comments and JavaDoc lines
for the documentation property and McCabe’s CC for the
code complexity property), it was not possible to ﬁnd the
complete set of metrics used internally by the tool.

In many cases, the tools compute also compound metrics
(i.e., metrics built on top of other ones reported in the
literature) or metrics that were not previously found in the
analysis of the literature performed to answer to RQ1. In
these cases, the tools were labelled as featuring other metrics:
this information is reported in the last row of the table.

As it is evident from the table, no tool supported all the
most popular metrics previously identiﬁed. 'e number of
supported metrics among the most popular ones ranged
from 1 to 10. Two tools featured just one suite/metric from
the set of the most popular ones. 'e Halstead Metrics Tool,
as evident from its name, is an open-source tool with the
only purpose of computing the entire set of metrics of the
Halstead suite; as well, the CodeMetrics plugin is a basic tool
capable of computing only the McCabe cyclomatic com-
plexity (for each method and the total for each class of the
project). Quamoco is indeed not only a tool but instead a
quality metamodel, based on a set of metrics that are deﬁned,
in the scope of the paper presenting the approach, as base

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License22

Scientiﬁc Programming

measures; the metamodel is theoretically applicable to any
kind of base measure that can be computed through static
analysis of source code; however, the literature presenting
the tool mentions only the LOC metric explicitly. Some
other tools, such as JSInspect, CCFinderX, and Ref-Finder
tools, featured a limited set of the maintainability metrics
previously identiﬁed, since they were mainly focused on
other aspects of code quality, e.g., detecting code duplicates
and code smells.

Tools such as MetricsReloaded, Squale, and SonarQube
featured large sets of derived metrics, which were obtained as
specializations, sums, or averages of basic metrics such as the
McCabe cyclomatic complexity or the coupling between
classes.

'e bar graph in Figure 7 reports the number of tools
that featured each of the considered metrics. Also, in this
case, the metrics were divided into three sections on the x-
axis: the 15 metrics/suites deemed as most popular in the
answer to RQ1, other metrics from the full set, and other
metrics not in the set of metrics mined from the literature.
Two metrics stood out in terms of the number of tools that
supported them. 'e LOC metric, despite many papers in
the literature question its usefulness as a maintainability
metric, was supported by 14 out of 19 tools. 'e metric is
closely followed by the cyclomatic complexity (CC), which
was supported by 13 tools. 'ose numbers were expectable
since both the metrics are simple to compute and are needed
by many other derived metrics. On the other hand, three of
the most popular metrics were used by only two of the
selected tools. 'e CHANGE metric refers to the changed
lines of code between diﬀerent releases of the same appli-
cation and was not computed by most of the tools that
performed static analysis on single versions of the appli-
cation; it was instead computed by two tools that were
particularly aiming at measuring code refactorings and
smells. 'e LCOM2 metric is an extension of the LCOM
metric, which is part of the C&K suite; several tools just
mentioned the adoption of the suite without explicitly
mentioning possible adoptions of enhanced versions of the
metrics; ﬁnally, the message passing coupling was adopted
by two tools and in both cases deﬁned with the synonym fan-
out.

In general, closed-source tools featured a higher number
of metrics than open-source counterparts. Open-source
tools, several times, were, in fact, plugins of limited di-
mension, tailored to compute just a single metric or suite. If
only the measures mined from the primary studies are
considered, the closed-source tools were able to compute an
average of slightly less than 8 metrics, while open-source
tools were able to compute an average of 5 metrics. Of the set
of 15 most popular metrics, on average 6 could be computed
by the closed-source tools and 3 by the open-source tools.

tools (more than the average for all programming languages)
supported them. 'e table reports all tools that can compute
a metric for a given language. For the case of the JLOC
metric, the relevant information is only related to the tools
compatible with Java, since the metric cannot be computed
for other programming languages. Open-source tools are
highlighted by using bold lettering. As it is evident from the
table, the most featured metrics (e.g., CC and LOC) can be
computed with many alternative tools (either closed source
or open source) for the same languages. On the other hand,
several metrics can be computed by just a single tool: for
instance, CCFinderX is the only tool that explicitly supports
the CHANGE metric for all the languages of the C family, or
the MPC (message passing coupling) metric is explicitly
supported only by the CAST’s Application Intelligence
Platform for the languages of the C family and JavaScript.

3.4. RQ2.2: Ideal Selection of Tools. Tables 10 and 11 show
the optimal set of tools to cover all the most popular metrics
shown in Table 5. 'e former takes into account both closed-
source and open-source tools; the latter only considers open-
source tools. We deﬁne an optimal set of tools as the
minimal set of tools which can cover the highest possible
amount of metrics (or suites) out of the set of 14 most
mentioned ones (15 for Java, for which also the JLOC metric
can be computed). Inside round brackets, we identiﬁed
alternative tools that could be selected without inﬂuencing
the number of tools in the optimal set or the number of
metrics covered.

By using both closed-source and open-source tools, it is
possible to compute all the most mentioned metrics with an
optimal set of 4 tools for all languages except for Java, for
which 5 tools were necessary. Speciﬁcally, for all the lan-
guages of the C family, all the metrics are covered by CAST’s
Application Intelligence Platform, Understand, CCFinderX,
and CMT++. Java needed also the adoption of a tool among
MetricsReloaded, Squale, or Codacy to compute the JLOC
metric; JHawk and Ref-Finder could be used, respectively, as
alternatives to CAST’s AIP and CCFinderX; CMTJava had to
be selected instead of CMT++. For JavaScript, escomplex
and one between CodeAnalyzers or eslint have to be in-
cluded in the set, replacing CCFinderX and CMT.

By using open-source tools only, it is not possible to
obtain full coverage of the most mentioned metrics. 'e
LCOM2 and MPC metrics were not explicitly supported by
any of the considered open-source tools. 'e maximum
amount of metrics that could be supported with an optimal
set of tools ranged between 8 (for the JavaScript pro-
gramming language, with two tools) and 13 (for Java, with 5
tools, also including the JLOC metric).

4. Threats to Validity

3.3.5. Correspondence between Tools and Languages.
Table 9 reports the tools able to compute each of the set of
most popular metrics for the ﬁve languages that were
supported the most (see bar plot in Figure 5). We took into
account C, C++, C#, Java, and JavaScript, since at least 7

6reats to construct validity, for an SLR, are related to
failures in the claim of covering all the possible studies
related to the topic of the review. In this study, the paper was
mitigated with a thorough and reproducible deﬁnition of the
search strategy and with the use of synonyms in the search

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

23

strings. Also, all the principal sources for the scientiﬁc lit-
erature were taken into consideration for the extraction of
the primary studies.

6reats to internal validity are related to the data ex-
traction phase of the SLR. 'e authors of this paper eval-
uated the papers manually, according to the deﬁned
inclusion and exclusion criteria. 'e authors limited biases
in the inclusion and exclusion of the paper by discussing
disagreements. 'e metric selection phase was performed
based on the opinions extracted from the examined primary
studies (considered as adverse, neutral, or positive). Again,
the reading of the papers and the subsequential opinion
assignments are based on the judgment of the authors and
may suﬀer from misinterpretation of the original opinions.
It is, however, worth mentioning that none of the authors of
this paper were biased towards the demonstration of a
speciﬁc preference for one of the available metrics.

6reats to external validity are related to the incapability
of obtaining generalized conclusions from the conducted
study. 'is threat is limited in this study since its main
results, i.e., the sets of most popular metrics, were formu-
lated w.r.t. to a set of programming languages. 'e results
are not generalized to programming languages that were not
discussed in the primary studies examined in the SLR.

5. Related Works

'e literature oﬀers several secondary studies regarding code
metrics and tools. However, usually, those studies analyze or
present a set of tools, and they describe the metrics based on
the features of the tool. Our review instead started from an
analysis of the literature that was tailored at ﬁnding all
metrics available in relevant studies in the literature, and
then the focus was moved to tools to understand whether the
found metrics were supported or not by those tools.

For example, in the literature review published in 2008,
Lincke et al. [67] compared diﬀerent software metric tools
showing that,
tools provided
in some cases, diﬀerent
uncompatible results; the authors also deﬁned a simple
universal software quality model, based on a set of metrics
that were extracted from the examined tools. Dias Canedo
et al. [68] performed a systematic literature review for
ﬁnding tools that can perform software measures. Starting
from the tools, the authors analyzed the tool features and
described the metrics the software could analyze. For their
secondary studies, the authors analyzed papers from 2007 to
2018.

On the other hand, there are also other secondary studies
explicitly focused on metrics as the comparative case study
published in 2012 by Sjoberg et al. [69], which has a focus on
code maintainability metrics but only considers a subset of
11 metrics for the Java language. 'e work had a primary
aim at questioning the consistency between diﬀerent metrics
in the evaluation of maintainability of software projects.

'e systematic mapping study published in 2017 by
Nun􏽥ez-Varela et al. [70] is one of the most complete works
on this topic. 'e authors discovered 300 source code
metrics by analyzing papers published from 2010 to 2015.

'ey also mapped those metrics with the tools that can use
them. 'is work, however, covers a limited time window and
does not focus on a speciﬁc family of software metrics,
gathering dynamic and change metrics along with static
ones.

In a recent systematic mapping and review, Elmidaoui
et al. identiﬁed 82 empirical studies about software product
maintainability prediction [71]. 'e paper focuses on ana-
lyzing the diﬀerent methods available for maintainability
estimation,
including fuzzy, neurofuzzy, artiﬁcial neural
network (ANN), support vector machines (SVMs), and
group method of data building (GMDH). 'e paper con-
cludes that the prediction of software maintainability, albeit
many techniques are available to perform it, is still limited in
industrial practice.

Our work diﬀers from the secondary studies presented
above. Our point of view is ﬁnding the most common
maintainability metrics and tools to be applied to new
programming languages. For doing so, we analyzed papers
in a 20-year time window (2000–2019). We also distin-
guished open-source tools from closed-source tools, and for
each of them, we mapped the maintainability metrics they
use. 'e output of this work is actionable by practitioners
wanting to create new tools for applying maintainability
metrics to new programming languages.

Other primary studies in the literature presented (or
used) popular software metric tools, which were, however,
not extracted during our study selection phase, since their
primary purpose was not analyzing code from a mainte-
nance point of view, and hence, the manuscripts could not
be found by searching for the maintainability keyword. A
relevant example of those tools is CCCC, a widespread tool
to evaluate code written with object-oriented languages
[72, 73].

6. Conclusion

Maintainability is a fundamental
feature for software
projects, and the scientiﬁc literature has proposed several
approaches, metrics, and tools to evaluate it in real-world
scenarios. With this systematic literature review, we wanted
to have an overview of the most used maintainability metrics
in the literature in the last twenty years, to ﬁnd the most
commonly used ones, which can be used to evaluate existing
software, and that can be adapted to measure the main-
tainability of new programming languages. In doing so, we
wanted to provide the readers actionable results by identi-
fying sets of (closed- and open-source) tools that can be
adopted to be able to compute all the most popular metrics
for a speciﬁc programming language.

With the application of a formalized SLR procedure, we
identiﬁed a total of 174 metrics, some of which were dis-
tributed in 10 metric suites. Among them, we extracted a set
of 15 most frequently mentioned ones, of which we reported
the deﬁnitions and formulae. We also identiﬁed a set of 38
tools mentioned in primary studies about software main-
tainability metrics: by ﬁltering those that were not made
available by the authors, could not be retrieved on the web,
or were no longer available, we came up with a set of 6

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License24

Scientiﬁc Programming

closed-source and 13 open-source tools that can be used to
evaluate software projects, covering 34 diﬀerent program-
ming languages. By analyzing the tools, we found that Java,
JavaScript, C, C++, and C# are the most common pro-
gramming language compatibles with the analyzed tools. By
pairing the information about supported programming
languages and supported metrics, we found that it is possible
to ﬁnd an optimal selection of at most ﬁve tools to cover all
the most mentioned metrics for the languages of the Java and
C family. However, not all the most popular metrics could be
computed by taking into consideration only open-source
tools.

'is manuscript can provide actionable guidelines for
practitioners who want to measure the maintainability of
their software by providing a mapping between popular
metrics and tools able to compute them. Also, this manu-
script provides actionable guidelines for practitioners and
researchers who may want to implement tools to measure
software metrics for newer programming languages. Our
work identiﬁes which tools can provide the computation of
the most popular maintenance metrics and the support they
provide to the most common programming languages. Our
work also provides pointers to existing open-source tools
already available for computing the metrics, which can be
leveraged by tool developers as guidelines for their coun-
terparts for source code written in diﬀerent languages.

As future work, we aim at implementing a tool that uses
the set of metrics we found in RQ1.2 to analyze code written
in the Rust programming language. For the Rust pro-
gramming language, we identiﬁed no tool capable of
computing the most popular maintainability metrics men-
tioned in the literature. We plan to extend a tool named
Tokei1, which oﬀers compatibility with many modern
programming languages. 'e results of these works are
considered capable of easing other researchers to create tools
for measuring the maintainability of modern programming
languages and for encouraging new comparisons between
programming languages.

Data Availability

'e data used to support the ﬁndings of this study are in-
cluded within the article in the form of references linking to
resources available on the FigShare public open repository.

Conflicts of Interest

'e authors declare that there are no conﬂicts of interest
regarding the publication of this paper.

Acknowledgments

Mozilla Research funded this project with the research grant
2018 H2. 'e project title is “Algorithms clarity in Rust:
advanced rate control and multithread support in rav1e.”
'is project aims to understand how the Rust programming
language improves
the maintainability of code while
implementing complex algorithms.

References

[1] F. Zampetti, S. Scalabrino, R. Oliveto, G. Canfora, and M. Di
Penta, “How open source projects use static code analysis
tools in continuous integration pipelines,” in Proceedings of
the 2017 IEEE/ACM 14th International Confer- Ence on
Mining Software Repositories (MSR), IEEE, Buenos Aires,
Argentina, May 2017.

[2] IEEE Standards Association, IEEE Standard Glossary of
Software Engineering Terminology, IEEE Standards Associa-
tion, Piscataway, NJ, USA, 1990.

[3] C. Van Koten and A. Gray, “An application of bayesian
network for predicting object-oriented software maintain-
ability,” Information and Software Technology, vol. 48, no. 1,
pp. 59–67, 2006.

[4] Y. Zhou and H. Leung, “Predicting object-oriented software
maintainability using multivariate
regression
splines,” Journal of Systems and Software, vol. 80, no. 8,
pp. 1349–1361, 2007.

adaptive

[5] A. Kaur, K. Kaur, and K. Pathak, “Software maintainability
prediction by data mining of software code metrics,” in
Proceedings of the 2014 International Conference on Data
Mining and Intelligent Computing (ICDMIC), Delhi, India,
September 2014.

[6] M. I. Sarwar, W. Tanveer, I. Sarwar, and W. Mahmood, “A
comparative study of mi tools: deﬁning the roadmap to mi
tools standardization,” in Proceedings of the 2008 IEEE In-
ternational Multitopic Conference, Karachi, Pakistan, De-
cember 2008.

[7] N. D. Matsakis and F. S. Klock II, “'e rust language,” ACM
SIGAda Ada Letters, vol. 34, no. 3, pp. 103-104, 2014.
[8] S. Klabnik and C. Nichols, 6e Rust Programming Language,

No Starch Press, San Francisco, CA, USA, 2018.

[9] A. Tahir and R. Ahmad, “An aop-based approach for col-
in
lecting soft- ware maintainability dynamic metrics,”
Proceedings of the 2010 Second International Conference on
Computer Research and Development, Beijing, China, May
2010.

[10] K. Barbara A and S. Charters, “Guidelines for performing
systematic literature reviews in software engineering,” Tech.
Rep. 2007, Durham University, Durham, England, 2007.
[11] B. A. Kitchenham, T. Dyba, and M. Jorgensen, “Evidence-
based soft- ware engineering,” in Proceedings of the 26th
International Conference on Software Engineering,
IEEE
Computer Society, New York, NY, USA, pp. 273–281, May
2004.

[12] B. Kitchenham, O. Pearl Brereton, D. Budgen, M. Turner,
J. Bailey, and S. Linkman, “Systematic literature reviews in
software engineering - a systematic literature review,” In-
formation and Software Technology, vol. 51, no. 1, pp. 7–15,
2009.

[13] R. van Solingen, V. Basili, G. Caldiera, and H. D. Rombach,

Goal Question Metric (GQM) Approach, 2002.

[14] J. Ostberg and S. Wagner, “On automatically collectable
metrics for software maintainability evaluation,” in Pro-
ceedings of the 2014 Joint Conference of the International
Workshop on Software Measurement and the International
Conference on Software Process And Product Measurement,
Rotterdam, 'e Netherlands, October 2014.

[15] J. Ludwig, S. Xu, and F. Webber, “Compiling static software
metrics for reliability and maintainability from github re-
positories,” in Proceedings of the 2017 IEEE International
Conference on Systems, Man, and Cybernetics (SMC), Banﬀ,
AB, Canada, October 2017.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons LicenseScientiﬁc Programming

25

[16] H. Liu, X. Gong, L. Liao, and B. Li, “Evaluate how cyclomatic
complexity changes in the context of software evolution,” in
Proceedings of the 2018 IEEE 42nd Annual Computer Software
and Applications Conference (COMPSAC), Tokyo, Japan, July
2018.

[17] P. Jacs´o, “Calculating the index and other bibliometric and
scientometric indicators from Google Scholar with the
Publish or Perish software,” Online information Review,
vol. 33, no. 6, pp. 1189–1200, 2009.

[18] C. Wohlin, “Guidelines for snowballing in systematic liter-
ature studies and a replication in software engineering,” in
Proceedings of the 18th International conference on evaluation
and assessment in software engineering, Ciudad Real, Spain,
May 2014.

[19] I. K´ad´ar, P. Hegedus, R. Ferenc, and T. Gyim´othy, “A code
refactoring dataset and its assessment regarding software
maintainability,” in Proceedings of the 2016 IEEE 23rd In-
ternational Conference on Software Analysis, Evolution, and
Reengineering (SANER), Osaka, Japan, March 2016.

[20] J. Gil, M. Goldstein, and D. Moshkovich, “An empirical in-
vestigation of changes in some software properties over time,”
in Proceedings of the 2012 9th IEEE Working Conference on
Mining Software Repositories (MSR), Zurich, Switzerland,
June 2012.

[21] A. Jain, S. Tarwani, and A. Chug, “An empirical investigation
of evolu- tionary algorithm for software maintainability
prediction,” in Proceedings of the 2016 IEEE Students’ Con-
ference on Electrical, Electronics and Computer Science
(SCEECS), Bhopal, India, March 2016.

[22] B. Curtis, J. Sappidi, and J. Subramanyam, “An evaluation of
the inter- nal quality of business applications: does size
matter?” in Proceedings of the 33rd International Conference
on Software Engineering, ICSE ’11), New York, NY, USA, May
2011.

[23] R. S. Chhillar and S. Gahlot, “An evolution of software
metrics: a review,” in Proceedings of the International Con-
ference on Advances in Image Processing, ICAIP 2017), New
York, NY, USA, 2017.

[24] Y. Tian, C. Chen, and C. Zhang, “Aode for source code metrics
for improved software maintainability,” in Proceedings of the
2008 Fourth International Con- Ference on Semantics,
Knowledge And Grid, Beijing, China, December 2008.
[25] A. Kaur, K. Kaur, and K. Pathak, “A proposed new model for
main- tainability index of open source software,” in Pro-
ceedings of 3rd International Conference on Reliability, Info-
com Technologies And Optimization, Noida, India, October
2014.

[26] N. Barbosa and K. Hirama, “Assessment of software main-
tainability evolution using C&K metrics,” IEEE Latin America
Transactions, vol. 11, no. 5, pp. 1232–1237, 2013.

[27] S. Misra, A. Adewumi,

and
R. Damasevicius, “A suite of object oriented cognitive com-
plexity metrics,” IEEE Access, vol. 6, pp. 8782–8796, 2018.

Fernandez-Sanz,

L.

[28] S. Rongviriyapanish, T. Wisuttikul, B. Charoendouysil,
P. Pitakket, P. Anancharoenpakorn, and P. Meananeatra,
“Changeability prediction model for java class based on
multiple layer perceptron neural network,” in Proceedings of
the 2016 13th International Conference on Electrical Engi-
neering/Electronics, Computer, Telecommunications and In-
formation Technology (ECTI-CON), Chiang Mai, 'ailand,
June 2016.

[29] S. Arshad and C. Tjortjis, “Clustering software metric values
extracted from c# code for maintainability assessment,” in

Proceedings of the 9th Hellenic Conference on Artiﬁcial In-
telligence, SETN ’16), New York, NY, USA, May 2016.
[30] M. Pizka, “Code normal forms,” in Proceedings of the 29th
IEEE/NASA Software Engineering Workshop,

Annual
Greenbelt, MD, USA, April 2005.

[31] M. A. A. Mamun, C. Berger, and J. Hansson, “Correlations of
software code metrics: an empirical study,” in Proceedings of
the 27th International Workshop on Software Measurement
And 12th International Conference on Software Process And
Product Measurement, IWSM Mensura ’17, New York, NY,
USA, May 2017.

[32] T. L. Alves, C. Ypma, and J. Visser, “Deriving metric
thresholds from benchmark data,” in Proceedings of the 2010
IEEE International Conference on Software Maintenance,
Timisoara,Romania, September 2010.

[33] T. Matsushita and I. Sasano, “Detecting code clones with gaps
by function applications,” in Proceedings of the 2017 ACM
SIGPLAN Work- Shop on Partial Evaluation and Program
Manipulation, PEPM 2017), New York, NY, USA, may 2017.
[34] L. M. d. Silva, F. Dantas, G. Honorato, A. Garcia, and
C. Lucena, “Detecting modularity ﬂaws of evolving code: what
the history can reveal?” in Proceedings of the 2010 Fourth
Brazilian Symposium on Software Components, Architectures
And Reuse, Bahia, Brazil, September 2010.

[35] A. Ch´avez, I. Ferreira, E. Fernandes, D. Cedrim, and
A. Garcia, “How does refactoring aﬀect internal quality at-
tributes?: a multi-project study,” in Proceedings of the 31st
Brazilian Symposium on Software Engineering, SBES’17), New
York, NY, USA, May 2017.

[36] Y. Ma, K. He, B. Li, and X. Zhou, “How multiple-dependency
structure of classes aﬀects their functions a statistical per-
spective,” in Proceedings of the 2010 2nd International Con-
ference on Software Technology and Engineering, San Juan, PR,
USA, October 2010.

[37] M. Wahler, U. Drofenik, and W. Snipes, “Improving code
maintainability: a case study on the impact of refactoring,” in
Proceedings of the 2016 IEEE Inter- national Conference on
Software Maintenance and Evolution (ICSME), North CA,
USA, October 2016.

[38] G. Kaur and B. Singh, “Improving the quality of software by
refactoring,” in Proceedings of the 2017 International Con-
ference on Intelligent Computing and Control Systems
(ICICCS), Madurai, India, June 2017.

[39] M. Yan, X. Zhang, C. Liu, J. Zou, L. Xu, and X. Xia, “Learning
to aggre- gate: an automated aggregation method for software
quality model,” in Proceedings of the 2017 IEEE/ACM 39th
International Conference on Software Engineering Companion
(ICSE-C), Buenos Aires, Argentina, May 2017.

[40] K. Chatzidimitriou, M. Papamichail, T. Diamantopoulos,
M. Tsapanos, and A. Symeonidis, “npm-miner: an infra-
structure for measuring the quality of the npm registry,” in
Proceddings of the 2018 IEEE/ACM 15th International Con-
ference on Mining Software Repositories (MSR), Gothenburg,
Sweden, May 2018.

[41] J. Bohnet and J. D¨ollner, “Monitoring code quality and
development activity by software maps,” in Proceedings of the
2Nd Workshop on Managing Technical Debt, MTD ’11), New
York, NY, USA, May 2011.

[42] N. Narayanan Prasanth, S. Ganesh, and G. Arul Dalton,
“Prediction of maintainability using software complexity
analysis: An extended frt,” in Proceedings of the 2008 Inter-
national Conference on Computing, Communication and
Networking, Karur, Tamil Nadu, India, December 2008.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License26

Scientiﬁc Programming

[43] L. Wang, X. Hu, Z. Ning, and W. Ke, “Predicting object-
oriented software maintainability using projection pursuit
regression,” in Proceedings of the 2009 First International
Conference on Information Science and Engineering, Nanjing,
China, December 2009.

[44] D. I. Sjøberg, B. Anda, and A. Mockus, “Questioning software
mainte- nance metrics: a comparative case study,” in Pro-
ceedings of the ACM-IEEE International Symposium on Em-
pirical Software Engineering and Measurement, ESEM
’12ACM, New York, NY, USA, ACM, September 2012.
[45] A. Hindle, M. W. Godfrey, and R. C. Holt, “Reading beside the
lines:
indentation as a proxy for complexity metric,” in
Proceedings of the 2008 16th IEEE In- ternational Conference
on Program Comprehension, Amsterdam, 'e Netherland,
June 2008.

[46] Y. Lee and K. H. Chang, “Reusability and maintainability
metrics for object-oriented software,” in Proceedings of the
38th Annual on South-east Regional Conference, ACM-SE 38),
New York, NY, USA, May 2000.

[47] B. R. Sinha, P. P. Dey, M. Amin, and H. Badkoobehi,
“Software com- plexity measurement using multiple criteria,”
Journal of Computing Sciences in Colleges, vol. 28, pp. 155–162,
April 2013.

[48] P. Vytovtov and E. Markov, “Source code quality classiﬁcation
based on software metrics,” in Proceedings of the 2017 20th
Conference of Open Innovations association (FRUCT), Saint
Petersburg, Russia, April 2017.

[49] N. E. Gold, A. M. Mohan, and P. J. Layzell, “Spatial complexity
metrics: an investigation of utility,” IEEE Transactions on
Software Engineering, vol. 31, no. 3, pp. 203–212, 2005.
[50] J. Ludwig, S. Xu, and F. Webber, “Static software metrics for
reliability and maintainability,” in Proceedings of the 2018
International Confer- Ence on Technical Debt, TechDebt ’18,
pp. 53-54, New York, NY, USA, May 2018.

[51] M. Saboe, “'e use of software quality metrics in the materiel
release process experience report,” in Proceedings of the
Second Asia-Paciﬁc Conference on Quality Software, Brisbane,
Queensland, Australia, December 2001.

[52] A. F. Yamashita, H. C. Benestad, B. Anda, P. E. Arnstad,
D. I. K. Sjoberg, and L. Moonen, “Using concept mapping for
maintainability assessments,” in Proceedings of the 2009 3rd
International Symposium on Empirical Soft-Ware Engineering
And Measurement, Lake Buena Vista, FL, USA, October 2009.
[53] D. 'rem, L. Yu, S. Ramaswamy, and S. D. Sudarsan, “Using
normalized compression distance to measure the evolutionary
stability of software systems,” in Proceedings of the 2015 IEEE
26th International Symposium on Soft- Ware Reliability En-
gineering (ISSRE), Gaithersbury, MD, USA, November 2015.
[54] R. Gon¸calves, I. Lima, and H. Costa, “Using Tdd for De-
veloping Object- Oriented Software — a Case Study,” in
Proceedings of the 2015 Latin American Computing Conference
(CLEI), Arequipa, Peru, October 2015.

[55] A. Jermakovics, R. Moser, A. Sillitti, and G. Succi, “Visualizing
software evolution with lagrein,” in Proceedings of
the
Companion to the 23rd ACM SIGPLAN Conference on Object-
Oriented Programming Systems Languages and Applications,
OOPSLA Companion ’08), New York, NY, USA, May 2008.
[56] T. J. McCabe, “A complexity measure,” IEEE Transactions on

Software Engineering, vol. SE-2, no. 4, pp. 308–320, 1976.

[57] R. S. D. H. N. K. C. W. G. Jay and J. Hale, “Cyclomatic
complexity and lines of code: empirical evidence of a stable
linear relationship,” Journal of Software Engineering and
Application, vol. 2, pp. 137–143, 2009.

[58] S. R. Chidamber and C. F. Kemerer, “A metrics suite for object
oriented design,” IEEE Transactions on Software Engineering,
vol. 20, no. 6, pp. 476–493, 1994.

[59] M. H. Halstead, Elements of Software Science (Operating and
Program- Ming Systems Series), Elsevier Science Inc., New
York, NY, USA, 1977.

[60] I. Herraiz, J. Gonzalez-Barahona, and G. Robles, “Towards a
theoretical model for software growth,” in Proceedings of the
Fourth International Workshop on Mining Software Reposi-
tories (MSR’07:ICSE Workshops 2007), Minneapolis, MN,
USA, May 2007.

[61] P. Oman and J. Hagemeister, “Metrics for assessing a software
system’s maintainability,” in Proceedings Conference on
Software Maintenance, Victoria, British Columbia, Canada,
November 1992.

[62] W. Li and S. Henry, “Object-oriented metrics that predict
maintainability,” Journal of Systems and Software, vol. 23,
no. 2, pp. 111–122, 1993.

[63] B. Curtis, J. Sappidi, and A. Szynkarski, “Estimating the
principal of an application’s technical debt,” IEEE Software,
vol. 29, no. 6, pp. 34–42, 2012.

[64] D. Spinellis, “Working with unix tools,” IEEE Software,

vol. 22, no. 6, pp. 9–11, 2005.

[65] S. Wagner, K. Lochmann, L. Heinemann et al., “'e quamoco
product quality modelling and assessment approach,” in
Proceedings of the 34th International Conference on Software
Engineering, IEEE Press, Zurich, Switzerland, June 2012.
[66] M. Fowler, Refactoring: Improving the Design of Existing Code,
Addison- Wesley Professional, Boston, MA, USA, 2018.
[67] R. Lincke, J. Lundberg, and W. L¨owe, “Comparing software
the 2008 International
metrics tools,” in Proceedings of
Symposium on Software testing and Analysis, Seattle, WA,
USA, July 2008.

[68] E. Dias Canedo, K. Valen¸ca, and G. A. Santos, “An analysis of
measure- ment and metrics tools: a systematic literature
in Proceedings of the 52nd Hawaii International
review,”
Conference on System Sciences, Maui, HI, USA, January 2019.
[69] D. I. Sjøberg, B. Anda, and A. Mockus, “Questioning software
main- tenance metrics: a comparative case study,” in Pro-
ceedings of the 2012 ACM-IEEE International Symposium on
Empirical Software Engineering and Measurement, IEEE,
Lund, Sweden, September 2012.

[70] A. S. Nun􏽥ez-Varela, H. G. P´erez-Gonzalez, F. E. Mart´ınez-
Perez, and C. Soubervielle-Montalvo, “Source code metrics: a
systematic mapping study,” Journal of Systems and Software,
vol. 128, pp. 164–197, 2017.

[71] S. Elmidaoui, L. Cheikhi, A. Idri, and A. Abran, “Empirical
studies on software product maintainability prediction: a
systematic mapping and review,” E-Informatica Software
Engineering Journal, vol. 13, no. 1, 2019.

[72] C. 'irumalai, P. A. Reddy, and Y. J. Kishore, “Evaluating
software metrics of gaming applications using code counter
tool for c and c++ (cccc),” in Proceedings of the 2017 Inter-
national Conference of Electronics, Communication and
Aerospace Technology (ICECA), Coimbatore, India, April
2017.

[73] U. Poornima, “Uniﬁed design quality metric tool for object-
oriented ap- proach including other principles,” International
Journal of Computer Applications in Technology, vol. 26,
pp. 1–4, 2011.

 5192, 2020, 1, Downloaded from https://onlinelibrary.wiley.com/doi/10.1155/2020/8840389 by Cochrane France, Wiley Online Library on [16/02/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
