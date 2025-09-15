"""
Pydantic models for data validation and structure in the Sales Agents application.

This module defines all the data models used throughout the application,
including email drafts, validation models, and output structures.
"""

from pydantic import BaseModel
from typing import Dict, List


class EmailDraft(BaseModel):
    """
    Model for email draft structure with validation.
    
    This model ensures that email drafts meet quality and safety requirements
    before being processed by the email system.
    """
    subject: str
    body: str

    @classmethod
    def _contains_banned_terms(cls, text: str) -> bool:
        """
        Check if text contains banned marketing terms.
        
        Args:
            text (str): Text to check for banned terms
            
        Returns:
            bool: True if banned terms are found, False otherwise
        """
        banned_terms = ["guarantee", "100%", "fully certified", "instant approval", "risk-free"]
        lowered = text.lower()
        return any(term in lowered for term in banned_terms)

    @classmethod
    def _looks_too_short(cls, text: str) -> bool:
        """
        Check if email body is too short to be meaningful.
        
        Args:
            text (str): Email body text to check
            
        Returns:
            bool: True if text is too short, False otherwise
        """
        return len(text.strip()) < 80

    @classmethod
    def _contains_placeholders_or_unsafe(cls, text: str) -> bool:
        """
        Check for placeholder content or potentially unsafe elements.
        
        Args:
            text (str): Text to check for unsafe content
            
        Returns:
            bool: True if unsafe content is found, False otherwise
        """
        return any(tok in text for tok in ["<script", "{{", "}}", "[placeholder]"])

    def model_post_init(self, __context):
        """
        Validate the email draft after initialization.
        
        Raises:
            ValueError: If validation fails for any reason
        """
        # Validate subject length
        if not (2 <= len(self.subject) <= 90):
            raise ValueError("subject length out of bounds")
            
        # Check for banned terms in subject
        if self._contains_banned_terms(self.subject):
            raise ValueError("subject contains banned terms")
            
        # Check email body length
        if self._looks_too_short(self.body):
            raise ValueError("body too short")
            
        # Check for unsafe content
        if self._contains_placeholders_or_unsafe(self.body):
            raise ValueError("body contains unsafe or placeholder content")


class SubjectLine(BaseModel):
    """
    Model for email subject line validation.
    
    Ensures subject lines meet length and content requirements.
    """
    subject: str

    def model_post_init(self, __context):
        """
        Validate the subject line after initialization.
        
        Raises:
            ValueError: If validation fails
        """
        text = (self.subject or "").strip()
        
        # Check length bounds
        if not (2 <= len(text) <= 90):
            raise ValueError("subject length out of bounds")
            
        # Check for banned terms
        lowered = text.lower()
        banned = ["re:", "fwd:", "100%", "guarantee"]
        if any(b in lowered for b in banned):
            raise ValueError("banned subject terms")


class HtmlEmailBody(BaseModel):
    """
    Model for HTML email body validation.
    
    Ensures HTML content is safe and follows security best practices.
    """
    html_body: str

    def model_post_init(self, __context):
        """
        Validate the HTML email body after initialization.
        
        Raises:
            ValueError: If validation fails
        """
        text = self.html_body or ""
        
        # Check for unencrypted links
        if "http://" in text:
            raise ValueError("unencrypted link present")
            
        # Check for potentially unsafe HTML
        if any(tok in text.lower() for tok in ["<script", "onload=", "onerror="]):
            raise ValueError("potentially unsafe html")


class EmailToSend(BaseModel):
    """
    Model for the final email payload before sending.
    
    This represents the validated and ready-to-send email structure.
    """
    subject: str
    html_body: str


class NameCheckOutput(BaseModel):
    """
    Model for name detection guardrail output.
    
    Used by the name detection guardrail to report findings.
    """
    is_name_in_message: bool
    name: str


class GuardrailResult(BaseModel):
    """
    Model for guardrail execution results.
    
    Standardizes the output format for all guardrail functions.
    """
    tripwire_triggered: bool
    output_info: Dict
    reason: str = ""


class EmailSendResult(BaseModel):
    """
    Model for email sending operation results.
    
    Provides structured feedback on email sending attempts.
    """
    status: str  # "success", "blocked", "error"
    reason: str = ""
    details: Dict = {}
