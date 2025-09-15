"""
Tool functions for the Sales Agents application.

This module contains all the function tools used by agents,
including email sending, HTML sanitization, and validation utilities.
"""

import re
import os
import sendgrid
from typing import Dict
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import function_tool
from config import config


def sanitize_html_basic(html_body: str) -> str:
    """
    Sanitize HTML content by removing potentially dangerous elements.
    
    This function:
    - Removes script tags and their content
    - Removes event handlers (onclick, onload, etc.)
    - Converts HTTP links to HTTPS for security
    
    Args:
        html_body (str): Raw HTML content to sanitize
        
    Returns:
        str: Sanitized HTML content
    """
    # Remove script tags and their content
    cleaned = re.sub(r"(?is)<script.*?>.*?</script>", "", html_body)
    
    # Remove event handlers
    cleaned = re.sub(r"\son\\w+=\"[^\"]*\"", "", cleaned)
    
    # Convert any HTTP links to HTTPS - multiple patterns
    cleaned = re.sub(r'href="http://', 'href="https://', cleaned)
    cleaned = re.sub(r"href='http://", "href='https://", cleaned)
    cleaned = re.sub(r'href=http://', 'href=https://', cleaned)
    
    # Also convert any standalone http:// URLs
    cleaned = re.sub(r'http://', 'https://', cleaned)
    
    return cleaned


def all_links_https(html_body: str) -> bool:
    """
    Check if all links in HTML content use HTTPS protocol.
    
    Args:
        html_body (str): HTML content to check
        
    Returns:
        bool: True if all links use HTTPS, False otherwise
    """
    # Check for various link patterns
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_body)
    
    # Also check for any remaining http:// patterns
    http_links = re.findall(r'http://[^\s<>"\']+', html_body)
    
    # Debug output for troubleshooting
    print(f"Found hrefs: {hrefs}")
    print(f"Found HTTP links: {http_links}")
    
    return len(http_links) == 0 and all(href.startswith("https://") for href in hrefs)


@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an HTML email with compliance and security validation.
    
    This function performs several validation checks before sending:
    1. Checks for required compliance elements (ComplAI, unsubscribe, support@)
    2. Validates that all links use HTTPS
    3. Sanitizes HTML content
    4. Sends the email via SendGrid
    
    Args:
        subject (str): Email subject line
        html_body (str): HTML email body content
        
    Returns:
        Dict[str, str]: Result status and details
        
    Raises:
        Exception: If email is blocked due to compliance or security issues
    """
    print(f"HTML body received: {html_body[:500]}...")  # Debug output
    
    # Initialize SendGrid client
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(config.FROM_EMAIL)
    to_email = To(config.TO_EMAIL)
    
    # Check for required compliance elements
    has_required = all(
        token.lower() in html_body.lower() 
        for token in config.REQUIRED_COMPLIANCE_ELEMENTS
    )
    if not has_required:
        raise Exception("Email blocked: missing required compliance text")
    
    # Check that all links use HTTPS
    if not all_links_https(html_body):
        raise Exception("Email blocked: non-HTTPS links detected")
    
    # Sanitize HTML content
    safe_html = sanitize_html_basic(html_body)
    print(f"Sanitized HTML: {safe_html[:500]}...")  # Debug output
    
    # Create and send email
    content = Content("text/html", safe_html)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    
    return {"status": "success"}


@function_tool
def build_email_to_send(subject: str, html_body: str) -> Dict[str, str]:
    """
    Validate and assemble the final email payload before sending.
    
    This function creates a validated EmailToSend object that can be
    safely passed to the send_html_email function.
    
    Args:
        subject (str): Email subject line
        html_body (str): HTML email body content
        
    Returns:
        Dict[str, str]: Validated email payload
    """
    from .models import EmailToSend
    
    # Create and validate the email payload
    payload = EmailToSend(subject=subject, html_body=html_body)
    return payload.model_dump()
