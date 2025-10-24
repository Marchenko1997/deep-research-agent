import asyncio
from crewai import Crew, Task
from deep_research.search_agent import search_agent
from deep_research.planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from deep_research.writer_agent import writer_agent, ReportData
from deep_research.email_agent import email_agent
from deep_research.evaluator import Evaluator, evaluator


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
            description=f"Plan search steps for query: {query}",
            agent=planner_agent,
            expected_output="WebSearchPlan", 
        )

        crew = Crew(
            agents=[planner_agent],
            tasks=[task],
            verbose=True,
        )

        result = crew.kickoff()
        print("Planning complete ✅")

       
        return result.final_output_as(WebSearchPlan)


    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        print("Starting searches...")
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]

        results: list[str] = []
        for i, task in enumerate(asyncio.as_completed(tasks), 1):
            try:
                result = await task
                if result:
                    results.append(result)
                print(f"Searching... {i}/{len(tasks)} done")
            except Exception as e:
                print(f"Search failed: {e}")

        print("All searches completed ✅")
        return results

   
    async def search(self, item: WebSearchItem) -> str | None:
        input_text = f"Search term: {item.query}\nReason: {item.reason}"

        try:
            task = Task(
                description=input_text,
                agent=search_agent,
                expected_output="String",
            )

            crew = Crew(agents=[search_agent], tasks=[task])
            result = crew.kickoff()

            return str(result.final_output)
        except Exception as e:
            print(f"Search error: {e}")
            return None


    async def evaluate(self, search_results: list[str]) -> Evaluator:
        print("Evaluating search results...")

        input_text = "Evaluate the following search results:\n" + "\n\n".join(
            search_results
        )

        task = Task(
            description=input_text,
            agent=evaluator,
            expected_output="Evaluator",
        )

        crew = Crew(agents=[evaluator], tasks=[task])
        result = crew.kickoff()

        print("Evaluation complete ✅")
        return result.final_output_as(Evaluator)


    async def write_report(
        self, query: str, search_results: list[str], evaluation: Evaluator
    ) -> ReportData:
        print("Writing report...")

        input_text = (
            f"Original query: {query}\n\n"
            f"Summarized search results:\n{search_results}\n\n"
            f"Evaluation:\n{evaluation}"
        )

        task = Task(
            description=input_text,
            agent=writer_agent,
            expected_output="ReportData",
        )

        crew = Crew(agents=[writer_agent], tasks=[task])
        result = crew.kickoff()

        print("Report ready ✅")
        return result.final_output_as(ReportData)

   
    async def send_email(self, report: ReportData) -> None:
        print("Sending email...")

        task = Task(
            description=report.markdown_report,
            agent=email_agent,
            expected_output="String",
        )

        crew = Crew(agents=[email_agent], tasks=[task])
        crew.kickoff()

        print("Email sent ✅")
