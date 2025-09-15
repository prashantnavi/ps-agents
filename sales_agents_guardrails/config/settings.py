"""
Configuration settings for the Sales Agents with Guardrails application.

This module contains all configuration settings, environment variable handling,
and validation for the sales email automation system.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


class Config:
    """Configuration class for the Sales Agents application."""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    GOOGLE_API_KEY: Optional[str] = os.getenv('GOOGLE_API_KEY')
    DEEPSEEK_API_KEY: Optional[str] = os.getenv('DEEPSEEK_API_KEY')
    GROQ_API_KEY: Optional[str] = os.getenv('GROQ_API_KEY')
    SENDGRID_API_KEY: Optional[str] = os.getenv('SENDGRID_API_KEY')
    
    # Email Configuration
    FROM_EMAIL: str = "prashant@psagents.online"
    TO_EMAIL: str = "prashant.mhd@gmail.com"
    
    # API Base URLs
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    # Model Names
    DEEPSEEK_MODEL: str = "deepseek-chat"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    LLAMA_MODEL: str = "llama-3.3-70b-versatile"
    GPT_MODEL: str = "gpt-4o-mini"
    
    # Compliance Requirements
    REQUIRED_COMPLIANCE_ELEMENTS: list = ["ComplAI", "unsubscribe", "support@"]
    UNSUBSCRIBE_URL: str = "https://complai.com/unsubscribe"
    SUPPORT_EMAIL: str = "support@complai.com"
    
    # Guardrail Settings
    MAX_MESSAGE_LENGTH: int = 800
    BANNED_TERMS: list = ["guarantee", "100%", "fully certified", "instant approval", "risk-free"]
    
    # Execution Settings
    MAX_TURNS: int = 10
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """
        Validate that required API keys are present.
        
        Returns:
            dict: Status of each API key (exists/not set)
        """
        return {
            "openai": bool(cls.OPENAI_API_KEY),
            "google": bool(cls.GOOGLE_API_KEY),
            "deepseek": bool(cls.DEEPSEEK_API_KEY),
            "groq": bool(cls.GROQ_API_KEY),
            "sendgrid": bool(cls.SENDGRID_API_KEY)
        }
    
    @classmethod
    def print_api_key_status(cls) -> None:
        """Print the status of API keys for debugging."""
        status = cls.validate_api_keys()
        
        if cls.OPENAI_API_KEY:
            print(f"OpenAI API Key exists and begins {cls.OPENAI_API_KEY[:8]}")
        else:
            print("OpenAI API Key not set")
            
        if cls.GOOGLE_API_KEY:
            print(f"Google API Key exists and begins {cls.GOOGLE_API_KEY[:2]}")
        else:
            print("Google API Key not set (and this is optional)")
            
        if cls.DEEPSEEK_API_KEY:
            print(f"DeepSeek API Key exists and begins {cls.DEEPSEEK_API_KEY[:3]}")
        else:
            print("DeepSeek API Key not set (and this is optional)")
            
        if cls.GROQ_API_KEY:
            print(f"Groq API Key exists and begins {cls.GROQ_API_KEY[:4]}")
        else:
            print("Groq API Key not set (and this is optional)")
            
        if cls.SENDGRID_API_KEY:
            print(f"SendGrid API Key exists and begins {cls.SENDGRID_API_KEY[:8]}")
        else:
            print("SendGrid API Key not set - EMAIL SENDING WILL NOT WORK")


# Global configuration instance
config = Config()
