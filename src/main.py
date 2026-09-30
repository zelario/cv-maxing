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
                "job": "https://www.mckinsey.com/careers/search-jobs/jobs/summerbusinessanalystintern-techai-110176?appsource=LinkedIn",
            }
        )
    )

    save_pipeline_outputs(result)

if __name__ == "__main__":
    run()
