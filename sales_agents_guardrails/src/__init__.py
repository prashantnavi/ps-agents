"""
Sales Agents with Guardrails - Main Package

This package provides a comprehensive sales email automation system with
built-in guardrails for compliance, security, and content validation.

Main Components:
- models: Pydantic models for data validation
- tools: Function tools for email processing and validation
- guardrails: Input validation and protection mechanisms
- agents: AI agent configurations and factories
- app: Main application orchestration

Usage:
    from src.app import SalesAgentApplication
    
    app = SalesAgentApplication()
    await app.run_protected_workflow("Your message here")
"""

from .app import SalesAgentApplication
from .models import EmailDraft, SubjectLine, HtmlEmailBody, EmailToSend
from .tools import send_html_email, build_email_to_send
from .guardrails import ALL_GUARDRAILS

__version__ = "1.0.0"
__author__ = "Sales Agents Team"

__all__ = [
    'SalesAgentApplication',
    'EmailDraft',
    'SubjectLine', 
    'HtmlEmailBody',
    'EmailToSend',
    'send_html_email',
    'build_email_to_send',
    'ALL_GUARDRAILS'
]
