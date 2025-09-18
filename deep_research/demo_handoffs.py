"""
Simple demonstration of handoff capabilities in the deep research system.
This script shows how handoffs work without running the full research process.
"""

import asyncio
from agents import Runner
from handoff_agents import (
    human_review_agent, expert_consultation_agent, 
    quality_assurance_agent, approval_agent
)

async def demo_human_review_handoff():
    """Demonstrate human review handoff"""
    print("👤 HUMAN REVIEW HANDOFF DEMO")
    print("=" * 40)
    
    result = await Runner.run(
        human_review_agent,
        "I need human review for this research decision: Should I focus on recent developments "
        "or historical context for AI research? Options: [recent_only, historical_only, both_balanced]"
    )
    
    print(f"Human Review Result: {result.final_output}")
    print()

async def demo_expert_consultation_handoff():
    """Demonstrate expert consultation handoff"""
    print("🎓 EXPERT CONSULTATION HANDOFF DEMO")
    print("=" * 40)
    
    result = await Runner.run(
        expert_consultation_agent,
        "I need expert consultation for medical research. Domain: cardiology. "
        "Questions: ['What are the latest treatments for heart disease?', 'What are the side effects?']"
    )
    
    print(f"Expert Consultation Result: {result.final_output}")
    print()

async def demo_quality_check_handoff():
    """Demonstrate quality check handoff"""
    print("✅ QUALITY CHECK HANDOFF DEMO")
    print("=" * 40)
    
    sample_report = """
    # AI Research Report
    
    This report covers the latest developments in artificial intelligence.
    The field has seen significant progress in recent years.
    
    ## Key Findings
    - Machine learning algorithms have improved
    - Natural language processing is more accurate
    - Computer vision applications are expanding
    
    ## Conclusion
    AI continues to evolve rapidly.
    """
    
    result = await Runner.run(
        quality_assurance_agent,
        f"Please perform a quality check on this report:\n\n{sample_report}\n\n"
        f"Check for: completeness, accuracy, clarity, and proper formatting."
    )
    
    print(f"Quality Check Result: {result.final_output}")
    print()

async def demo_approval_handoff():
    """Demonstrate approval handoff"""
    print("📋 APPROVAL HANDOFF DEMO")
    print("=" * 40)
    
    result = await Runner.run(
        approval_agent,
        "Requesting approval to send research report via email. "
        "Report summary: 'AI trends analysis with 5 key findings'. "
        "Report length: 2000 characters. Recipients: research team."
    )
    
    print(f"Approval Result: {result.final_output}")
    print()

async def run_all_demos():
    """Run all handoff demonstrations"""
    print("🚀 HANDOFF CAPABILITIES DEMONSTRATION")
    print("=" * 50)
    print("This demonstrates the handoff capabilities available in the research system.\n")
    
    await demo_human_review_handoff()
    await demo_expert_consultation_handoff()
    await demo_quality_check_handoff()
    await demo_approval_handoff()
    
    print("✅ All handoff demos completed!")
    print("=" * 50)
    print("\nTo use these handoffs in your research:")
    print("1. Run: python enhanced_deep_research.py")
    print("2. Enable handoffs in the interface")
    print("3. Ask complex questions that trigger handoffs")

if __name__ == "__main__":
    asyncio.run(run_all_demos())
