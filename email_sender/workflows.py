"""
Workflows Module
Handles all the different email generation and sending workflows.
"""

import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import get_sales_agents, get_sales_picker, Runner, trace
from tools import get_sales_tools, get_email_tools
from agents import AgentFactory


class EmailWorkflows:
    """Class containing all email generation and sending workflows."""
    
    @staticmethod
    async def test_email_service():
        """
        Test the email service functionality.
        
        Returns:
            int: HTTP status code
        """
        from email_service import send_test_email
        print("🧪 Testing email service...")
        return send_test_email()
    
    @staticmethod
    async def generate_single_email(agent_index: int = 0, message: str = "Write a cold sales email"):
        """
        Generate a single email using a specific sales agent.
        
        Args:
            agent_index (int): Index of the sales agent (0-2)
            message (str): Prompt for the agent
            
        Returns:
            str: Generated email content
        """
        sales_agents = get_sales_agents()
        if agent_index >= len(sales_agents):
            raise ValueError(f"Agent index {agent_index} out of range. Available: 0-{len(sales_agents)-1}")
        
        agent = sales_agents[agent_index]
        agent_name = agent.name
        
        print(f"📧 Generating email with {agent_name}...")
        
        result = await Runner.run(agent, message)
        return result.final_output
    
    @staticmethod
    async def generate_single_email_streamed(agent_index: int = 0, message: str = "Write a cold sales email"):
        """
        Generate a single email with streaming output.
        
        Args:
            agent_index (int): Index of the sales agent (0-2)
            message (str): Prompt for the agent
        """
        sales_agents = get_sales_agents()
        if agent_index >= len(sales_agents):
            raise ValueError(f"Agent index {agent_index} out of range. Available: 0-{len(sales_agents)-1}")
        
        agent = sales_agents[agent_index]
        agent_name = agent.name
        
        print(f"📧 Generating email with {agent_name} (streaming)...")
        
        result = Runner.run_streamed(agent, input=message)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        print()  # New line after streaming
    
    @staticmethod
    async def generate_parallel_emails(message: str = "Write a cold sales email"):
        """
        Generate emails from all three sales agents in parallel.
        
        Args:
            message (str): Prompt for all agents
            
        Returns:
            list: List of generated emails
        """
        sales_agents = get_sales_agents()
        
        print("🚀 Generating emails from all sales agents in parallel...")
        
        with trace("Parallel cold emails"):
            results = await asyncio.gather(
                *[Runner.run(agent, message) for agent in sales_agents]
            )
        
        outputs = [result.final_output for result in results]
        
        print(f"✅ Generated {len(outputs)} emails")
        return outputs
    
    @staticmethod
    async def select_best_email(message: str = "Write a cold sales email"):
        """
        Generate multiple emails and select the best one.
        
        Args:
            message (str): Prompt for all agents
            
        Returns:
            str: The best email selected by the sales picker
        """
        sales_agents = get_sales_agents()
        sales_picker = get_sales_picker()
        
        print("🎯 Generating emails and selecting the best one...")
        
        with trace("Selection from sales people"):
            # Generate emails from all agents
            results = await asyncio.gather(
                *[Runner.run(agent, message) for agent in sales_agents]
            )
            outputs = [result.final_output for result in results]
            
            # Combine emails for selection
            emails = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(outputs)
            
            # Select the best email
            best = await Runner.run(sales_picker, emails)
            
            print(f"✅ Best email selected by {sales_picker.name}")
            return best.final_output
    
    @staticmethod
    async def automated_sales_workflow(message: str = "Send a cold sales email addressed to 'Dear CEO'"):
        """
        Complete automated sales workflow with email sending.
        
        Args:
            message (str): Initial prompt for the sales manager
            
        Returns:
            str: Result of the workflow
        """
        print("🤖 Starting automated sales workflow...")
        
        # Create tools and agents
        sales_tools = get_sales_tools()
        email_tools = get_email_tools()
        
        # Create email manager agent
        factory = AgentFactory()
        email_manager = factory.create_email_manager(email_tools)
        
        # Create sales manager with tools and handoffs
        sales_manager = factory.create_sales_manager(
            tools=sales_tools,
            handoffs=[email_manager]
        )
        
        with trace("Automated SDR"):
            result = await Runner.run(sales_manager, message)
            
        print("✅ Automated sales workflow completed")
        return result.final_output
    
    @staticmethod
    async def simple_sales_workflow(message: str = "Send a cold sales email addressed to 'Dear CEO'"):
        """
        Simple sales workflow without handoffs.
        
        Args:
            message (str): Initial prompt for the sales manager
            
        Returns:
            str: Result of the workflow
        """
        print("📧 Starting simple sales workflow...")
        
        # Create tools
        sales_tools = get_sales_tools()
        
        # Create sales manager with tools only
        factory = AgentFactory()
        sales_manager = factory.create_sales_manager(tools=sales_tools)
        
        with trace("Sales manager"):
            result = await Runner.run(sales_manager, message)
            
        print("✅ Simple sales workflow completed")
        return result.final_output


# Convenience functions
async def test_email():
    """Test the email service."""
    return await EmailWorkflows.test_email_service()


async def generate_email(agent_index: int = 0):
    """Generate a single email."""
    return await EmailWorkflows.generate_single_email(agent_index)


async def generate_email_streamed(agent_index: int = 0):
    """Generate a single email with streaming."""
    return await EmailWorkflows.generate_single_email_streamed(agent_index)


async def generate_emails_parallel():
    """Generate emails from all agents in parallel."""
    return await EmailWorkflows.generate_parallel_emails()


async def select_best():
    """Generate emails and select the best one."""
    return await EmailWorkflows.select_best_email()


async def run_automated_workflow():
    """Run the complete automated sales workflow."""
    return await EmailWorkflows.automated_sales_workflow()


async def run_simple_workflow():
    """Run the simple sales workflow."""
    return await EmailWorkflows.simple_sales_workflow()
