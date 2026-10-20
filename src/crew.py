import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DEFAULT_MODEL = os.getenv("MODEL", "openrouter/free")
MODEL_CV_PARSER = os.getenv("MODEL_CV_PARSER") or DEFAULT_MODEL
MODEL_JOB_PARSER = os.getenv("MODEL_JOB_PARSER") or DEFAULT_MODEL
MODEL_CV_REVIEWER = os.getenv("MODEL_CV_REVIEWER") or DEFAULT_MODEL
MODEL_CV_OPTIMIZER = os.getenv("MODEL_CV_OPTIMIZER") or DEFAULT_MODEL
MODEL_CV_GENERATOR = os.getenv("MODEL_CV_GENERATOR") or DEFAULT_MODEL

from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

from models.cv import StructuredCV
from models.job import StructuredJob
from models.review import ReviewerResult
from models.optimization import CVOptimizationResult

from tools.cv_extraction import convert_cv_to_markdown
from tools.job_extraction import convert_job_to_markdown
from tools.cv_evaluation import get_evaluation_framework
from tools.cv_optimization import ask_user
from models.generated_cv import GeneratedCV


@CrewBase
class CVMaxingCrew:

    agents_config = str(Path(__file__).resolve().parent / "config" / "agents.yaml")
    tasks_config = str(Path(__file__).resolve().parent / "config" / "tasks.yaml")

    @agent
    def cv_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_parser"],
            tools=[convert_cv_to_markdown],
            llm=MODEL_CV_PARSER,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def job_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["job_parser"],
            tools=[convert_job_to_markdown],
            llm=MODEL_JOB_PARSER,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def cv_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_reviewer"],
            tools=[get_evaluation_framework],
            llm=MODEL_CV_REVIEWER,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def cv_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_optimizer"],
            tools=[ask_user],
            llm=MODEL_CV_OPTIMIZER,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def cv_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_generator"],
            llm=MODEL_CV_GENERATOR,
            verbose=True,
            allow_delegation=False,
        )

    @task
    def parse_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["parse_cv_task"],
            agent=self.cv_parser(),
            output_pydantic=StructuredCV,
            async_execution=True,
        )

    @task
    def parse_job_task(self) -> Task:
        return Task(
            config=self.tasks_config["parse_job_task"],
            agent=self.job_parser(),
            output_pydantic=StructuredJob,
            async_execution=True,
        )

    @task
    def review_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_cv_task"],
            agent=self.cv_reviewer(),
            context=[
                self.parse_cv_task(),
                self.parse_job_task(),
            ],
            output_pydantic=ReviewerResult,
        )

    @task
    def optimize_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_cv_task"],
            agent=self.cv_optimizer(),
            context=[
                self.parse_cv_task(),
                self.parse_job_task(),
                self.review_cv_task(),
            ],
            output_pydantic=CVOptimizationResult,
        )

    @task
    def generate_cv_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_cv_task"],
            agent=self.cv_generator(),
            context=[
                self.parse_cv_task(),
                self.parse_job_task(),
                self.optimize_cv_task(),
            ],
            output_pydantic=GeneratedCV,
        )

    @crew
    def crew(self) -> Crew:

        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

        return crew
