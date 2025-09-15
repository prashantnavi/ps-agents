"""
Email Service Module
Handles all email-related functionality including sending emails via SendGrid.
"""

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, MailSettings, Bcc, Cc, Header
from typing import Dict, Optional
from config import EMAIL_CONFIG


class EmailService:
    """Service class for handling email operations."""
    
    def __init__(self):
        """Initialize the email service with SendGrid client."""
        self.sg = sendgrid.SendGridAPIClient(api_key=EMAIL_CONFIG["sendgrid_api_key"])
        self.from_email = Email(EMAIL_CONFIG["from_email"])
        self.to_email = To(EMAIL_CONFIG["to_email"])
    
    def send_test_email(self) -> int:
        """
        Send a test email to verify email service is working.
        
        Returns:
            int: HTTP status code from SendGrid
        """
        try:
            content = Content("text/plain", EMAIL_CONFIG["test_body"])
            mail = Mail(self.from_email, self.to_email, EMAIL_CONFIG["test_subject"], content).get()
            response = self.sg.client.mail.send.post(request_body=mail)
            print(f"✅ Test email sent successfully. Status: {response.status_code}")
            return response.status_code
        except Exception as e:
            print(f"❌ Failed to send test email: {e}")
            raise
    
    def send_plain_email(self, body: str, subject: str = "Sales email") -> Dict[str, str]:
        """
        Send a plain text email.
        
        Args:
            body (str): Email body content
            subject (str): Email subject line
            
        Returns:
            Dict[str, str]: Status response
        """
        try:
            content = Content("text/plain", body)
            mail = Mail(self.from_email, self.to_email, subject, content).get()
            self.sg.client.mail.send.post(request_body=mail)
            print(f"✅ Plain email sent successfully: {subject}")
            return {"status": "success", "subject": subject}
        except Exception as e:
            print(f"❌ Failed to send plain email: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_html_email(self, html_body: str, subject: str, in_reply_to: Optional[str] = None, references: Optional[str] = None) -> Dict[str, str]:
        """
        Send an HTML formatted email.
        
        Args:
            html_body (str): HTML formatted email body
            subject (str): Email subject line
            
        Returns:
            Dict[str, str]: Status response
        """
        try:
            content = Content("text/html", html_body)
            mail_obj = Mail(self.from_email, self.to_email, subject, content)

            # Threading headers for replies
            if in_reply_to:
                mail_obj.add_header(Header("In-Reply-To", in_reply_to))
            if references:
                mail_obj.add_header(Header("References", references))

            mail = mail_obj.get()
            self.sg.client.mail.send.post(request_body=mail)
            print(f"✅ HTML email sent successfully: {subject}")
            return {"status": "success", "subject": subject}
        except Exception as e:
            print(f"❌ Failed to send HTML email: {e}")
            return {"status": "error", "message": str(e)}
    
    def send_email_with_attachments(self, body: str, subject: str, attachments: Optional[list] = None) -> Dict[str, str]:
        """
        Send an email with optional attachments.
        
        Args:
            body (str): Email body content
            subject (str): Email subject line
            attachments (list, optional): List of file paths to attach
            
        Returns:
            Dict[str, str]: Status response
        """
        try:
            content = Content("text/plain", body)
            mail = Mail(self.from_email, self.to_email, subject, content)
            
            # Add attachments if provided
            if attachments:
                for attachment_path in attachments:
                    # Implementation for attachments would go here
                    pass
            
            mail = mail.get()
            self.sg.client.mail.send.post(request_body=mail)
            print(f"✅ Email with attachments sent successfully: {subject}")
            return {"status": "success", "subject": subject}
        except Exception as e:
            print(f"❌ Failed to send email with attachments: {e}")
            return {"status": "error", "message": str(e)}


# Global email service instance
email_service = EmailService()


def send_test_email() -> int:
    """Convenience function to send a test email."""
    return email_service.send_test_email()


def send_plain_email(body: str, subject: str = "Sales email") -> Dict[str, str]:
    """Convenience function to send a plain text email."""
    return email_service.send_plain_email(body, subject)


def send_html_email(html_body: str, subject: str) -> Dict[str, str]:
    """Convenience function to send an HTML email."""
    return email_service.send_html_email(html_body, subject)
