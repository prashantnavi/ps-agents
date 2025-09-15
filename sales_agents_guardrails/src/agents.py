"""
Agent definitions for the Sales Agents application.

This module contains all agent configurations, including sales agents,
email management agents, and their associated tools and instructions.
"""

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from .models import EmailDraft, SubjectLine, HtmlEmailBody, EmailToSend
from .tools import send_html_email, build_email_to_send
from .guardrails import ALL_GUARDRAILS
from config import config


class SalesAgentFactory:
    """Factory class for creating configured sales agents."""
    
    def __init__(self):
        """Initialize the factory with API clients."""
        self._setup_clients()
        self._setup_models()
    
    def _setup_clients(self):
        """Set up API clients for different providers."""
        self.deepseek_client = AsyncOpenAI(
            base_url=config.DEEPSEEK_BASE_URL, 
            api_key=config.DEEPSEEK_API_KEY
        )
        self.gemini_client = AsyncOpenAI(
            base_url=config.GEMINI_BASE_URL, 
            api_key=config.GOOGLE_API_KEY
        )
        self.groq_client = AsyncOpenAI(
            base_url=config.GROQ_BASE_URL, 
            api_key=config.GROQ_API_KEY
        )
    
    def _setup_models(self):
        """Set up model configurations."""
        self.deepseek_model = OpenAIChatCompletionsModel(
            model=config.DEEPSEEK_MODEL, 
            openai_client=self.deepseek_client
        )
        self.gemini_model = OpenAIChatCompletionsModel(
            model=config.GEMINI_MODEL, 
            openai_client=self.gemini_client
        )
        self.llama_model = OpenAIChatCompletionsModel(
            model=config.LLAMA_MODEL, 
            openai_client=self.groq_client
        )
    
    def create_sales_agents(self):
        """
        Create the three different sales agent personalities.
        
        Returns:
            tuple: Three sales agents with different styles
        """
        # Professional sales agent instructions
        instructions1 = """You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"""

        # Humorous sales agent instructions
        instructions2 = """You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"""

        # Concise sales agent instructions
        instructions3 = """You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"""

        # Create the three sales agents
        sales_agent1 = Agent(
            name="DeepSeek Sales Agent", 
            instructions=instructions1, 
            model=self.deepseek_model
        )
        
        sales_agent2 = Agent(
            name="Gemini Sales Agent", 
            instructions=instructions2, 
            model=self.gemini_model
        )
        
        sales_agent3 = Agent(
            name="Llama3.3 Sales Agent",
            instructions=instructions3,
            model=self.llama_model
        )
        
        return sales_agent1, sales_agent2, sales_agent3


class EmailAgentFactory:
    """Factory class for creating email management agents."""
    
    def create_subject_writer(self):
        """
        Create an agent for writing email subjects.
        
        Returns:
            Agent: Configured subject writing agent
        """
        subject_instructions = """You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response."""
        
        return Agent(
            name="Email Subject Writer", 
            instructions=subject_instructions, 
            model=config.GPT_MODEL, 
            output_type=SubjectLine
        )
    
    def create_html_converter(self):
        """
        Create an agent for converting text to HTML email format.
        
        Returns:
            Agent: Configured HTML conversion agent
        """
        html_instructions = f"""You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design. \
Your response must be in JSON format with 'html_body' field containing the HTML content. \
Example: {{'html_body': '<html><body>Your HTML content here</body></html>'}} \
IMPORTANT: You MUST include the following compliance elements in your HTML output: \
1. The company name 'ComplAI' somewhere in the email body \
2. An unsubscribe link with the text 'unsubscribe' (use {config.UNSUBSCRIBE_URL}) \
3. A support email address containing 'support@' (e.g., {config.SUPPORT_EMAIL}) \
CRITICAL: ALL links must use HTTPS protocol (https://) - never use HTTP (http://). \
If you include any links, they must start with 'https://' or the email will be blocked. \
These elements are required for compliance and the email will be blocked without them."""
        
        return Agent(
            name="HTML Email Body Converter", 
            instructions=html_instructions, 
            model=config.GPT_MODEL
        )
    
    def create_email_manager(self, subject_tool, html_tool):
        """
        Create the main email management agent.
        
        Args:
            subject_tool: Tool for writing email subjects
            html_tool: Tool for converting to HTML
            
        Returns:
            Agent: Configured email management agent
        """
        instructions = """You are an email formatter and sender. You receive the body of an email to be sent. \
First, call subject_writer to obtain a structured SubjectLine. \
Second, call html_converter to obtain a structured HtmlEmailBody. \
Third, call build_email_to_send(subject, html_body) to validate and assemble an EmailToSend object. \
Finally, call send_html_email with the validated subject and html_body. Return the final EmailToSend as your output."""
        
        email_tools = [subject_tool, html_tool, build_email_to_send, send_html_email]
        
        return Agent(
            name="Email Manager",
            instructions=instructions,
            tools=email_tools,
            model=config.GPT_MODEL,
            output_type=EmailToSend,
            handoff_description="Convert an email to HTML and send it"
        )


class SalesManagerFactory:
    """Factory class for creating sales manager agents."""
    
    def create_sales_manager(self, sales_tools, email_manager):
        """
        Create a basic sales manager without guardrails.
        
        Args:
            sales_tools: List of sales agent tools
            email_manager: Email management agent
            
        Returns:
            Agent: Configured sales manager
        """
        instructions = """You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You may retry tools only once if a draft is clearly unusable; otherwise proceed.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.

CRITICAL: You must hand off EXACTLY ONE email draft to the Email Manager. Do NOT hand off multiple emails. Do NOT hand off all three drafts. Choose the best one and hand off only that one.

Stop Conditions:
- After handing off the single winning draft, STOP immediately. Do not call any more tools or continue the conversation.
- If the Email Manager reports any errors or blocking issues, STOP immediately. Do not retry or continue.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
- NEVER hand off multiple emails or all three drafts.
- STOP immediately if any errors occur during the process."""
        
        return Agent(
            name="Basic Sales Manager",
            instructions=instructions,
            tools=sales_tools,
            handoffs=[email_manager],
            model=config.GPT_MODEL
        )
    
    def create_protected_sales_manager(self, sales_tools, email_manager):
        """
        Create a sales manager with input guardrails for protection.
        
        Args:
            sales_tools: List of sales agent tools
            email_manager: Email management agent
            
        Returns:
            Agent: Configured protected sales manager
        """
        instructions = """You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You may retry tools only once if a draft is clearly unusable; otherwise proceed.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.

CRITICAL: You must hand off EXACTLY ONE email draft to the Email Manager. Do NOT hand off multiple emails. Do NOT hand off all three drafts. Choose the best one and hand off only that one.

Stop Conditions:
- After handing off the single winning draft, STOP immediately. Do not call any more tools or continue the conversation.
- If the Email Manager reports any errors or blocking issues, STOP immediately. Do not retry or continue.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
- NEVER hand off multiple emails or all three drafts.
- STOP immediately if any errors occur during the process."""
        
        return Agent(
            name="Protected Sales Manager",
            instructions=instructions,
            tools=sales_tools,
            handoffs=[email_manager],
            model=config.GPT_MODEL,
            input_guardrails=ALL_GUARDRAILS
        )
