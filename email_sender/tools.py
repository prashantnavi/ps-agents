"""
Tools Module
Defines all function tools and agent-to-tool conversions used in the email sender application.
"""

from agents import function_tool
from typing import Dict
from email_service import send_plain_email, send_html_email
from agents import get_sales_agents, get_subject_writer, get_html_converter


@function_tool
def send_email(body: str) -> Dict[str, str]:
    """
    Send out an email with the given body to all sales prospects.
    
    Args:
        body (str): The email body content
        
    Returns:
        Dict[str, str]: Status response
    """
    return send_plain_email(body, "Sales email")


@function_tool
def send_html_email_tool(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send out an email with the given subject and HTML body to all sales prospects.
    
    Args:
        subject (str): Email subject line
        html_body (str): HTML formatted email body
        
    Returns:
        Dict[str, str]: Status response
    """
    return send_html_email(html_body, subject)


def create_sales_agent_tools():
    """
    Convert sales agents to tools.
    
    Returns:
        list: List of sales agent tools
    """
    sales_agents = get_sales_agents()
    description = "Write a cold sales email"
    
    tools = [
        agent.as_tool(
            tool_name=f"sales_agent{i+1}", 
            tool_description=description
        )
        for i, agent in enumerate(sales_agents)
    ]
    
    return tools


def create_email_tools():
    """
    Create email-related tools.
    
    Returns:
        list: List of email tools
    """
    subject_writer = get_subject_writer()
    html_converter = get_html_converter()
    
    subject_tool = subject_writer.as_tool(
        tool_name="subject_writer", 
        tool_description="Write a subject for a cold sales email"
    )
    
    html_tool = html_converter.as_tool(
        tool_name="html_converter",
        tool_description="Convert a text email body to an HTML email body"
    )
    
    return [subject_tool, html_tool, send_html_email_tool]


def create_all_tools():
    """
    Create all tools used in the application.
    
    Returns:
        dict: Dictionary containing all tool categories
    """
    sales_tools = create_sales_agent_tools()
    email_tools = create_email_tools()
    
    # Add send_email tool to sales tools
    sales_tools.append(send_email)
    
    return {
        "sales_tools": sales_tools,
        "email_tools": email_tools,
        "all_tools": sales_tools + email_tools
    }


# Global tool instances
tools = create_all_tools()

# Convenience accessors
def get_sales_tools():
    """Get sales agent tools."""
    return tools["sales_tools"]


def get_email_tools():
    """Get email-related tools."""
    return tools["email_tools"]


def get_all_tools():
    """Get all tools."""
    return tools["all_tools"]


def get_send_email_tool():
    """Get the send email tool."""
    return send_email


def get_send_html_email_tool():
    """Get the send HTML email tool."""
    return send_html_email_tool
