"""
Basic tests for the Sales Agents with Guardrails system.

This module contains basic tests to verify the system functionality
and configuration validation.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

from src.app import SalesAgentApplication
from config import config


class TestConfiguration:
    """Test configuration validation and setup."""
    
    def test_config_validation(self):
        """Test that configuration validation works correctly."""
        # This test will pass if the config module loads without errors
        assert config is not None
        assert hasattr(config, 'validate_api_keys')
        assert hasattr(config, 'print_api_key_status')
    
    def test_api_key_validation(self):
        """Test API key validation functionality."""
        api_status = config.validate_api_keys()
        
        # Check that all expected keys are in the status
        expected_keys = ['openai', 'google', 'deepseek', 'groq', 'sendgrid']
        for key in expected_keys:
            assert key in api_status
            assert isinstance(api_status[key], bool)


class TestApplication:
    """Test the main application functionality."""
    
    def test_application_initialization(self):
        """Test that the application can be initialized."""
        # This test will pass if the application can be created without errors
        app = SalesAgentApplication()
        assert app is not None
        assert hasattr(app, 'sales_factory')
        assert hasattr(app, 'email_factory')
        assert hasattr(app, 'manager_factory')
    
    def test_application_validation(self):
        """Test application setup validation."""
        app = SalesAgentApplication()
        
        # Mock the API key validation to return True
        with patch.object(config, 'validate_api_keys', return_value={
            'openai': True,
            'sendgrid': True,
            'google': False,
            'deepseek': False,
            'groq': False
        }):
            result = app.validate_setup()
            assert result is True
    
    def test_application_validation_failure(self):
        """Test application validation failure scenarios."""
        app = SalesAgentApplication()
        
        # Mock the API key validation to return False for required keys
        with patch.object(config, 'validate_api_keys', return_value={
            'openai': False,  # Required key missing
            'sendgrid': True,
            'google': False,
            'deepseek': False,
            'groq': False
        }):
            result = app.validate_setup()
            assert result is False


class TestModels:
    """Test Pydantic models and validation."""
    
    def test_email_draft_validation(self):
        """Test EmailDraft model validation."""
        from src.models import EmailDraft
        
        # Test valid email draft
        valid_draft = EmailDraft(
            subject="Test Subject",
            body="This is a test email body that is long enough to pass validation."
        )
        assert valid_draft.subject == "Test Subject"
        assert valid_draft.body == "This is a test email body that is long enough to pass validation."
        
        # Test invalid email draft (too short body)
        with pytest.raises(ValueError, match="body too short"):
            EmailDraft(
                subject="Test Subject",
                body="Too short"
            )
    
    def test_subject_line_validation(self):
        """Test SubjectLine model validation."""
        from src.models import SubjectLine
        
        # Test valid subject line
        valid_subject = SubjectLine(subject="Valid Subject")
        assert valid_subject.subject == "Valid Subject"
        
        # Test invalid subject line (too long)
        with pytest.raises(ValueError, match="subject length out of bounds"):
            SubjectLine(subject="x" * 100)  # Too long


class TestGuardrails:
    """Test guardrail functionality."""
    
    def test_guardrail_imports(self):
        """Test that guardrails can be imported."""
        from src.guardrails import (
            guardrail_against_name,
            guardrail_against_pii,
            guardrail_against_risky_claims,
            guardrail_length,
            ALL_GUARDRAILS
        )
        
        assert guardrail_against_name is not None
        assert guardrail_against_pii is not None
        assert guardrail_against_risky_claims is not None
        assert guardrail_length is not None
        assert len(ALL_GUARDRAILS) == 4


class TestTools:
    """Test tool functionality."""
    
    def test_tools_import(self):
        """Test that tools can be imported."""
        from src.tools import send_html_email, build_email_to_send, sanitize_html_basic, all_links_https
        
        assert send_html_email is not None
        assert build_email_to_send is not None
        assert sanitize_html_basic is not None
        assert all_links_https is not None
    
    def test_html_sanitization(self):
        """Test HTML sanitization functionality."""
        from src.tools import sanitize_html_basic
        
        # Test script tag removal
        html_with_script = '<p>Hello</p><script>alert("bad")</script><p>World</p>'
        sanitized = sanitize_html_basic(html_with_script)
        assert '<script>' not in sanitized
        assert 'alert("bad")' not in sanitized
        assert '<p>Hello</p>' in sanitized
        assert '<p>World</p>' in sanitized
    
    def test_https_link_conversion(self):
        """Test HTTP to HTTPS link conversion."""
        from src.tools import sanitize_html_basic
        
        html_with_http = '<a href="http://example.com">Link</a>'
        sanitized = sanitize_html_basic(html_with_http)
        assert 'href="https://example.com"' in sanitized
        assert 'href="http://example.com"' not in sanitized


if __name__ == "__main__":
    pytest.main([__file__])
