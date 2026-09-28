from dotenv import load_dotenv

load_dotenv()

from crew import CVMaxingCrew
from utils.save_outputs import save_pipeline_outputs


def run():
    result = (
        CVMaxingCrew()
        .crew()
        .kickoff(
            inputs={
                "cv": "tests/cv.pdf",
                "job": "https://www.revolut.com/en-PT/careers/position/internship-programme-2027-data-scientist-and-analyst-36855ffa-f704-40be-bf77-a8b4deb360fa/",
            }
        )
    )

    save_pipeline_outputs(result)

if __name__ == "__main__":
    run()
