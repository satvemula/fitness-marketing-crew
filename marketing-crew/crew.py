import os
import sys
from typing import List
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Verify keys exist before starting
if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPER_API_KEY"):
    print("❌ Error: API keys not found. Please set GOOGLE_API_KEY and SERPER_API_KEY in your .env file.")
    sys.exit(1)

# Initialize LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7
)

class Content(BaseModel):
    content_type: str = Field(..., description="Type of content (blog, social post, video)")
    topic: str = Field(..., description="The main topic")
    target_audience: str = Field(..., description="Target audience segment")
    tags: List[str] = Field(..., description="Relevant tags/keywords")
    content: str = Field(..., description="The actual content body")

@CrewBase
class TheFitnessMarketingCrew:
    """The fitness marketing crew responsible for content creation and strategy."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def fitness_trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["fitness_trend_researcher"],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), FileWriterTool()],
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def fitness_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["fitness_content_creator"],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), FileWriterTool()],
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def social_media_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["social_media_strategist"],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), FileWriterTool()],
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["seo_specialist"],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), FileWriterTool()],
            verbose=True,
            llm=gemini_llm
        )

    @task
    def market_research(self) -> Task:
        return Task(config=self.tasks_config["market_research"])

    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(config=self.tasks_config["prepare_marketing_strategy"])

    @task
    def create_content_calendar(self) -> Task:
        return Task(config=self.tasks_config["create_content_calendar"])

    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_post_drafts"],
            output_pydantic=Content # Using Pydantic for structured output
        )

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_scripts_for_reels"],
            output_pydantic=Content
        )

    @task
    def content_research_for_blogs(self) -> Task:
        return Task(config=self.tasks_config["content_research_for_blogs"])

    @task
    def draft_blogs(self) -> Task:
        return Task(
            config=self.tasks_config["draft_blogs"],
            output_pydantic=Content
        )

    @task
    def seo_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["seo_optimization"],
            output_pydantic=Content
        )

    @crew
    def fitness_marketing_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True,
            planning_llm=gemini_llm
        )

def run():
    """Run the crew."""
    inputs = {
        "product_name": "Hybrid Athlete Training Program",
        "target_audience": "Hybrid athletes, fitness enthusiasts, gym-goers",
        "product_description": "A comprehensive training and nutrition plan designed for hybrid athletes to improve strength and endurance.",
        "budget": "$5,000",
        "current_date": "2025-08-07", # Updated year
    }
    
    print("## Starting Fitness Marketing Crew")
    print("-----------------------------------")
    TheFitnessMarketingCrew().fitness_marketing_crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()