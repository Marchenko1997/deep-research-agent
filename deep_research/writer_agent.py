from pydantic import BaseModel, Field
from crewai import Agent

INSTRUCTIONS = (
    "You are a senior research writer tasked with creating a cohesive and insightful report "
    "for a research query. You will receive the original query along with summarized research "
    "from other agents. Begin by outlining the report structure, then generate a detailed "
    "markdown-formatted document. The report must be factual, well-organized, and comprehensive, "
    "covering all relevant findings in 5–10 pages (at least 1000 words)."
)


class ReportData(BaseModel):
    short_summary: str = Field(
        description="A short 2–3 sentence summary of the findings."
    )
    markdown_report: str = Field(
        description="The final, full research report in markdown format."
    )
    follow_up_questions: list[str] = Field(
        description="Suggested topics for further investigation."
    )


writer_agent = Agent(
    name="WriterAgent",
    role="Research Report Writer",
    goal="Compose a detailed, accurate, and structured markdown report summarizing all research findings.",
    backstory=(
        "An experienced AI research writer known for crafting in-depth, data-driven analyses "
        "with clear logic and professional tone. Expert in summarizing complex information "
        "into accessible and insightful documents."
    ),
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
