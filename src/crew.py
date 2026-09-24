import os
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("MODEL", "openrouter/free")

from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

from models.cv import StructuredCV
from models.job import StructuredJob
from models.review import ReviewerResult
from models.optimization import CVOptimizationResult

from tools.cv_extraction import convert_cv_to_markdown
from tools.job_extraction import convert_job_to_markdown
from tools.cv_evaluation import get_evaluation_framework
from tools.cv_optimization import (
    ask_user,
    save_optimized_cv_markdown,
)
from tools.json_storage import save_json


@CrewBase
class CVMaxingCrew:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def cv_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_parser"],
            tools=[convert_cv_to_markdown, save_json],
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def job_parser(self) -> Agent:
        return Agent(
            config=self.agents_config["job_parser"],
            tools=[convert_job_to_markdown, save_json],
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["reviewer"],
            tools=[get_evaluation_framework, save_json],
            llm=MODEL,
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def cv_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_optimizer"],
            tools=[
                ask_user,
                save_json,
                save_optimized_cv_markdown,
            ],
            llm=MODEL,
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
            agent=self.reviewer(),
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

    @crew
    def crew(self) -> Crew:

        crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

        return crew
