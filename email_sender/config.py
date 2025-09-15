"""
Configuration module for the Email Sender application.
Centralizes all settings, environment variables, and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Email Configuration
EMAIL_CONFIG = {
    "from_email": "prashant@psagents.online",
    "to_email": "prashant.mhd@gmail.com",
    "sendgrid_api_key": os.environ.get('SENDGRID_API_KEY'),
    "test_subject": "Test email",
    "test_body": "This is an important test email"
}

# AI Model Configuration
AI_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": None,
    "max_tokens": None
}

# Company Information
COMPANY_INFO = {
    "name": "ComplAI",
    "description": "a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI"
}

# Agent Instructions
AGENT_INSTRUCTIONS = {
    "professional": f"You are a sales agent working for {COMPANY_INFO['name']}, {COMPANY_INFO['description']}. You write professional, serious cold emails.",
    
    "humorous": f"You are a humorous, engaging sales agent working for {COMPANY_INFO['name']}, {COMPANY_INFO['description']}. You write witty, engaging cold emails that are likely to get a response.",
    
    "concise": f"You are a busy sales agent working for {COMPANY_INFO['name']}, {COMPANY_INFO['description']}. You write concise, to the point cold emails.",
    
    "sales_picker": "You pick the best cold sales email from the given options. Imagine you are a customer and pick the one you are most likely to respond to. Do not give an explanation; reply with the selected email only.",
    
    "subject_writer": "You can write a subject for a cold sales email. You are given a message and you need to write a subject for an email that is likely to get a response.",
    
    "html_converter": "You can convert a text email body to an HTML email body. You are given a text email body which might have some markdown and you need to convert it to an HTML email body with simple, clear, compelling layout and design.",
    
    "email_manager": "You are an email formatter and sender. You receive the body of an email to be sent. You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. Finally, you use the send_html_email tool to send the email with the subject and HTML body.",
    
    "sales_manager": f"""
You are a Sales Manager at {COMPANY_INFO['name']}. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You can use the tools multiple times if you're not satisfied with the results from the first try.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
"""
}

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    if not EMAIL_CONFIG["sendgrid_api_key"]:
        raise ValueError("SENDGRID_API_KEY environment variable is required")
    
    if not EMAIL_CONFIG["from_email"] or not EMAIL_CONFIG["to_email"]:
        raise ValueError("Email addresses must be configured")
    
    print("✅ Configuration validated successfully")
    return True
