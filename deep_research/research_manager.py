import asyncio
from crewai import Crew
from deep_research.search_agent import search_agent
from deep_research.planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from deep_research.writer_agent import writer_agent, ReportData
from deep_research.email_agent import email_agent
from deep_research.evaluator import Evaluator, evaluator
from crewai import Crew, Task


class ResearchManager:
    async def run(self, query: str):
        print("=== Starting Deep Research ===")
        yield "Starting research..."

        search_plan = await self.plan_searches(query)
        yield "Searches planned, starting to search..."

        search_results = await self.perform_searches(search_plan)
        yield "Searches complete, evaluating..."

        evaluation = await self.evaluate(search_results)
        yield "Evaluation complete, writing report..."

        report = await self.write_report(query, search_results, evaluation)
        yield "Report written, sending email..."

        await self.send_email(report)
        yield "Email sent, research complete"

        yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        print("Planning searches...")

        task = Task(
            description=f"Query: {query}",
            agent=planner_agent,
            expected_output=WebSearchPlan,
        )

        crew = Crew(
        agents=[planner_agent],
        tasks=[task],
        verbose=True
        )

        result = crew.kickoff()

        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        print("Searching...")
        num_completed = 0

        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results: list[str] = []

        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")

        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            crew = Crew(agents=[search_agent], tasks=[input_text])
            result = crew.kickoff()
            return str(result.final_output)
        except Exception as e:
            print(f"Search error: {e}")
            return None

    async def evaluate(self, search_results: list[str]) -> Evaluator:
        print("Evaluating search results...")
        input_text = "Search results to evaluate:\n" + "\n\n".join(search_results)

        crew = Crew(agents=[evaluator], tasks=[input_text])
        result = crew.kickoff()

        print("Evaluation complete")
        return result.final_output_as(Evaluator)

    async def write_report(
        self, query: str, search_results: list[str], evaluation: Evaluator
    ) -> ReportData:
        print("Writing report...")

        input_text = (
            f"Original query: {query}\n"
            f"Summarized search results: {search_results}\n"
            f"Evaluation: {evaluation}"
        )

        crew = Crew(agents=[writer_agent], tasks=[input_text])
        result = crew.kickoff()

        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        print("Sending email...")
        crew = Crew(agents=[email_agent], tasks=[report.markdown_report])
        crew.kickoff()
        print("Email sent")
        return report
