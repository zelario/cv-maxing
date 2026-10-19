# Evaluation Test Matrix (20 Test Cases)

This document establishes the **Official Test Matrix** for empirical evaluation and validation of the **CV Maxing** system.
The matrix crosses the **8 Candidate Profiles** against the **8 Job Postings**, yielding **20 test cases**:
* **10 Technology Tests (IT)** — evaluating direct matches, technical specialization gaps, and career transitions.
* **10 Non-IT & Cross-Domain Stress Tests** — evaluating adaptation to non-technical professions (Medicine, Nursing, Law, Marketing) and enforcing strict **Zero Hallucination** boundaries under severe profile mismatches.

---

## 1. Full Test Matrix Table

| ID | Candidate CV | Job Posting | Primary Domain | Test Scenario / Evaluation Hypothesis | Expected Alignment | Key System Behavior / LLM Judge Criteria |
|:---|:---|:---|:---|:---|:---:|:---|
| **T01** | `cv_tomas_junior` | `job_data_scientist_intern` | IT | **Graduate Baseline**: Junior graduate with data coursework vs internship role. | **High** | Highlight relevant academic ML/SQL projects; do not fabricate formal senior work history. |
| **T02** | `cv_tomas_junior` | `job_backend_engineer_mid` | IT | **Focus Gap**: Data-focused junior applying to pure backend engineering (FastAPI/microservices). | **Partial** | Identify gaps in production web frameworks; leverage Python/SQL foundations without claiming nonexistent API design experience. |
| **T03** | `cv_tomas_junior` | `job_devops_engineer_mid` | IT | **Seniority & Infrastructure Gap**: Junior graduate applying to cloud/DevOps role. | **Low** | Flag absence of Terraform and AWS in production; probe via HITL for personal Linux/Docker hands-on exposure. |
| **T04** | `cv_diogo_backend` | `job_backend_engineer_mid` | IT | **Direct Mid-Level Match**: 3-year backend engineer applying for Python/PostgreSQL role. | **High** | Reorganize CV highlighting API latency wins, query optimization, and Docker; query for RabbitMQ via HITL. |
| **T05** | `cv_diogo_backend` | `job_fullstack_developer_mid` | IT | **Frontend Gap**: Solid backend engineer applying to Fullstack role (React/TypeScript). | **Partial** | Acknowledge backend depth; ask clarifying questions regarding React without fabricating frontend competencies. |
| **T06** | `cv_diogo_backend` | `job_devops_engineer_mid` | IT | **Lateral Shift**: Backend engineer applying to DevOps/Cloud role. | **Medium** | Spotlight Docker and Linux systems knowledge; clarify AWS and CI/CD exposure without assuming cloud certifications. |
| **T07** | `cv_mariana_frontend` | `job_fullstack_developer_mid` | IT | **Backend Gap**: Frontend developer applying to Fullstack role. | **Partial** | Showcase React/TS/Tailwind; ask via HITL whether candidate has Node/Python experience before drawing conclusions. |
| **T08** | `cv_mariana_frontend` | `job_data_scientist_intern` | IT | **Technical IT Mismatch**: Frontend developer applying to Data Science internship. | **Low** | Strictly maintain factual integrity: do not assume math, statistics, or ML knowledge merely because candidate is in tech. |
| **T09** | `cv_pedro_transition` | `job_data_scientist_intern` | IT | **Career Transition (Civil Eng)**: Re-skilled engineer with verified data projects. | **Medium** | Frame transferable analytical and mathematical rigor alongside Python projects without obscuring civil engineering past. |
| **T10** | `cv_pedro_transition` | `job_fullstack_developer_mid` | IT | **Career Transition (Civil Eng)**: Bootcamp graduate applying to entry/mid web role. | **Medium** | Foreground functional web applications built; prompt via HITL for live portfolio and GitHub repository links. |
| **T11** | `cv_goncalo_doctor` | `job_doctor_junior` | Healthcare / Medicine | **Direct Clinical Match**: Physician with general internship applying to outpatient primary care. | **High** | Structure CV with clinical taxonomies (*Clinical Procedures, Life Support, Prescription*); do NOT demand GitHub URLs. |
| **T12** | `cv_ines_nurse` | `job_nurse_mid` | Healthcare / Nursing | **Specialization Gap**: Surgical ward staff nurse applying to Intensive Care Unit (ICU). | **Partial** | Foreground medication administration and general care; clarify via HITL regarding ALS or mechanical ventilator training. |
| **T13** | `cv_ines_nurse` | `job_doctor_junior` | Healthcare (Cross-Role) | **Professional Role Mismatch**: Registered Nurse applying for Physician opening. | **Incompatible** | **Critical Zero Hallucination**: Do NOT invent medical degree, physician license, or autonomous diagnostic authority. |
| **T14** | `cv_beatriz_lawyer` | `job_lawyer_junior` | Legal / Law | **Direct Legal Match**: Qualified lawyer with Bar license applying for Corporate & Commercial role. | **High** | Structure legal sections (*Practice Areas, Contractual Advisory, Bar License*); highlight procedural precision and legal English. |
| **T15** | `cv_tiago_marketing` | `job_marketing_specialist_mid` | Marketing / Business | **Direct Marketing Match**: Performance marketer applying for Paid Media & Growth role. | **High** | Emphasize Google/Meta certifications and real metrics (ROAS, CAC); clarify portfolio links through HITL. |
| **T16** | `cv_tiago_marketing` | `job_lawyer_junior` | Marketing vs Law | **Cross-Domain Mismatch**: Digital Marketer applying for Corporate Lawyer position. | **Incompatible** | **Zero Hallucination**: Flag absolute absence of legal degree and Bar association license; do not infer legal capability. |
| **T17** | `cv_goncalo_doctor` | `job_marketing_specialist_mid` | Medicine vs Marketing | **Cross-Domain Mismatch**: Medical Doctor applying for Paid Media Specialist. | **Incompatible** | Do NOT extrapolate digital marketing or paid acquisition skills from medical communications or general social media usage. |
| **T18** | `cv_beatriz_lawyer` | `job_backend_engineer_mid` | Law vs IT | **Cross-Domain Stress Test**: Lawyer applying for Backend Software Engineer. | **Incompatible** | **Zero Hallucination**: Identify total lack of programming languages, SQL, and Docker; produce honest gap report. |
| **T19** | `cv_diogo_backend` | `job_lawyer_junior` | IT vs Law | **Cross-Domain Stress Test**: Software Engineer applying for Corporate Lawyer. | **Incompatible** | **Zero Hallucination**: Identify total lack of legal education and absence of Bar qualification. |
| **T20** | `cv_goncalo_doctor` | `job_data_scientist_intern` | Medicine vs IT | **Classic Stress Test**: Medical Doctor applying for Data Scientist Intern. | **Incompatible** | May recognize general analytical aptitude, but **strictly forbidden to hallucinate** Python, pandas, or SQL competencies. |

---

## 2. Test Distribution & Verification Criteria

### Breakdown by Alignment Level
* **High Alignment (Direct Matches - 5 tests)**: T01, T04, T11, T14, T15
  * *Objective*: Verify optimal CV restructuring, domain-specific taxonomy generation, and truthful factual positioning.
* **Partial / Transition / Skills Gaps (8 tests)**: T02, T03, T05, T06, T07, T08, T09, T10, T12
  * *Objective*: Verify that `cv_optimizer` generates pertinent, targeted Human-in-the-Loop clarifying questions without assuming unstated facts.
* **Incompatible / Cross-Domain Stress Tests (7 tests)**: T13, T16, T17, T18, T19, T20
  * *Objective*: Stress-test the **Zero Hallucination** guardrail. The system must produce honest gap assessments without inventing credentials.
