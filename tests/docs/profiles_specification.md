# Test Profiles Specification: CVs (PDF) & Ground-Truth Context (Simulator)

This document defines the **8 candidate profiles** used in the evaluation and validation suite for the CV Maxing system.
Each candidate profile consists of two distinct components:
1. **Visible CV Content (PDF)**: The concise, explicitly documented information present in the candidate's PDF submitted to the pipeline.
2. **Extra Context (Simulator Ground Truth)**: Factual career history, background details omitted from the summary CV, verified profile URLs, and strict factual boundaries regarding what the candidate does and does not know. This ground truth is used by the `CandidateSimulator` LLM to answer clarification questions (*Human-in-the-Loop*) truthfully, enforcing the core **Zero Hallucination** requirement.

---

## 1. Technology Profiles (IT)

### Profile 1: `cv_it_junior` (Graduate / Data & Software Focus)
* **Summary Profile**: Computer Science graduate seeking an entry-level opportunity in data science or software engineering.
* **Visible on CV (PDF)**:
  * **Name**: Tomás Silva
  * **Education**: B.Sc. in Computer Science (University of Coimbra, 2021–2024). Grade: 15/20.
  * **Experience**: Curricular Summer Internship (3 months) focused on software testing and internal tool support.
  * **Key Projects**: Capstone project in Python analyzing customer churn and retention using Pandas, Scikit-Learn, and SQL (PostgreSQL).
  * **Listed Skills**: Python, SQL, Git, Pandas, NumPy, Unit Testing.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/tomassilva-dev`), GitHub (`github.com/tomassilva-data`).
  * **True Additional Facts**: Regularly used Linux (Ubuntu) during coursework; built basic Dockerfiles for class assignments (knows Docker fundamentals but has no production deployment experience); C1 English proficiency.
  * **Negative Constraints / Factual Boundaries**: Has NO cloud experience (AWS/GCP), NO frontend framework expertise (React/Angular), and NO hands-on experience with Kubernetes, Kafka, or distributed pipelines. Must respond "I do not have experience with that" if prompted.

---

### Profile 2: `cv_it_backend` (Mid-Level Backend Software Engineer)
* **Summary Profile**: Software engineer with 3 years of professional experience building RESTful APIs, microservices, and managing relational databases.
* **Visible on CV (PDF)**:
  * **Name**: Diogo Santos
  * **Education**: B.Sc. in Informatics and Computing Engineering (FEUP, 2017–2020).
  * **Experience**: 
    * *Backend Software Engineer* (2021–Present, 3 years) at CloudScale: Developing RESTful APIs in Python (FastAPI/Django), PostgreSQL schema design and query optimization, Docker containerization, and RabbitMQ message broker integration.
  * **Listed Skills**: Python, FastAPI, Django, PostgreSQL, Redis, Docker, RabbitMQ, Git, Linux.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/diogosantos-backend`), GitHub (`github.com/dsantos-code`).
  * **True Additional Facts**: Familiar with AWS basics (worked with S3 storage and EC2 instances); configured basic CI/CD pipelines via GitHub Actions; fluent English speaker collaborating with distributed international teams.
  * **Negative Constraints / Factual Boundaries**: Does NOT know React or modern frontend development (only rudimentary HTML/CSS); has NO experience with Terraform, Kubernetes, or advanced cloud architecture; holds NO formal cloud certifications.

---

### Profile 3: `cv_it_frontend` (Frontend Web Developer)
* **Summary Profile**: Web developer with 2 years of experience specializing in responsive interfaces, design systems, and client-side performance.
* **Visible on CV (PDF)**:
  * **Name**: Mariana Costa
  * **Education**: B.Sc. in Design and Multimedia (2018–2021).
  * **Experience**:
    * *Frontend Developer* (2022–Present, 2 years) at PixelWave: Building single-page web applications using React and TypeScript; implementing component design systems with Tailwind CSS; integrating REST APIs.
  * **Listed Skills**: JavaScript, TypeScript, React, Next.js, HTML5, CSS3/Tailwind, Git, Figma, Redux Toolkit.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/marianacosta-frontend`), GitHub (`github.com/marianacosta-ui`), Online Portfolio (`marianacosta.dev`).
  * **True Additional Facts**: Experienced with frontend testing (Jest, React Testing Library); familiar with GraphQL queries; daily cross-functional collaboration with UX/UI designers.
  * **Negative Constraints / Factual Boundaries**: Does NOT build backend services (cannot write production servers in Python, Java, or Go; only basic Node.js tooling scripts); has NO relational database design experience; NO Docker or server-side DevOps experience.

---

### Profile 4: `cv_it_transition` (Career Transition: Civil Engineering to Software)
* **Summary Profile**: Former Civil Engineer who completed an intensive 9-month fullstack software bootcamp and built a verified portfolio of working applications.
* **Visible on CV (PDF)**:
  * **Name**: Pedro Oliveira
  * **Education**: Integrated Master's (M.Sc.) in Civil Engineering (2013–2018); Fullstack Web Development Bootcamp (9 months, 2023).
  * **Experience**:
    * *Civil Project Engineer* (2018–2022, 4 years): Structural calculations, site coordination, and project timeline/budget management.
    * *Freelance Web Developer / Personal Projects* (2023–Present): Built 3 complete web applications utilizing Python/Flask and JavaScript.
  * **Listed Skills**: Python, JavaScript, Flask, SQLite, HTML/CSS, Git, Project Management, Analytical Problem Solving.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/pedro-oliveira-dev`), GitHub (`github.com/poliveira-projects`).
  * **True Additional Facts**: Strong mathematical and structural modeling foundation from civil engineering; learned Python autonomously to automate engineering spreadsheets prior to formal career change; professional B2 English proficiency.
  * **Negative Constraints / Factual Boundaries**: Does NOT have a formal Computer Science degree; has NO senior experience in distributed systems architecture; has never led a software engineering team.

---

## 2. Non-IT Profiles (Domain-Specific)

### Profile 5: `cv_doctor` (General Medical Practitioner / Resident)
* **Summary Profile**: Medical doctor with completed general internship, experienced in outpatient consultations, emergency department triage, and inpatient rotations.
* **Visible on CV (PDF)**:
  * **Name**: Dr. Gonçalo Ferreira
  * **Education**: Integrated Master's in Medicine (Faculty of Medicine, University of Porto, 2016–2022).
  * **Professional Registration**: Medical Association License No. 68421.
  * **Experience**:
    * *General Practice Medical Resident* (2023–2024, São João University Hospital): Clinical rotations across Internal Medicine, General Surgery, Pediatrics, and Adult Emergency Care; primary triage and basic emergency intervention.
  * **Listed Skills**: Clinical Patient Assessment, Basic Life Support (BLS), Pharmacological Prescription, Electronic Health Records, Doctor-Patient Communication.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/dr-goncalo-ferreira`). Has NO GitHub, code repository, or technical portfolio.
  * **True Additional Facts**: Certified in Advanced Life Support (ALS) in 2023; co-authored a published clinical poster on arterial hypertension; fluent medical English.
  * **Negative Constraints / Factual Boundaries**: Has NOT completed a specialized medical residency (is a licensed general physician); **possesses ZERO programming, computer science, or data science knowledge** (if questioned on Python, SQL, or machine learning, must unequivocally answer "I have no education or experience in programming or computer science").

---

### Profile 6: `cv_nurse` (Registered General Care Nurse)
* **Summary Profile**: Registered Nurse with 3 years of hospital ward experience in post-operative surgical and internal medicine care.
* **Visible on CV (PDF)**:
  * **Name**: Inês Martins
  * **Education**: B.Sc. in Nursing (Coimbra Nursing School, 2017–2021).
  * **Professional Registration**: Nursing Council License No. 94312.
  * **Experience**:
    * *General Care Staff Nurse* (2021–Present, CHUC University Hospital): Direct patient care in surgical ward, medication preparation and administration (IV/IM/Oral), wound dressing and wound care management, vital signs monitoring, patient admission/discharge records.
  * **Listed Skills**: Surgical Patient Care, Medication Administration, Catheterization, Infection Prevention & Control, Basic Life Support, Multidisciplinary Teamwork.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/inesmartins-enf`).
  * **True Additional Facts**: Completed certified continuing education in Prevention & Management of Complex Wounds and Pressure Ulcers (2022); available for rotating shifts.
  * **Negative Constraints / Factual Boundaries**: Does NOT hold an advanced specialist nursing title; **has NO Intensive Care Unit (ICU) experience** and NO specialized training in invasive mechanical ventilation; is NOT a doctor and does not prescribe medicine; zero IT knowledge beyond hospital record systems.

---

### Profile 7: `cv_lawyer` (Junior Associate Lawyer / Corporate & Contract Law)
* **Summary Profile**: Qualified legal practitioner admitted to the Bar, focusing on commercial contract drafting, corporate advisory, and litigation assistance.
* **Visible on CV (PDF)**:
  * **Name**: Dra. Beatriz Matos
  * **Education**: Master's in Forensic Law and Arbitration (University of Lisbon School of Law, 2019–2021); LL.B. / Bachelor of Laws (2015–2019).
  * **Professional Registration**: Admitted to the Bar Association, License No. 54192L.
  * **Experience**:
    * *Junior Associate Lawyer* (2021–Present, Matos & Associados Law Firm): Drafting and revising commercial agreements, corporate governance (incorporations, board resolutions, articles of association), preparing court pleadings, doctrinal and jurisprudential legal research.
  * **Listed Skills**: Commercial & Corporate Law, Contract Drafting, Civil Litigation, Case Law Research, Negotiation & Mediation, Legal Database Systems.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/beatrizmatos-adv`).
  * **True Additional Facts**: Fluent in Legal English (certified by TOLES - Test of Legal English Skills); attended certified training on the EU General Data Protection Regulation (GDPR).
  * **Negative Constraints / Factual Boundaries**: Does NOT specialize in complex tax/customs law; possesses NO technical programming or software engineering competencies (if confronted with software development requirements, clarifies that expertise is exclusively legal).

---

### Profile 8: `cv_marketing` (Digital Marketing & Paid Media Specialist)
* **Summary Profile**: Marketing specialist with 3 years of professional experience managing paid traffic acquisition campaigns, conversion funnels, and performance analytics.
* **Visible on CV (PDF)**:
  * **Name**: Tiago Ribeiro
  * **Education**: B.Sc. in Communication Sciences and Marketing (University of Minho, 2018–2021).
  * **Experience**:
    * *Digital Marketing Specialist* (2021–Present, Impulso Digital Agency): Managing paid advertising campaigns on Meta Ads and Google Ads focusing on B2B lead generation; on-page SEO optimization; building conversion funnel performance reports in Google Analytics 4.
  * **Listed Skills**: Google Ads, Meta Ads (Facebook/Instagram), Search Engine Optimization (SEO), Google Analytics 4, Copywriting, Email Marketing, Conversion Funnel Optimization.
* **Simulator Ground Truth (Extra Context)**:
  * **Verified URLs**: LinkedIn (`linkedin.com/in/tiagoribeiro-mkt`), Campaign Portfolio (`tiagoribeiro.com`).
  * **True Additional Facts**: Active Google certifications (Google Search Ads, Google Analytics Certification); manages monthly paid ad spend budgets up to €15,000; professional English fluency.
  * **Negative Constraints / Factual Boundaries**: Has NO education in law or medicine; is NOT a programmer or data scientist (does not write Python or JavaScript; only handles basic tracking code insertion via Google Tag Manager); must not invent exaggerated campaign metrics beyond recorded facts.
