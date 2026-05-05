Dear Andrey,

Thank you for your submission to the EASE 2026 Short Papers and Emerging Results track for the 30th International Conference on Evaluation and Assessment in Software Engineering in Glasgow.

After the review process, we regret to inform you that we are unable to accept your paper for the program this year. We received 89 submissions and were only able to accept a limited number of papers to maintain the track's focus (26 papers accepted, 29% acceptance rate)

While the reviewers noted specific strengths, the final decision was based on identified weaknesses and overall quality of other submissions.

We appreciate the opportunity to consider your work and wish you the best with your research.

Best regards, 

Marie & Peggy

SUBMISSION: 385
TITLE: Improving Software Maintainability Through LLM-Implemented Architectural Tactics: Early Empirical Evidence

----------------------- REVIEW 1 ---------------------

SUBMISSION: 385
TITLE: Improving Software Maintainability Through LLM-Implemented Architectural Tactics: Early Empirical Evidence

----------- Overall Comments for Authors -----------
The paper proposed a pipeline based on LLMs to perform high-level refactorings guided by the detected architectural style, aiming to improve maintainability. The authors report a study with open-source Python projects that shows promising results.

The paper motivated the study and identified an existing gap in the literature, while covering recent work in related fields. The study methodology is well described, and the results are reported appropriately.

One suggestion to the authors is to separate the proposed approach from the study's methodology. In my view, this is a contribution of the work that is not well highlighted in the way it is presented.

A positive aspect of the paper is that the discussion does not focus solely on the quantitative analysis of the metrics but also brings this information into the architectural discussion. An example of this is the reflection regarding the results and the selected tactics in each architectural style.

Considering the expected contributions of a short paper, I believe this one explored a current gap in the literature, making a contribution, while also leaving several possibilities for further development in future studies.


----------------------- REVIEW 2 ---------------------

SUBMISSION: 385
TITLE: Improving Software Maintainability Through LLM-Implemented Architectural Tactics: Early Empirical Evidence

----------- Overall Comments for Authors -----------
This paper aims to assess the effectiveness of using LLMs to identify architectural characteristics of existing codebases, and to apply transformations to the code to improve architectural qualities.

This is a nice idea, but I found the treatment in this paper to be quite shallow.

The approach taken is to process GitHub repositories, looking for codebases written in Python (but rationale for working only with Python is given), that have a requirements.txt, and are under active development. No indication of the size of the repositories processed is given. Given the context-window size of the LLM is identified as a constraint, I think giving the size of the codebases is an important detail.

The LLM is tasked with classifying the architectural style of each codebase. The Conclusion states that "the pipeline produced architecture classifications for all 162 repositories with high *self-reported* confident" - but this is not checked against any ground truth in the study. I don't think we should take self-reported confidence as a measure of accuracy here.

Then the LLM is tasked with picking an appropriate architectural tactic, applying it to the codebase, and the study measures a small selection of metrics for comparison. It is a shame that there is no real description of how the architectural tactics are described, or how the LLM-based system applies the code edits. For example "Reduced coupling - introducing interfaces..." - it's not clear to me how this would manifest in a Python codebase. It would be helpful for the paper to give more concrete examples of the application of these tactics. How is the large codebase structured within a single prompt? How does the LLM edit the codebase? Purely through textual edits? Is an autonomous agent being utilised? What feedback loops does it have?

The range of architectural tactics seems quite limited. One of the metrics taken is the amount of documentation per function, which does not seem like an architectural concern - even if it does affect maintainabilty.

It is notable that the paper discusses checking for "syntactic correctness" after transformation, but not "semantic correctness" or "behaviour preservation". A vital feature of a refactoring is that it does not affect the behaviour of the system.

There is also some discussion of TDD, it seems to be suggested that TDD would be a method for performing refactoring (but left to future work). I guess what is meant here is running automated test suites before and after transformations to check behaviour preservation. But that is different from TDD, which requires adding a new failing test to drive out a particular change.

Overall, given the title, I didn't feel that the sorts of changes being discussed here were very architectural in nature. The most common change seemed to breaking down large scripts into smaller ones. That seems quite different from introducing a new microservice, or creating a service layer to allow for testing via test-doubles, etc etc. That was the level of change I was expecting given the title

I think this is an interesting area, and I encourage the authors to do more work in the area, but to think about larger scale architectural changes in large projects.


----------------------- REVIEW 3 ---------------------

SUBMISSION: 385
TITLE: Improving Software Maintainability Through LLM-Implemented Architectural Tactics: Early Empirical Evidence

----------- Overall Comments for Authors -----------
This paper introduces and evaluates an automation pipeline for applying architectural refactorings to achieve maintainability. The pipeline evaluates projects for architectural characteristics and uses this information to select and apply architectural tactics to Python

In my opinion, this paper tries to do too much. Any one of the 'Architecture Detection', 'Tactic Selection', or 'Tactic Implementation' topics would be worth a paper-length investigation. Combining them into the engineering effort of building a pipeline deemphasizes the problems and analyses for each of those important topics and delays the refinement of each of those topics that would be necessary to automate work at the architectural layer. The new ideas that are probably there are buried in the effort. The good news is that you have a worthwhile research agenda in those topics.