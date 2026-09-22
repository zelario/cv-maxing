# Lab Project Description
## HCAI 2026/2027

Luís Macedo

## 1 Introduction

The Human-Centered Artificial Intelligence (HCAI) course comprises: (i) a theoretical-practical component, evaluated in a written exam, and (ii) a practical work, consisting of the development of a Lab Project on one or more topics covered by the course. This document describes the latter, which will be carried out in two stages: Project Proposal, and Design and Development.

## 2 Project Proposal

The deliverable of the first stage is a written document where the project to be developed is proposed. The document should have **no more than 3 pages in a 2-column format**[^1], and should be written either in English or Portuguese.

The project must tackle a problem involving human-centered AI systems that prioritize trustworthy, pro-active cooperation with humans while respecting their values, control, and promoting their condition. As aforementioned, it should be related to, at least, one topic covered in HCAI (see the syllabus of the course in the official site). This relation must be made explicit, either in the title of the project or in its documentation.

The project proposal must be well-supported, by contextualizing and reviewing approaches to the problem with appropriate bibliographic references, while answering the following questions:

- **Problem and Motivation:** What is the problem? Why is it interesting? Why is it important?
- **Background:** What scientific literature provides context and background on the problem?
- **Goals:** What is the project's aim? What would be considered a successful work? What are the expected contributions?
- **Approach:** What method(s) or algorithm(s) will be proposed? If there are existing implementations, are they going to be used? What is the plan to improve or modify such implementations? An exact answer is not necessary at this stage, but there should be a general sense of how the problem is going to be tackled.
- **Materials (including Data):** What data is going to be used? If new data is required, how is it going to be collected? Which frameworks and tools are going to be used for this?
- **Evaluation:** How are the results going to be evaluated? If qualitatively, what kind of results are expected (e.g., plots or figures)? If quantitatively, what type of analysis will be adopted for evaluating and/or comparing the results achieved (e.g., performance metrics or statistical tests)?

As long as their use is well-supported, any computational tools and data sources may be employed.

## 3 Design and Development

The proposed project will be developed throughout the semester and in the PL classes. Students are expected to perform several experiments, produce a piece of software, and write a scientific paper describing the outcomes of the project.

### 3.1 Paper

The paper should be written in English, and have at most 15 pages in a 2-column format[^2], excluding the pages needed for bibliographic references.

The following structure is suggested (see more details in Section 5):

1. Introduction (including motivation, problem description, goal and approach; may reuse part of the Project Proposal);
2. Related Work (may include part of the Project Proposal);
3. Data & Approach (an overview of the data used and of the approach adopted for tackling the problem);
4. Experimentation (setup, quantitative and/or qualitative evaluation, and their discussion);
5. Conclusions (stressing the main achievements and main difficulties faced, and a reflection on the relation between the work to HCAI topics) and Future Work (what could still be done);
6. Bibliographic References.

### 3.2 Submission Instructions

The software developed must be made available on GitHub (alternatives are accepted if previously required). The final submission must include a PDF file, the paper, containing somewhere the URL of the repository where the software is available. This document must be submitted through Inforestudante.

### 3.3 Evaluation

Overall, the project is worth **60% of the final grade** of the HCAI course (12/20), split into the following:

- Project Proposal;
- Project (including paper, software, defence).

Evaluation will consider the following criteria:

- Relevance of the topic.
- Significance of the contributions.
- Novelty/Originality of the problem and approaches.
- Quality/Technical Soundness of the performed experiments, developed software, claims and conclusions.
- Clarity of the paper and of running instructions.

## 4 Important dates

### 4.1 Deadline

The project has the following deadlines, with results to be submitted to the course area in Inforestudante:

- Project Proposal: 9th October, 2026
- Final Project: 27nd, November, 2026

Oral defences are scheduled to the classes of the subsequent weeks after submission.

### 4.2 Stages

Although there are only two mandatory, immutable deadlines (one for the proposal and another for the final software and report), you are advised to consider intermediate stages in the development of the project. You can submit them in the course communication platforms defined for that (informally, to Discord; formally, to Inforestudante). The following list includes suggested dates that are reasonable and balanced so that success is achieved. However, you may change them as you like, with the exception of the last one.

The stages of the project implementation:

- 1 - Submission of the project proposal -> October, 9th; (suggested)
- 2 - Introduction and Related Work (including the State of the Art) -> October, 20th; (suggested)
- 3 - Mastering of the tool(s) (possible submission of a tutorial) –> October, 20th; (suggested)
- 4 - Submission of the prototype of the AI system –> November, 10th; (suggested)
- 5 - Submission of the final version of the AI system –> November, 21st; (suggested)
- 6 - Final submission (AI system+paper+supplements) –> November, 27; 

For the final submission consider the following. Recently, conferences and journals are requiring supplements to the papers that include information about reproducibility (e.g., NIPS, ICML). A superbly written paper provides enough information for the expert reader to reproduce its results. So, the ideal submission consists of extremely careful and detailed descriptions of the experiments, their parameters, and is accompanied by a master script (at least a readme file) that:

1. installs all systems needed
2. generates or fetches all needed input data,
3. reruns all experiments and generates all results,
4. generates all graphs, plots, and tables, and finally,
5. recompiles the sources of the paper.

Notebooks from Jupyter or Google Colab allow addressing almost all those aspects, with exception of item 5. So, especially for those that used Jupyter for coding, I recommend the inclusion of notebook files (e.g., .ipynb) in their submission. For item 5, include the Word or the Latex files. This will be convenient to give you feedback in case the paper is selected to be submitted to a conference.

## 5 On Writing the Paper/Report

Here are some guidelines for writing the final paper/report. Although not rigid, you may structure your paper into the following parts or in equivalent ones (not necessarily in the same number):

1 - Introduction
2 - Related Work
3 - Materials (Data sets, tools, frameworks, etc.)
4 - Methods (including experimental setup and procedure)
5 - Results
6 - Discussion
7 - Conclusions

or

1 - Introduction
2 - Related Work
3 - Materials (Data sets, tools, frameworks, etc.)
4 - Methods
5 - Experiments
6 - Results
7 - Discussion
8 - Conclusions

More details about what this parts are described in the following subsections.

### 5.1 Introduction

Please keep in mind that, when you write a report/paper, if the reader is not excited by the introduction, paper is lost.

The function of the Introduction is to:

- Establish the context of the work being reported. This is accomplished by discussing the relevant primary research literature (with citations) and summarizing our current understanding of the problem you are investigating;
- State the purpose of the work in the form of the hypothesis, question, or problem you investigated; and, briefly explain your rationale and approach and, whenever possible, the possible outcomes your study can reveal.

The Introduction must answer the questions, "What was I studying? Why was it an important question? What did we know about it before I did this study? How will this study advance the state of the art?"

A recipe for the structure of successful introductions:

- **paragraph 1:** motivation: broadly, what is problem area, why important? Establish the context, background and/or importance of the topic. Establish the context by providing a brief and balanced review of the pertinent published literature that is available on the subject.
- **paragraph 2:** Narrow down: what is the problem you specifically consider? (this paragraph might be included in paragraph 1)
- **paragraph 3:** Explain how others solved it. Indicate a problem, controversy or gap of knowledge in those approaches/solutions proposed by others.
- **paragraph 4:** Explain shortly how you are going to solve it. This is the most crucial paragraph. Tell your elevator pitch, i.e., a summary that is short enough to give during an elevator ride: "In the paper, we...", "The purpose of this study was to..." or "We investigated three possible mechanisms to explain the ..."
- **paragraph 5:** how different/better/relates to other work. Provide a clear statement of the rationale for your approach to the problem studied. For example: State briefly how you approached the problem. Why did you choose this kind of experiment or experimental design? What are the scientific merits of this particular model system? What advantages does it confer in answering the particular question(s) you are posing? Do not discuss here the details. If you are using a novel (new, revolutionary, never used before) technique or methodology, the merits of the new technique/method versus the previously used methods should be presented here. (this paragraph might be included in the previous paragraph)
- **paragraph 6:** Provide an overview of the structure of the paper: "The remainder of this paper is structured as follows..."

### 5.2 Related Work

Discuss published work that relates to your project. How is your approach similar or different from others? It is of utmost importance that a submitted paper/report situates the work with respect to the current state of the art. Papers that are closely related to the presented work should be cited, discussed, and compared to the presented work. Although a superficial part of the related work is included in the Introduction, here you go deeper, with more details, more discussion, more comparison, etc.

### 5.3 Materials

Describe the data you are working with for your project. What type of data is it? Where did it come from? How much data are you working with? Did you have to do any preprocessing, or other special treatment to use this data in your project? Mention the tools that you use for implementing the project.

### 5.4 Methods

In the section Methods of a research article, you should give an account of how you carried out your research. The Methods should be clear and detailed enough for another experienced person to repeat the research and reproduce the results. As all of you implemented someway a system, this usually involves a description of:

- how you implemented it
- how you tested it (experimental setup and experimental methods).

This usually comprise two sections, the first titled, for instance, with the name of the system, and the second titled Experimental Setup or simply Experiments (in this case including a subsection with Experimental Setup).

A different/alternative scenario, and probably more common in AI, considers the subsection devoted to the experiments as a main section. In this case, the section Methods is confined to describe your approach for solving the problem that you set up in the introduction, while the section Experiments is devoted for describing the experiments that you performed to demonstrate that your approach solves the problem. The exact experiments will vary depending on the project, but you might compare your approach with previously published methods, perform an ablation study to determine the impact of various components of your system, experiment with different hyperparameters or architectural choices, use visualization techniques to gain insight into how your model works, discuss common failure modes of your model, etc. You should include graphs, tables, or other figures to illustrate your experimental results. Note that this is still methodology, in this case, experimental methodology.

### 5.5 Results

Results should be clear and concise. The standard approach to this section is to merely present the results, without elaborate discussion or comment. This does not mean that you do not need any text to describe data presented in tables and figures. You may comment on the significant data presented in the tables and figures. This often takes the form of the location or summary statement, which identifies the table or figure and indicates its content. This is normally followed by a statement or statements which point out and describe the relevant or significant data. All your tables/figs should be numbered and given a title.

More elaborate commentary on the results is normally restricted to the Discussion section. In research articles, however, authors may comment extensively on their results as they are presented, and it is not uncommon for the Results section to be combined with the Discussion section under the heading: Results and Discussion

However, it is also possible that Results be the second of the two subsections of section Experiments, the first being Experimental Setup.

### 5.6 Discussion

This should explore the significance of the results of the work, not repeat them. A combined Results and Discussion section is sometimes appropriate.

### 5.7 Conclusions

The main conclusions of the study may be presented in a short Conclusions section, which may stand alone or form a subsection of a Discussion section, or of a Results and Discussion section. Conclusions are shorter sections of academic texts which usually serve two functions. The first is to summarise and bring together the main areas covered in the writing, which might be called "looking back"; and the second is to give a final comment or judgement on this. The final comment may also include making suggestions for improvement and speculating on future directions. Conclusions tend to include sections on significance of the findings and recommendations for future work. It is therefore valuable to honestly identify the limitations of your work and possible directions to solve this limitations.

## A Suggested Topics

All the topics of course. Extra topics can be used, but at least one topic of the course should be involved.

[^1]: Formatted according to the IJCAI guidelines, https://www.ijcai.org/authors_kit
[^2]: Formatted according to the IJCAI guidelines, https://www.ijcai.org/authors_kit