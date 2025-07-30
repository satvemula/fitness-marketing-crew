from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

_ = load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)


class Content(BaseModel):
    content_type: str = Field(
        ...,
        description="The type of content to be created (e.g., blog post, social media post, video)",
    )
    topic: str = Field(..., description="The topic of the content")
    target_audience: str = Field(..., description="The target audience for the content")
    tags: List[str] = Field(..., description="Tags to be used for the content")
    content: str = Field(..., description="The content itself")


@CrewBase
class TheFitnessMarketingCrew:
    """
    The fitness marketing crew responsible for fitness content creation,
    strategy development, and campaign management.
    """

    agents_config = "marketing-crew/config/agents.yaml"
    tasks_config = "marketing-crew/config/tasks.yaml"

    @agent
    def fitness_trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["fitness_trend_researcher"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("marketing-crew/resources/saved_drafts"),
                FileWriterTool(),
                FileReadTool(),
            ],
            reasoning=True,
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_rpm=3,
        )

    @agent
    def fitness_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["fitness_content_creator"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("marketing-crew/resources/saved_drafts"),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iter=30,
            max_rpm=3,
        )

    @agent
    def social_media_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["social_media_strategist"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("marketing-crew/resources/saved_drafts"),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iter=10,
            max_rpm=3,
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["seo_specialist"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                DirectoryReadTool("marketing-crew/resources/saved_drafts/blogs"),
                FileWriterTool(),
                FileReadTool(),
            ],
            inject_date=True,
            llm=llm,
            allow_delegation=True,
            max_iter=5,
            max_rpm=3,
        )

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.fitness_trend_researcher(),
        )

    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_marketing_strategy"],
            agent=self.fitness_trend_researcher(),
        )

    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config["create_content_calendar"],
            agent=self.social_media_strategist(),
        )

    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_post_drafts"],
            agent=self.fitness_content_creator(),
            output_json=Content,
        )

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_scripts_for_reels"],
            agent=self.fitness_content_creator(),
            output_json=Content,
        )

    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config=self.tasks_config["content_research_for_blogs"],
            agent=self.fitness_content_creator(),
        )

    @task
    def draft_blogs(self) -> Task:
        return Task(
            config=self.tasks_config["draft_blogs"],
            agent=self.fitness_content_creator(),
            output_json=Content,
        )

    @task
    def seo_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["seo_optimization"],
            agent=self.seo_specialist(),
            output_json=Content,
        )

    @crew
    def fitness_marketing_crew(self) -> Crew:
        """Creates the Fitness Marketing Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=llm,
            max_rpm=3,
        )


if __name__ == "__main__":
    from datetime import datetime

    inputs = {
        "product_name": "Hybrid Athlete Training Program",
        "target_audience": "Hybrid athletes, fitness enthusiasts, gym-goers",
        "product_description": "A comprehensive training and nutrition plan designed for hybrid athletes to improve strength and endurance.",
        "budget": "$5,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    crew = TheFitnessMarketingCrew()
    crew.fitness_marketing_crew().kickoff(inputs=inputs)
    print("Fitness marketing crew has been successfully created and run.")
