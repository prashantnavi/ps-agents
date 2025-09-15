"""
Main application module for the Sales Agents with Guardrails system.

This module orchestrates the entire sales email automation workflow,
including agent creation, tool setup, and execution management.
"""

import asyncio
from agents import Runner, trace
from .agents import SalesAgentFactory, EmailAgentFactory, SalesManagerFactory
from config import config


class SalesAgentApplication:
    """
    Main application class for the Sales Agents system.
    
    This class manages the entire workflow from agent creation to execution,
    providing a clean interface for running the sales email automation.
    """
    
    def __init__(self):
        """Initialize the application with all necessary components."""
        self.sales_factory = SalesAgentFactory()
        self.email_factory = EmailAgentFactory()
        self.manager_factory = SalesManagerFactory()
        
        # Initialize agents and tools
        self._setup_agents()
        self._setup_tools()
    
    def _setup_agents(self):
        """Set up all agents used in the application."""
        # Create sales agents
        self.sales_agent1, self.sales_agent2, self.sales_agent3 = self.sales_factory.create_sales_agents()
        
        # Create email management agents
        self.subject_writer = self.email_factory.create_subject_writer()
        self.html_converter = self.email_factory.create_html_converter()
        self.email_manager = self.email_factory.create_email_manager(
            self.subject_writer.as_tool("subject_writer", "Write a subject for a cold sales email"),
            self.html_converter.as_tool("html_converter", "Convert a text email body to an HTML email body")
        )
        
        # Create sales managers
        self.sales_manager = self.manager_factory.create_sales_manager(
            self.sales_tools, self.email_manager
        )
        self.protected_sales_manager = self.manager_factory.create_protected_sales_manager(
            self.sales_tools, self.email_manager
        )
    
    def _setup_tools(self):
        """Set up all tools used by the sales agents."""
        description = "Write a cold sales email"
        
        self.sales_tools = [
            self.sales_agent1.as_tool("sales_agent1", description),
            self.sales_agent2.as_tool("sales_agent2", description),
            self.sales_agent3.as_tool("sales_agent3", description)
        ]
    
    async def run_basic_workflow(self, message: str):
        """
        Run the basic sales workflow without guardrails.
        
        Args:
            message (str): The user message to process
        """
        with trace("Automated SDR"):
            await Runner.run(self.sales_manager, message, max_turns=config.MAX_TURNS)
    
    async def run_protected_workflow(self, message: str):
        """
        Run the protected sales workflow with input guardrails.
        
        Args:
            message (str): The user message to process
        """
        with trace("Protected Automated SDR"):
            await Runner.run(self.protected_sales_manager, message, max_turns=config.MAX_TURNS)
    
    async def run_comparison_workflow(self, message: str):
        """
        Run both workflows for comparison purposes.
        
        Args:
            message (str): The user message to process
        """
        print("Running basic workflow...")
        await self.run_basic_workflow(message)
        
        print("\nRunning protected workflow...")
        await self.run_protected_workflow(message)
    
    def validate_setup(self) -> bool:
        """
        Validate that the application is properly configured.
        
        Returns:
            bool: True if setup is valid, False otherwise
        """
        api_status = config.validate_api_keys()
        
        # Check critical API keys
        if not api_status["openai"]:
            print("ERROR: OpenAI API key is required")
            return False
        
        if not api_status["sendgrid"]:
            print("ERROR: SendGrid API key is required for email sending")
            return False
        
        # Print status of optional keys
        config.print_api_key_status()
        
        return True


async def main():
    """
    Main entry point for the application.
    
    This function demonstrates the usage of the Sales Agent system
    with different message types and workflow configurations.
    """
    # Initialize the application
    app = SalesAgentApplication()
    
    # Validate setup
    if not app.validate_setup():
        print("Application setup validation failed. Please check your configuration.")
        return
    
    # Test messages (designed to not trigger guardrails)
    test_messages = [
        "Send out a cold sales email addressed to Dear CEO from our sales team",
        "Send out a cold sales email addressed to Dear CEO from our business development team"
    ]
    
    # Run workflows
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*50}")
        print(f"Running test {i}: {message}")
        print(f"{'='*50}")
        
        try:
            await app.run_protected_workflow(message)
        except Exception as e:
            print(f"Workflow failed with error: {e}")
        
        print(f"\nTest {i} completed.")


if __name__ == "__main__":
    asyncio.run(main())
