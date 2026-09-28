from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "assets"
STYLE_DIR = BASE_DIR / "assets"


def generate_cv_pdf(cv_data, output_path):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("cv.html")

    html = template.render(
        **cv_data,
        css_path=STYLE_DIR / "cv.css",
    )

    HTML(
        string=html,
        base_url=str(BASE_DIR),
    ).write_pdf(output_path)

cv_data = {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+351 912 345 678",
    "location": "Coimbra, Portugal",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe",
    "summary": (
        "Computer Engineering student interested in artificial intelligence "
        "and data science."
    ),
    "experience": [
        {
            "position": "Data Science Intern",
            "company": "Example Company",
            "start_date": "2025",
            "end_date": "Present",
            "bullets": [
                "Developed machine learning models for customer segmentation.",
                "Improved data processing efficiency by 25%.",
                "Built data analysis pipelines using Python and SQL.",
            ],
        },
        {
            "position": "Software Engineering Intern",
            "company": "Another Company",
            "start_date": "2024",
            "end_date": "2025",
            "bullets": [
                "Developed REST APIs using Python.",
                "Implemented automated tests for backend services.",
            ],
        },
    ],
    "education": [
        {
            "degree": "BSc in Computer Engineering",
            "institution": "University of Coimbra",
            "start_date": "2023",
            "end_date": "2026",
        }
    ],
    "skills": [
        "Python",
        "SQL",
        "Machine Learning",
        "Git",
        "Docker",
    ],
}


if __name__ == "__main__":
    generate_cv_pdf(cv_data, "test_cv.pdf")
    print("CV generated successfully.")