"""
Input guardrails for the Sales Agents application.

This module contains all input validation guardrails that protect against
inappropriate or risky content in user messages and agent interactions.
"""

import re
from agents import input_guardrail, GuardrailFunctionOutput, Runner
from .models import NameCheckOutput
from config import config


@input_guardrail
async def guardrail_against_name(ctx, agent, message: str) -> GuardrailFunctionOutput:
    """
    Guardrail to detect and block messages containing personal names.
    
    This guardrail uses an AI agent to intelligently detect when a user
    is trying to include someone's personal name in their request, which
    could be a privacy concern or inappropriate use.
    
    Args:
        ctx: Context object containing execution context
        agent: The agent being protected
        message (str): The user message to check
        
    Returns:
        GuardrailFunctionOutput: Result of the guardrail check
    """
    # Create a name detection agent
    guardrail_agent = agent.__class__(
        name="Name Check Agent",
        instructions="Check if the user is including someone's personal name in what they want you to do.",
        output_type=NameCheckOutput,
        model=config.GPT_MODEL
    )
    
    # Run the name detection
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    
    return GuardrailFunctionOutput(
        output_info={"found_name": result.final_output},
        tripwire_triggered=is_name_in_message
    )


@input_guardrail
async def guardrail_against_pii(ctx, agent, message: str) -> GuardrailFunctionOutput:
    """
    Guardrail to detect and block personally identifiable information (PII).
    
    This guardrail uses regex patterns to detect:
    - Email addresses
    - Phone numbers
    - Professional titles (CTO, CFO, VP, etc.)
    
    Args:
        ctx: Context object containing execution context
        agent: The agent being protected
        message (str): The user message to check
        
    Returns:
        GuardrailFunctionOutput: Result of the guardrail check
    """
    # Email pattern detection
    email = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", message, re.I)
    
    # Phone number pattern detection
    phone = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}", message)
    
    # Professional title detection
    titles = re.search(r"\b(CTO|CFO|VP|Director|Head of|Mr\.?|Ms\.?|Mrs\.?|Dr\.)\b", message, re.I)
    
    # Check if any PII was detected
    hit = bool(email or phone or titles)
    
    return GuardrailFunctionOutput(
        output_info={
            "email": bool(email), 
            "phone": bool(phone), 
            "title": bool(titles)
        }, 
        tripwire_triggered=hit
    )


@input_guardrail
async def guardrail_against_risky_claims(ctx, agent, message: str) -> GuardrailFunctionOutput:
    """
    Guardrail to detect and block risky marketing claims.
    
    This guardrail prevents the use of potentially misleading or
    legally problematic marketing language that could cause issues.
    
    Args:
        ctx: Context object containing execution context
        agent: The agent being protected
        message (str): The user message to check
        
    Returns:
        GuardrailFunctionOutput: Result of the guardrail check
    """
    lowered = message.lower()
    tripped = any(term in lowered for term in config.BANNED_TERMS)
    
    return GuardrailFunctionOutput(
        output_info={"banned_terms": [t for t in config.BANNED_TERMS if t in lowered]}, 
        tripwire_triggered=tripped
    )


@input_guardrail
async def guardrail_length(ctx, agent, message: str) -> GuardrailFunctionOutput:
    """
    Guardrail to prevent excessively long messages.
    
    This guardrail helps prevent abuse and ensures messages stay
    within reasonable length limits for processing.
    
    Args:
        ctx: Context object containing execution context
        agent: The agent being protected
        message (str): The user message to check
        
    Returns:
        GuardrailFunctionOutput: Result of the guardrail check
    """
    tripped = len(message) > config.MAX_MESSAGE_LENGTH
    
    return GuardrailFunctionOutput(
        output_info={"length": len(message)}, 
        tripwire_triggered=tripped
    )


# List of all available guardrails for easy import
ALL_GUARDRAILS = [
    guardrail_against_name,
    guardrail_against_pii,
    guardrail_against_risky_claims,
    guardrail_length
]
