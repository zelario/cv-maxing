from dotenv import load_dotenv

load_dotenv()

from crew import CVMaxingCrew


def run():
    result = CVMaxingCrew().crew().kickoff(
        inputs={
            "cv": "data/cv.pdf",
            "job": "https://jobs.deloitte.pt/job/Lisboa-Consultant-Senior-Artificial-Intelligence-&-Data/1325292655/?utm_source=LINKEDIN&utm_medium=referrer",
        }
    )

    print("\n===== STRUCTURED CV =====")
    print(result.tasks_output[0].pydantic)

    print("\n===== STRUCTURED JOB =====")
    print(result.tasks_output[1].pydantic)


if __name__ == "__main__":
    run()