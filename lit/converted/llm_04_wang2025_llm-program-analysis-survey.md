A Contemporary Survey of Large Language Model
Assisted Program Analysis
Jiayimei Wang, Tao Ni, Wei-Bin Lee, Qingchuan Zhao∗

1

5
2
0
2

b
e
F
5

]
E
S
.
s
c
[

1
v
4
7
4
8
1
.
2
0
5
2
:
v
i
X
r
a

Abstract—The increasing complexity of software systems
has driven significant advancements in program analysis,
as traditional methods unable to meet the demands of mod-
ern software development. To address these limitations,
deep learning techniques, particularly Large Language
Models (LLMs), have gained attention due to their context-
aware capabilities in code comprehension. Recognizing the
potential of LLMs, researchers have extensively explored
their application in program analysis since their intro-
duction. Despite existing surveys on LLM applications in
cybersecurity, comprehensive reviews specifically address-
ing their role in program analysis remain scarce. In this
survey, we systematically review the application of LLMs
in program analysis, categorizing the existing work into
static analysis, dynamic analysis, and hybrid approaches.
Moreover, by examining and synthesizing recent studies,
we identify future directions and challenges in the field.
This survey aims to demonstrate the potential of LLMs
in advancing program analysis practices and offer action-
able insights for security researchers seeking to enhance
detection frameworks or develop domain-specific models.

Keywords—Large Language Model, Program Analysis,

Vulnerability Detection

I.

INTRODUCTION

With the continuous advancement of information
technology, software plays an increasingly signif-
icant role in daily life, making its quality and
reliability a critical concern for both academia and
industry [1]. This is because software vulnerabili-
ties in domains such as finance, healthcare, critical
infrastructure, aerospace, and cybersecurity [2] can
lead to considerable financial losses or even societal
harm [3]. Examples include data breaches in finan-
cial systems, malfunctioning medical devices, dis-
ruptions to power grids, failures in aviation control

Jiayimei Wang, Tao Ni, and Qingchuan Zhao are with the
Department of Computer Science, City University of Hong
jwang2664-c@my.cityu.edu.hk,
Kong, Hong Kong SAR (e-mail:
taoni2@cityu.edu.hk, cs.qczhao@cityu.edu.hk). Wei-Bin Lee is with
the Information Security Center, Hon Hai Research Institute, Taipei,
Taiwan and the Department of Information Engineering and Com-
puter Science, Feng Chia University, Taichung, Taiwan (e-mail: wei-
bin.lee@foxconn.com, wblee@fcu.edu.tw).

∗ The corresponding author.

systems, and exploitation of security loopholes in
sensitive government networks. Accordingly, many
techniques have been proposed to detect such vul-
nerabilities that compromise software quality and
reliability, and program analysis has been proven
effective in such tasks. It aims to examine compter
programs to identify or verify their properties to
detect vulnerabilities through abstract interpretation,
constraint solving, and automated reasoning [4].

However, as software complexity and scale in-
crease,
traditional program analysis methods en-
counter challenges in meeting the demands of con-
temporary development. Specifically,
these tradi-
tional methods face substantial challenges in han-
dling dynamic behaviors, cross-language interac-
tions, and large-scale codebases [5], [6]. Fortunately,
recent advancements in machine learning have ini-
tiated a shift in program analysis [7] and shed light
on a promising research direction to address the
limitations of traditional program analysis methods.
In particular, the literature has attempted to com-
bine deep learning with program analysis, applying
it to strengthen the detection of vulnerabilities and
achieve automated code fixes, thereby minimizing
human intervention and increasing precision [8].
However, deep learning models lack the ability to
effectively integrate contextual
information over
long sequences, limiting their performance in tasks
requiring deep reasoning or multi-turn understand-
ing [9], [10]. Consequently, these models struggle
to handle complex software and large codebases
and lack the capability for cross-project analysis.

Fortunately, the most recent advancement, i.e.,
large language model
(LLM), has been found
promising in addressing the limitations of early
deep learning models, such as constrained con-
textual understanding and generalization, enabling
them to handle tasks across multiple domains with
greater versatility [11]–[15]. Particularly, as for
program analysis, LLMs surpass traditional deep
learning methods and have been applied to various

2

Fig. 1: Taxonomy of the survey.

tasks [16]–[20], including automated vulnerability
and malware detection, code generation and repair,
and providing scalable solutions that integrate static
and dynamic analysis methods. Moreover, it also
shows a great potential to cope with the growing
difficulty of analyzing modern software systems.

Though promising, the literature lacks a com-
prehensive and systematica view of LLM-assisted
program analysis given the presence of numerous
related attempts and applications. Therefore,
this
work aims to systematically review the state-of-the-
art of LLM-assisted program analysis applications
and specify its role in the development of program
analysis. To this end, we systematically review the
use of LLMs in program analysis and organized
them into a structured taxonomy. Figure 1 illustrates
the classification framework, where the relevant re-
search is categorized into LLM for static analysis,
LLM for dynamic analysis, and hybrid approach.
Unlike previous surveys that broadly examined the
applications of LLMs in cybersecurity, our work
narrows its focus to program analysis, delivering
a more detailed and domain-specific exploration.
In addition, we collect the limitations mentioned
in selected studies and analyze the improvements
brought by the integration of LLMs, and specify the
potential challenges and future research directions of
LLMs in this domain.

The survey is organized as follows. We first
introduce the background of program analysis and
large language model in § II. We then examine the
application of LLMs in static analysis in § III and
discusses the use of LLMs in dynamic analysis in
§ IV. We next explore how LLMs assist hybrid
approaches that combine static and dynamic analysis
in § V. We finally address the challenges of applying
LLMs to program analysis and outline potential

future research directions in § VI and conclude the
survey in § VII.

II. BACKGROUND
In this section, we first introduce prior knowledge
about program analysis (§ II-A), including static
analysis and dynamic analysis and the limitations in
existing approaches, and then present the concepts
of LLMs as well as the necesseity of leveraging
LLMs for advancing program analysis (§ II-B).

A. Program Analysis

Program analysis is the process of analyzing the
behavior of computer programs to learn about their
properties [21]. Program analysis can find bugs or
security vulnerabilities, such as null pointer deref-
erences or array index out-of-bounds errors. It is
also used to generate software test cases, automate
software patching and improve program execution
speed through compiler optimization. Specifically,
program analysis can be categorized into two main
types: static analysis and dynamic analysis [22].
Static analysis examines a program’s code without
execution, dynamic analysis collects runtime infor-
mation through execution, and hybrid analysis com-
bines both approaches for comprehensive results.

Static Analysis. Static analysis (a.k.a. compile-
time analysis)
is a program analysis approach
that identifies program properties by examining its
source code without executing the program. The
pipeline for static analysis consists of key stages
illustrated in Figure 2. The process begins with
parsing the code to extract essential structures and
relationships, which are transformed into interme-
diate representations (IRs) such as symbol tables,
abstract syntax trees (ASTs), control flow graphs
(CFGs), and data flow graphs (DFGs). These IRs are

LLM for  Program AnalysisLLM for  Static Analysis (§ III)LLM for Dynamic Analysis (§ IV)LLM for Hybrid Approach (§ V)Vulnerability Detection (§ III-A)Malware Detection (§ III-B)Program Verification (§ III-C)Static Analysis Enhancement (§ III-D)Malware Detection (§ IV-A)Fuzzing (§ IV-B)Penetration Testing (§ IV-C)Unit Test Generation (§ V-A)Others (§ V-B)3

Fig. 2: Static analysis workflow.

Fig. 3: Dynamic analysis workflow.

then analyzed to detect issues such as unreachable
code, data dependencies, and syntactic errors. These
series of processes ultimately enhance code quality
and reliability.

Dynamic Analysis. Dynamic analysis (a.k.a. run-
time analysis) is a program analysis approach that
uncovers program properties by repetitively exe-
cuting programs in one or more runs [23]. The
stages involved in dynamic analysis are depicted
in Figure 3. These stages include instrumenting the
source code to enable runtime tracking, compiling
the instrumented code into a binary, and executing
it with test suites. After completing the above steps,
program traces such as function calls, memory ac-
cesses and system calls are captured.

B. Large Language Models

Large Language Models (LLMs) are large-scale
neural networks built on deep learning techniques,
primarily utilizing the Transformer architecture [24].
Transformer models utilize self-attention mecha-
nism to identify relationships between elements
within a sequence, which enables them to out-
perform other machine learning models in under-
standing contextual relationships. Trained on vast
datasets, LLMs learn syntax, semantics, context,
and relationships within language, enabling them
to generate and comprehend natural language [25].
Furthermore, LLMs possess knowledge reasoning
capabilities, allowing them to retrieve and synthesize
information from large datasets to answer questions
involving common sense and factual knowledge.

The architecture and configuration features of
LLMs (e.g., model families, parameter size, and
context window length) collectively determine their
capabilities, performance and applicability. The
studies selected in this survey involve LLM model
families such as LLaMA [26], CodeLLaMA [27]
and GPT [28],
[29]. The parameter size of a
large model
typically refers to the number of
variables used for learning and storing knowledge.
The parameter size represents a model’s learning
capacity, indicating its ability to capture complexity
and detail from data. Generally, larger parameter
expressive power,
sizes
enabling it to learn more intricate patterns and finer
details. The context window refers to the range
of text fragments a model uses when generating
each output. It determines the amount of contextual
information the model
can reference during
generation. Selecting appropriate architectures and
configurations for LLMs in different scenarios is
crucial for optimizing their performance.

the model’s

enhance

III. LLM FOR STATIC ANALYSIS
Static analysis examines various objects, such
as analyzing vulnerabilities and detecting malware
in source code binary executables. Analyzing vul-
nerabilities in source code requires techniques like
dependency analysis and taint tracking to trace the
flow of sensitive data. On the other hand, Detecting
malware focuses on control flow examination and
behavior modeling to identify malicious patterns.
Consequently, LLM assistance differs by program

Source Codepublic class example{  public static int example(int x) {     if (x > 0) {      int result = 1; while (x > 1) result *= x--; return result;        }     return 0;    }  public static void main(String[] args) {              int y = example(5)      System.out.println(y);  }}Model ExtractionIntermediate RepresentationsASTCFGDFGAnalysisControl AnalysisComplexity EvaluationPath SimulationVulnerability DetectionResultsExecution MetricsCoverage Detected Defectspublic class example{  public static void main(String[] args) {    int a = 3;    int b = 5;    int c = 2;    int d; ①   if (a == 3 || b == 5) {     ②     a = b + c;         d = a + 2;     System.out.println("Value of a: " + a);    System.out.println("Value of d: " + d);  }}Source CodeInstrumented Code①Tmp1 = a == 3;Tmp2 = b == 5;Tmp3 = Tmp1 || Tmp2;Top.id = InstanceID;Top.index = 4;$sample_values(Tmp1,Tmp2,Tmp3);if(Tmp3)②a  = b + c;d  = a + 2;Top.id = InstanceID;Top.index = 5;$count_stmt;Compiled ProgramProgram TraceTest SuiteI/O OperationsExecution PathsThread EventsAPI CallsBinaryDebug Information4

Reference

AST CFG DFG OS App Vulnerability Type

LLM’s assistance

LLift [30]
SLFHunter [31]
LATTE [32]

IMMI [33]

DefectHunter [34]
IRIS [35]
VERACATION [36]

Mao et al. [37]

MSIVD [38]

GPTScan [39]
Yang et al. [40]
LLbezpeky [41]
SkipAnalyzer [42]

HYPERION [43]

Zhang et al. [44]
GPTLENS [45]
LuaTaint [46]

✗
✓
✗

✗

✓
✗
✓

✓

✗

✓
✓
✗
✓

✗

✓
✓
✓

✓
✓
✓

✓

✓
✓
✗

✗

✓

✗
✗
✗
✗

✓

✗
✗
✓

✗
✓
✓

✓

✓
✓
✓

✓

✓

✓
✗
✗
✓

✓

✓
✓
✓

✓
✓
✓

✓

✗
✗
✗

✗

✗

✗
✗
✗
✗

✗

✗
✗
✗

✗
✗
✗

✗

✓
✓
✓

✓

✓

✓
✓
✓
✓

✓

✓
✓
✓

Use-before-initialization (UBI).
Command injection vulnerabilities.
Binary taint analysis for data flows.

Kernel memory bugs.

General vulnerability.
Taint analysis in smart contracts.
Syntactic-based vulnerability.
Vulnerabilities in Code review pro-
cesses.

General vulnerability.

Smart contract logic vulnerabilities.
IoT software vulnerability.
Android security vulnerability.
Bug detection.

DApp Inconsistencies.

General vulnerability.
Smart contract vulnerability.
IoT vulnerability

Path analysis.
Taint sinks.
Binary taint analysis and code slicing.
Memory allocation and deallocation inten-
tions
Code sequence embeddings.
Taint sources and sinks.
Filters non-vulnerability-related statements.

Simulates multi-role discussions.

Fine-tuned with multitask self-instructed
learning.
Analyzes smart contract semantics.
Explains vulnerabilities in code.
Android application security.
Identifies bugs and generates patches.
Extracts attributes of smart contract byte-
code.
Detects vulnerabilities and fixes.
Generates diverse vulnerability hypotheses.
Prunes false alarms.

TABLE I: Overview of the intermediate representations (AST, CFG, DFG) employed, their application
domains (OS-level or application-level vulnerabilities), their application to specific vulnerability types,
and the assistance provided by LLMs across selected studies

type and analysis purpose, which will be discussed
in this section across four directions: (i) vulnera-
bility detection (§ III-A), (ii) malware detection (§
III-B), (iii) program verification (§ III-C), and (iv)
static analysis enhancement (§ III-D).

A. LLM for Vulnerability Detection

code

tools

automated

Leveraging

and
analysis

Vulnerability detection focuses on identifying
potential security risks or weaknesses in software
techniques,
through
and a
which demand precise
[47],
deep understanding of program behavior
[48].
contextual
comprehension, LLMs can analyze both semantic
and syntactic patterns in source code, providing
actionable suggestions and remediation strategies for
addressing vulnerabilities. As a result, integrating
LLMs into vulnerability detection has become a
prominent application in program analysis.

advanced

their

the

To provide a clearer understanding of LLM
in vulnerability detection, Table I
applications
summarizes
representations
(IRs) utilized and the specific vulnerability types
addressed in selected studies. Figure 4 offers a visual
overview of LLM integration at various stages,
highlighting their roles in contextual understanding,

intermediate

feature extraction, enhanced detection accuracy, and
remediation strategies. These capabilities enable
efficient and precise identification of OS-level and
a
application-level vulnerabilities. Additionally,
detailed comparison of the best-performing LLMs in
the reviewed studies reveals key factors influencing
their effectiveness and adoption. Table II presents a
comprehensive summary of these models, including
their model family, parameter sizes, context window
sizes, and open-source availability.

disrupt

access,

OS-level Vulnerability. OS-level vulnerabilities
refer to security flaws within critical components
of an operating system, such as the kernel, system
libraries, or device drivers. These vulnerabilities
can compromise the stability and security of
to gain
the entire system, allowing attackers
unauthorized
or
cause system-wide failures affecting all running
applications. Common examples include memory
management
and
resource misuse. Leveraging LLMs, tools like the
LLift framework [30] address challenges such as
path sensitivity and scalability in detecting OS-level
vulnerabilities. By combining constraint-guided
path analysis with task decomposition, LLift
improves the detection of issues like use-before-
initialization (UBI) in large-scale codebases. Ye et

operations,

escalation,

privilege

errors,

5

Fig. 4: A diagram of LLMs’ application in vulnerability detection.

al. [31] developed SLFHunter, which integrates
static taint analysis with LLMs to identify command
injection vulnerabilities in Linux-based embedded
firmware. The LLMs are utilized to analyze
custom dynamically linked library functions and
traditional analysis
enhance the capabilities of
tools. Furthermore, Liu et al.
[32] proposed a
system called LATTE, which combines LLMs
with binary taint analysis. The code slicing and
prompt construction modules serve as the core of
LATTE, where dangerous data flows are isolated for
analysis. These modules reduce the complexity for
LLMs by providing context-specific input, allowing
improved efficiency and precision in vulnerability
detection through tailored prompt sequences that
guide the LLM in the analysis process. In addition,
Liu et al. [33] proposed a system for detecting
kernel memory bugs using a novel heuristic
called Inconsistent Memory Management Intentions
(IMMI). The system detects kernel memory bugs by
summarizing memory operations and slicing code
related to memory objects. It uses static analysis
to infer inconsistencies in memory management
responsibilities between caller and callee functions.
in interpreting complex memory
LLMs assist
management mechanisms
the
and
such as memory leaks
identification of bugs
and use-after-free errors with improved precision.

enable

Application-level Vulnerability. Application-
level vulnerabilities are security weaknesses found
within individual software programs. These vulner-

abilities can compromise the application’s perfor-
mance, data integrity, or user privacy. However, they
typically do not affect the overall stability of the
operating system. Common examples include input
logic errors, and misconfigura-
validation issues,
tions. These vulnerabilities can result in unautho-
rized access or data breaches, as well as application-
specific security incidents [49]–[55].

To address the challenges in application-level
vulnerability detection, Wang et al. [34] introduced
the Conformer mechanism, which integrates self-
attention and convolutional networks to capture both
local and global feature patterns. To further refine
the detection process, they optimize the attention
mechanism to reduce noise in multi-head attention
and improve model stability. By combining struc-
tural
information processing, pre-trained models,
and the Conformer mechanism in a multi-layered
framework, the approach improves detection accu-
racy and efficiency. Building on these advancements,
IRIS [35] proposes a neuro-symbolic approach that
combines LLMs with static analysis to support
reasoning across entire projects. The static analysis
is responsible for extracting candidate sources and
sinks, while the LLM infers taint specifications
for specific CWE categories. Similarly, Cheng et
al. [36] combined semantic-level code clone de-
tection with LLM-based vulnerability feature ex-
traction. By integrating program slicing techniques
with the LLM’s semantic understanding, they re-
fined vulnerability feature detection. This approach

Semantic & Syntactic AnalysisData Flow TrackingControl Flow TrackingAutomatic Vulnerability DetectionFalse Positive FilteringPatch Solution Generation Contextual UnderstandingFeature ExtractionEnhance Detection Accuracy & Reduce False PositiveAutomatic Code Review & Patch GenerationRemediation RecommendationsConfidence ScoresPre-processingDetection ModelVulnerability Reports         LLM AssistanceVulnerability TypesVulnerable ComponentsRoot CausesData CollectionOS-level VulnerabilityApplication-level VulnerabilityKernel CodeApplication Source CodeIoT SoftwareCode Sourceaddresses the limitations of traditional syntactic-
based analysis.

Reference

LLM

MF

Param CW Open-Source

-
-
-
-

-
GPT-4
GPT-4

GPT-4
GPT-4-0613
GPT-4
GPT-4.0
GPT-4.0
GPT-4
ChatGPT-4-1106 GPT-4

LLift [30]
SLFHunter [31]
LATTE [32]
IMMI [33]
DefectHunter [34] UniXcoder
IRIS [35]
GPT-4.0
VERACATION [36] GPT-4.0
Mao et al. [37]
MSIVD [38]
GPTScan [39]
Yang [40]
LLbezpeky [41]
SkipAnalyzer [42] ChatGPT-4.0
HYPERION [43]
Zhang et al. [44]
GPTLENS [45]
LuaTaint [46]

32768
32768
32768
32768
250M 768
32768
1024
GPT-3.5-turbo GPT-3.5
175B 4096
CodeLlama-13B CodeLlama 13B 2048
175B 4096
GPT-3.5-turbo GPT-3.5
32768
ChatGPT-4.0
32768
GPT-4.0
8192
4096
8192
32768
1920

GPT-4
GPT-4
GPT-4
LLaMA
GPT-4
GPT-4
GPT-4

LLaMA2 [56]
ChatGPT-4.0
GPT-4.0
GPT-4.0

-
-
-
-
-
-
-

-
-

✗
✗
✗
✗
✓
✗
✗
✗
✓
✗
✗
✗
✗
✓
✗
✗
✗

TABLE II: Overview of the best-performing LLMs
used in referenced papers, their model families
(MF), parameter sizes (Param), context window
sizes (CW), and open-source availability.

Mao et al. [37] implemented a multi-role ap-
proach where LLMs act as different roles, such
as testers and developers, simulating interactions
in a real-life code review process. This strategy
fosters discussions between these roles, enabling
each LLM to provide distinct insights on potential
vulnerabilities. MSIVD [38] introduces a multi-task
self-instructed fine-tuning technique that combines
vulnerability detection, explanation, and repair, im-
proving the LLM’s ability to understand and reason
about code through multi-turn dialogues. Addition-
ally, the system integrates LLMs with a data flow
analysis-based GNN, which models the program’s
control flow graph to capture variable definitions
and data propagation paths. This enables the model
to rely not only on the literal information in the
code but also on the program’s graph structure for
more precise detection. Similarly, GPTScan [39]
demonstrates how GPT can be applied to code un-
derstanding and matching scenarios, reducing false
positives and uncovering new vulnerabilities previ-
ously missed by human auditors.

In the domain of IoT software, Yang et al. [40]
explored the application of LLMs combined with
static code analysis for detecting vulnerabilities.
By leveraging prompt engineering, LLMs enhance

6

the efficiency of vulnerability detection and reduce
costs, ultimately improving scalability and feasi-
bility in large IoT systems [57]–[59]. Meanwhile,
Xiang et al. [46] proposed LuaTaint, a static anal-
ysis framework designed to detect vulnerabilities
in the web configuration interfaces of IoT de-
vices. LuaTaint integrates flow-, context-, and field-
sensitive static taint analysis with key features such
as framework-specific adaptations for the LuCI web
interface and pruning capabilities powered by GPT-
4. By converting Lua code into ASTs and CFGs,
the framework performs precise taint analysis to
identify vulnerabilities like command injection and
path traversal. The system uses dispatching rules and
LLM-powered alarm pruning to improve detection
precision, reduce false positives, and efficiently an-
alyze firmware across large-scale datasets.

Mohajer et al. [42] presented SkipAnalyzer, a tool
that employs LLMs for bug detection, false positive
filtering, and patch generation. By improving the
precision of existing bug detectors and automating
patching, this approach significantly reduces false
positives and ensures accurate bug repair. Mean-
while, Zhang et al. [44] introduced tailored prompt
engineering techniques with GPT-4 [29], leveraging
auxiliary information such as API call sequences
and data flow graphs to provide structural and se-
quential context. This approach also employs chain-
of-thought prompting to enhance reasoning capabil-
ities, demonstrating improved accuracy in detecting
vulnerabilities across Java and C/C++ datasets. Ex-
tending the application of LLMs in decentralized
applications and smart contract analysis, Yang et
al. [43] developed HYPERION, which combines
language analysis with sym-
LLM-based natural
bolic execution to address inconsistencies between
DApp descriptions and smart contracts. The system
integrates a fine-tuned LLM to analyze front-end
descriptions, while symbolic execution processes
contract bytecode to recover program states, effec-
tively identifying discrepancies that may undermine
user trust.

For smart contract vulnerability detection, Hu et
al. [45] introduced GPTLENS, a two-stage adversar-
ial framework leveraging LLMs. GPTLENS assigns
two synergistic roles to LLMs: an auditor generates
a diverse set of vulnerabilities with associated rea-
soning, while a critic evaluates and ranks these vul-
nerabilities based on correctness, severity, and prof-
itability. This open-ended prompting approach facil-

itates the identification of a broader range of vulner-
abilities, including those that are uncategorized or
previously unknown. Experimental results on real-
world smart contracts show that GPTLENS outper-
forms traditional one-stage detection methods while
maintaining low false positive rates. Focusing on
Android security and software bug detection, Math-
ews et al. [41] introduced LLbezpeky, an AI-driven
workflow that assists developers in detecting and
rectifying vulnerabilities. Their approach analyzed
Android applications, achieving over 90% success in
identifying vulnerabilities in the Ghera benchmark.

Takeaway 1

Researchers utilize static analysis with dif-
ferent intermediate representations and LLMs
to address different types of vulnerabilities.
ASTs enhance syntactic reasoning and code
representation for syntax-related vulnerabili-
ties. CFGs address control flow issues such as
privilege escalation by prioritizing paths and
detecting anomalies. DFGs focus on data-flow
vulnerabilities such as command injection,
enabling LLMs to infer taint sources and
refine detection rules. This integration of IRs
and LLMs strengthens detection capabilities.
Among LLMs, GPT-4 is commonly adopted
for its large context window and versatil-
ity. Task-specific models like UniXcoder [60]
perform well in specialized scenarios, while
open-source models such as CodeLlama [61]
provide reproducibility and flexibility.

B. LLM for Malware Detection

Malware detection determines whether a program
has malicious intent and is an essential aspect of pro-
gram analysis research. Initially, signature-based de-
tection methods were predominantly used. As mal-
ware evolved, new detection techniques emerged,
including behavior-based detection, heuristic detec-
tion, and model checking approaches. Data mining
and machine learning algorithms soon followed,
further enhancing detection capabilities [62]–[67].

Traditional malware detection methods struggle
with challenges like obfuscation and polymorphic
malware. LLMs offer a new approach to enhance
to evolving threats
detection accuracy and adapt
by analyzing code semantics and patterns. Fujii et

7

al. [68] utilized decompiled and disassembled out-
puts of the Babuk ransomware as inputs to the LLM
to generate function descriptions through carefully
designed prompts. The generated descriptions were
evaluated using BLEU [69] and ROUGE [70] met-
rics to measure functional coverage and agreement
with analysis articles. Additionally, Simion et al.
[71] evaluated the feasibility of using out-of-the-box
open-source LLMs for malware detection by analyz-
ing API call sequences extracted from binary files.
The study benchmarked four open-source LLMs
(Llama2-13B, Mistral [72], Mixtral, and Mixtral-
FP16 [73]) using API call sequences extracted from
20,000 malware and benign files. The results showed
that the models, without fine-tuning, achieved low
accuracy and were unsuitable for real-time detec-
the need for fine-
tion. These findings highlight
tuning and integration with traditional security tools.
Analyzing malicious behaviors to detect malware
is another approach. Zahan et al. [74] employed
a static analysis tool named CodeQL [75] to pre-
screen npm packages. This step filtered out benign
files, thereby reducing the number of packages re-
quiring further investigation. Following this step,
they utilized GPT-3 and GPT-4 models to analyze
the remaining JavaScript code for detecting complex
or subtle malicious behaviors. The outputs from the
LLMs were refined iteratively. Accuracy improved
through continuous adjustments to the model’s focus
based on feedback and re-evaluation.

on

focus

Other

studies

applying LLMs
specifically to Android malware detection. Khan et
al. [76] extracted Android APKs to obtain source
code and opcode sequences, constructing call graphs
the structural relationships between
to represent
functions. Models such as CodeBERT [77] and
GPT were employed to generate semantic feature
representations, which were used to annotate the
nodes in the call graphs. The graphs were enriched
with structural and semantic information. These
enriched graphs were then processed through a
graph-based neural network to detect malware in
Android applications. Zhao et al. [78] first extracted
features
from Android APK files using static
analysis, categorizing them into permission view,
API view, and URL & uses-feature view. A multi-
view prompt engineering approach was applied to
guide the LLM in generating textual descriptions
and summaries for each feature category. The
generated descriptions were transformed into vector

representations, which served as inputs for a deep
neural network (DNN)-based classifier to determine
whether the APK was malicious or benign. Finally,
the LLM produced a diagnostic report summarizing
the potential risks and detection results.

Takeaway 2

The integration of LLMs with static analysis
techniques enables the analysis of structured
input sources,
including decompiled func-
tions, API call sequences, JavaScript code
files, and APK attributes. A key commonality
across approaches is the reliance on LLMs
to process static features and generate se-
mantic representations, textual descriptions,
or embeddings, which are subsequently used
for classification or detection tasks. Addition-
ally, we notice that both open-source LLMs
(e.g., Llama2-13B and Mistral) and propri-
etary models (e.g., GPT-4) are widely utilized
in this task.

C. LLM for Program Verification

Automated program verification employs tools
and algorithms to ensure that a program’s behav-
ior aligns with predefined specifications, enhanc-
ing both software reliability and security. Tradi-
tional verification methods often require substantial
manual effort, particularly for writing specifications
and selecting strategies. These processes are often
complex and prone to errors, especially in large-
scale systems. In contrast, automated verification
generates key elements such as invariants, precon-
ditions, and postconditions, using techniques like
static analysis and model checking to ensure correct-
ness. The integration of LLMs further enhances this
process by enabling the automatic analysis of code
features and the efficient selection of verification
strategies. This reduces manual
intervention and
significantly accelerates verification. Consequently,
automated program verification has evolved into
a more efficient and reliable method for ensuring
software quality. This subsection introduces diverse
applications of LLMs in program verification, high-
lighting their role in automating and enhancing
critical tasks.

Table III provides an overview of various studies
utilizing LLMs for program verification. It summa-
rizes their targets, methodologies, and outcomes to

8

highlight the diverse applications of these models
in automating verification tasks. The inputs in
these studies can be categorized into four types: (i)
Code, which includes program implementations or
snippets used for analysis or synthesis. (ii) Specifi-
cations, referring to formal descriptions of program
behavior, such as preconditions, postconditions, or
logical formulas. (iii) Formal methods, encompass-
ing mathematical constructs like theorems, proofs,
and loop invariants for ensuring correctness. (iv)
Error and debugging information, such as coun-
terexamples, type hints, or failed code generation
cases that aid in resolving programming issues.

Proof Generation. Proof generation in program
verification automates the creation of formal proofs
to ensure program correctness, logical consistency,
and compliance with specifications. This process
reduces the need for manual effort and enhances ver-
ification efficiency by streamlining complex proof
tasks. Kozyrev et al. [79] developed CoqPilot, a
VSCode plugin that integrates LLMs such as GPT-4,
GPT-3.5, LLaMA-2 [26], and Anthropic Claude [93]
with Coq-specific tools like CoqHammer [94] and
to automate proof generation in
Tactician [95]
the Coq theorem prover. The authors implemented
premise selection for better LLM prompting and
created an LLM-guided mechanism that attempted
fixing failing proofs with the help of the Coq’s error
messages. Additionally, Zhang et al. [80] developed
the Selene framework to automate proof generation
in software verification using LLMs. The framework
is built on the industrial-level operating system
microkernel [96], seL4 [97], and introduces the
technique of lemma isolation to reduce verification
time. Its key contributions include efficient proof
validation, dependency augmentation, and showcas-
ing the potential of LLMs in automating complex
verification tasks.

Invariant Generation. Invariant generation iden-
tifies properties that remain true during program
execution, providing a logical foundation for ver-
ifying correctness and analyzing complex iterative
structures like loops and recursion.

Some studies have explored various ways to
leverage LLMs for generating and ranking loop
invariants. Janßen et al. [82] investigated the utility
of ChatGPT in generating loop invariants. The
authors used ChatGPT to annotate 106 C programs
from the SV-COMP Loops category [98] with loop
invariants written in ACSL [99], evaluating the

Reference

Target

LLM

Param OS

Input

Output

9

CoqPilot [79]

Selene [80]

iRank [81]

Janßen et al. [82]
Pirzada et al. [83]

Proof generation

Proof generation

Claude
LLaMA-2-13B
GPT-3.5
GPT-4*
GPT-3.5-turbo
GPT-4*
GPT-3.5-turbo
GPT-4*
Loop invariant generation GPT-3.5
Loop invariant generation GPT-3.5-Turbo-Instruct

Loop invariant ranking

LaM4Inv [84]

Loop invariant generation

Pei et al. [85]

Invariant prediction

AutoSpec [86]

Specification synthesis

LEMUR [87]

Automated verification

SynVer [88]

Automated verification

LLaMA-3-8B
GPT-3.5-Turbo
GPT-4-Turbo*
GPT-4
GPT-3.5-turbo-0613*
Llama-2-70B
GPT-3.5-turbo
GPT-4*
GPT-4

PropertyGPT [89]

Smart contract verification GPT-4-0125-preview

LLM-Sym [90]

CFStra [91]

Chapman et al. [92]

Python symbolic execu-
tion
Verification strategy selec-
tion
Error specification infer-
ence

GPT-4o-mini
GPT-4o

GPT-3.5-turbo

GPT-4

-
13B
-
-
175B
-
175B
-
175B
175B
8B
175B
-
-
175B
70B
175B
-
-

-

-
-

175B

-

✗
✓
✗
✗
✗
✗
✗
✗
✗
✗
✓
✗
✗
✗
✗
✓
✗
✗
✗

✗

✗
✗

✗

✗

Formal methods

Coq proofs

Specifications

Formal proofs

Formal methods

Specifications
Formal methods

Reranked LLM-generated invari-
ants
Valid loop invariants
Loop invariants

Code

Code

Code

Loop invariants

Static invariants

Specifications

Specifications

Loop invariants

Specifications
Code and specifica-
tions
Error and debugging
Error and debugging
Code and specifica-
tions

Candidate C programs

Formal verification properties

Initial Z3Py code
Refined Z3Py code

Identified code features

Formal methods

Error specifications

TABLE III: Overview referenced studies, detailing their targets, LLMs employed, parameter sizes
(Param), open-source availability (OS), input types, and resulting outputs.

validity and usefulness of these invariants. They
integrated ChatGPT with the Frama-C [100] inter-
active verifier and the CPAchecker [101] automatic
verifier to assess how well the generated invariants
enable these tools to solve verification tasks. Results
showed that ChatGPT can produce valid and useful
invariants for many cases,
facilitating software
verification by augmenting traditional methods with
insights provided by LLMs. Additionally, Chakra-
bor et al. [81] observed that employing LLMs in
a zero-shot setting to generate loop invariants often
led to numerous attempts before producing correct
invariants, resulting in a high number of calls to
the program verifier. To mitigate this issue, they
introduced iRank, a re-ranking mechanism based on
contrastive learning, which effectively distinguishes
correct
invariants. This method
significantly reduces the verification calls required,
improving efficiency in invariant generation.

from incorrect

Besides, Pei et al. [85] explored using LLMs to
predict program invariants that were traditionally
generated through dynamic analysis. By fine-tuning
LLMs on a dataset of Java programs annotated with

invariants from the Daikon [102] dynamic analyzer,
they developed a static analysis-based method using
a scratchpad approach. This technique incrementally
generates invariants and achieves performance com-
parable to Daikon without requiring code execution.
It also provides a static and cost-effective alternative
to dynamic analysis.

Integrating LLMs with Bounded Model Checking
(BMC) has shown potential
in enhancing loop
invariant generation. Pirzada et al. [83] proposed
a modification to the classical BMC procedure that
avoids the computationally expensive process of
loop unrolling by transforming the CFG. Instead
of unrolling loops,
the framework replaces loop
segments in the CFG with nodes that assert the
invariants of the loop. These invariants are generated
using LLMs and validated for correctness using
a first-order theorem prover. This transformation
produces loop-free program variants in a sound
manner, enabling efficient verification of programs
with unbounded loops. Their experimental results
resulting tool, ESBMC
demonstrate
ibmc, significantly improves the capability of the

that

the

industrial-strength software verifier ESBMC [103],
verifying more programs compared to state-of-the-
art tools such as SeaHorn [104] and VeriAbs [105],
including cases
these tools could not handle.
Wu et al. [84] proposed LaM4Inv, a framework that
integrates LLMs with BMC to improve this process.
The framework employs a ’query-filter-reassemble’
pipeline. LLMs generate
invariants,
candidate
incorrect predicates, and valid
BMC filters out
predicates are iteratively refined and reassembled
into invariants.

Automated Program Verification. Automating
program specification presents challenges such as
handling programs with complex data types and
code structures. To address these issues, Wen et
al. [86] introduced an approach called AutoSpec.
Driven by static analysis and program verification,
AutoSpec uses LLMs to generate candidate spec-
ifications. Programs are decomposed into smaller
components to help LLMs focus on specific sec-
tions. The generated specifications are iteratively
validated to minimize error accumulation. This pro-
cess enables AutoSpec to handle complex code
structures, such as nested loops and pointers, mak-
ing it more versatile than traditional specification
synthesis techniques. Wu et al. [87] introduced the
LEMUR framework. In this hybrid system, LLMs
generate program properties like invariants as sub-
goals, which are then verified and refined by rea-
soners such as CBMC [106], ESBMC [103] or
UAUTOMIZER [107]. The framework is based on a
sound proof system, thus ensuring correctness when
LLMs propose incorrect properties. An oracle-based
refinement mechanism improves these properties,
enabling LEMUR to enhance efficiency in verifi-
cation and handle complex programs more effec-
tively than traditional tools. Additionally, Mukher-
jee et al. [88] introduced SynVer, a framework
that integrates LLMs with formal verification tools
for automating the synthesis and verification of C
programs. SynVer takes specifications in Separa-
tion Logic, function signatures, and input-output
examples as input. It leverages LLMs to generate
candidate programs and uses SepAuto, a verification
the
backend,
specifications. The framework prioritizes recursive
program generation, reducing the dependency on
manual loop invariants and improving verification
success rates.

to validate these programs against

Others. Other applications of LLMs in program

10

verification include smart contract verification,
symbolic execution, strategy selection and error
specification inference. For instance, Liu et al. [89]
developed a novel framework named PropertyGPT,
leveraging GPT-4 to automate the generation of
formal properties such as invariants, pre-/post-
conditions, and rules for smart contract verification.
The framework embeds human-written properties
into a vector database and retrieves reference
properties
for customized property generation,
ensuring their compilation, appropriateness, and
runtime verifiability through iterative feedback and
ranking. Similarly, Wang et al. [90] introduced an
iterative framework named LLM-Sym. This tool
leverages LLMs to bridge the gap between program
constraints and SMT solvers. The process begins
by extracting control flow paths, performing type
inference, and iteratively generating Z3 [108] code
to solve path constraints. A notable feature of LLM-
Sym is its self-refinement mechanism, which utilizes
error messages to debug and enhance the generated
Z3 code. If the code generation process fails, the
system directly employs LLMs to solve the con-
straints. Once constraints are resolved, Python test
cases are automatically generated from Z3’s outputs.
Another approach [91] automates the selection
of verification strategies to overcome limitations
of traditional tools like CPAchecker [101]. These
tools often require users to manually select strate-
gies, making the process more complex and time-
consuming. LLMs analyze code features to identify
suitable strategies, streamlining the verification pro-
cess and minimizing user input. This automation
not only improves efficiency but also minimizes
reliance on expert knowledge. Additionally, Chap-
man et al. [92] proposed a method that combines
static analysis with LLM prompting to infer error
specifications in C programs. Their system queries
the LLM when static analysis encounters incomplete
information, enhancing the accuracy of error specifi-
cation inference. This approch is effective for third-
party functions and complex error-handling paths.

Takeaway 3

The applications of LLMs in program veri-
fication span various tasks, including proof
generation, specification synthesis, loop in-
variant generation, and strategy selection.

These methods streamline the verification
process by automating the generation of prop-
erties, invariants, and other critical compo-
nents essential for program analysis. Despite
their diverse applications, these methods share
a common goal: reducing reliance on expert
knowledge and improving verification effi-
ciency. A key aspect of achieving this goal
is the iterative refinement of LLM-generated
outputs. This refinement process often incor-
porates static analysis or hybrid frameworks
that integrate formal verification tools, further
enhancing reliability.

D. LLM for Static Analysis Enhancement

Beyond the previously mentioned applications of
LLMs, other studies focus on leveraging LLMs to
assist in certain processes of static analysis.

that

Code Review Automation. Lu et al. [109] pro-
leverages
posed LLaMA-Reviewer, a model
LLMs to automate code review. It
incorporates
instruction-tuning of a pre-trained model and em-
ploys Parameter-Efficient Fine-Tuning techniques to
minimize resource requirements. The system auto-
mates essential code review tasks, including pre-
dicting review necessity, generating comments, and
refining code.

[110]

Code Coverage Prediction. Dhulipala

et
al.
introduced CodePilot, a system that
integrates planning strategies and LLMs to predict
code coverage by analyzing program control flow.
CodePilot first generates a plan by analyzing
program semantics, dividing the code into steps
derived from control flow structures, such as loops
adopts
and branches. Subsequently, CodePilot
in
either a single-prompt approach (Plan+Predict
one step) or a two-prompt approach (planning first,
followed by coverage prediction). These approaches
guide LLMs to predict which parts of the code are
likely to be executed based on the formulated plan.
Decompiler Optimization. Hu et al. [111] pro-
posed DeGPT, a framework designed to enhance
the clarity and usability of decompiler outputs for
reverse engineering tasks. DeGPT begins by ana-
lyzing the raw output of decompilers, identifying
issues such as ambiguous variable names, missing
comments, and poorly structured code. The frame-
work leverages LLMs in three distinct roles:Referee,

11

Advisor, and Operator to propose and implement op-
timizations while preserving semantic correctness.
Explainable Fault Localization. Yan et al. [112]
proposed CrashTracker, a hybrid framework that
combines static analysis with LLMs. This approach
improves the accuracy and explainability of crashing
fault localization in framework-based applications.
CrashTracker introduces Exception-Thrown Sum-
maries (ETS) to represent fault-inducing elements
in the framework. It also uses Candidate Informa-
tion Summaries (CIS) to extract relevant contextual
information for identifying buggy methods. ETS
models are employed to identify potential buggy
methods. LLMs then generate natural language fault
reports based on CIS data, enhancing the clarity of
fault explanations. CrashTracker demonstrates state-
of-the-art performance in precision and explainabil-
ity when applied to Android applications.

a

tool

[113]

Extract Method Refactoring. Pomian
introduced EM-Assist,

et
al.
that
combines LLMs and static analysis to enhance
Extract Method (EM)
refactoring in Java and
Kotlin projects. EM-Assist uses LLMs to generate
static
EM refactoring suggestions and applies
analysis to discard irrelevant or impractical options.
To improve the quality of suggestions,
the tool
employs program slicing and ranking mechanisms
to prioritize refactorings aligned with developer
preferences. EM-Assist
entire
refactoring process by leveraging the IntelliJ IDEA
platform to safely implement changes.

automates

the

Obfuscated Code Disassembly. Rong et al. [114]
introduced DISASLLM, a framework that combines
traditional disassembly techniques with LLMs. The
LLM component validates disassembly results and
repairs errors in obfuscated binaries, enhancing the
quality of the output. Through batch processing and
GPU parallelization, DISASLLM achieves substan-
tial improvements in both the accuracy and speed
of decoding obfuscated code, outperforming state-
of-the-art methods

Privilege Variable Detection. Wang et al. [115]
presented a hybrid workflow that combines LLMs
with static analysis to detect user privilege-related
variables in programs. The program is first ana-
lyzed to identify relevant variables and their data
flows, which provides an initial set of potential
user privilege-related variables. The LLM is used
to evaluate these variables by understanding their
context and scoring them based on their relationship

to user privileges.

tools

Static Bug Warning

Inspection. Wen et
al. [116] proposed LLM4SA, a framework that
integrates LLMs with static analysis
to
automatically inspect large volumes of static bug
warnings. LLM4SA first extracts bug-relevant code
snippets using program dependence traversal. It then
formulates customized prompts with techniques
such as Chain-of-Thought reasoning and few-shot
learning. To ensure precision,
the framework
applies pre- and post-processing steps to validate
challenges
the
like token limitations by optimizing input size,
reduces inconsistencies in LLM responses through
structured prompt engineering, and mitigates false
positives via comprehensive validation.

approach tackles

results. This

Static Analysis Alert Adjudication. Flynn et
al. [117] proposed using LLMs to automatically
adjudicate static analysis alerts. The system gener-
ates prompts with relevant code and alert details,
enabling the LLM to classify alerts as true or false
positives. To address context window limitations,
the system summarizes relevant code and provides
mechanisms for the LLM to request additional de-
tails or verify its classifications.

Static Analysis Enhancement by Pseudo-code
Execution. Hao et al. [118] presented E&V, a
system designed to enhance static analysis using
LLMs by simulating the execution of pseudo-code
and verifying the results without needing external
validation. It validates the results of the analy-
sis through an automatic verification process that
checks for errors and inconsistencies in the pseudo-
code execution. This system is particularly useful for
tasks like crash triaging and backward taint analysis
in large codebases like the Linux kernel.

Takeaway 4

The methods in this subsection demonstrate
how LLMs integrate with static analysis
across domains such as debugging, fault lo-
calization, code refactoring, and privilege de-
tection. A notable insight is the use of LLMs
not just as generative tools but as collabora-
tors that complement static analysis through
contextual reasoning and iterative refinement.

12

IV. LLM FOR DYNAMIC ANALYSIS

Dynamic analysis encompasses profiling and test-
ing. Profiling focuses on understanding program per-
formance by analyzing execution, such as counting
statement or procedure executions through instru-
mentation. Testing aims to make sure the test suites
can cover a program. Statement coverage verifies
that every statement in the code is executed at least
once during testing. Branch, condition, and path
coverage evaluate how thoroughly all branches, con-
ditions, and execution paths are tested [23]. This sec-
tion examines how LLMs enhance dynamic analysis,
focusing on (i) malware detection (§ IV-A) under
profiling, (ii) fuzzing (§ IV-B) and (iii) penetration
testing (§ IV-C) under testing.

A. LLM for Malware Detection

As discussed in § III-B, the definition of malware
subsection focuses
detection is provided. This
on using LLMs
to analyze runtime data for
malware detection. The distinction between static
and dynamic analysis depends primarily on the
input source. For instance, if API call sequences
are captured during program runtime, such as
through sandboxes, debuggers, or runtime analysis
frameworks, they are classified as dynamic analysis.
Conversely, API call sequences extracted through
methods like decompilation or disassembly from
static files are classified as static analysis. Table IV
provides an overview of LLMs in both static and
dynamic approaches and their testing accuracy.

Yan et al. [119] proposed a dynamic malware
detection method that utilizes GPT-4 to generate text
representations for API calls, which are an essential
feature in dynamic malware analysis. Their method
incorporates the innovative use of prompt engineer-
ing, allowing GPT-4 to generate highly detailed,
context-rich descriptions for each API call
in a
sequence. These descriptions go beyond simple API
names and delve into the specifics of how each API
call behaves within the context of the malware’s ex-
ecution. This provides a much deeper understanding
of the malware’s actions, as opposed to traditional
approaches that primarily rely on raw, unprocessed
sequences of API calls. After generating these de-
scriptions, the next step in the pipeline involves
using BERT to convert
the textual descriptions
into embeddings. These embeddings encapsulate the
semantic information of the API calls and their

Reference

Target Malware

Input Source

Type

LLM

Param CW OS Accuracy

13

Fujii et al. [68]

Babuk ransomware

Decompiled/disassembled functions

Static

Simion et al. [71]

General malicious files API call sequences

Zahan et al. [74]

Malicious packages

JavaScript code files

Khan et al. [76]

Android malware

APK files

Zhao et al. [78]

Android malware

APK files

Static

Static

Static

Static

Yan et al. [119]

General malware

API call sequences

Dynamic

ChatGPT-4.0
Llama2-13B
Mistral
Mixtral
Mixtral-FP16
GPT-3.5-turbo-1106
GPT-4-1106-preview
CodeBERT
GPT-2
RoBERTa
GPT-4-1106-preview
BERT
GPT-4

Sun et al. [120]

Linux-based malware

System call traces

Dynamic ChatGPT-3.5

Sanchez et al. [121]

IoT malware

System call traces

Dynamic

Li et al. [122]

Android malware

Code features and system calls

Hybrid

BERT
DistilBERT
GPT-2
BigBird
Longformer
Mistral
ChatGPT

4096
8192
125M 512
1.5B
125M 512

✗
-
8192
4096 ✓
13B
8192 ✓
7.3B
7∼13B 4096 ✓
7∼13B 4096 ✓
✗
175B
✗
-
✓
1024 ✓
✓
✗
✓
✗
-
✗
175B
✓
110M 512
✓
512
66M
1024 ✓
1.5B
110M 4096 ✓
150M 4096 ✓
8192 ✓
7.3B
✗
-
-

110M 512
8192
4096

8192

-

90.90%
50%
51%
67%
72%
91%
99%
95.29%
94.89%
94.94%
97.15%

95.61%

-
67.72%
63%
69%
87%
86%
58%
-

TABLE IV: Overview of the LLMs used in referenced papers, their target malware, input sources, type of
analysis, parameter sizes (Param), context window sizes (CW), open-source availability (OS), and testing
accuracy.

interactions, thereby forming a high-quality repre-
sentation of the entire API sequence. These repre-
sentations are then passed through a CNN, which
performs feature extraction and classification. This
comprehensive approach addresses several major
challenges faced by traditional API-based models.

Takeaway 5

Dynamic malware detection with LLMs ana-
lyzes runtime behaviors like API and system
call
traces to improve accuracy and inter-
pretability. Larger models like GPT-4 enhance
adaptability to unseen patterns, while smaller
models like BERT are efficient for real-time
tasks. Hybrid approaches further optimize de-
tection by balancing interpretability and scal-
ability.

Similarly, Sun et al. [120] developed a frame-
work that uses dynamic analysis and LLMs to
generate detailed cyber threat
intelligence (CTI)
reports. The framework captures syscall execution
traces of malware and converts them into natural
language descriptions using a Linux syscall trans-
former. These descriptions are organized into an
Attack Scenario Graph (ASG) to preserve essential
details and reduce redundancy. Sanchez et al. [121]
applied pre-trained LLMs with transfer learning for
malware detection. They fine-tuned the models with
a classification layer on a dataset of benign and
malicious system calls. This approach allows the
model to distinguish between normal and malicious
behavior while avoiding the need for training from
scratch by leveraging pre-trained LLMs.

B. LLM for Fuzzing

Fuzzing is a technique for automated software
testing that inputs randomized data into a program
to detect vulnerabilities like crashes, assertion fail-
ures, or undefined behaviors. The classifications of
fuzzing is shown in Figure 5. Fuzzing approaches
are categorized by three dimensions: test case gen-
eration, input structure, and program structure. Test
case generation can be mutation-based which alters
existing inputs, or generation-based which creates
new inputs from scratch. Input structure distin-
guishes smart fuzzing which utilizes input format
knowledge, from dumb fuzzing which generates
inputs blindly. Program structure analysis classifies
fuzzing as black-box, grey-box, or white-box, based
on the tester’s level of program insight.

14

and transitions to unexplored protocol states. This
approach overcomes challenges like reliance on
initial seeds and restricted state-space exploration.
Beyond domain-specific applications, frameworks
like LLAMAFUZZ [127] and CHATFUZZ [129]
showcase the adaptability of LLMs for general
program fuzzing. Zhang et al. proposed LLAMA-
FUZZ, which combines greybox fuzzing with LLM-
based mutation to enhance branch coverage and
bug detection. Its focus on structured data inputs
makes it an effective tool for augmenting traditional
fuzzing methods, demonstrating improvements over
AFL++ [137]. Similarly, Hu et al. introduced CHAT-
FUZZ,
leveraging ChatGPT to generate format-
conforming test cases for highly structured inputs,
addressing the efficiency limitations of traditional
mutation- and grammar-based fuzzers. These frame-
works demonstrate the ability of LLMs to adapt
to structured program requirements while advancing
fuzzing efficiency.

Lemieux et al. [130] introduced CODAMOSA,
an approach that integrates LLMs into testing work-
flows. CODAMOSA combines Search-Based Soft-
ware Testing (SBST) with Codex [135] to gener-
ate test cases and address coverage stagnation. It
integrates LLM-generated Python code into SBST
workflows, highlighting the collaboration between
traditional testing and LLM-driven techniques. As-
mita et al. [132] explored LLM-based fuzzing in
BusyBox [138], a widely used Linux utility suite.
Their approach combines LLM-assisted seed gen-
eration with crash reuse to enhance efficiency in
black-box fuzzing workflows. Using GPT-4, they
demonstrated how LLMs handle complex inputs and
reuse crashes for cross-variant testing, improving
vulnerability detection. Additionally, Xia et al. [133]
proposed Fuzz4All, a universal fuzzing framework
that extends fuzzing beyond language- or system-
specific constraints. Fuzz4All uses autoprompting
and an iterative fuzzing loop to transform user-
provided inputs into prompts for generating diverse
test cases.

Takeaway 6

LLM-based fuzzing frameworks have ad-
vanced automated testing by combining
mutation-based and generation-based strate-
gies with models like GPT-3.5, Codex, and

Fig. 5: Fuzzing classifications.

The use of LLMs for fuzzing is summarized in
Table V, which highlights the strategies, program
structures, LLMs employed, and applications in the
studies. Most research utilizing LLMs for fuzzing
focuses on greybox fuzzing.

[123]

Qiu et al.

introduced CHEMFuzz, an
LLM-assisted fuzzing framework designed for
quantum chemistry software. CHEMFuzz uses
an evolutionary fuzzing approach with LLM-
based input mutation and output analysis
to
address the syntactic and semantic complexities
of quantum chemistry software. The two-module
system combining syntactic mutation operators with
anomaly detection detected 40 bugs and 81 potential
warnings in Siesta 4.1.5 [134]. Eom et al. [126]
introduced CovRL, a framework that
integrates
coverage-guided
learning with
reinforcement
LLMs to enhance fuzzing for JavaScript engines.
The approach combines Term Frequency-Inverse
Document Frequency (TF-IDF) weighted coverage
maps with reinforcement
learning to guide the
LLM-based mutator. This enables the generation of
more effective test cases, discovering new coverage
areas and improving the efficiency of JavaScript
engine fuzzing. Deng et al.
introduced
FuzzGPT, a framework for fuzzing deep learning
libraries. By mining
bug-triggering
programs and leveraging LLMs such as Codex
[135] and CodeGen [136], FuzzGPT generates edge-
case inputs using strategies like few-shot, zero-shot,
and fine-tuned learning. This targeted approach
illustrating
exploits API-specific vulnerabilities,
the effectiveness of LLMs in managing complex
software ecosystems. Meng et al. [131] introduced
CHATAFL,
LLM-guided mutation-based
framework for protocol fuzzing. The framework
extracts protocol grammars, enhances seed diversity,

historical

[128]

an

Fuzzing ClassificationTest Case GenerationInput StructureProgram StructureMutation-based Generation-based Smart Fuzzing Dumb Fuzzing Blackbox Greybox Whitebox Reference

Target

TCG

PS

LLM

Param

OS

LLMs Usage

15

CHEMFuzz [123]

Quantum chemistry
software

Mutation

Greybox

CovRL [126]

JavaScript Engines

Mutation

Greybox

GPT-3.5
Claude-2* [124]
Bard [125]
CodeT5+

LLAMAFUZZ [127]

Real-world programs

Mutation

Greybox

llama-2-7b-chat-hf

175B
-
-
220M

7B

✗
✗
✗
✓

✓

FuzzGPT [128]

Deep Learning Libraries

Mutation

Greybox

Codex (code-davinci-002)
CodeGen (350M/2B/6B-mono)

CHATFUZZ [129]

General programs

Mutation

Greybox

GPT-3.5-turbo

-

✗
350M/2B/6B ✓
✗

175B

CODAMOSA [130]

Python modules

Mutation

Greybox

Codex

CHATAFL [131]

Network protocol
implementations

Asmitaet al. [132]

BusyBox

Fuzz4All [133]

Compilers, SMT solvers,
quantum frameworks and
programming toolchains.

Mutation

Greybox

GPT-3.5-turbo

Mutation

Mutation,
generation

Greybox,
blackbox

GPT-4-0613

Greybox

GPT-4.0

-

175B

-

-

✗

✗

✗

✗

Input file mutation and output
analysis

Generates valid test cases
Mutate structured data inputs
and generate new seeds
Mutatie and refine test cases
Generates initial test cases
Generates format-conforming
variations of existing seeds
Generates tailored inputs and
extends callable sets
Extracts grammars and enrich
seed corpora

Generate seeds

Generates fuzzing inputs

TABLE V: Overview of the LLM-based fuzzers used in referenced papers, including their target software,
test case generation (TCG), program structure (PS), model parameters, open-source availability (OS), and
usage details.

CodeGen. As shown in Table V, these tools
share common goals, such as improving test
coverage, addressing domain-specific chal-
lenges, and automating seed generation and
refinement.

C. LLM for Penetration Testing

Penetration testing is a controlled security assess-
ment that simulates real-world attacks to identify,
evaluate, and mitigate vulnerabilities in systems and
networks [139].

Deng et al. [140] explored the capabilities of
LLMs in penetration testing, revealing that while
they face chal-
these models excel at sub-tasks,
lenges in maintaining context across multi-step
workflows. To address this limitation,
the au-
thors proposed PentestGPT, a framework integrating
reasoning, generation, and parsing modules. This
framework significantly improved task completion
rates by 228.6% compared to GPT-3.5 and demon-
strated effective performance in real-world scenar-
ios. Huang et al. [141] developed PenHeal, an LLM-
based framework combining penetration testing and
includes a Pentest Module
remediation. PenHeal
that uses techniques like counterfactual prompting to
autonomously detect vulnerabilities. Its remediation
module offers tailored strategies based on sever-
ity and cost efficiency. Compared to PentestGPT,
PenHeal increased detection coverage by 31%, im-

proved remediation effectiveness by 32%, and re-
duced costs by 46%. Additionally, Goyal et al. [142]
proposed Pentest Copilot, a framework that uses
GPT-4-turbo to enhance penetration testing work-
flows. Pentest Copilot incorporates chain-of-thought
reasoning and retrieval-augmented generation to au-
tomate tool orchestration and exploit exploration.
It ensures adaptability with a web-based interface.
This approach combines automation with expert
oversight, enhancing the accessibility of penetration
testing while preserving technical depth.

Additionally,

human
established

some frameworks are designed
as agent-based systems. Bianou et al.
[143]
presented PENTEST-AI, a framework guided by
the MITRE ATT&CK framework for multi-agent
penetration testing. The
framework automates
reconnaissance, exploitation, and reporting tasks
using specialized LLM agents. PENTEST-AI
intervention while
reduces
aligning
cybersecurity methodologies,
with
illustrating
and
between LLMs
structured security frameworks in addressing real-
world challenges. Muzsai et al. [144] proposed
HackSynth, an LLM-driven penetration testing
agent with two modules: a Planner for generating
commands
for processing
feedback. Tested on newly developed CTF-based
benchmarks, HackSynth demonstrated its capability
to autonomously exploit vulnerabilities and achieve
optimal performance with GPT-4. Gioacchini et

and a Summarizer

synergy

the

16

Fig. 6: Integration of LLMs across the six steps of penetration testing.

al. [145] developed AutoPenBench, a framework
with 33 tasks covering experimental and real-
world penetration testing scenarios. AutoPenBench
compares autonomous and semi-autonomous agents,
tackling reproducibility challenges in penetration
testing research. Fully autonomous agents achieved
a 21% success rate, significantly lower than the 64%
success rate of semi-autonomous setups. Shen et
al. [146] introduced PentestAgent, leveraging LLMs
to
and Retrieval-Augmented Generation (RAG)
vulnerability
automate
analysis,
PentestAgent
dynamically integrates tools and adapts to diverse
improving task completion and
environments,
operational
existing
It outperforms
LLM-based penetration testing systems.

exploitation.

intelligence

efficiency.

gathering,

and

As illustrated in Figure 6, penetration test-
ing involves six stages: pre-engagement
interac-
tions, reconnaissance, vulnerability identification,
exploitation, post-exploitation, and reporting. Pre-
engagement interactions establish objectives, define
scope, and set rules of engagement. Reconnaissance
gathers target information through passive and active
methods to identify attack vectors. Vulnerability
identification uses automated tools and manual tech-
niques to detect and verify weaknesses. Exploita-
tion leverages these vulnerabilities to demonstrate
potential risks, while post-exploitation assesses the
breach’s impact and ensures persistence if needed.
Finally, reporting consolidates findings into struc-
tured documentation with risk assessments and re-
mediation strategies.

Takeaway 7

LLMs can be applied across multiple stages
of penetration testing. For example, LLM-
driven frameworks simplify reconnaissance
by automating tool output interpretation and

intelligence gathering. They improve vulnera-
bility identification through dynamic analysis
methods, including counterfactual prompting.
Additionally, LLMs assist in post-exploitation
by facilitating multi-step attack strategies.

V. LLM FOR HYBRID APPROACH

A hybrid approach employs both static and dy-
namic analysis techniques at different stages. For
example, combining static features like code struc-
ture or permissions with dynamic behaviors such as
system calls or memory usage represents a hybrid
approach. This section discusses the role of LLMs
in hybrid approaches, focusing on two aspects: (i)
LLM for unit test generation (§ V-A) and (ii) other
hybrid methods (§ V-B).

A. LLM for Unit Test Generation

Unit testing is a fundamental practice in soft-
ware development
that focuses on verifying the
functionality of individual components or ”units”
of a program. By isolating and testing each unit,
developers can ensure code correctness, detect errors
early, and improve overall code quality. Traditional
unit test generation methods are written manually
by developers and generally involve search-based,
constraint-based, or random techniques to maximize
code coverage
test gen-
eration leverages tools and techniques to generate
tests automatically, reducing developer workload
and improving coverage. Static analysis is essential
in guiding test generation by examining the pro-
gram’s structure, dependencies, and control flow.
Dynamic analysis complements this by evaluating
the generated tests through runtime execution, iden-
tifying errors, and refining test quality. Together,
these hybrid approaches enhance the efficiency and
effectiveness of unit test generation.

[147]. Automated unit

Pre-EngagementInteractionsReconnaissanceVulnerabilityIdentificationExploitationPostExploitationReportingEstablish ObjectivesDefine ScopeSet Rules of Engagement PentestGPT:  Interprets tool outputs and generates actionable steps.Pentest Copilot: Optimizes tool orchestration and command generation.PENTEST-AI: Automates intelligence gathering.Gather target information passively and actively.Use automated tools or manual techniques to detect vulnerabilities.PenHeal: Enhances vulnerability detection with Counterfactual Prompting.HackSynth:  Vulnerability identification via iterative commands.PentestAgent: Dynamically analyzes and verifies vulnerabilities.HackSynth: Automates exploitation processes.Pentest Copilot:  Generates and optimizes exploitation scripts.PENTEST-AI: Executes automated exploitation tasks.PentestGPT: Assists with lateral movement and multi-step tasks.PentestAgent: Supports attack path analysis and persistence strategies.PenHeal: Provides remediation strategies based on severity and cost.Pentest Copilot: Generates structured and detailed reports.PentestAgent: Automates comprehensive report creation.Exploit vulnerabilities to gain access or escalate privileges.Gather additional insights and assess the impact.Provide risk assessments  and remediation strategies.17

dependencies or fail to focus on critical components
of the code.

Dynamic Analysis-Assited Unit Test Genera-
tion. Dynamic analysis complements static tech-
niques by validating and refining test cases through
improving coverage and cor-
iterative processes,
rectness. For example, TestART [153] uses a co-
evolutionary framework to iteratively generate and
repair tests based on runtime feedback, addressing
flaky or invalid tests often produced by traditional
methods. In ChatUniTest [151], dynamic validation
integrates runtime error detection with rule-based
and LLM-driven repair, ensuring that generated tests
are compilable and logically sound. Furthermore,
ChatTester [154] demonstrates how iterative prompt-
ing based on dynamic feedback can address missed
statements and branches, progressively improving
line and branch coverage. These dynamic techniques
allow LLM-based approaches to adapt and refine
tests, addressing limitations of traditional static tools
that lack iterative capabilities.

Prompt Engineering. Techniques like adaptive
in ChatUniTest [151] and program
focal context
slicing in HITS [155] streamline prompts by re-
ducing irrelevant
information, ensuring the LLM
remain focused. Chain-of-thought reasoning, as seen
in aster [150], enhanced the LLM’s ability to han-
dle complex dependencies and generated logically
coherent
tests. Additionally, AGONETEST [156]
employed structured prompts incorporating mock
dependencies and example inputs, guiding the LLM
to generate more comprehensive test cases. These
techniques address the inflexibility of traditional
tools, which often rely on predefined templates and
lack the ability to dynamically adapt prompts based
on code context.

Takeaway 8

Static and dynamic analysis operate at dis-
tinct stages in unit
test generation. Static
analysis extracts dependencies and slices pro-
grams, enabling LLMs to generate targeted,
logically structured tests. Dynamic analysis
then validates and refines these tests through
runtime feedback. Prompt engineering tech-
niques such as adaptive focal context and
structured prompts, align test generation with
code semantics to enhance coverage.

Fig. 7: Workflow of unit test generation with LLMs.

Performance Comparison Between LLMs and
Traditional Test Generation Tools. A study eval-
uated the performance of ChatGPT and Pyn-
guin [148] in generating unit tests for Python pro-
grams, focusing on three types of code structures:
procedural scripts, function-based modular code,
and class-based modular code. Bhatia et al. [149]
compared the tools in terms of coverage, correct-
ness, and iterative improvement
through prompt
engineering. They found that ChatGPT and Pynguin
achieved comparable statement and branch cover-
age. Iterative prompting improved ChatGPT’s cov-
erage for function- and class-based code, saturating
after four iterations, but showed no improvement for
procedural scripts. The study also revealed minimal
overlap in missed statements, suggesting combining
the tools could enhance coverage. However, Chat-
GPT often generated incorrect assertions, especially
for less structured code, due to its focus on natural
language over code semantics. The authors con-
cluded that while LLMs like ChatGPT are promis-
integrating semantic
ing for unit
understanding and combining them with traditional
tools could address current limitations and improve
performance.

test generation,

Static Analysis-Assited Unit Test Generation.
One improvement is the ability of LLMs to generate
focused and meaningful test cases by using static
analysis to extract and structure relevant context.
For instance, aster [150] and ChatUniTest [151]
integrate techniques such as dependency extrac-
tion, program slicing, and adaptive focal context.
These methods ensure that prompts sent to LLMs
are concise and focused, enabling the generation
of tests that better align with the target methods.
Similarly, APT [152] employs a property-based ap-
proach to guide LLMs in generating tests using
the ”Given-When-Then” paradigm, which improves
logical structure in generated tests. These static anal-
ysis techniques address the limitations of traditional
methods, which often struggle to extract relevant

Automated Test GenerationSource FilePrompt EngineeringExisting Test SuiteCoverage Report  LLMsGenerated Test SuiteTest CommandRun TestTest PassCoverage IncreasePost-Process & Update Test FileExisting Test SuiteCoverage ReportB. Others

In addition to the previously discussed methods
for unit
test generation, other hybrid approaches
integrate static and dynamic analysis through an
agent framework. This framework first performs
static analysis, such as extracting ASTs and ana-
lyzing code structure, and then conducts dynamic
testing.

Multi-Agent Framework for Secure Code Gen-
eration. Nunez et al. [157] introduced AutoSafe-
Coder, an innovative multi-agent framework de-
signed to improve the security of automatically gen-
erated code. The framework leverages three distinct
LLM-driven agents working collaboratively to gen-
erate, analyze, and secure code. The Coding Agent
is responsible for generating the initial code, while
the Static Analyzer Agent identifies potential vul-
nerabilities through AST analysis. Meanwhile, the
Fuzzing Agent detects runtime errors by employing
mutation-based fuzzing techniques, ensuring that the
generated code performs securely during execution.
Interactive feedback loops integrate both static and
dynamic testing methods into the code generation
process, optimizing the outputs from the LLM at
each stage.

Coverage Test Generation. Pizzorno et al. [158]
presented CoverUp, a method for generating Python
regression tests with high code coverage. CoverUp
evaluates existing code coverage,
identifies gaps,
and uses LLMs to generate new tests informed
by static analysis. If tests fail to execute or en-
hance coverage, CoverUp iteratively refines them
using error messages and code context. This process
continues until all segments are fully tested and
integration issues are resolved.

Malware Analysis. Li et al. [122] used reverse
engineering tools to extract static and dynamic
features from Android APK files, organizing them
into permissions, system calls, and metadata. They
used tailored prompts to guide ChatGPT in gener-
ating textual analyses and maliciousness scores for
each application. These results were compared with
three existing Android malware detection models:
Drebin [159], MaMaDroid [160], and XMAL [161].
Although traditional models showed strong classi-
fication capabilities, the authors noted their limi-
tations in interpretability and dataset dependency.
ChatGPT offered comprehensive analyses and ex-
planations but lacked decision-making capabilities.

18

Malware Reverse Engineering. Williamson et
al. [162] integrated LLMs with static and dynamic
analysis techniques to enhance malware reverse
engineering. In the static phase,
tools like IDA
Pro examined binaries to extract structural details
such as embedded strings and control flow. In the
dynamic phase, sandboxes monitored malware be-
havior, capturing network and system interactions.
LLMs synthesized results from both phases, deriv-
ing actionable insights and identifying indicators of
compromise (IoCs).

Takeaway 9

LLMs enhance hybrid methods by iteratively
refining the outputs of static (e.g., AST anal-
ysis in AutoSafeCoder, coverage gaps in
CoverUp) and dynamic (e.g., fuzzing, runtime
feedback) analysis process. They bridge code
structures with runtime behaviors, enabling
secure code generation, high-coverage tests,
and actionable malware analysis.

VI. DISCUSSION
The use of LLMs in the field of program anal-
ysis has mitigated several previous limitations such
as false positives, performance overhead, inherent
knowledge barriers, path explosion,
the trade-off
between speed and accuracy, and the difficulty of
achieving automation across diverse systems without
heavy manual intervention. Despite these advance-
ments, new limitations and challenges have emerged
with the introduction of LLMs. The following sub-
sections provide an overview of these challenges (§
VI-A) and discuss potential future research direc-
tions (§ VI-B).

A. Challenges

Technical Limitations. LLMs face several tech-
nical challenges in program analysis. First, incor-
rect data type identification and information loss
during decompilation reduce analysis accuracy. Sec-
ond, LLMs often oversimplify patches,
limiting
their ability to address vulnerabilities in real-world
applications. In some cases, they produce empty
responses, particularly during software verification
and patching tasks. Third, LLMs struggle with
variable reuse, often confusing identically named
variables in different scopes. Finally, LLMs struggle

to analyze logic vulnerabilities involving intricate
control flows, complex nesting, and time-based com-
petition conditions. These challenges reduce their
effectiveness in assessing such scenarios.

for

inputs,

identical

Model Characteristics and Limitations.LLMs
are non-deterministic and may produce varying
outputs
complicating
consistency in repeated vulnerability assessments.
This variability hinders reliable and repeatable
results. Additionally,
to
hallucinations, generating fabricated information
that misleads
detection. These
limitations in consistency and accuracy make LLMs
insufficient for reliable program analysis.

vulnerability

LLMs

prone

are

Cost and Dependency Issues. The effectiveness
of LLM-based program analysis relies on prompt
engineering, which requires significant expertise.
Poorly designed prompts can lead to ineffective
results or introduce biases,
limiting the model’s
ability to detect vulnerabilities. Furthermore, using
LLMs can be costly, especially when analyzing long
code segments, due to the large number of tokens
required. The inherent token limits of LLMs also
restrict their ability to handle extensive or complex
programs, making scalability a challenge in real-
world applications.

B. Future Directions

Deep Integration of LLMs with Analysis Tech-
niques. Most current methods use LLMs inde-
pendently of program analysis. Integrating LLMs
with static analysis into a unified workflow offers
opportunities for enhanced effectiveness. Some stud-
ies [30] have acknowledged that their methods lack
effective integration of LLMs with other models
or techniques. Frameworks combining LLMs with
GNNs [38] for program control and data flow have
shown significant improvements in detection accu-
racy. Future work should focus on integrating LLMs
with static and dynamic analysis to create more
effective solutions for vulnerability detection.

Transforming Dynamic Analysis into Static
Analysis. Transforming tasks traditionally requiring
dynamic analysis into static analysis with LLMs
is an emerging direction. Tasks
like runtime
vulnerability detection and memory corruption
analysis
dynamic
analysis to capture execution-specific behaviors.
to
LLM integration can shift

these processes

historically

depended

on

19

early

enabling

analysis,

static
vulnerability
detection without runtime execution. This reduces
computational overhead, avoids repeated executions,
and improves scalability for analyzing large systems.
Pei et al. [163] showed how fine-tuning LLMs
eliminates the need for runtime information by
predicting program invariants from source code,
enabling earlier safety checks during compilation.

Emulating Human Security Researchers for
Vulnerability Detection. Advancing code under-
standing and reasoning capabilities enable LLMs
to replicate systematic approaches used by human
security researchers. LLMs overcome the rule-based
limitations of traditional tools by analyzing complex
code contexts and identifying nuanced vulnerabili-
ties. This enables LLMs to mimic hypothesis-driven
processes, identifying subtle vulnerabilities missed
by automated methods. Glazunov et al. [164] in-
troduced Project Naptime to replicate human secu-
rity researchers’ workflows for vulnerability detec-
tion. The framework employs tools such as a code
browser, Python interpreter, and debugger, enabling
LLMs to perform expert-level code analysis and vul-
nerability detection. Evaluated on the CyberSecEval
2 [165] benchmark, this approach improves detec-
tion and demonstrates the feasibility of automating
complex security tasks.

VII. CONCLUSION

scalability,

capabilities,

combined with

Integrating LLMs into program analysis enhances
vulnerability detection, code comprehension, and
language
security assessments. LLMs’ natural
processing
static
and dynamic analysis techniques have improved
automation,
and interpretability in
program analysis. These advancements facilitate
faster vulnerability detection and provide deeper
insights into software behavior. Challenges such
as token limitations, path explosion, complex logic
vulnerabilities, and LLM hallucinations
remain
survey
reviewed in this
barriers. The studies
highlight recent progress, offering insights into its
current state and emerging opportunities. Future di-
rections include developing domain-specific models,
refining hybrid methods, and enhancing reliability
and interpretability to fully utilize LLMs in program
analysis. This survey aims to assist in addressing the
mentioned challenges and inspire the development
of more effective program analysis frameworks.

REFERENCES

[1] T. Mens, M. Wermelinger, S. Ducasse, S. Demeyer,
R. Hirschfeld, and M. Jazayeri, “Challenges in software
evolution,” in Eighth International Workshop on Principles
of Software Evolution (IWPSE’05).
IEEE, 2005, pp. 13–22.

[2] H. Li, H. Kwon, J. Kwon, and H. Lee, “Clorifi: software
vulnerability discovery using code clone verification,” Con-
currency and Computation: Practice and Experience, vol. 28,
pp. 1900 – 1917, 2016.

[3] A. Aggarwal and P. Jalote, “Integrating static and dynamic
analysis for detecting vulnerabilities,” 30th Annual Inter-
national Computer Software and Applications Conference
(COMPSAC’06), vol. 1, pp. 343–350, 2006.

[4] K. Goseva-Popstojanova and A. Perhinschi, “On the capability
of static code analysis to detect security vulnerabilities,” Inf.
Softw. Technol., vol. 68, pp. 18–33, 2015.

[5] S. Siddiqui, R. Metta, and K. Madhukar, “Towards multi-
language static code analysis,” 2023 IEEE 34th International
Symposium on Software Reliability Engineering Workshops
(ISSREW), pp. 81–82, 2023.

[6]

J. Wang, M. Huang, Y. Nie, and J. Li, “Static analysis of
source code vulnerability using machine learning techniques:
A survey,” 2021 4th International Conference on Artificial
Intelligence and Big Data (ICAIBD), pp. 76–86, 2021.

[7] B. Chernis and R. M. Verma, “Machine learning methods for
software vulnerability detection,” Proceedings of the Fourth
ACM International Workshop on Security and Privacy Ana-
lytics, 2018.

[8] M. Pradel and K. Sen, “Deepbugs: A learning approach
to name-based bug detection,” Proceedings of the ACM on
Programming Languages, vol. 2, no. OOPSLA, pp. 1–25,
2018.

[9] D. Zou, Y. Zhu, S. Xu, Z. Li, H. Jin, and H. Ye, “Interpreting
deep learning-based vulnerability detector predictions based
on heuristic searching,” ACM Transactions on Software En-
gineering and Methodology (TOSEM), vol. 30, pp. 1 – 31,
2021.

[10] G. Ye, Z. Tang, H. Wang, D. Fang, J. Fang, S. Huang,
and Z. Wang, “Deep program structure modeling through
multi-relational graph-based learning,” in Proceedings of
the ACM International Conference on Parallel Architectures
and Compilation Techniques, ser. PACT ’20. New York,
NY, USA: Association for Computing Machinery, 2020,
p. 111–123.
[Online]. Available: https://doi.org/10.1145/
3410463.3414670

[11] T. Ahmed and P. Devanbu, “Few-shot

training llms for
project-specific code-summarization,” Proceedings of the 37th
IEEE/ACM International Conference on Automated Software
Engineering, 2022.

[12] S. Choi, Y. K. Tan, M. H. Meng, M. Ragab, S. Mondal,
D. Mohaisen, and K. M. M. Aung, “I can find you in sec-
onds! leveraging large language models for code authorship
attribution,” arXiv preprint arXiv:2501.08165, 2025.

[13] S. Choi and D. Mohaisen, “Attributing chatgpt-generated
source codes,” IEEE Transactions on Dependable and Secure
Computing, 2025.

[14] Z. Lin, G. Qu, Q. Chen, X. Chen, Z. Chen, and K. Huang,
“Pushing large language models to the 6g edge: Vision, chal-
lenges, and opportunities,” arXiv preprint arXiv:2309.16739,
2023.

20

[15] Z. Lin, X. Hu, Y. Zhang, Z. Chen, Z. Fang, X. Chen, A. Li,
P. Vepakomma, and Y. Gao, “Splitlora: A split parameter-
efficient fine-tuning framework for large language models,”
arXiv preprint arXiv:2407.00952, 2024.

[16] P. Sharma and B. Dash, “Impact of big data analytics and chat-
gpt on cybersecurity,” in 2023 4th International Conference
on Computing and Communication Systems (I3CS).
IEEE,
2023, pp. 1–6.

[17] T. Ni, Y. Du, Q. Zhao, and C. Wang, “Non-intrusive and
unconstrained keystroke inference in vr platforms via infrared
side channel,” arXiv preprint arXiv:2412.14815, 2024.

[18] T. Ni, X. Zhang, and Q. Zhao, “Recovering fingerprints from
in-display fingerprint sensors via electromagnetic side chan-
nel,” in Proceedings of the 2023 ACM SIGSAC Conference on
Computer and Communications Security, 2023, pp. 253–267.

[19] T. Ni, X. Zhang, C. Zuo, J. Li, Z. Yan, W. Wang, W. Xu,
X. Luo, and Q. Zhao, “Uncovering user interactions on
smartphones via contactless wireless charging side channels,”
in 2023 IEEE Symposium on Security and Privacy (SP).
IEEE, 2023, pp. 3399–3415.

[20] Z. Fang, Z. Lin, Z. Chen, X. Chen, Y. Gao, and Y. Fang, “Au-
tomated federated pipeline for parameter-efficient fine-tuning
of large language models,” arXiv preprint arXiv:2404.06448,
2024.

[21] F. Nielson, H. R. Nielson, and C. Hankin, Principles of
springer, 2015.

program analysis.

[22] A. K. Ashish and J. Aghav, “Automated techniques and tools
for program analysis: Survey,” in 2013 Fourth International
Conference on Computing, Communications and Networking
Technologies (ICCCNT), 2013, pp. 1–7.

[23] F. L¨osch, “Instrumentation of java program code for control
flow analysis,” Ph.D. dissertation, Universit¨atsbibliothek der
Universit¨at Stuttgart, 2005.

[24] A. Vaswani, “Attention is all you need,” Advances in Neural

Information Processing Systems, 2017.

[25] M. R. Douglas, “Large language models,” Communications

of the ACM, vol. 66, pp. 7 – 7, 2023.

[26] H. Touvron, T. Lavril, G.

Izacard, X. Martinet, M.-A.
Lachaux, T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro,
F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample,
“Llama: Open and efficient foundation language models,”
2023. [Online]. Available: https://arxiv.org/abs/2302.13971

[27] M. AI, “Codellama: Open code-focused language models,”

https://ai.meta.com/research/code-llama, 2023.

[28] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan,
P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell
et al., “Language models are few-shot learners,” in Advances
in Neural Information Processing Systems, vol. 33, 2020, pp.
1877–1901.
[Online]. Available: https://arxiv.org/abs/2005.
14165

[29] OpenAI,

“Gpt-4

technical

report,”

https://openai.com/

research/gpt-4, 2023.

[30] H. Li, Y. Hao, Y. Zhai, and Z. Qian, “The hitchhiker’s guide
to program analysis: A journey with large language models,”
2023. [Online]. Available: https://arxiv.org/abs/2308.00245

[31]

J. Ye, X. Fei, X. de Carn´e de Carnavalet, L. Zhao, L. Wu,
and M. Zhang, “Detecting command injection vulnerabilities
in linux-based embedded firmware with llm-based taint
analysis of library functions,” Computers & Security, vol.
[Online]. Available: https://www.
144, p. 103971, 2024.
sciencedirect.com/science/article/pii/S0167404824002761

[32] P. Liu, C. Sun, Y. Zheng, X. Feng, C. Qin, Y. Wang,
Z. Li, and L. Sun, “Harnessing the power of
llm to
support binary taint analysis,” 2023. [Online]. Available:
https://arxiv.org/abs/2310.08275

[33] D. Liu, Z. Lu, S. Ji, K. Lu, J. Chen, Z. Liu, D. Liu,
R. Cai, and Q. He, “Detecting kernel memory bugs through
inconsistent memory management intention inferences,” in
33rd USENIX Security Symposium (USENIX Security 24).
Philadelphia, PA: USENIX Association, Aug. 2024, pp. 4069–
4086. [Online]. Available: https://www.usenix.org/conference/
usenixsecurity24/presentation/liu-dinghao-detecting

[34]

J. Wang, Z. Huang, H. Liu, N. Yang, and Y. Xiao,
“Defecthunter: A novel llm-driven boosted-conformer-based
code vulnerability detection mechanism,” 2023. [Online].
Available: https://arxiv.org/abs/2309.15324

[35] Z. Li, S. Dutta, and M. Naik, “Llm-assisted static analysis for
detecting security vulnerabilities,” 2024. [Online]. Available:
https://arxiv.org/abs/2405.17238

[36] Y. Cheng, L. K. Shar, T. Zhang, S. Yang, C. Dong, D. Lo,
S. Lv, Z. Shi, and L. Sun, “Llm-enhanced static analysis
for precise identification of vulnerable oss versions,” 2024.
[Online]. Available: https://arxiv.org/abs/2408.07321

[37] Z. Mao, J. Li, D. Jin, M. Li, and K. Tei, “Multi-role consensus
through llms discussions for vulnerability detection,” 2024.
[Online]. Available: https://arxiv.org/abs/2403.14274

[38] A. Z. H. Yang, H. Tian, H. Ye, R. Martins, and C. L.
Goues, “Security vulnerability detection with multitask
self-instructed fine-tuning of large language models,” 2024.
[Online]. Available: https://arxiv.org/abs/2406.05892

[39] Y. Sun, D. Wu, Y. Xue, H. Liu, H. Wang, Z. Xu, X. Xie,
and Y. Liu, “Gptscan: Detecting logic vulnerabilities in
smart contracts by combining gpt with program analysis,”
IEEE/ACM 46th International
in Proceedings of
Conference on Software Engineering,
ICSE ’24.
ser.
ACM, Apr. 2024, p. 1–13.
[Online]. Available: http:
//dx.doi.org/10.1145/3597503.3639117

the

[40] Y. Yang, “Iot software vulnerability detection techniques
through large language model,” in Formal Methods and
Software Engineering: 24th International Conference on
Formal Engineering Methods, ICFEM 2023, Brisbane, QLD,
Australia, November 21–24, 2023, Proceedings. Berlin,
Heidelberg: Springer-Verlag, 2023, p. 285–290. [Online].
Available: https://doi.org/10.1007/978-981-99-7584-6 21

[41] N. S. Mathews, Y. Brus, Y. Aafer, M. Nagappan, and
S. McIntosh, “Llbezpeky: Leveraging large language models
for vulnerability detection,” 2024.
[Online]. Available:
https://arxiv.org/abs/2401.01269

[42] M. M. Mohajer, R. Aleithan, N. S. Harzevili, M. Wei, A. B.
Belle, H. V. Pham, and S. Wang, “Skipanalyzer: A tool
for static code analysis with large language models,” 2023.
[Online]. Available: https://arxiv.org/abs/2310.18532

[43] S. Yang, X. Lin, J. Chen, Q. Zhong, L. Xiao, R. Huang,
Y. Wang, and Z. Zheng, “Hyperion: Unveiling dapp
inconsistencies using llm and dataflow-guided symbolic
execution,” 2024. [Online]. Available: https://arxiv.org/abs/
2408.06037

[44] C. Zhang, H. Liu, J. Zeng, K. Yang, Y. Li, and H. Li, “Prompt-
enhanced software vulnerability detection using chatgpt,”
2024. [Online]. Available: https://arxiv.org/abs/2308.12697

[45] S. Hu, T. Huang, F.

˙Ilhan, S. F. Tekin, and L. Liu,
“Large language model-powered smart contract vulnerability

21

detection: New perspectives,” 2023.
https://arxiv.org/abs/2310.01152

[Online]. Available:

[46]

J. Xiang, L. Fu, T. Ye, P. Liu, H. Le, L. Zhu, and W. Wang,
“Luataint: A static analysis system for web configuration
interface vulnerability of internet of things devices,” 2024.
[Online]. Available: https://arxiv.org/abs/2402.16043

[47] Y. Chen, R. Tang, C. Zuo, X. Zhang, L. Xue, X. Luo, and
Q. Zhao, “Attention! your copied data is under monitoring:
A systematic study of clipboard usage in android apps,” in
Proceedings of the 46th IEEE/ACM International Conference
on Software Engineering, 2024, pp. 1–13.

[48] H. Lu, Q. Zhao, Y. Chen, X. Liao, and Z. Lin, “Detecting
and measuring aggressive location harvesting in mobile apps
via data-flow path embedding,” Proceedings of the ACM on
Measurement and Analysis of Computing Systems, vol. 7,
no. 1, pp. 1–27, 2023.

[49] Q. Zhao, C. Zuo, G. Pellegrino, and Z. Lin, “Geo-locating
drivers: A study of sensitive data leakage in ride-hailing
services,” in 26th Annual Network and Distributed System
Security Symposium (NDSS 2019).

Internet Society, 2019.

[50] Q. Zhao, H. Wen, Z. Lin, D. Xuan, and N. Shroff, “On the
accuracy of measured proximity of bluetooth-based contact
tracing apps,” in Security and Privacy in Communication
Networks: 16th EAI International Conference, SecureComm
2020, Washington, DC, USA, October 21-23, 2020, Proceed-
ings, Part I 16. Springer, 2020, pp. 49–60.

[51] T. Ni, G. Lan, J. Wang, Q. Zhao, and W. Xu, “Eavesdropping
mobile app activity via {Radio-Frequency} energy harvest-
ing,” in 32nd USENIX Security Symposium (USENIX Security
23), 2023, pp. 3511–3528.

[52] T. Ni, J. Li, X. Zhang, C. Zuo, W. Wang, W. Xu, X. Luo,
and Q. Zhao, “Exploiting contactless side channels in wireless
charging power banks for user privacy inference via few-shot
learning,” in Proceedings of the 29th Annual International
Conference on Mobile Computing and Networking, 2023, pp.
1–15.

[53] T. Ni, Y. Chen, W. Xu, L. Xue, and Q. Zhao, “Xporter: A
study of the multi-port charger security on privacy leakage
and voice injection,” in Proceedings of the 29th Annual Inter-
national Conference on Mobile Computing and Networking,
2023, pp. 1–15.

[54] T. Ni, “Sensor security in virtual reality: Exploration and
mitigation,” in Proceedings of the 22nd Annual International
Conference on Mobile Systems, Applications and Services,
2024, pp. 758–759.

[55] Q. Zhao, C. Zuo, B. Dolan-Gavitt, G. Pellegrino, and Z. Lin,
“Automatic uncovering of hidden behaviors from input vali-
dation in mobile apps,” in 2020 IEEE Symposium on Security
and Privacy (SP).

IEEE, 2020, pp. 1106–1120.

[56] H. Touvron, T. Lavril, G.

Izacard, X. Martinet, M.-A.
Lachaux, T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro,
F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample,
“Llama: Open and efficient foundation language models,”
2023. [Online]. Available: https://arxiv.org/abs/2302.13971

[57] S. Yuan, H. Li, X. Han, G. Xu, W. Jiang, T. Ni, Q. Zhao, and
Y. Fang, “Itpatch: An invisible and triggered physical adver-
sarial patch against traffic sign recognition,” arXiv preprint
arXiv:2409.12394, 2024.

[58] Y. Chen, T. Ni, W. Xu, and T. Gu, “Swipepass: Acoustic-
based second-factor user authentication for smartphones,”
Proceedings of the ACM on Interactive, Mobile, Wearable and
Ubiquitous Technologies, vol. 6, no. 3, pp. 1–25, 2022.

[59] Q. Zhao, C. Zuo, J. Blasco, and Z. Lin, “Periscope: Compre-
hensive vulnerability analysis of mobile app-defined bluetooth
peripherals,” in Proceedings of the 2022 ACM on Asia Con-
ference on Computer and Communications Security, 2022, pp.
521–533.

[60] D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, and
J. Yin, “Unixcoder: Unified cross-modal pre-training for
code
[Online]. Available: https:
//arxiv.org/abs/2203.03850

representation,” 2022.

[61] B. Rozi`ere, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E.
Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin,
A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C.
Ferrer, A. Grattafiori, W. Xiong, A. D´efossez, J. Copet,
F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom,
and G. Synnaeve, “Code llama: Open foundation models for
code,” 2024. [Online]. Available: https://arxiv.org/abs/2308.
12950

[62] O. A. Aslan and R. Samet, “A comprehensive review on
malware detection approaches,” IEEE Access, vol. 8, pp.
6249–6271, 2020.

[63] H. Alasmary, A. Anwar, J. Park, J. Choi, D. Nyang, and
A. Mohaisen, “Graph-based comparison of iot and android
malware,” in Computational Data and Social Networks, 2018,
pp. 259–272.

[64] F. Shen, J. Del Vecchio, A. Mohaisen, S. Y. Ko, and L. Ziarek,
“Android malware detection using complex-flows,” IEEE
Transactions on Mobile Computing, vol. 18, no. 6, pp. 1231–
1245, 2018.

[65] H. Alasmary, A. Khormali, A. Anwar, J. Park, J. Choi,
A. Abusnaina, A. Awad, D. Nyang, and A. Mohaisen, “An-
alyzing and detecting emerging internet of things malware:
A graph-based approach,” IEEE Internet of Things Journal,
vol. 6, no. 5, pp. 8977–8988, 2019.

[66] H. Kang, J.-w. Jang, A. Mohaisen, and H. K. Kim, “De-
tecting and classifying android malware using static analysis
along with creator information,” International Journal of
Distributed Sensor Networks, vol. 11, no. 6, p. 479174, 2015.
[67] A. Mohaisen, O. Alrawi, and M. Mohaisen, “Amal: high-
fidelity, behavior-based automated malware analysis and clas-
sification,” computers & security, vol. 52, pp. 251–266, 2015.
[68] S. Fujii and R. Yamagishi, “Feasibility study for supporting
static malware analysis using llm,” 2024. [Online]. Available:
https://arxiv.org/abs/2411.14905

[69] M. Post, “A call for clarity in reporting bleu scores,” 2018.
[Online]. Available: https://arxiv.org/abs/1804.08771
[70] K. Ganesan, “Rouge 2.0: Updated and improved measures
[Online].

for evaluation of summarization tasks,” 2018.
Available: https://arxiv.org/abs/1803.01937

[71] C.-A. Simion, G. Balan, and D. T. GavriluT¸ , “Benchmarking
out of the box open-source llms for malware detection based
on api calls sequences,” in Intelligent Data Engineering and
Automated Learning – IDEAL 2024, V. Julian, D. Camacho,
H. Yin, J. M. Alberola, V. B. Nogueira, P. Novais, and
A. Tall´on-Ballesteros, Eds. Cham: Springer Nature Switzer-
land, 2025, pp. 133–142.

[72] A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford,
D. S. Chaplot, D. de las Casas, F. Bressand, G. Lengyel,
G. Lample, L. Saulnier, L. R. Lavaud, M.-A. Lachaux,
P. Stock, T. L. Scao, T. Lavril, T. Wang, T. Lacroix,
and W. E. Sayed, “Mistral 7b,” 2023. [Online]. Available:
https://arxiv.org/abs/2310.06825

[73] A. Q. Jiang, A. Sablayrolles, A. Roux, A. Mensch, B. Savary,

22

C. Bamford, D. S. Chaplot, D. de las Casas, E. B. Hanna,
F. Bressand, G. Lengyel, G. Bour, G. Lample, L. R. Lavaud,
L. Saulnier, M.-A. Lachaux, P. Stock, S. Subramanian,
S. Yang, S. Antoniak, T. L. Scao, T. Gervet, T. Lavril,
T. Wang, T. Lacroix, and W. E. Sayed, “Mixtral of experts,”
2024. [Online]. Available: https://arxiv.org/abs/2401.04088

[74] N. Zahan, P. Burckhardt, M. Lysenko, F. Aboukhadijeh,
and L. Williams, “Shifting the lens: Detecting malicious
npm packages using large language models,” 2024. [Online].
Available: https://arxiv.org/abs/2403.12196

[76]

[75] GitHub, “Codeql: Github’s static analysis engine for code
vulnerabilities,” https://codeql.github.com/, 2025, accessed:
January 15, 2025.
I. Khan and Y.-W. Kwon, “A structural-semantic approach
integrating graph-based and large language models represen-
tation to detect android malware,” in ICT Systems Security and
Privacy Protection, N. Pitropakis, S. Katsikas, S. Furnell, and
K. Markantonakis, Eds. Cham: Springer Nature Switzerland,
2024, pp. 279–293.

[77] Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong,
L. Shou, B. Qin, T. Liu, D. Jiang, and M. Zhou, “Codebert: A
pre-trained model for programming and natural languages,”
2020. [Online]. Available: https://arxiv.org/abs/2002.08155

[78] W. Zhao, J. Wu, and Z. Meng, “Apppoet: Large language
model based android malware detection via multi-view
prompt
[Online]. Available: https:
//arxiv.org/abs/2404.18816

engineering,” 2024.

[79] A. Kozyrev, G. Solovev, N. Khramov, and A. Podkopaev,
“Coqpilot, a plugin for llm-based generation of proofs,” 10
2024, pp. 2382–2385.

[80] L. Zhang, S. Lu, and N. Duan, “Selene: Pioneering automated
proof in software verification,” 2024. [Online]. Available:
https://arxiv.org/abs/2401.07663

[81] S. Chakraborty, S. K. Lahiri, S. Fakhoury, M. Musuvathi,
A. Lal, A. Rastogi, A. Senthilnathan, R. Sharma, and
N. Swamy, “Ranking llm-generated loop invariants for
program verification,” 2024.
[Online]. Available: https:
//arxiv.org/abs/2310.09342

[82] C. Janßen, C. Richter, and H. Wehrheim, “Can chatgpt
support software verification?” 2023. [Online]. Available:
https://arxiv.org/abs/2311.02433

loop unrolling,” in Proceedings of

[84] G. Wu, W. Cao, Y. Yao, H. Wei, T. Chen,

[83] M. A. A. Pirzada, G. Reger, A. Bhayat, and L. C.
Cordeiro, “Llm-generated invariants for bounded model
the
checking without
39th IEEE/ACM International Conference on Automated
Software Engineering, ser. ASE ’24. New York, NY, USA:
Association for Computing Machinery, 2024, p. 1395–1407.
[Online]. Available: https://doi.org/10.1145/3691620.3695512
and
X. Ma, “Llm meets bounded model checking: Neuro-
the
symbolic loop invariant
39th IEEE/ACM International Conference on Automated
Software Engineering, ser. ASE ’24. New York, NY, USA:
Association for Computing Machinery, 2024, p. 406–417.
[Online]. Available: https://doi.org/10.1145/3691620.3695014
[85] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can
large language models reason about program invariants?”
in Proceedings of
the 40th International Conference on
Machine Learning, ser. Proceedings of Machine Learning
Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt,
S. Sabato, and J. Scarlett, Eds., vol. 202.
PMLR,
[Online]. Available:
23–29 Jul 2023, pp. 27 496–27 520.
https://proceedings.mlr.press/v202/pei23a.html

inference,” in Proceedings of

[86] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C.
Cheung, and C. Tian, “Enchanting program specification
synthesis by large language models using static analysis
and program verification,” in Computer Aided Verification:
36th International Conference, CAV 2024, Montreal, QC,
Canada, July 24–27, 2024, Proceedings, Part II. Berlin,
Heidelberg: Springer-Verlag, 2024, p. 302–328. [Online].
Available: https://doi.org/10.1007/978-3-031-65630-9 16

[87] H. Wu, C. Barrett, and N. Narodytska, “Lemur: Integrating
large language models in automated program verification,”
2024. [Online]. Available: https://arxiv.org/abs/2310.04870

[88] P. Mukherjee

and B. Delaware,

automated
verification of llm-synthesized c programs,” 2024. [Online].
Available: https://arxiv.org/abs/2410.14835

“Towards

[89] Y. Liu, Y. Xue, D. Wu, Y. Sun, Y. Li, M. Shi, and
Y. Liu, “Propertygpt: Llm-driven formal verification of smart
contracts through retrieval-augmented property generation,”
2024. [Online]. Available: https://arxiv.org/abs/2405.02580

[91]

[90] W. Wang, K. Liu, A. R. Chen, G. Li, Z. Jin, G. Huang, and
L. Ma, “Python symbolic execution with llm-powered code
generation,” 2024. [Online]. Available: https://arxiv.org/abs/
2409.09271
J. Su, L. Deng, C. Wen, S. Qin,
and C. Tian,
“Cfstra: Enhancing configurable program analysis through
llm-driven strategy selection based on code features,”
in Theoretical Aspects of Software Engineering: 18th
International Symposium, TASE 2024, Guiyang, China, July
29 – August 1, 2024, Proceedings. Berlin, Heidelberg:
Springer-Verlag, 2024, p. 374–391.
[Online]. Available:
https://doi.org/10.1007/978-3-031-64626-3 22

static

[92] P. J. Chapman, C. Rubio-Gonz´alez, and A. V. Thakur,
in
analysis
“Interleaving
the 13th ACM SIGPLAN International
Proceedings of
in Program Analysis,
Workshop on the State Of
ser. SOAP 2024. New York, NY, USA: Association for
Computing Machinery, 2024, p. 9–17. [Online]. Available:
https://doi.org/10.1145/3652588.3663317

llm prompting,”

the Art

and

[93] Anthropic,

“Claude,”

https://www.anthropic.com/claude,

[94]

2025, accessed: January 16, 2025.
z. Czajka and C. Kaliszyk, “Hammer for coq: Automation
type theory,” J. Autom. Reason., vol. 61,
for dependent
no. 1–4, p. 423–453,
[Online]. Available:
https://doi.org/10.1007/s10817-018-9458-4

Jun. 2018.

[95] L. Blaauwbroek, J. Urban, and H. Geuvers, The Tactician:
A Seamless, Interactive Tactic Learner and Prover for Coq.
Springer International Publishing, 2020, p. 271–277. [Online].
Available: http://dx.doi.org/10.1007/978-3-030-53518-6 17

[96] G. Klein,

J. Andronick, K. Elphinstone, T. Murray,
T. Sewell, R. Kolanski, and G. Heiser, “Comprehensive
formal verification of an os microkernel,” ACM Trans.
Comput. Syst., vol. 32, no. 1, Feb. 2014. [Online]. Available:
https://doi.org/10.1145/2560537

[97] T. S. Group, “sel4: The world’s first operating-system kernel
with an end-to-end proof of implementation correctness,”
https://sel4.systems/, n.d., accessed: 2025-01-18.

[98] D. Beyer, Competition on Software Verification and Witness
Validation: SV-COMP 2023, 04 2023, pp. 495–522.
[99] P. Baudin, J.-C. Filliˆatre, C. March´e, B. Monate, Y. Moy,
and V. Prevosto, ACSL: ANSI/ISO C Specification Language.
[Online]. Available: http://frama-c.com/download/acsl.pdf

[100] P. Baudin, F. Bobot, D. B¨uhler, L. Correnson, F. Kirchner,
N. Kosmatov, A. Maroneze, V. Perrelle, V. Prevosto,

23

J. Signoles, and N. Williams, “The dogged pursuit of
bug-free c programs: the frama-c software analysis platform,”
Commun. ACM, vol. 64, no. 8, p. 56–68, Jul. 2021. [Online].
Available: https://doi.org/10.1145/3470569

[101] D. Beyer and M. E. Keremoglu, “Cpachecker: A tool for
configurable software verification,” in Computer Aided Ver-
ification, G. Gopalakrishnan and S. Qadeer, Eds.
Berlin,
Heidelberg: Springer Berlin Heidelberg, 2011, pp. 184–190.

[102] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant,
C. Pacheco, M. S. Tschantz, and C. Xiao, “The daikon
system for dynamic detection of likely invariants,” Science
of Computer Programming, vol. 69, no. 1, pp. 35–45,
2007, special issue on Experimental Software and Toolkits.
[Online]. Available: https://www.sciencedirect.com/science/
article/pii/S016764230700161X

[103] R. Menezes, M. Aldughaim, B. Farias, X. Li, E. Manino,
F. Shmarov, K. Song, F. Brauße, M. R. Gadelha, N. Tihanyi,
K. Korovin, and L. C. Cordeiro, “Esbmc v7.4: Harnessing
the power of intervals,” 2023. [Online]. Available: https:
//arxiv.org/abs/2312.14746

[104] A. Gurfinkel, T. Kahsai, A. Komuravelli, and J. A. Navas,
“The seahorn verification framework,” in Computer Aided
Verification, D. Kroening and C. S. P˘as˘areanu, Eds. Cham:
Springer International Publishing, 2015, pp. 343–361.

[105] P. Darke, S. Agrawal, and R. Venkatesh, “Veriabs: A
tool for scalable verification by abstraction (competition
contribution),” in Tools and Algorithms for the Construction
and Analysis of Systems: 27th International Conference,
TACAS 2021, Held as Part of
the European Joint
Conferences on Theory and Practice of Software, ETAPS
2021, Luxembourg City, Luxembourg, March 27 – April 1,
2021, Proceedings, Part II. Berlin, Heidelberg: Springer-
Verlag, 2021, p. 458–462.
[Online]. Available: https:
//doi.org/10.1007/978-3-030-72013-1 32

[106] D. Kroening and M. Tautschnig, “Cbmc – c bounded model
checker,” in Tools and Algorithms for the Construction and
´Abrah´am and K. Havelund, Eds.
Analysis of Systems, E.
Berlin, Heidelberg: Springer Berlin Heidelberg, 2014, pp.
389–391.

[107] M. Heizmann, J. Christ, D. Dietsch, E. Ermis, J. Hoenicke,
M. Lindenmann, A. Nutz, C. Schilling, and A. Podelski, “Ul-
timate automizer with smtinterpol,” in Tools and Algorithms
for the Construction and Analysis of Systems, N. Piterman
and S. A. Smolka, Eds. Berlin, Heidelberg: Springer Berlin
Heidelberg, 2013, pp. 641–643.

[108] L. De Moura and N. Bjørner, “Z3: an efficient smt solver,” in
Proceedings of the Theory and Practice of Software, 14th In-
ternational Conference on Tools and Algorithms for the Con-
struction and Analysis of Systems, ser. TACAS’08/ETAPS’08.
Berlin, Heidelberg: Springer-Verlag, 2008, p. 337–340.

[109]

J. Lu, L. Yu, X. Li, L. Yang, and C. Zuo, “Llama-
reviewer: Advancing code review automation with large
language models through parameter-efficient fine-tuning,” in
2023 IEEE 34th International Symposium on Software
Reliability Engineering (ISSRE).
Los Alamitos, CA,
USA:
IEEE Computer Society, oct 2023, pp. 647–658.
[Online]. Available: https://doi.ieeecomputersociety.org/10.
1109/ISSRE59848.2023.00026

[110] H. Dhulipala, A. Yadavally, and T. N. Nguyen, “Planning
to guide llm for code coverage prediction,” in Proceedings
of
International Conference
on AI Foundation Models and Software Engineering, ser.
FORGE ’24. New York, NY, USA: Association for

the 2024 IEEE/ACM First

Computing Machinery, 2024, p. 24–34. [Online]. Available:
https://doi.org/10.1145/3650105.3652292

[125] Google, “Bard,” 2023, accessed: 2024-12-09.

[Online].

Available: https://bard.google.com

[111] P. Hu, R. Liang, and K. Chen, “Degpt: Optimizing decompiler
output with llm,” Proceedings 2024 Network and Distributed
System Security Symposium, 2024.
[Online]. Available:
https://api.semanticscholar.org/CorpusID:267622140

[126]

J. Eom, S. Jeong, and T. Kwon, “Covrl: Fuzzing javascript
engines with coverage-guided reinforcement
learning for
llm-based mutation,” 2024.
[Online]. Available: https:
//arxiv.org/abs/2402.12222

24

[112]

J. Huang, C. Fang,

J. Yan, and J. Zhang,
J. Yan,
“Better debugging: Combining static analysis and llms
for explainable crashing fault localization,” 2024. [Online].
Available: https://arxiv.org/abs/2408.12070

[113] D. Pomian, A. Bellur, M. Dilhara, Z. Kurbatova,
“Together
and D. Dig,
E. Bogomolov, T. Bryksin,
static
we
for
analysis
ide
and
further: Llms
extract method refactoring,” 2024.
[Online]. Available:
https://arxiv.org/abs/2401.15298

go

[114] H. Rong, Y. Duan, H. Zhang, X. Wang, H. Chen, S. Duan, and
S. Wang, “Disassembling obfuscated executables with llm,”
2024. [Online]. Available: https://arxiv.org/abs/2407.08924

[115] H. Wang, Z. Wang, and P. Liu, “A hybrid llm workflow
in
can help identify user privilege
programs of any size,” 2024. [Online]. Available: https:
//arxiv.org/abs/2403.15723

related variables

[116] C. Wen, Y. Cai, B. Zhang, J. Su, Z. Xu, D. Liu, S. Qin,
Z. Ming, and T. Cong, “Automatically inspecting thousands of
static bug warnings with large language model: How far are
we?” ACM Trans. Knowl. Discov. Data, vol. 18, no. 7, Jun.
2024. [Online]. Available: https://doi.org/10.1145/3653718

[117] L.

Flynn

and W.
static-analysis

automate
CrossTalk:
Engineering, May
[Online].
using-llms-to-automate-static-analysis-adjudication-and-rationales/

llms
to
rationales,”
Software
version.
https://insights.sei.cmu.edu/library/

“Using
Klieber,
and
adjudication
of
Defense
pre-publication

Journal
2024,

Available:

The

[127] H. Zhang, Y. Rong, Y. He, and H. Chen, “Llamafuzz: Large
language model enhanced greybox fuzzing,” 2024. [Online].
Available: https://arxiv.org/abs/2406.07714

[128] Y. Deng, C. S. Xia, C. Yang, S. D. Zhang, S. Yang, and
L. Zhang, “Large language models are edge-case fuzzers:
Testing deep learning libraries via fuzzgpt,” 2023. [Online].
Available: https://arxiv.org/abs/2304.02014

[129]

J. Hu, Q. Zhang, and H. Yin, “Augmenting greybox
fuzzing with generative ai,” 2023.
[Online]. Available:
https://arxiv.org/abs/2306.06782

[130] C. Lemieux,

J. P.

Inala, S. K. Lahiri, and S. Sen,
“Codamosa: Escaping coverage plateaus in test generation
with pre-trained large language models,” in Proceedings of
the 45th International Conference on Software Engineering,
ser. ICSE ’23.
IEEE Press, 2023, p. 919–931. [Online].
Available: https://doi.org/10.1109/ICSE48619.2023.00085

[131] R. Meng, M. Mirchev, M. B¨ohme, and A. Roychoudhury,
“Large language model guided protocol fuzzing,” in Pro-
ceedings of the 31st Annual Network and Distributed System
Security Symposium (NDSS), 2024.

[132] Y. Oliinyk, M. Scott, R. Tsang, C. Fang, H. Homayoun
et al., “Fuzzing busybox: Leveraging llm and crash reuse for
embedded bug unearthing,” arXiv preprint arXiv:2403.03897,
2024.

[133] C. S. Xia, M. Paltenghi, J. L. Tian, M. Pradel, and L. Zhang,
“Fuzz4all: Universal fuzzing with large language models,”
2024. [Online]. Available: https://arxiv.org/abs/2308.04748

[118] Y. Hao, W. Chen, Z. Zhou, and W. Cui, “E&v: Prompting
large language models to perform static analysis by pseudo-
code execution and verification,” 2023. [Online]. Available:
https://arxiv.org/abs/2312.08477

[119] P. Yan, S. Tan, M. Wang, and J. Huang, “Prompt
engineering-assisted malware dynamic analysis using gpt-4,”
2023. [Online]. Available: https://arxiv.org/abs/2312.08317

[120] Y. S. Sun, Z.-K. Chen, Y.-T. Huang, and M. C. Chen,
“ Unleashing Malware Analysis and Understanding With
,” IEEE Security & Privacy, vol. 22,
Generative AI
no. 03, pp. 12–23, May 2024. [Online]. Available: https:
//doi.ieeecomputersociety.org/10.1109/MSEC.2024.3384415

[121] P. M. S. S´anchez, A. H. Celdr´an, G. Bovet, and G. M. P´erez,
“Transfer learning in pre-trained large language models for
malware detection based on system calls,” 2024. [Online].
Available: https://arxiv.org/abs/2405.09318

[122] Y. Li, S. Fang, T. Zhang, and H. Cai, “Enhancing
android malware detection: The influence of chatgpt on
decision-centric task,” 2024.
[Online]. Available: https:
//arxiv.org/abs/2410.04352

[123] F. Qiu, P. Ji, B. Hua, and Y. Wang, “Chemfuzz: Large
language models-assisted fuzzing for quantum chemistry
software bug detection,” 2023 IEEE 23rd International
Conference on Software Quality, Reliability, and Security
Companion (QRS-C), pp. 103–112, 2023. [Online]. Available:
https://api.semanticscholar.org/CorpusID:267771438

[124] Anthropic, “Claude-2,” 2023, accessed: 2024-12-09. [Online].
Available: https://www.anthropic.com/index/claude-2

[134]

ICMAB-CSIC,
2024-12-09.
2023,
[Online]. Available: https://departments.icmab.es/leem/siesta/

accessed:

“Siesta,”

[135] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto,
J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry,
P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov,
A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P.
Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes,
A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak,
J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders,
C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra,
E. Morikawa, A. Radford, M. Knight, M. Brundage,
M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei,
S. McCandlish, I. Sutskever, and W. Zaremba, “Evaluating
large language models trained on code,” 2021. [Online].
Available: https://arxiv.org/abs/2107.03374

[136] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou,
S. Savarese, and C. Xiong, “Codegen: An open large
language model for code with multi-turn program synthesis,”
2023. [Online]. Available: https://arxiv.org/abs/2203.13474

[137] A. Fioraldi, D. Maier, H. Eißfeldt, and M. Heuse, “AFL++
: Combining incremental steps of fuzzing research,” in 14th
USENIX Workshop on Offensive Technologies (WOOT 20).
USENIX Association, Aug. 2020. [Online]. Available: https:
//www.usenix.org/conference/woot20/presentation/fioraldi

[138] N. Wells, “Busybox: A swiss army knife for linux,” Linux

Journal, vol. 2000, no. 78es, pp. 10–es, 2000.

[139] B. Arkin, S. Stender, and G. McGraw, “Software penetration

testing,” IEEE Security & Privacy, vol. 3, no. 1, pp. 84–87,
2005.

[140] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li,
Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass,
“PentestGPT: Evaluating and harnessing large language
33rd
models
24).
USENIX Security
Philadelphia, PA: USENIX Association, Aug. 2024, pp. 847–
864. [Online]. Available: https://www.usenix.org/conference/
usenixsecurity24/presentation/deng

in
Symposium (USENIX Security

penetration

automated

testing,”

for

[141]

and Q.

framework

J. Huang
llm
optimal
655e0b6b-8ece-4830-bb82-649bac33bd5e, 6 2024.

“Penheal: A two-stage
and
pentesting
https://synthical.com/article/

remediation,”

automated

Zhu,

for

[142] D. Goyal, S. Subramanian, and A. Peela, “Hacking, the lazy
way: Llm augmented pentesting,” 2024. [Online]. Available:
https://arxiv.org/abs/2409.09493

[143] S. G. Bianou and R. G. Batogna, “Pentest-ai, an llm-powered
multi-agents framework for penetration testing automation
leveraging mitre attack,” in 2024 IEEE International Con-
ference on Cyber Security and Resilience (CSR), 2024, pp.
763–770.

[144] L. Muzsai, D. Imolai, and A. Luk´acs, “Hacksynth: Llm
agent and evaluation framework for autonomous penetration
testing,” 2024. [Online]. Available: https://arxiv.org/abs/2412.
01778

[145] L. Gioacchini, M. Mellia,
R.
Siracusano,

I. Drago, A. Delsanto,
G.
“Autopenbench:
Bifulco,
Benchmarking generative agents for penetration testing,”
2024. [Online]. Available: https://arxiv.org/abs/2410.03225

and

[146] X. Shen, L. Wang, Z. Li, Y. Chen, W. Zhao, D. Sun,
J. Wang, and W. Ruan, “Pentestagent: Incorporating llm
agents to automated penetration testing,” 2024. [Online].
Available: https://arxiv.org/abs/2411.05185

[147] S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test
generation using generative ai : A comparative performance
analysis of autogeneration tools,” in Proceedings of the 1st
International Workshop on Large Language Models for Code,
ser. LLM4Code ’24. New York, NY, USA: Association for
Computing Machinery, 2024, p. 54–61. [Online]. Available:
https://doi.org/10.1145/3643795.3648396

[148] S. Lukasczyk and G. Fraser, “Pynguin: automated unit test
the ACM/IEEE
generation for python,” in Proceedings of
44th International Conference on Software Engineering:
Companion Proceedings,
ICSE ’22. ACM, May
ser.
2022. [Online]. Available: http://dx.doi.org/10.1145/3510454.
3516829

[149] S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test
generation using generative ai : A comparative performance
analysis of autogeneration tools,” 2024. [Online]. Available:
https://arxiv.org/abs/2312.10622

[150] R. Pan, M. Kim, R. Krishna, R. Pavuluri, and S. Sinha,
test generation using llms,” 2024.

“Multi-language unit
[Online]. Available: https://arxiv.org/abs/2409.03093

[151] Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, and J. Yin,
“Chatunitest: A framework for llm-based test generation,”
in Companion Proceedings of the 32nd ACM International
Conference on the Foundations of Software Engineering,
New York, NY, USA: Association
ser. FSE 2024.
for Computing Machinery, 2024, p. 572–576.
[Online].
Available: https://doi.org/10.1145/3663529.3663801

[152] Z. Zhang, X. Liu, Y. Lin, X. Gao, H. Sun, and Y. Yuan,

25

“Llm-based unit test generation via property retrieval,” 2024.
[Online]. Available: https://arxiv.org/abs/2410.13542
[153] S. Gu, Q. Zhang, C. Fang, F. Tian, L. Zhu, J. Zhou,
and Z. Chen, “Testart: Improving llm-based unit testing via
co-evolution of automated generation and repair iteration,”
2024. [Online]. Available: https://arxiv.org/abs/2408.03095

[154] Z. Yuan, Y. Lou, M. Liu, S. Ding, K. Wang, Y. Chen, and
X. Peng, “No more manual tests? evaluating and improving
chatgpt for unit test generation,” 2024. [Online]. Available:
https://arxiv.org/abs/2305.04207

[155] Z. Wang, K. Liu, G. Li, and Z. Jin, “Hits: High-coverage
test generation via method slicing,” 2024.

llm-based unit
[Online]. Available: https://arxiv.org/abs/2408.11324
[156] A. Lops, F. Narducci, A. Ragone, M. Trizio, and C. Bartolini,
“A system for automated unit test generation using large
language models and assessment of generated test suites,”
2024. [Online]. Available: https://arxiv.org/abs/2408.07846

[157] A. Nunez, N. T. Islam, S. Jha, and P. Najafirad, “Autosafe-
coder: A multi-agent framework for securing llm code gen-
eration through static analysis and fuzz testing,” 09 2024.
J. A. Pizzorno and E. D. Berger, “Coverup: Coverage-
guided llm-based test generation,” 2024. [Online]. Available:
https://arxiv.org/abs/2403.16218

[158]

[159] R. Kumar, Z. Xiaosong, R. U. Khan, J. Kumar, and I. Ahad,
“Effective and explainable detection of android malware
based on machine learning algorithms,” in Proceedings
of
the 2018 International Conference on Computing and
Artificial Intelligence, ser. ICCAI ’18. New York, NY,
USA: Association for Computing Machinery, 2018, p. 35–40.
[Online]. Available: https://doi.org/10.1145/3194452.3194465
[160] L. Onwuzurike, E. Mariconti, P. Andriotis, E. D. Cristofaro,
G. Ross, and G. Stringhini, “Mamadroid: Detecting android
malware by building markov chains of behavioral models
(extended version),” 2019. [Online]. Available: https://arxiv.
org/abs/1711.07477

[161] B. Wu, S. Chen, C. Gao, L. Fan, Y. Liu, W. Wen, and
M. R. Lyu, “Why an android app is classified as malware?
towards malware classification interpretation,” 2020. [Online].
Available: https://arxiv.org/abs/2004.11516

[162] A. Williamson and M. Beauparlant, “Malware reverse engi-
neering with large language model for superior code compre-
hensibility and ioc recommendations,” 2024.

[163] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can
large language models reason about program invariants?”
in Proceedings of
the 40th International Conference on
Machine Learning, ser. Proceedings of Machine Learning
Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt,
PMLR,
S. Sabato, and J. Scarlett, Eds., vol. 202.
23–29 Jul 2023, pp. 27 496–27 520.
[Online]. Available:
https://proceedings.mlr.press/v202/pei23a.html

[164] S. Glazunov and M. Brand, “Project naptime: Evaluating
language
security
https://googleprojectzero.blogspot.com/2024/06/

offensive
models,”
project-naptime.html, 2024, accessed: 2024-10-16.

capabilities

large

of

[165] M. Bhatt, S. Chennabasappa, Y. Li, C. Nikolaidis, D. Song,
S. Wan, F. Ahmad, C. Aschermann, Y. Chen, D. Kapil,
D. Molnar, S. Whitman, and J. Saxe, “Cyberseceval
2: A wide-ranging cybersecurity evaluation suite
for
large language models,” 2024. [Online]. Available: https:
//arxiv.org/abs/2404.13161


