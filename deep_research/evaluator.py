from crewai import Agent
from pydantic import BaseModel, Field


INSTRUCTIONS = (
    "You are an evaluation agent that assesses the quality of research results. "
    "You should evaluate whether the search results are comprehensive, relevant, and sufficient "
    "to answer the research query. Consider factors like: "
    "- Relevance to the original query "
    "- Breadth and depth of information "
    "- Quality and reliability of sources "
    "- Completeness of coverage. "
    "Provide a clear and structured assessment with reasoning."
)



class Evaluator(BaseModel):
    is_good: bool = Field(
        description="Whether the search results are good enough to proceed with report writing"
    )
    reason: str = Field(
        description="Detailed reasoning for the evaluation, including strengths and weaknesses"
    )



evaluator = Agent(
    role="Research Evaluator",
    goal="Evaluate the quality, depth, and reliability of AI research results",  
    backstory=(
        "You are a meticulous and objective evaluator with a background in research methodology. "
        "Your job is to assess whether the collected research data is comprehensive, unbiased, and relevant "
        "before it is passed on to the report writing phase."
    ),
    name="Evaluator",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Evaluator,
)
