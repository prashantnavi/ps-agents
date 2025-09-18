"""
Example handoff scenarios for the deep research system.
This file demonstrates different ways to use handoffs in research workflows.
"""

import asyncio
from enhanced_research_manager import EnhancedResearchManager
from handoff_models import ResearchContext, HandoffType
from agents import Runner

class HandoffExamples:
    """Collection of example handoff scenarios"""
    
    def __init__(self):
        self.research_manager = EnhancedResearchManager(enable_handoffs=True)
    
    async def example_medical_research(self):
        """Example: Medical research requiring expert consultation"""
        print("🏥 MEDICAL RESEARCH EXAMPLE")
        print("=" * 50)
        
        query = "What are the latest medical treatments for Type 2 diabetes?"
        
        print(f"Research Query: {query}")
        print("This query will trigger expert consultation handoff due to medical domain...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")
    
    async def example_legal_research(self):
        """Example: Legal research requiring expert consultation"""
        print("\n⚖️ LEGAL RESEARCH EXAMPLE")
        print("=" * 50)
        
        query = "What are the legal implications of AI-generated content for copyright law?"
        
        print(f"Research Query: {query}")
        print("This query will trigger expert consultation handoff due to legal domain...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")
    
    async def example_complex_analysis(self):
        """Example: Complex analysis requiring human review"""
        print("\n🔍 COMPLEX ANALYSIS EXAMPLE")
        print("=" * 50)
        
        query = "Compare and analyze the effectiveness of different renewable energy strategies"
        
        print(f"Research Query: {query}")
        print("This query will trigger human review handoff due to complex analysis...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")
    
    async def example_technical_research(self):
        """Example: Technical research requiring expert consultation"""
        print("\n🔧 TECHNICAL RESEARCH EXAMPLE")
        print("=" * 50)
        
        query = "What are the engineering challenges in building quantum computers?"
        
        print(f"Research Query: {query}")
        print("This query will trigger expert consultation handoff due to technical domain...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")
    
    async def example_financial_research(self):
        """Example: Financial research requiring expert consultation"""
        print("\n💰 FINANCIAL RESEARCH EXAMPLE")
        print("=" * 50)
        
        query = "What are the financial implications of cryptocurrency regulation changes?"
        
        print(f"Research Query: {query}")
        print("This query will trigger expert consultation handoff due to financial domain...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")
    
    async def example_simple_research(self):
        """Example: Simple research without handoffs"""
        print("\n📚 SIMPLE RESEARCH EXAMPLE")
        print("=" * 50)
        
        query = "What are the benefits of reading books?"
        
        print(f"Research Query: {query}")
        print("This query will NOT trigger handoffs as it's a simple topic...")
        
        async for chunk in self.research_manager.run(query):
            print(f"📄 {chunk}")

async def run_all_examples():
    """Run all handoff examples"""
    examples = HandoffExamples()
    
    print("🚀 DEEP RESEARCH HANDOFF EXAMPLES")
    print("=" * 60)
    print("This demonstrates different handoff scenarios in the research system.")
    print("Each example shows how handoffs are triggered based on query content.\n")
    
    # Run examples
    await examples.example_medical_research()
    await examples.example_legal_research()
    await examples.example_complex_analysis()
    await examples.example_technical_research()
    await examples.example_financial_research()
    await examples.example_simple_research()
    
    print("\n✅ All examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_all_examples())
