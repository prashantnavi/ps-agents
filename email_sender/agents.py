"""
Agents Module
Defines and configures all AI agents used in the email sender application.
"""

from config import AI_CONFIG, AGENT_INSTRUCTIONS
import openai
import os
import asyncio
from typing import Optional, List, Dict, Any, Tuple


class Agent:
    """Simple Agent class for the email sender application."""
    
    def __init__(self, name: str, instructions: str, model: str = "gpt-4o-mini", 
                 tools: Optional[List] = None, handoffs: Optional[List] = None, 
                 handoff_description: Optional[str] = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.handoffs = handoffs or []
        self.handoff_description = handoff_description
    
    async def run(self, message: str) -> str:
        """Run the agent with a given message.

        Supports OpenAI tool-calling and dispatch of local tools and handoffs.
        """
        client_kwargs = {}
        project_env = os.environ.get("OPENAI_PROJECT")
        if project_env:
            client_kwargs["project"] = project_env
        client = openai.AsyncOpenAI(**client_kwargs)

        system_prompt = f"{self.instructions}\n\nYou are {self.name}."

        # Prepare conversation
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        # Build tool schemas from provided tools and handoffs
        tool_schemas, tool_runtime = _build_tooling(self)

        # If no tools/handoffs, do a single shot call
        if not tool_schemas:
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message.content

        # Tool-enabled loop
        max_tool_turns = 8
        for _ in range(max_tool_turns):
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                tools=tool_schemas,
                tool_choice="auto",
            )

            choice = response.choices[0]
            msg = choice.message

            # If assistant returned final content with no tool calls -> done
            tool_calls = getattr(msg, "tool_calls", None)
            if not tool_calls:
                return msg.content or ""

            # Handle tool calls sequentially, append results
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args_json = tool_call.function.arguments or "{}"

                result_text = await _execute_tool_call(tool_name, tool_args_json, tool_runtime)

                # Add assistant tool call and tool result messages
                messages.append({
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {"name": tool_name, "arguments": tool_args_json},
                        }
                    ],
                    "content": None,
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_text,
                })

        # Fallback if the model keeps asking for tools
        return ""


class Runner:
    """Simple runner class for agents."""
    
    @staticmethod
    async def run(agent: Agent, message: str):
        """Run an agent and return a result object."""
        result = await agent.run(message)
        return SimpleResult(result)
    
    @staticmethod
    def run_streamed(agent: Agent, input: str):
        """Run an agent with streaming output."""
        return StreamedResult(agent, input)


class SimpleResult:
    """Simple result class."""
    
    def __init__(self, final_output: str):
        self.final_output = final_output


class StreamedResult:
    """Simple streamed result class."""
    
    def __init__(self, agent: Agent, input: str):
        self.agent = agent
        self.input = input
    
    async def stream_events(self):
        """Stream events from the agent."""
        # Simple implementation - just yield the result
        result = await self.agent.run(self.input)
        yield SimpleStreamEvent("raw_response_event", SimpleTextDelta(result))


class SimpleStreamEvent:
    """Simple stream event class."""
    
    def __init__(self, type: str, data):
        self.type = type
        self.data = data


class SimpleTextDelta:
    """Simple text delta class."""
    
    def __init__(self, delta: str):
        self.delta = delta


def trace(name: str):
    """Simple trace context manager."""
    class SimpleTrace:
        def __init__(self, name: str):
            self.name = name
        
        def __enter__(self):
            print(f"🔍 Starting trace: {self.name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"✅ Completed trace: {self.name}")
    
    return SimpleTrace(name)


def _build_tooling(agent: "Agent") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Build OpenAI tool schemas and runtime dispatch table from an Agent's tools and handoffs.

    Returns:
        (tool_schemas, runtime): A list of OpenAI tool definitions and a runtime dict for dispatch.
    """
    tool_schemas: List[Dict[str, Any]] = []
    runtime: Dict[str, Any] = {}

    # Helper to add a function tool schema
    def add_tool_schema(name: str, description: str, parameters: Dict[str, Any]):
        tool_schemas.append({
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        })

    # Map agent.tools (which may be dicts or functions) to tool schemas
    for t in (agent.tools or []):
        # send_html_email_tool is a function
        if callable(t):
            name = "send_html_email_tool"
            description = "Send an HTML email with a subject and html body."
            parameters = {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "html_body": {"type": "string"},
                },
                "required": ["subject", "html_body"],
            }
            add_tool_schema(name, description, parameters)
            runtime[name] = t  # call directly
            continue

        if isinstance(t, dict) and "name" in t and "agent" in t:
            tool_name = t["name"]
            tool_agent: Agent = t["agent"]
            # Minimal parameter schema: pass a single field "message" or "body"
            param_name = "message"
            description = t.get("description", "Invoke a helper agent.")
            parameters = {
                "type": "object",
                "properties": {param_name: {"type": "string"}},
                "required": [param_name],
            }
            add_tool_schema(tool_name, description, parameters)
            runtime[tool_name] = tool_agent

    # Expose handoff agents as tools as well
    for h in (agent.handoffs or []):
        if isinstance(h, Agent):
            name = f"handoff_{h.name.replace(' ', '_').lower()}"
            description = h.handoff_description or f"Handoff work to {h.name}"
            parameters = {
                "type": "object",
                "properties": {"body": {"type": "string"}},
                "required": ["body"],
            }
            add_tool_schema(name, description, parameters)
            runtime[name] = h

    return tool_schemas, runtime


async def _execute_tool_call(tool_name: str, tool_args_json: str, runtime: Dict[str, Any]) -> str:
    """Execute a tool call and return a stringified result for the model."""
    import json

    try:
        args = json.loads(tool_args_json or "{}")
    except Exception:
        args = {}

    tool = runtime.get(tool_name)
    if tool is None:
        return f"{{\n  \"error\": \"Unknown tool: {tool_name}\"\n}}"

    # If tool is a Python function (e.g., send_html_email_tool)
    if callable(tool):
        try:
            subject = args.get("subject", "")
            html_body = args.get("html_body", "")
            result = tool(subject=subject, html_body=html_body)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    # Otherwise assume tool is an Agent: pass message/body
    if isinstance(tool, Agent):
        text = args.get("message") or args.get("body") or ""
        result = await tool.run(text)
        return json.dumps({"final_output": result})

    return f"{{\n  \"error\": \"Unhandled tool type for {tool_name}\"\n}}"


def function_tool(func):
    """Simple function tool decorator."""
    # Add a method to convert agent to tool
    def as_tool(self, tool_name: str, tool_description: str):
        """Convert agent to tool."""
        return {
            "name": tool_name,
            "description": tool_description,
            "agent": self
        }
    
    # Add the as_tool method to the Agent class
    Agent.as_tool = as_tool
    
    return func


class AgentFactory:
    """Factory class for creating and managing AI agents."""
    
    @staticmethod
    def create_sales_agents():
        """
        Create the three specialized sales agents.
        
        Returns:
            tuple: (professional_agent, humorous_agent, concise_agent)
        """
        professional_agent = Agent(
            name="Professional Sales Agent",
            instructions=AGENT_INSTRUCTIONS["professional"],
            model=AI_CONFIG["model"]
        )
        
        humorous_agent = Agent(
            name="Engaging Sales Agent",
            instructions=AGENT_INSTRUCTIONS["humorous"],
            model=AI_CONFIG["model"]
        )
        
        concise_agent = Agent(
            name="Busy Sales Agent",
            instructions=AGENT_INSTRUCTIONS["concise"],
            model=AI_CONFIG["model"]
        )
        
        return professional_agent, humorous_agent, concise_agent
    
    @staticmethod
    def create_sales_picker():
        """
        Create the sales picker agent that selects the best email.
        
        Returns:
            Agent: Sales picker agent
        """
        return Agent(
            name="Sales Picker",
            instructions=AGENT_INSTRUCTIONS["sales_picker"],
            model=AI_CONFIG["model"]
        )
    
    @staticmethod
    def create_subject_writer():
        """
        Create the subject writer agent.
        
        Returns:
            Agent: Subject writer agent
        """
        return Agent(
            name="Email Subject Writer",
            instructions=AGENT_INSTRUCTIONS["subject_writer"],
            model=AI_CONFIG["model"]
        )
    
    @staticmethod
    def create_html_converter():
        """
        Create the HTML converter agent.
        
        Returns:
            Agent: HTML converter agent
        """
        return Agent(
            name="HTML Email Body Converter",
            instructions=AGENT_INSTRUCTIONS["html_converter"],
            model=AI_CONFIG["model"]
        )
    
    @staticmethod
    def create_email_manager(tools):
        """
        Create the email manager agent.
        
        Args:
            tools (list): List of tools available to the agent
            
        Returns:
            Agent: Email manager agent
        """
        return Agent(
            name="Email Manager",
            instructions=AGENT_INSTRUCTIONS["email_manager"],
            tools=tools,
            model=AI_CONFIG["model"],
            handoff_description="Convert an email to HTML and send it"
        )
    
    @staticmethod
    def create_sales_manager(tools, handoffs=None):
        """
        Create the sales manager agent.
        
        Args:
            tools (list): List of tools available to the agent
            handoffs (list, optional): List of handoff agents
            
        Returns:
            Agent: Sales manager agent
        """
        return Agent(
            name="Sales Manager",
            instructions=AGENT_INSTRUCTIONS["sales_manager"],
            tools=tools,
            handoffs=handoffs or [],
            model=AI_CONFIG["model"]
        )


# Create agent instances
def create_all_agents():
    """
    Create all agents used in the application.
    
    Returns:
        dict: Dictionary containing all agent instances
    """
    factory = AgentFactory()
    
    # Create sales agents
    professional_agent, humorous_agent, concise_agent = factory.create_sales_agents()
    
    # Create other agents
    sales_picker = factory.create_sales_picker()
    subject_writer = factory.create_subject_writer()
    html_converter = factory.create_html_converter()
    
    return {
        "professional_agent": professional_agent,
        "humorous_agent": humorous_agent,
        "concise_agent": concise_agent,
        "sales_picker": sales_picker,
        "subject_writer": subject_writer,
        "html_converter": html_converter
    }


# Global agent instances
agents = create_all_agents()

# Convenience accessors
def get_sales_agents():
    """Get the three sales agents as a list."""
    return [
        agents["professional_agent"],
        agents["humorous_agent"],
        agents["concise_agent"]
    ]


def get_sales_picker():
    """Get the sales picker agent."""
    return agents["sales_picker"]


def get_subject_writer():
    """Get the subject writer agent."""
    return agents["subject_writer"]


def get_html_converter():
    """Get the HTML converter agent."""
    return agents["html_converter"]
