from datetime import datetime
from pathlib import Path

from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

from models.cv import StructuredCV
from models.job import StructuredJob

from tools.cv_extraction import convert_cv_to_markdown
from tools.job_extraction import convert_job_to_markdown


LOG_DIR = Path("logs")
MAX_LOG_FILES = 10


@CrewBase
class CVMaxingCrew:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cv_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_parser"],
            tools=[convert_cv_to_markdown],
            llm="gemini/gemini-3.5-flash-lite",
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def job_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["job_parser"],
            tools=[convert_job_to_markdown],
            llm="gemini/gemini-3.5-flash-lite",
            verbose=True,
            allow_delegation=False,
        )

    @task
    def parse_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["parse_cv_task"],
            agent=self.cv_parser(),
            output_pydantic=StructuredCV,
        )

    @task
    def parse_job_task(self) -> Task:
        return Task(
            config=self.tasks_config["parse_job_task"],
            agent=self.job_parser(),
            output_pydantic=StructuredJob,
        )

    @crew
    def crew(self) -> Crew:
        LOG_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = LOG_DIR / f"execution_{timestamp}.txt"

        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            output_log_file=str(log_path),
        )

        self._cleanup_logs()

        return crew

    @staticmethod
    def _cleanup_logs():
        logs = sorted(
            LOG_DIR.glob("execution_*.txt"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

        for log in logs[MAX_LOG_FILES:]:
            log.unlink()