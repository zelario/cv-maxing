# CV Evaluation Research

## Research Objective

The goal of this research is to identify the factors most relevant when evaluating a CV against a specific job posting. The findings will be used to define the evaluation framework for the CV Maxing Reviewer Agent.

The research covers company hiring practices, recruiter and HR guidance, Applicant Tracking Systems (ATS), resume-job matching, and academic research on automated and AI-assisted recruitment.

A key finding is that there is **no universal weighting system** for CV evaluation. The importance of each criterion depends on the requirements and context of the specific job. The framework should therefore establish a general hierarchy while allowing the importance of individual criteria to change according to the job posting. [1][2][3][4]

---

## 1. Required Skills and Qualifications

**Priority: Very High**

Required skills and qualifications are consistently among the most important factors in candidate screening.

NACE reports that 70% of surveyed employers use skills-based hiring and that 65% use it during the screening process. [5] Indeed recommends starting resume screening by checking whether candidates meet the skills and qualifications required for the position. [3]

LinkedIn's job matching system also compares candidate skills, education, years of experience, and job title against job requirements. [2]

The system should therefore distinguish between:

```text
Required skill → High importance

Preferred skill → Lower importance

Non-required skill → Context-dependent
```

Explicit requirements should receive more weight than generic CV best practices.

---

## 2. Relevant Experience

**Priority: Very High**

Relevant professional experience is another consistently important criterion.

Resume screening guidance recommends examining previous positions, responsibilities, duration, progression, and their relevance to the target position. [3][4]

Microsoft's documented career matching system also considers relevant experience, job titles, experience categories, and seniority. [1]

The system should therefore evaluate:

```text
Role relevance + Responsibilities + Seniority + Duration + Similarity to target position
```

Years of experience alone should not determine relevance. Experience should be evaluated in the context of the specific job.

---

## 3. Demonstrated Skills and Evidence

**Priority: Very High**

A major distinction should be made between a skill being **listed** and a skill being **demonstrated**.

For example:

```text
Skills: Python, SQL, AWS
```

provides weaker evidence than:

```text
Developed a Python data pipeline using SQL and AWS.
```

NACE emphasizes employers' interest in whether candidates have actually demonstrated relevant competencies. [5] Resume screening guidance also recommends examining how previous experience demonstrates the candidate's capabilities rather than relying solely on a list of skills. [3]

This supports the following classification:

```text
Satisfied, Weak Evidence or Missing
```

A skill mentioned only in a skills section should generally receive weaker evidential support than a skill demonstrated through work experience or relevant projects.

---

## 4. Achievements and Impact

**Priority: High**

Relevant experience becomes more informative when it demonstrates impact.

Indeed recommends evaluating the scope and impact of previous work and looking for measurable outcomes, accomplishments, promotions, awards, process improvements, and other indicators of contribution. [3]

For example:

```text
Weak: Developed reports using Python.

Stronger: Developed a Python reporting pipeline that reduced manual processing time by 40%.
```

The Reviewer should therefore distinguish between:

```text
Responsibilities + Demonstrated impact
```

Quantified achievements should strengthen the evidence for relevant experience when they are genuinely supported by the CV.

---

## 5. Relevant Projects and Practical Experience

**Priority: High, particularly for entry-level candidates**

Projects, internships, and other forms of experiential learning are particularly relevant when candidates have limited professional experience.

NACE reports that employers value experiential learning and the demonstration of skills through practical experiences. [5]

For entry-level candidates, relevant evidence can include:

```text
Internships, University projects, Personal projects, Research, Open-source work or Practical coursework
```

The importance of projects should therefore depend partly on the candidate's career stage.

For an entry-level candidate:

```text
Relevant project ≈ Practical evidence of skills
```

while for an experienced candidate, professional experience may provide stronger evidence.

---

## 6. Soft Skills and Competencies

**Priority: Medium-High**

Employers also look for evidence of competencies such as:

* Teamwork
* Communication
* Problem-solving

NACE identifies these competencies among those employers look for in entry-level candidates. [5]

However, the system should avoid giving substantial weight to self-declared claims such as:

```text
"Excellent communicator" or "Strong team player"
```

without supporting evidence.

Evidence such as:

```text
"Led a team of four students", "Presented project results to stakeholders", "Resolved a production issue affecting..."
```

provides stronger support.

Therefore:

```text
Claimed competency < Demonstrated competency
```

---

## 7. Education and Certifications

**Priority: Context-dependent**

Education is an important component of candidate matching, but its importance depends strongly on the job requirements.

Microsoft and LinkedIn both include education in candidate-job matching. [1][2]

However, the growth of skills-based hiring suggests that education should not automatically dominate the assessment when it is not a core requirement. [5]

The system should therefore distinguish between:

```text
Required degree / certification → High importance

Preferred degree / certification → Medium importance

Unrelated or unnecessary education → Low importance
```

Education should therefore be evaluated relative to the specific job rather than assigned a fixed universal weight.

---

## 8. Keywords and ATS Alignment

**Priority: Medium**

Keywords are relevant to automated screening and candidate-job matching, particularly during initial screening. [1][3]

However, the research does not support treating CV evaluation as a simple keyword-counting problem.

Greenhouse describes matching approaches that can consider related terminology and synonyms, reducing the limitations of exact keyword matching. [6]

Academic research also supports semantic approaches to resume-job matching using Transformer-based models. [7]

Therefore, CV Maxing should combine:

```text
Literal Matching  + Semantic Matching + Context + Evidence
```

For example:

```text
"predictive modelling" = "machine learning"
```

may represent related experience even when the exact terminology differs.

---

## 9. CV Structure and Presentation

**Priority: Medium-Low**

CV structure and presentation affect readability and potentially automated extraction, but they should not dominate the candidate-job fit assessment.

Resume screening guidance recommends checking:

* Organization
* Clarity
* Grammar
* Formatting
* Compliance with application instructions [3][4]

However, these aspects should generally act as supporting criteria rather than overriding substantive evidence of skills and experience.

A useful principle is:

```text
Poor structure → Potential penalty

Clear structure → Baseline

Excellent formatting → Limited additional benefit
```

The system should prioritize the candidate's demonstrated suitability over visual presentation.

---

# Overall Priority Order

Based on the convergence of the sources, the initial hierarchy for CV Maxing should be:

```text
1. Required Skills / Qualifications
2. Relevant Experience
3. Demonstrated Skills / Evidence
4. Achievements / Impact
5. Relevant Projects / Practical Experience
6. Soft Skills / Competencies
7. Education / Certifications
8. Keywords / ATS Alignment
9. CV Structure / Presentation
```

This should not be converted directly into fixed numerical weights.

Instead, the importance of each criterion should be adjusted according to the specific job.

For example:

```text
Job A:
"Master's degree in Computer Science required" → Education becomes a high-priority criterion.

Job B:
"3+ years of production experience with AWS required" → Relevant Experience + AWS become high-priority criteria.

Job C:
"Entry-level Data Analyst" → Skills + Projects + Demonstrated Evidence may become more important because the candidate may have limited professional experience.
```

The job-specific requirements should therefore take precedence over a universal ranking.

---

# Evidence Strength

One of the central concepts for the Reviewer Agent should be **evidence strength**.

A requirement should not simply be classified as present or absent.

The system should distinguish:

```text
Missing → Mentioned → Supported → Strongly Demonstrated
```

Example:

```text
SQL

Missing: No evidence of SQL.

Mentioned: SQL appears in the Skills section.

Supported: SQL appears in the Skills section and in a project.

Strongly Demonstrated: The project describes concrete SQL usage and its impact.
```

This distinction is important because recruitment guidance emphasizes the demonstration of skills rather than only their self-declaration. [3][5]

---

# Sources

[1] Microsoft Careers. **Transparency FAQ**
https://careers.microsoft.com/v2/global/en/transparency.html

[2] LinkedIn. **How You Match**
https://www.linkedin.com/business/talent/blog/product-tips/linkedin-how-you-match

[3] Indeed. **How to Read an Applicant Resume**
https://www.indeed.com/hire/c/info/how-to-read-a-resume

[4] SHRM. **How to Screen Resumes Efficiently: A Beginner's Guide**
https://www.shrm.org/in/topics-tools/news/blogs/how-to-screen-resumes-efficiently--a-beginner-s-guide

[5] NACE. **Employer Use of Skills-Based Hiring Practices Grows**
https://naceweb.org/job-market/trends-and-predictions/employer-use-of-skills-based-hiring-practices-grows

[6] Greenhouse. **What Really Happens After You Apply for a Job?**
https://my.greenhouse.com/blogs/what-really-happens-after-you-apply-for-a-job

[7] Son, Y. et al. **Competence-Level Prediction and Resume & Job Description Matching Using a Pre-trained Language Model**. EMNLP 2020.
https://aclanthology.org/2020.emnlp-main.679/

[8] **Signal or Noise? Evaluating Large Language Models in Resume Screening**. 2025.
https://arxiv.org/abs/2507.08019

[9] **Should I Trust the Artificial Intelligence to Recruit?**
https://pmc.ncbi.nlm.nih.gov/articles/PMC9298741/

[10] **Enablers and Inhibitors of AI Assimilation in Hiring**. 2025.
https://www.sciencedirect.com/org/science/article/pii/S0959384524000046

[11] European Union. **Regulation (EU) 2024/1689 (Artificial Intelligence Act)**
https://eur-lex.europa.eu/eli/reg/2024/1689/oj
