# 🤖 AI Email Sender - Modular Application

A sophisticated, modular AI-powered email generation and sending system built with OpenAI Agents SDK.

## 🚀 Features

### **AI-Powered Email Generation**
- **Multiple Sales Agents**: Professional, Humorous, and Concise writing styles
- **Parallel Processing**: Generate multiple emails simultaneously
- **Smart Selection**: AI-powered email selection and optimization
- **Streaming Output**: Real-time email generation display

### **Advanced Workflows**
- **Automated Sales Pipeline**: Complete end-to-end email automation
- **Agent Collaboration**: Multi-agent workflows with handoffs
- **Tool Integration**: Seamless integration with email services
- **HTML Conversion**: Automatic text-to-HTML email conversion
 - **Inbound Replies**: SendGrid Inbound Parse webhook auto-responds with SDR agent

### **Modular Architecture**
- **Clean Separation**: Independent, testable modules
- **Configurable**: Centralized configuration management
- **Extensible**: Easy to add new agents and workflows
- **Maintainable**: Well-documented, organized codebase

## 📁 Project Structure

```
email_sender/
├── main.py              # Main application entry point
├── config.py            # Configuration and settings
├── email_service.py     # Email sending functionality
├── agents.py            # AI agent definitions
├── tools.py             # Function tools and conversions
├── workflows.py         # Email generation workflows
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## 🛠️ Installation

### **Prerequisites**
- Python 3.8 or higher
- OpenAI API key
- SendGrid API key

### **Setup**

1. **Clone and navigate to the project**
   ```bash
   cd email_sender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   # Create .env file with your API keys
   echo "OPENAI_API_KEY=your_openai_api_key" > .env
   echo "SENDGRID_API_KEY=your_sendgrid_api_key" >> .env
   echo "PARSE_TOKEN=your_inbound_token" >> .env
   echo "EMAIL_DB_PATH=./email_conversations.db" >> .env
   ```

4. **Configure email settings**
   - Update `config.py` with your email addresses
   - Verify your sender email in SendGrid

## 🎯 Usage

### **Command Line Interface**

```bash
# Run interactive mode
python main.py

# Run specific commands
python main.py demo          # Run complete demo
python main.py test          # Test email service
python main.py generate 0    # Generate email with agent 0
python main.py parallel      # Generate emails from all agents
python main.py select        # Generate and select best email
python main.py simple        # Run simple workflow
python main.py automated     # Run automated workflow
uvicorn webhook_server:app --reload --port 8080   # Run inbound webhook
## ✉️ Inbound Reply Automation

1. Configure SendGrid Inbound Parse to POST to:

   POST https://YOUR_PUBLIC_HOST/webhooks/sendgrid/inbound?token=YOUR_INBOUND_TOKEN

2. Expose local dev with ngrok:

```
ngrok http 8080
```

3. The server will:
- parse and thread the inbound message
- call the SDR agent to craft a short reply
- send an HTML reply in-thread via SendGrid
- persist both inbound and outbound messages in SQLite

See `webhook_server.py` and `database.py`.
```

### **Interactive Mode Commands**

```
Available commands:
1. test - Test email service
2. generate <agent> - Generate email (0=Professional, 1=Humorous, 2=Concise)
3. stream <agent> - Generate email with streaming
4. parallel - Generate emails from all agents
5. select - Generate and select best email
6. simple - Run simple workflow
7. automated - Run automated workflow
8. demo - Run complete demo
9. quit - Exit application
```

### **Programmatic Usage**

```python
import asyncio
from workflows import generate_email, run_automated_workflow

# Generate a single email
email = await generate_email(agent_index=0)
print(email)

# Run automated workflow
result = await run_automated_workflow()
print(result)
```

## 🔧 Configuration

### **Email Settings** (`config.py`)
```python
EMAIL_CONFIG = {
    "from_email": "your-email@domain.com",
    "to_email": "recipient@domain.com",
    "sendgrid_api_key": os.environ.get('SENDGRID_API_KEY')
}
```

### **AI Model Settings**
```python
AI_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": None,
    "max_tokens": None
}
```

### **Agent Instructions**
All agent instructions are centralized in `config.py` and can be easily customized.

## 🏗️ Architecture

### **Module Responsibilities**

- **`config.py`**: Centralized configuration and validation
- **`email_service.py`**: Email sending functionality with error handling
- **`agents.py`**: AI agent definitions and factory patterns
- **`tools.py`**: Function tools and agent-to-tool conversions
- **`workflows.py`**: Email generation and automation workflows
- **`main.py`**: Application orchestration and user interface

### **Design Patterns**

- **Factory Pattern**: Agent creation and management
- **Service Pattern**: Email service abstraction
- **Workflow Pattern**: Complex email generation processes
- **Configuration Pattern**: Centralized settings management

## 🧪 Testing

### **Email Service Test**
```bash
python main.py test
```

### **Individual Workflow Tests**
```bash
# Test single email generation
python main.py generate 0

# Test parallel generation
python main.py parallel

# Test automated workflow
python main.py automated
```

## 🔄 Workflows

### **1. Single Email Generation**
- Uses one sales agent to generate an email
- Supports streaming output
- Configurable agent selection

### **2. Parallel Email Generation**
- Generates emails from all three agents simultaneously
- Improves performance with async processing
- Returns multiple email options

### **3. Best Email Selection**
- Generates multiple emails
- Uses AI to select the best option
- Optimizes for response likelihood

### **4. Simple Workflow**
- Sales manager coordinates multiple agents
- Generates and sends one email
- Uses tools for email sending

### **5. Automated Workflow**
- Complete end-to-end automation
- Multi-agent collaboration with handoffs
- HTML conversion and formatting

## 🚀 Performance Features

- **Async Processing**: Non-blocking email generation
- **Parallel Execution**: Multiple agents working simultaneously
- **Streaming Output**: Real-time response display
- **Error Handling**: Robust error recovery and logging
- **Memory Efficient**: Optimized for large-scale operations

## 🔧 Customization

### **Adding New Agents**
1. Add agent instructions to `config.py`
2. Create agent in `agents.py`
3. Add to workflows in `workflows.py`

### **Adding New Tools**
1. Define function in `tools.py`
2. Add `@function_tool` decorator
3. Include in agent tool lists

### **Modifying Workflows**
1. Update workflow methods in `workflows.py`
2. Add new commands to `main.py`
3. Update documentation

## 🐛 Troubleshooting

### **Common Issues**

1. **API Key Errors**
   - Verify environment variables are set
   - Check API key validity

2. **Email Sending Failures**
   - Verify SendGrid configuration
   - Check sender email verification
   - Review SendGrid logs

3. **Async Errors**
   - Ensure proper async/await usage
   - Check for event loop conflicts

### **Debug Mode**
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Future Enhancements

- **Email Templates**: Pre-defined email templates
- **A/B Testing**: Automated email performance testing
- **Analytics**: Email performance tracking
- **CRM Integration**: Customer relationship management
- **Scheduling**: Automated email scheduling
- **Personalization**: Dynamic content personalization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is developed for educational and professional showcase purposes.

---

**Built with ❤️ using OpenAI Agents SDK and modern Python practices!**
