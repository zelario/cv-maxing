import json
from pathlib import Path

from crewai.tools import tool


FRAMEWORK_PATH = Path("src/config/evaluation_framework.yaml")


@tool("calculate_deterministic_score")
def calculate_deterministic_score(
    structured_cv: str,
    structured_job: str,
) -> str:
    """
    Perform deterministic CV-job matching and scoring using the evaluation
    framework. This tool produces the reproducible baseline used by the
    Reviewer Agent.
    """

    import yaml

    cv = json.loads(structured_cv)
    job = json.loads(structured_job)

    with open(FRAMEWORK_PATH, "r", encoding="utf-8") as file:
        framework = yaml.safe_load(file)

    criteria = framework["criteria"]

    # ---------------------------------------------------------
    # 1. Extract job requirements
    # ---------------------------------------------------------

    required_skills = [
        skill["name"]
        for skill in job.get("skills", [])
        if skill.get("requirement_type") == "required"
    ]

    preferred_skills = [
        skill["name"]
        for skill in job.get("skills", [])
        if skill.get("requirement_type") == "preferred"
    ]

    cv_skills = {
        skill["name"].lower()
        for skill in cv.get("skills", [])
    }

    # Skills demonstrated through experience/projects
    demonstrated_skills = set()

    for experience in cv.get("experience", []):
        for skill in experience.get("skills_evidenced", []):
            demonstrated_skills.add(skill.lower())

    for project in cv.get("projects", []):
        for skill in project.get("skills_evidenced", []):
            demonstrated_skills.add(skill.lower())

        for technology in project.get("technologies", []):
            demonstrated_skills.add(technology.lower())

    # ---------------------------------------------------------
    # 2. Requirement matching
    # ---------------------------------------------------------

    matches = []

    for requirement in required_skills + preferred_skills:

        normalized = requirement.lower()

        if normalized in demonstrated_skills:
            status = "satisfied"
            score = 1.0

        elif normalized in cv_skills:
            status = "weak_evidence"
            score = 0.5

        else:
            status = "missing"
            score = 0.0

        matches.append(
            {
                "requirement": requirement,
                "status": status,
                "match_score": score,
            }
        )

    # ---------------------------------------------------------
    # 3. Criterion scores
    # ---------------------------------------------------------

    criterion_scores = []

    if required_skills:
        required_score = sum(
            item["match_score"]
            for item in matches
            if item["requirement"] in required_skills
        ) / len(required_skills)
    else:
        required_score = 1.0

    criterion_scores.append(
        {
            "criterion": "required_skills",
            "score": required_score * 100,
        }
    )

    # TODO:
    # Add experience, projects, achievements, education,
    # keywords and structure scoring.

    criterion_values = {
        "required_skills": required_score,
        "relevant_experience": 0.0,
        "demonstrated_skills": 0.0,
        "projects": 0.0,
        "achievements": 0.0,
        "education": 0.0,
        "keywords": 0.0,
        "cv_structure": 0.0,
    }

    # ---------------------------------------------------------
    # 4. Weighted deterministic score
    # ---------------------------------------------------------

    deterministic_score = sum(
        criterion_values[name] * criteria[name]["weight"]
        for name in criterion_values
    )

    result = {
        "deterministic_score": round(
            deterministic_score * 100,
            2
        ),
        "criterion_scores": criterion_scores,
        "requirement_matches": matches,
    }

    return json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )


@tool("save_structured_review")
def save_structured_review(structured_review: str) -> None:
    """
    Save a structured review as a formatted JSON file.
    """

    json_path = Path("data/structured_review_temp.json")

    data = json.loads(structured_review)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"[TOOL] Structured Review saved to {json_path}")