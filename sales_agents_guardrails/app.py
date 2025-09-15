from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, function_tool, OpenAIChatCompletionsModel, input_guardrail, GuardrailFunctionOutput
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from pydantic import BaseModel
import asyncio
import re

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")

instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails. \
Your response must be in JSON format with 'subject' and 'body' fields. \
Example: {'subject': 'Your Subject Here', 'body': 'Your email body content here'}"


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"



deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)

deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)
llama3_3_model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=groq_client)

class EmailDraft(BaseModel):
    subject: str
    body: str

    @classmethod
    def _contains_banned_terms(cls, text: str) -> bool:
        banned_terms = ["guarantee", "100%", "fully certified", "instant approval", "risk-free"]
        lowered = text.lower()
        return any(term in lowered for term in banned_terms)

    @classmethod
    def _looks_too_short(cls, text: str) -> bool:
        return len(text.strip()) < 80

    @classmethod
    def _contains_placeholders_or_unsafe(cls, text: str) -> bool:
        return any(tok in text for tok in ["<script", "{{", "}}", "[placeholder]"])

    def model_post_init(self, __context):
        if not (2 <= len(self.subject) <= 90):
            raise ValueError("subject length out of bounds")
        if self._contains_banned_terms(self.subject):
            raise ValueError("subject contains banned terms")
        if self._looks_too_short(self.body):
            raise ValueError("body too short")
        if self._contains_placeholders_or_unsafe(self.body):
            raise ValueError("body contains unsafe or placeholder content")

class SubjectLine(BaseModel):
    subject: str

    def model_post_init(self, __context):
        text = (self.subject or "").strip()
        if not (2 <= len(text) <= 90):
            raise ValueError("subject length out of bounds")
        lowered = text.lower()
        banned = ["re:", "fwd:", "100%", "guarantee"]
        if any(b in lowered for b in banned):
            raise ValueError("banned subject terms")

class HtmlEmailBody(BaseModel):
    html_body: str

    def model_post_init(self, __context):
        text = self.html_body or ""
        if "http://" in text:
            raise ValueError("unencrypted link present")
        if any(tok in text.lower() for tok in ["<script", "onload=", "onerror="]):
            raise ValueError("potentially unsafe html")

class EmailToSend(BaseModel):
    subject: str
    html_body: str

sales_agent1 = Agent(name="DeepSeek Sales Agent", instructions=instructions1, model=deepseek_model)
sales_agent2 =  Agent(name="Gemini Sales Agent", instructions=instructions2, model=gemini_model)
sales_agent3  = Agent(name="Llama3.3 Sales Agent",instructions=instructions3,model=llama3_3_model)

description = "Write a cold sales email"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

def sanitize_html_basic(html_body: str) -> str:
    cleaned = re.sub(r"(?is)<script.*?>.*?</script>", "", html_body)
    cleaned = re.sub(r"\son\\w+=\"[^\"]*\"", "", cleaned)
    # Convert any HTTP links to HTTPS - multiple patterns
    cleaned = re.sub(r'href="http://', 'href="https://', cleaned)
    cleaned = re.sub(r"href='http://", "href='https://", cleaned)
    cleaned = re.sub(r'href=http://', 'href=https://', cleaned)
    # Also convert any standalone http:// URLs
    cleaned = re.sub(r'http://', 'https://', cleaned)
    return cleaned

def all_links_https(html_body: str) -> bool:
    # Check for various link patterns
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html_body)
    # Also check for any remaining http:// patterns
    http_links = re.findall(r'http://[^\s<>"\']+', html_body)
    print(f"Found hrefs: {hrefs}")
    print(f"Found HTTP links: {http_links}")
    return len(http_links) == 0 and all(href.startswith("https://") for href in hrefs)

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    print(f"HTML body received: {html_body[:500]}...")  # Debug: show first 500 chars
    
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("prashant@psagents.online")  # Change to your verified sender
    to_email = To("prashant.mhd@gmail.com")  # Change to your recipient
    must_have = ["ComplAI", "unsubscribe", "support@"]
    has_required = all(token.lower() in html_body.lower() for token in must_have)
    if not has_required:
        raise Exception("Email blocked: missing required compliance text")
    
    # Check links before sanitization
    if not all_links_https(html_body):
        raise Exception("Email blocked: non-HTTPS links detected")
    
    safe_html = sanitize_html_basic(html_body)
    print(f"Sanitized HTML: {safe_html[:500]}...")  # Debug: show sanitized version
    
    content = Content("text/html", safe_html)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

subject_instructions = "You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design. \
Your response must be in JSON format with 'html_body' field containing the HTML content. \
Example: {'html_body': '<html><body>Your HTML content here</body></html>'} \
IMPORTANT: You MUST include the following compliance elements in your HTML output: \
1. The company name 'ComplAI' somewhere in the email body \
2. An unsubscribe link with the text 'unsubscribe' (use https://complai.com/unsubscribe) \
3. A support email address containing 'support@' (e.g., support@complai.com) \
CRITICAL: ALL links must use HTTPS protocol (https://) - never use HTTP (http://). \
If you include any links, they must start with 'https://' or the email will be blocked. \
These elements are required for compliance and the email will be blocked without them."

subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o-mini", output_type=SubjectLine)
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o-mini")
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

email_tools = [subject_tool, html_tool, send_html_email]

@function_tool
def build_email_to_send(subject: str, html_body: str) -> EmailToSend:
    """Validate and assemble the final email payload before sending."""
    payload = EmailToSend(subject=subject, html_body=html_body)
    return payload.model_dump()

email_tools = [subject_tool, html_tool, build_email_to_send, send_html_email]

instructions ="You are an email formatter and sender. You receive the body of an email to be sent. \
First, call subject_writer to obtain a structured SubjectLine. \
Second, call html_converter to obtain a structured HtmlEmailBody. \
Third, call build_email_to_send(subject, html_body) to validate and assemble an EmailToSend object. \
Finally, call send_html_email with the validated subject and html_body. Return the final EmailToSend as your output."


emailer_agent = Agent(
    name="Email Manager",
    instructions=instructions,
    tools=email_tools,
    model="gpt-4o-mini",
    output_type=EmailToSend,
    handoff_description="Convert an email to HTML and send it")

tools = [tool1, tool2, tool3]
handoffs = [emailer_agent]

sales_manager_instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
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
- STOP immediately if any errors occur during the process.
"""


sales_manager = Agent(
    name="Basic Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini")

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,
    model="gpt-4o-mini"
)

@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

@input_guardrail
async def guardrail_against_pii(ctx, agent, message: str):
    email = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", message, re.I)
    phone = re.search(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}", message)
    titles = re.search(r"\b(CTO|CFO|VP|Director|Head of|Mr\.?|Ms\.?|Mrs\.?|Dr\.)\b", message, re.I)
    hit = bool(email or phone or titles)
    return GuardrailFunctionOutput(output_info={"email":bool(email), "phone":bool(phone), "title":bool(titles)}, tripwire_triggered=hit)

@input_guardrail
async def guardrail_against_risky_claims(ctx, agent, message: str):
    banned = ["guarantee", "100%", "fully certified", "instant approval", "risk-free"]
    lowered = message.lower()
    tripped = any(term in lowered for term in banned)
    return GuardrailFunctionOutput(output_info={"banned_terms":[t for t in banned if t in lowered]}, tripwire_triggered=tripped)

@input_guardrail
async def guardrail_length(ctx, agent, message: str):
    tripped = len(message) > 800
    return GuardrailFunctionOutput(output_info={"length": len(message)}, tripwire_triggered=tripped)

careful_sales_manager = Agent(
    name="Protected Sales Manager",
    instructions=sales_manager_instructions,
    tools=tools,
    handoffs=[emailer_agent],
    model="gpt-4o-mini",
    input_guardrails=[guardrail_against_name, guardrail_against_pii, guardrail_against_risky_claims, guardrail_length]
    )

message = "Send out a cold sales email addressed to Dear CEO from our sales team"

async def main():
    with trace("Automated SDR"):
        await Runner.run(sales_manager, message, max_turns=10)

    with trace("Protected Automated SDR"):
        await Runner.run(careful_sales_manager, message, max_turns=10)

    next_message = "Send out a cold sales email addressed to Dear CEO from our business development team"
    with trace("Protected Automated SDR"):
        await Runner.run(careful_sales_manager, next_message, max_turns=10)

if __name__ == "__main__":
    asyncio.run(main())