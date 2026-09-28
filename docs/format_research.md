# CV Format Research

## Research Objective

The goal of this research is to identify which CV format, structure and file conventions employers and recruiters prefer, and which formatting choices affect how a CV is read by both Applicant Tracking Systems (ATS) and human reviewers. The findings will be used to define the format framework for CV Maxing and the CV template.

The research covers recruiter and HR guidance, recruitment agencies, university career centres, ATS behaviour, eye-tracking and survey studies, and regional conventions for Portugal and Europe (Europass, GDPR, EU AI Act).

A key finding is that there is **no single universal CV format**. There is, however, a strong consensus on the core structure (reverse-chronological, single-column, clean and scannable), while file type, length, photo and language depend on the job, the employer and the country. The framework should therefore establish a safe default and define the conditions under which it changes. [1][2][3]

---

## 1. Section Order: Reverse-Chronological Structure

Reverse-chronological is the most consistently recommended structure. Several guides state that it is the most widely preferred by employers because it shows the most recent experience first and makes career progression easy to scan. [1][2] In Portugal, Randstad describes it as the standard format, with the most recent experience at the top, as recruiters expect. [2]

The hybrid format (skills block followed by a chronology) is presented as an option for senior roles and career changers. [1] The functional format (skills instead of a work history) is the most discouraged: sources report that both ATS systems and recruiters tend to distrust it, and a Portuguese guide notes that some recruiters suspect it hides something. [1][2]

The system should therefore apply:

```text
Default → Reverse-chronological

Career change / senior role → Hybrid (skills block + chronology)

Functional → Avoid, except for specific gaps and with explanation
```

Entry-level candidates are an exception to the order of sections, not to the structure: with little or no professional experience, Education can come before Experience. [4]

---

## 2. ATS-Parseable Content

The most important technical requirement is that the CV contains a real, readable text layer in a predictable order.

The main documented failure causes are:

* Scanned or image-only PDFs, which parse as blank. [9]
* Contact details placed in the document header or footer, which many parsers skip. [8][9]
* Job titles or date formats the parser does not recognise. [9]

The claim that ATS systems automatically reject CVs is heavily contested. Several sources state that most ATS filter, rank and store rather than reject, and that rejections usually trace back to knockout questions or searches configured by a recruiter. [9] A LinkedIn poll of recruiters (630 votes, so indicative only) found 83% saying their ATS does not reject candidates automatically. [9] An analysis of 20,000 CVs from a parsing tool reported that about 3% of tech CVs failed at the parsing stage. [9] In the EU, GDPR Article 22 already restricts decisions based solely on automated processing. [14]

---

## 3. Length

The one-page rule is no longer treated as universal. The evidence points to one page for early-career candidates and up to two pages for experienced ones.

* A survey by Criteria, reported by Fortune, found 53% of recruiters expect two pages, 43% still prefer one and 4% want more than two. [5]
* The ResumeGo study (482 recruiters, as summarised by ResuFit) reported that two-page CVs were preferred 2.3 times more often than one-page CVs, and that recruiters spent longer reading them. [6]
* A vendor survey reported that many HR professionals consider two pages ideal. [6]
* Pages three and beyond are the weakest choice in all sources found. [6]
* In Portugal, guides recommend one to two pages for most profiles, and two to three for executives and academics. [4][3]

The second page must earn its place: the first page has to make the case on its own, and the second should strengthen it with supporting evidence. [8]

---

## 4. Layout: One Column vs Two Columns

Sources disagree on whether two columns are a real risk.

* Vendor tests concluded that two-column CVs can lose little text during extraction, but single-column templates still tend to perform better. [9]
* Other sources describe multi-column layouts and tables as common parsing failure points, particularly in older systems. [9]
* The Ladders eye-tracking study listed multiple columns, long sentences and little white space among the traits of poorly performing CVs. [7]

Modern parsers handle two columns better than the old myth suggests, but a single column is never worse and is always safer when the destination system is unknown.

---

## 5. First-Page Scanability

Recruiters skim before they read. The best-known study (Ladders, 2018, eye-tracking with 30 recruiters) reported an average of 7.4 seconds on the initial screen, and that recruiters spent more time on job titles than on any other element. CVs that held attention had simple layouts, clear section headings and bold job titles. [7] This study is 8 years old, and the exact figure is contested, but the pattern is consistent across later sources. [7]

Documented scanning behaviour:

* The top third of page one is read first; the current job title, company and dates are the anchor. [7]
* The first bullet under the most recent role is disproportionately important. [7]
* A vague summary wastes the space; a one-line positioning statement is more effective than a long generic paragraph. [7]

Related: a recruiter survey cited by one guide reports that hiring professionals look at the skills section early. [7] Treat as indicative.

---

## 6. Achievement-Oriented Bullets

Content structure inside the format matters as much as the section order. University career centres recommend starting every bullet with an action verb, being specific about what you did, and quantifying results where possible. [11][12]

Both sources note that not every bullet needs a number, and that the contribution described should be the candidate's own, not the team's. [11][12] Quantified achievements are often considered important after relevant experience. [7] Treat as indicative.

Typical structure: 3–5 bullets for the most recent role, 2–3 for earlier roles.

---

## 7. Typography and Spacing

Font and spacing choices rarely cause rejection on their own, but they affect readability and, marginally, parsing.

* Calibri and Arial are the most consistently recommended fonts; Georgia and Times New Roman are accepted for traditional sectors. [10]
* Tests across ATS engines generally report strong parse completeness for standard sans-serif fonts. [10]
* Body text: 10–12 pt (10.5–11 pt is the most cited sweet spot). Headings: 14–16 pt. Name: 18–24 pt. [10]
* Margins: at least 0.5 inch, most sources suggest 0.75–1 inch. [10]
* Paper size: A4 outside the US. A wrong page size on PDF export can shift margins and break parsing. [10]

---

# Recommended Default Format

## Summary

```text
Structure:   Reverse-chronological, single column
Length:      1 page (< 5 years) / 2 pages (5+ years)
Font:        Calibri or Arial, 10.5–11 pt body, headings 14–16 pt
Margins:     ~2 cm, A4
Sections:    Summary → Experience → Education → Skills → Languages
             → Certifications → Projects (optional) → GDPR line
Contact:     In the body (not header/footer), with LinkedIn
Bullets:     Action verb + measurable result, 3–5 per recent role
File:        Text-based PDF by default; Word if requested
Photo:       Optional in Portugal; omit for international roles
Consistency: Titles and dates identical to LinkedIn
```

## CV Example

# [FIRST NAME LAST NAME]

**[Target job title or professional headline]** | [Main specialisation]

[+351 912 345 678] | [first.last@email.com] | [City, Country]
[linkedin.com/in/your-profile] | [portfolio or GitHub, if relevant]

---

## PROFESSIONAL SUMMARY

[2 to 3 lines: who you are (role + years of experience), your field or sector, 2 or 3 key skills aligned with the job, and one concrete result. E.g.: "Project manager with 8 years in B2B software, specialised in Agile and stakeholder management; delivered 15 projects with an average schedule variance below 5%."]

---

## PROFESSIONAL EXPERIENCE

**[Most recent job title]** — [Month YYYY] – Present
*[Company] · [Location] · [Sector or company size, if helpful]*

- [Action verb + measurable result + how: "Reduced delivery time by 30% by restructuring process X"]
- [Achievement relevant to the job, with numbers (%, €, deadlines, volume, team size)]
- [Achievement relevant to the job, with numbers]
- [Responsibility or key tool from the job posting, in the context of a result]

**[Previous job title]** — [Month YYYY] – [Month YYYY]
*[Company] · [Location]*

- [Action verb + measurable result]
- [Action verb + measurable result]
- [Action verb + measurable result]

<!-- Copy the "job title + company + bullets" block for each earlier role; the older the role, the shorter it should be (1 to 2 bullets). -->

---

## EDUCATION

**[Degree and programme, e.g.: MSc in Computer Science]** — [YYYY] – [YYYY]
*[Institution] · [Location] · [Final grade, if strong]*

**[Other relevant degree or training]** — [YYYY] – [YYYY]
*[Institution] · [Location]*

---

## SKILLS

**Technical:** [skill 1, skill 2, skill 3; use the exact terms from the job posting]
**Tools and software:** [e.g.: advanced Excel, SAP, Power BI, Jira, Figma]
**Methodologies:** [e.g.: Agile/Scrum, Lean, PMP]
**Transferable:** [only 2 or 3, and demonstrated in the experience above, not just stated]

---

## LANGUAGES

**Portuguese:** native
**English:** C1 (listening C1 · speaking B2 · writing B2) · [certification, if any]
**[Other language]:** [CEFR level from A1 to C2]

---

## CERTIFICATIONS AND ADDITIONAL TRAINING

- [Relevant certification] · [Issuing body] · [YYYY]
- [Relevant course or training] · [Provider] · [YYYY]

---

## PROJECTS, VOLUNTEERING AND OTHER (OPTIONAL)

[Only what strengthens the application. E.g.: personal project with link, volunteering, publications, awards.]

---

*I consent to the processing of my personal data for recruitment purposes, in accordance with the GDPR (Regulation (EU) 2016/679).*

---

# Sources

[1] Resume.io. **Top Resume Formats for 2026**
https://resume.io/blog/resume-formats

[2] Randstad Portugal. **Como Fazer um Currículo? 25 Dicas para um CV Atrativo**
https://www.randstad.pt/tendencias-360/procura-de-emprego/25-dicas-para-fazer-um-curriculo-atrativo-simples-e-objetivo/

[3] Grafton Portugal. **Como fazer um CV em Portugal: estrutura, tamanho e conteúdo**
https://pt.grafton.com/pt-pt/como-fazer-cv-portugal-estrutura-tamanho-conteudo

[4] Santander Portugal. **Como e onde fazer um currículo em Portugal**
https://www.santander.pt/salto/curriculo-portugal

[5] Fortune (report by Criteria). **Say goodbye to the 1-page résumé: most recruiters say 2 pages is the new normal**
https://www.fortune.com/2024/09/24/two-page-resume-new-normal-ai-job-seekers

[6] ResuFit. **Should a Resume Be One Page? What the Data Says** (summarises the ResumeGo study)
https://resufit.com/blog/mastering-the-one-page-cv-template-how-to-create-a-powerful-concise-resume/

[7] The Ladders. **Why do recruiters spend only 7.4 seconds on resumes?**
https://www.theladders.com/career-advice/why-do-recruiters-spend-only-7-4-seconds-on-resumes

[8] Jobscan. **Resume PDF vs Word**
https://www.jobscan.co/blog/resume-pdf-vs-word/

[9] Resumefast. **PDF vs Word: Which Resume Format Do ATS Prefer?**
https://www.resumefast.io/blog/ats-pdf-vs-word

[10] Resume Optimizer Pro. **Best Resume Fonts 2026: 12 Tested on 5 ATS Engines**
https://resumeoptimizerpro.com/blog/ats-friendly-resume-fonts-and-styles

[11] Columbia University Center for Career Education. **Resumes with Impact: Creating Strong Bullet Points**
https://careereducation.columbia.edu/resources/resumes-impact-creating-strong-bullet-points

[12] Yale Office of Career Strategy. **Writing Impactful Resume Bullets**
https://ocs.yale.edu/resources/writing-impactful-resume-bullets/

[13] Europass (European Union). **Create your Europass CV**
https://europass.europa.eu/en/create-europass-cv

[14] Fontvera. **EU AI Act for Recruitment and HR: Hiring AI Rules 2026**
https://fontvera.eu/intelligence/ai-act-recruitment-hr

