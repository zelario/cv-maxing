from dotenv import load_dotenv

load_dotenv()

from crew import CVMaxingCrew


def run():
    result = (
        CVMaxingCrew()
        .crew()
        .kickoff(
            inputs={
                "cv": "data/curriculo.pdf",
                "job": "https://www.revolut.com/en-PT/careers/position/internship-programme-2027-data-scientist-and-analyst-36855ffa-f704-40be-bf77-a8b4deb360fa/",
            }
        )
    )

    print("\n===== STRUCTURED CV =====")
    print(result.tasks_output[0].pydantic)

    print("\n===== STRUCTURED JOB =====")
    print(result.tasks_output[1].pydantic)

    print("\n===== CV OPTIMIZATION =====")
    print(result.tasks_output[3].pydantic)


if __name__ == "__main__":
    run()
