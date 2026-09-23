# Development Plan: CV Maxing

## Phase 1: Define the Problem

### Goal

Develop an intelligent system capable of analyzing a Curriculum Vitae in relation to a job posting, evaluating the candidate's suitability based on recruitment and selection criteria identified through research into Human Resources practices and Applicant Tracking Systems (ATS).

The system will identify missing requirements, weak evidence, and areas for improvement. An AI Reviewer Agent will perform the matching and evaluation process, using deterministic scoring methods as a foundation and then applying its own reasoning to provide a qualitative assessment and generate recommendations.

The user will remain involved in the decision-making process through a Human-in-the-Loop approach.

### Input

* CV in PDF format
* Job posting URL

### Output

* Deterministic Fit Score
* AI Reviewer Assessment
* Missing Requirements
* Weak Evidence
* Potential Improvements
* Optimized CV

### What the System Does Not Do

* It does not decide whether someone should be hired.
* It does not invent experience or qualifications.
* It does not treat a nonexistent skill as an existing skill.
* The score is a CV-to-job fit indicator, not a real probability of being hired.
* AI recommendations must be supported by information contained in the original CV.
* The system does not guarantee that an optimized CV will result in an interview or job offer.

---

## Phase 2: Research

### Research Areas

**Companies**

* Hiring criteria
* ATS practices
* Career guides
* CV requirements
* Job posting requirements

**Recruiters / HR Professionals**

* What recruiters look for in a CV
* How experience is assessed
* Importance of skills, projects, achievements, and keywords
* Common reasons for rejecting CVs
* How recruiters evaluate candidate-job fit

**Academic Literature**

* CV screening
* Automated recruitment
* Resume-job matching
* NLP for recruitment
* Applicant Tracking Systems
* Algorithmic hiring
* Human-AI collaboration in recruitment
* LLMs in recruitment and resume evaluation

### Expected Output: Evaluation Framework

The research will be used to define an evidence-based evaluation framework.

Example criteria:

```text
1. Required Skills
2. Preferred Skills
3. Relevant Experience
4. Projects
5. Education
6. Keywords
7. CV Structure
8. Achievements
9. ATS Compatibility
```

For each criterion:

```text
Criterion
Evidence
Importance
Evaluation Method
```

The final scoring framework and weights will be determined and justified based on the research conducted in this phase.

---

## Phase 3: Dataset

### Job Postings

Collect job postings for relevant roles, such as:

* Data Scientist
* Data Analyst
* Data Engineer
* Machine Learning Engineer

Possible sources:

* Kaggle
* Hugging Face
* Public company career pages

### CVs

Prefer **synthetic CVs** to avoid privacy concerns.

Create multiple CV variations for the same candidate profile, for example:

* Strong CV
* Weak CV
* Missing required skills
* Poorly presented CV
* Relevant experience poorly described
* Keyword-misaligned CV

Possible sources for existing datasets:

* Kaggle
* Hugging Face

The dataset will primarily be used for development, testing, and evaluation.

A supervised training dataset is not required for the initial system because the core evaluation relies on a research-based framework, deterministic methods, and LLM reasoning rather than training a new predictive model.

---

## Phase 4: CV Extraction and Structuring

The system must support CVs with different layouts and structures.

### Pipeline

```text
PDF
 ↓
Document Text Extraction
 ↓
CV Parser Agent
 ↓
Structured CV
 ↓
Validation
```

The CV Parser Agent uses an LLM to interpret and structure the extracted information.

### Tools

* **Docling** for PDF text extraction
* **LLM** for interpreting and structuring extracted CV information

The original document content should remain available so that extracted information can be validated and information loss can be detected.

### Example Output

```json
{
  "education": [],
  "experience": [],
  "skills": [],
  "projects": [],
  "certifications": [],
  "languages": [],
  "achievements": []
}
```

The extraction process must follow strict rules:

* Do not invent information.
* Preserve relevant information from the original CV.
* Distinguish between explicitly stated information and uncertain information.
* Validate the structured output against the original extracted text.

---

## Phase 5: Job Extraction and Structuring

### Pipeline

```text
Job Posting URL
 ↓
Web Page Extraction
 ↓
Job Parser Agent
 ↓
Structured Job
 ↓
Validation
```

The system must extract the relevant content from the job posting while ignoring unrelated page content.

### Example Output

```json
{
  "required_skills": [],
  "preferred_skills": [],
  "experience": [],
  "education": [],
  "responsibilities": [],
  "keywords": [],
  "other_requirements": []
}
```

The same validation principles used for CV extraction should be applied to job extraction.

---

## Phase 6: Reviewer Agent

The **Reviewer Agent is the central component of the system**. It performs the complete evaluation process.

The Reviewer receives:

```text
Structured CV
Structured Job
Evaluation Framework
```

It then performs the following stages:

```text
1. Requirement Matching
2. Evidence Analysis
3. Deterministic Scoring
4. Independent AI Reasoning
5. Final Review
```

### Stage 1: Requirement Matching

The Reviewer identifies how each job requirement corresponds to evidence in the CV.

Both literal and semantic matching can be used.

#### Literal Matching

```text
Python → Python ✓
SQL → SQL ✓
Spark → Absent ✗
```

#### Semantic Matching

Use **Sentence Transformers** to identify semantically related concepts.

Example:

```text
"predictive modelling"
        ↕
"machine learning"
```

### Result Per Requirement

```text
Python → Match: 1.00 | Evidence: Project X
SQL    → Match: 0.87 | Evidence: Skills + Project Y
Spark  → Match: 0.00 | Evidence: None
```

Each match must retain the evidence supporting the decision.

---

### Stage 2: Evidence Analysis

The Reviewer classifies requirements according to the strength of the available evidence.

```text
✓ Satisfied
⚠ Weak Evidence
✗ Missing
```

Example:

```text
✓ Python
  Required and demonstrated in Project X.

⚠ SQL
  Present in the Skills section but with limited
  evidence of practical usage.

✗ Spark
  Required by the job but no evidence was found.
```

The Reviewer should distinguish between:

* Skill explicitly demonstrated
* Skill mentioned but weakly supported
* Semantically related experience
* Requirement not found
* Requirement contradicted by the CV

---

### Stage 3: Deterministic Scoring

The Reviewer uses the Evaluation Framework to obtain a deterministic score.

Example:

```text
Required Skills    30%
Experience         25%
Projects           15%
Education          10%
Keywords           10%
CV Quality         10%
```

The actual calculation is performed by a deterministic scoring tool.

Example:

```text
Hiring Fit: 74/100

Required Skills: 82%
Experience:      75%
Projects:        68%
Education:      100%
Keywords:        55%
```

The Reviewer does not directly invent the numerical result.

Instead, it calls the scoring tool:

```text
calculate_score(
    matching_results,
    evaluation_framework
)
```

This provides a reproducible baseline.

---

### Stage 4: Independent AI Reasoning

After obtaining the deterministic results, the Reviewer performs an independent qualitative assessment.

The Reviewer receives:

```text
CV
Job Description
Matching Results
Deterministic Score
Evidence
Missing Requirements
Weak Evidence
```

It then asks:

```text
Does the deterministic score accurately represent the
candidate's overall fit?

Are there important factors that the deterministic
system did not capture?

Are some requirements more or less important in context?

Is the evidence actually convincing?

What would a recruiter likely notice?
```

The Reviewer may agree or disagree with the deterministic score.

Example:

```text
Deterministic Score: 74/100

AI Reviewer Assessment: 78/100

Reasoning:

The deterministic score penalizes the candidate for
missing Spark. However, Spark appears mainly as a
preferred technology and is not central to the core
responsibilities of the position.

The candidate demonstrates strong Python, SQL and
machine learning experience through relevant projects.

Overall, the candidate appears to be a strong but
incomplete match.
```

The system should preserve both assessments:

```text
Deterministic Score: 74/100
AI Reviewer Assessment: 78/100
```

The AI assessment should not simply overwrite the deterministic score.

---

### Stage 5: Final Review

The Reviewer produces a structured final assessment containing:

```text
Deterministic Score
AI Assessment
Agreement / Disagreement
Strengths
Missing Requirements
Weak Evidence
Priority Improvements
Reasoning
```

Example:

```text
Deterministic Score: 74/100
AI Assessment: 78/100

Strengths:
- Strong Python experience
- Relevant machine learning projects
- Appropriate educational background

Missing Requirements:
- Spark
- AWS

Weak Evidence:
- SQL

Priority Improvements:
1. Provide stronger evidence of SQL usage
2. Improve the description of Project X
3. Align relevant keywords with the job posting
```

---

## Phase 7: Gap and Evidence Prioritization

The Reviewer prioritizes the identified weaknesses.

```text
HIGH PRIORITY
- Missing required skill
- Weak evidence for a critical requirement

MEDIUM PRIORITY
- Relevant experience poorly described
- Important keywords missing

LOW PRIORITY
- Minor presentation improvements
```

The prioritization should consider both:

* Importance of the requirement
* Current strength of the candidate's evidence

---

## Phase 8: AI Recommendation and CV Optimization

The AI system uses the Reviewer output to generate recommendations.

The LLM can assist with:

* Explaining evaluation results
* Generating recommendations
* Identifying which improvement should be addressed first
* Rewriting CV bullets
* Improving descriptions of relevant experience and projects
* Improving keyword alignment
* Checking whether proposed changes are supported by the original CV

### Optimization Loop

```text
CV
 ↓
Reviewer Agent
 ↓
Deterministic Score + AI Assessment
 ↓
Identify Biggest Weakness
 ↓
Generate Improvement
 ↓
Human Approval
 ↓
Modify CV
 ↓
Reviewer Agent
 ↓
Recalculate Score + Reassess
 ↓
Repeat or Stop
```

### Example

```text
Original Deterministic Score: 72
Original AI Assessment: 75

Change 1: +4
Change 2: +3
Change 3: +1

Final Deterministic Score: 80
Final AI Assessment: 82
```

### Stopping Criteria

The optimization loop must have an explicit stopping criterion:

* Maximum number of iterations
* Minimum required score improvement
* Stop when marginal improvement falls below a predefined threshold
* Stop when all high-priority improvements have been addressed
* Stop when the Reviewer determines that further changes provide limited value

The system must never introduce information that is not supported by the original CV.

---

## Phase 9: CrewAI Integration

Once the core pipeline is functional, integrate **CrewAI** to orchestrate the different AI agents and tasks.

### Agent Architecture

```text
                         CrewAI
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
       CV Parser Agent             Job Parser Agent
              │                           │
              └─────────────┬─────────────┘
                            ↓
                     Reviewer Agent
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
          Matching       Scoring        Reasoning
           Tools           Tool             │
             └──────────────┬──────────────┘
                            ↓
                   Review & Recommendations
                            ↓
                   Optimization Agent
```

The key distinction is that **matching, scoring, and reasoning are tasks performed by the Reviewer Agent**, not separate agents.

---

## Phase 10: Human-in-the-Loop

The user remains involved in the optimization process.

### Recommendation Approval

```text
AI Recommendation

"Strengthen SQL evidence in Project X."

[ Accept ] [ Edit ] [ Reject ]
```

### Optimization Workflow

```text
Original CV
 ↓
Reviewer Analysis
 ↓
AI Recommendation
 ↓
Human Approval
 ↓
CV Modification
 ↓
Reviewer Reassessment
 ↓
New Score
```

The system should store user feedback:

```text
Accepted
Rejected
Edited
```

This feedback can later be used to evaluate the quality and usefulness of the recommendations.

---

## Phase 11: System Evaluation

### Matching Evaluation

Compare the Reviewer's classifications against human evaluations or suitable labeled datasets.

Possible metrics:

* Precision
* Recall
* F1-score
* Human-system agreement

### Deterministic Scoring Evaluation

Evaluate whether the deterministic scoring framework produces results consistent with human evaluations.

Possible measures:

* Correlation with human ratings
* Score consistency
* Criterion-level agreement
* Human-system agreement

### AI Reviewer Evaluation

Evaluate:

* Agreement with human evaluators
* Quality of reasoning
* Ability to identify missed requirements
* Recommendation acceptance rate
* Recommendation rejection rate
* Invalid recommendations
* Fabricated information
* Consistency
* Agreement with deterministic scoring

### Deterministic vs. AI Reviewer

A central research question is:

```text
Does the AI Reviewer provide useful information
beyond deterministic CV-job matching and scoring?
```

Compare:

```text
Deterministic Score
        vs.
AI Reviewer Assessment
        vs.
Human Evaluation
```

This allows the project to determine whether the AI reasoning component actually adds value.

### Optimization Evaluation

Measure whether the system improves CV-job fit without introducing false information.

Example:

```text
Average Original Deterministic Score: 63
Average Optimized Deterministic Score: 78

Average Original AI Assessment: 67
Average Optimized AI Assessment: 81
```

The evaluation must always verify:

```text
Did the score improve?

        AND

Was the new information factually supported?

        AND

Did the modification improve the CV according
to human evaluation?
```

An increase in score caused by fabricated or unsupported information must be considered a failure.

---

## Phase 12: Interface

### Example Interface

```text
CV MAXING

├── Upload your CV
├── Job Posting URL
└── [ ANALYZE ]

→ Deterministic Fit: 74/100

→ AI Reviewer Assessment: 78/100

→ Missing Requirements:
   ✗ Spark
   ✗ AWS

→ Weak Evidence:
   ⚠ SQL

→ Reviewer Summary:
   Strong Python and ML experience,
   but limited evidence of Spark usage.

→ Improvements:
   1. Strengthen SQL evidence
   2. Improve Project X
   3. Improve keyword alignment

→ [ OPTIMIZE CV ]
```

The interface should also allow the user to review and approve/reject proposed modifications.

---

## Final Architecture

```text
                         CV + Job URL
                              │
               ┌──────────────┴──────────────┐
               ↓                             ↓
       CV Document Extraction         Job Page Extraction
               ↓                             ↓
         CV Parser Agent              Job Parser Agent
               ↓                             ↓
          Structured CV                 Structured Job
               └──────────────┬──────────────┘
                              ↓
                     ┌─────────────────┐
                     │ Reviewer Agent  │
                     │                 │
                     │ 1. Match        │
                     │ 2. Score        │
                     │ 3. Analyze      │
                     │ 4. Reason       │
                     └────────┬────────┘
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
          Matching Tools  Scoring Tool   LLM Reasoning
                │             │             │
                └─────────────┼─────────────┘
                              ↓
                    Reviewer Assessment
                              ↓
                  Recommendations
                              ↓
                     Human Approval
                              ↓
                  Optimization Agent
                              ↓
                       Modified CV
                              ↓
                     Reviewer Agent
                              ↓
                  Re-score + Re-review
                              ↓
                         Final CV
```

## Final Stack

```text
Python
│
├── PyMuPDF
├── python-docx
├── spaCy
├── Sentence Transformers
├── Pydantic
│
├── LLM-based Information Extraction
├── Custom Evaluation Framework
├── Matching Tools
├── Deterministic Scoring Engine
│
├── CrewAI
│   ├── CV Parser Agent
│   ├── Job Parser Agent
│   ├── Reviewer Agent
│   └── Optimization Agent
│
└── LLM
```
