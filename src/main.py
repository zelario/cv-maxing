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
                "job": "https://www.revolut.com/en-PT/careers/position/data-scientist-credit-5bfed8c7-9f9d-48e2-8e28-7ecf00ac17a8/",
            }
        )
    )

    save_pipeline_outputs(result)

if __name__ == "__main__":
    run()
