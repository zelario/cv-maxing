from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from crew import CVMaxingCrew
from utils.save_outputs import save_pipeline_outputs
from tools.cv_generation import render_cv
from utils.save_outputs import save_markdown

cv = Path("tests") / "cv.pdf"
job = """# Data Scientist Intern

**Revolut · London / Hybrid**

### About Revolut

Revolut is a technology-driven financial services company building products that help customers manage, spend, save, and invest their money. Our teams use data, experimentation, and technology to solve complex problems and improve customer experiences at scale.

### About the Role

We are looking for a **Data Scientist Intern** to join a cross-functional team working on data-driven products and customer experiences.

You will work closely with Data Scientists, Engineers, Product Managers, and other stakeholders to analyse large datasets, develop analytical solutions, run experiments, and turn data into actionable insights.

### What You'll Do

* Analyse large and complex datasets to identify trends, patterns, and opportunities.
* Build and evaluate statistical and machine learning models for business and product problems.
* Design and analyse experiments and A/B tests.
* Define and monitor relevant metrics to measure product performance.
* Translate analytical findings into clear recommendations for technical and non-technical stakeholders.
* Work with engineers and product teams to productionise data-driven solutions.
* Communicate results through clear visualisations, reports, and presentations.

### What We're Looking For

* Currently pursuing a Bachelor's or Master's degree in **Computer Science, Data Science, Mathematics, Statistics, Engineering, or a related quantitative field**.
* Strong foundation in **statistics, probability, and quantitative analysis**.
* Experience with **Python** and **SQL**.
* Familiarity with common data analysis and machine learning libraries such as **pandas, NumPy, scikit-learn, or similar tools**.
* Understanding of **machine learning fundamentals** and model evaluation.
* Ability to investigate ambiguous problems and break them down into structured analytical tasks.
* Strong analytical and problem-solving skills.
* Good communication skills and ability to work effectively in a team.
* Comfortable working in a fast-paced, international environment.

### Nice to Have

* Experience with experimentation, A/B testing, or causal inference.
* Experience working with large datasets or data pipelines.
* Knowledge of data visualisation tools or frameworks.
* Experience with cloud platforms or distributed data technologies.
* Personal, academic, research, or open-source projects demonstrating practical application of data science.

### What You'll Learn

During the internship, you will gain experience working on real-world data problems, collaborating with experienced Data Scientists and Engineers, designing experiments, developing machine learning solutions, and communicating data-driven decisions.

### Application

Please submit your CV and provide examples of projects, research, coursework, or other experience that demonstrate your interest and practical ability in data science.

**This is a synthetic job posting created for CV Maxing testing and evaluation purposes and is not an official Revolut job advertisement.**
"""


def run():
    result = (
        CVMaxingCrew()
        .crew()
        .kickoff(
            inputs={
                "cv": cv,
                "job": job
            }
        )
    )

    generated = save_pipeline_outputs(result)
    markdown = render_cv(generated)
    save_markdown(markdown)

if __name__ == "__main__":
    run()
