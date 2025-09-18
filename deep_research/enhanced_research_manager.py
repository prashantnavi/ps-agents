from agents import Runner, trace, gen_trace_id, handoff
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from handoff_agents import (
    human_review_agent, expert_consultation_agent, 
    quality_assurance_agent, approval_agent
)
from handoff_models import (
    ResearchContext, HumanReviewRequest, ExpertConsultationRequest,
    AdditionalResearchRequest, QualityCheckRequest, ApprovalRequest
)
import asyncio
from typing import Optional, List

class EnhancedResearchManager:
    """Enhanced research manager with handoff capabilities"""

    def __init__(self, enable_handoffs: bool = True):
        self.enable_handoffs = enable_handoffs

    async def run(self, query: str):
        """Run the enhanced deep research process with handoffs"""
        trace_id = gen_trace_id()
        with trace("Enhanced Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            # Create research context
            context = ResearchContext(
                original_query=query,
                current_stage="initialization",
                metadata={"trace_id": trace_id}
            )
            
            print("Starting enhanced research...")
            yield "Starting enhanced research..."
            
            # Stage 1: Planning with potential handoff
            search_plan = await self.plan_searches_with_handoff(query, context)
            yield "Searches planned, starting to search..."
            
            # Stage 2: Searching with potential handoff
            search_results = await self.perform_searches_with_handoff(search_plan, context)
            yield "Searches complete, writing report..."
            
            # Stage 3: Writing with quality check handoff
            report = await self.write_report_with_handoff(query, search_results, context)
            yield "Report written, performing quality check..."
            
            # Stage 4: Quality check handoff
            if self.enable_handoffs:
                quality_result = await self.perform_quality_check_handoff(report, context)
                if not quality_result.get("approved", True):
                    yield "Quality issues found, revising report..."
                    report = await self.revise_report(report, quality_result, context)
            
            # Stage 5: Email with approval handoff
            if self.enable_handoffs:
                approval_result = await self.request_email_approval_handoff(report, context)
                if approval_result.get("approved", True):
                    yield "Approval received, sending email..."
                    await self.send_email(report)
                    yield "Email sent, research complete"
                else:
                    yield "Email not approved, research complete without email"
            else:
                yield "Sending email..."
                await self.send_email(report)
                yield "Email sent, research complete"
            
            yield report.markdown_report

    async def plan_searches_with_handoff(self, query: str, context: ResearchContext) -> WebSearchPlan:
        """Plan searches with potential expert consultation handoff"""
        print("Planning searches...")
        
        # Check if expert consultation is needed
        if self.enable_handoffs and self._needs_expert_consultation(query):
            print("Requesting expert consultation for search planning...")
            expert_result = await Runner.run(
                expert_consultation_agent,
                f"Query: {query}\nContext: {context.current_stage}\n"
                f"I need help planning search terms for this research query. "
                f"What search terms would be most effective for finding comprehensive information?"
            )
            print(f"Expert consultation completed: {expert_result.final_output}")
        
        # Proceed with normal planning
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches_with_handoff(self, search_plan: WebSearchPlan, context: ResearchContext) -> List[str]:
        """Perform searches with potential human review handoff"""
        print("Searching...")
        
        # Request approval for searches if needed
        if self.enable_handoffs and len(search_plan.searches) > 5:
            approval_result = await Runner.run(
                approval_agent,
                f"Requesting approval to perform {len(search_plan.searches)} searches. "
                f"Search terms: {[s.query for s in search_plan.searches]}"
            )
            print(f"Search approval: {approval_result.final_output}")
        
        # Perform searches
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        
        print("Finished searching")
        return results

    async def write_report_with_handoff(self, query: str, search_results: List[str], context: ResearchContext) -> ReportData:
        """Write report with potential human review handoff"""
        print("Thinking about report...")
        
        # Check if human review is needed for complex topics
        if self.enable_handoffs and self._needs_human_review(query):
            print("Requesting human review for report structure...")
            review_result = await Runner.run(
                human_review_agent,
                f"Query: {query}\nSearch results available: {len(search_results)}\n"
                f"Should I proceed with writing a comprehensive report? Options: [proceed, request_more_research, focus_specific_aspect]"
            )
            print(f"Human review result: {review_result.final_output}")
        
        # Write the report
        input_text = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input_text,
        )
        
        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def perform_quality_check_handoff(self, report: ReportData, context: ResearchContext) -> dict:
        """Perform quality check with handoff"""
        print("Performing quality check...")
        
        quality_result = await Runner.run(
            quality_assurance_agent,
            f"Please perform a quality check on this report:\n\n"
            f"Summary: {report.short_summary}\n\n"
            f"Report: {report.markdown_report[:1000]}...\n\n"
            f"Check for: completeness, accuracy, clarity, and proper formatting."
        )
        
        print(f"Quality check completed: {quality_result.final_output}")
        return quality_result.final_output

    async def request_email_approval_handoff(self, report: ReportData, context: ResearchContext) -> dict:
        """Request approval to send email"""
        print("Requesting email approval...")
        
        approval_result = await Runner.run(
            approval_agent,
            f"Requesting approval to send research report via email.\n"
            f"Report summary: {report.short_summary}\n"
            f"Report length: {len(report.markdown_report)} characters\n"
            f"Recipients: configured email addresses"
        )
        
        print(f"Email approval: {approval_result.final_output}")
        return approval_result.final_output

    async def revise_report(self, report: ReportData, quality_result: dict, context: ResearchContext) -> ReportData:
        """Revise report based on quality check feedback"""
        print("Revising report based on quality feedback...")
        
        # In a real implementation, this would use the quality feedback to improve the report
        # For now, we'll just return the original report
        return report

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a search for the query"""
        input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input_text,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def send_email(self, report: ReportData) -> None:
        """Send email with the report"""
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report

    def _needs_expert_consultation(self, query: str) -> bool:
        """Determine if expert consultation is needed"""
        expert_keywords = ["medical", "legal", "financial", "technical", "scientific", "engineering"]
        return any(keyword in query.lower() for keyword in expert_keywords)

    def _needs_human_review(self, query: str) -> bool:
        """Determine if human review is needed"""
        complex_keywords = ["analysis", "comparison", "evaluation", "assessment", "strategy"]
        return any(keyword in query.lower() for keyword in complex_keywords)
