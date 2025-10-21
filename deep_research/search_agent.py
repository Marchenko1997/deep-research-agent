from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# создаём LLM вручную
llm = LLM(model="gpt-4o-mini")

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points succinctly, without unnecessary text."
)

# инструмент для поиска
search_tool = SerperDevTool()

search_agent = Agent(
    name="Search Agent",
    role="Web Researcher",
    goal="Find and summarize key information from the web based on search queries.",
    backstory=(
        "An expert internet researcher specialized in collecting reliable information "
        "from multiple sources quickly and summarizing it clearly and efficiently."
    ),
    instructions=INSTRUCTIONS,
    tools=[search_tool],
    llm=llm,
    verbose=True,
)
