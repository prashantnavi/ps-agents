# Sales Agents with Guardrails

A sophisticated AI-powered sales email automation system with built-in compliance, security, and content validation guardrails. This system uses multiple AI models to generate diverse sales emails while ensuring all outputs meet strict compliance and security requirements.

## 🚀 Features

- **Multi-Model AI Agents**: Uses DeepSeek, Gemini, and Llama models for diverse email generation
- **Comprehensive Guardrails**: Input validation for PII, risky claims, personal names, and message length
- **Compliance Automation**: Automatic inclusion of required compliance elements (ComplAI branding, unsubscribe links, support contacts)
- **Security Validation**: HTTPS link enforcement and HTML sanitization
- **Error Handling**: Robust error handling with automatic workflow termination on blocking
- **Modular Architecture**: Clean, maintainable code structure with separation of concerns

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for the following services:
  - **OpenAI** (required) - For GPT models and agent orchestration
  - **SendGrid** (required) - For email delivery
  - **Google AI** (optional) - For Gemini model
  - **DeepSeek** (optional) - For DeepSeek model
  - **Groq** (optional) - For Llama model

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd sales_agents_guardrails
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   
   # Optional API Keys (for additional models)
   GOOGLE_API_KEY=your_google_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🏗️ Project Structure

```
sales_agents_guardrails/
├── src/                    # Main source code
│   ├── __init__.py        # Package initialization
│   ├── app.py             # Main application orchestration
│   ├── agents.py          # Agent definitions and factories
│   ├── models.py          # Pydantic data models
│   ├── tools.py           # Function tools for agents
│   └── guardrails.py      # Input validation guardrails
├── config/                # Configuration management
│   ├── __init__.py
│   └── settings.py        # Application settings and constants
├── tests/                 # Test files (to be added)
├── docs/                  # Documentation (to be added)
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .env                  # Environment variables (create this)
```

## 🚦 Usage

### Basic Usage

```python
import asyncio
from src.app import SalesAgentApplication

async def main():
    # Initialize the application
    app = SalesAgentApplication()
    
    # Run a protected workflow (with guardrails)
    message = "Send out a cold sales email addressed to Dear CEO from our sales team"
    await app.run_protected_workflow(message)

# Run the application
asyncio.run(main())
```

### Advanced Usage

```python
from src.app import SalesAgentApplication

app = SalesAgentApplication()

# Validate setup before running
if app.validate_setup():
    # Run basic workflow (without guardrails)
    await app.run_basic_workflow("Your message here")
    
    # Run protected workflow (with guardrails)
    await app.run_protected_workflow("Your message here")
    
    # Run comparison workflow (both basic and protected)
    await app.run_comparison_workflow("Your message here")
```

### Command Line Usage

```bash
# Run the main application
python -m src.app

# Or run directly
python src/app.py
```

## 🛡️ Guardrails and Restrictions

### Input Guardrails

The system includes multiple layers of protection:

1. **Name Detection Guardrail**
   - Detects attempts to include personal names in requests
   - Uses AI to intelligently identify name references
   - **Restriction**: Blocks messages containing personal names

2. **PII Detection Guardrail**
   - Detects email addresses, phone numbers, and professional titles
   - Uses regex patterns for comprehensive PII detection
   - **Restriction**: Blocks messages containing PII

3. **Risky Claims Guardrail**
   - Detects potentially misleading marketing language
   - **Banned terms**: "guarantee", "100%", "fully certified", "instant approval", "risk-free"
   - **Restriction**: Blocks messages containing banned terms

4. **Length Guardrail**
   - Prevents excessively long messages
   - **Restriction**: Blocks messages longer than 800 characters

### Email Compliance Requirements

All generated emails must include:

1. **Company Branding**: "ComplAI" must appear in the email body
2. **Unsubscribe Link**: Must include an unsubscribe link (https://complai.com/unsubscribe)
3. **Support Contact**: Must include a support email address (support@complai.com)
4. **HTTPS Links**: All links must use HTTPS protocol (HTTP links are automatically converted)

### Security Features

- **HTML Sanitization**: Removes script tags and event handlers
- **Link Security**: Converts HTTP links to HTTPS
- **Content Validation**: Validates email structure and content
- **Error Handling**: Stops execution immediately on blocking conditions

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT models |
| `SENDGRID_API_KEY` | Yes | SendGrid API key for email delivery |
| `GOOGLE_API_KEY` | No | Google AI API key for Gemini model |
| `DEEPSEEK_API_KEY` | No | DeepSeek API key for DeepSeek model |
| `GROQ_API_KEY` | No | Groq API key for Llama model |

### Application Settings

Key settings can be modified in `config/settings.py`:

- `MAX_TURNS`: Maximum number of agent turns (default: 10)
- `MAX_MESSAGE_LENGTH`: Maximum message length for guardrails (default: 800)
- `BANNED_TERMS`: List of banned marketing terms
- `REQUIRED_COMPLIANCE_ELEMENTS`: Required elements in emails

## 🔧 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

### Code Formatting

```bash
# Format code with black
black src/ config/

# Check code style
flake8 src/ config/
```

### Type Checking

```bash
# Run type checking
mypy src/ config/
```

## 🚨 Important Restrictions and Limitations

### Content Restrictions

1. **No Personal Names**: The system blocks any attempts to include personal names
2. **No PII**: Email addresses, phone numbers, and titles are blocked
3. **No Risky Claims**: Banned marketing terms are strictly prohibited
4. **Message Length**: Messages must be under 800 characters

### Technical Limitations

1. **API Dependencies**: Requires valid API keys for core functionality
2. **Model Availability**: Some models may not be available in all regions
3. **Rate Limits**: Subject to API rate limits of respective providers
4. **Email Delivery**: Depends on SendGrid service availability

### Compliance Requirements

1. **Mandatory Elements**: All emails must include ComplAI branding, unsubscribe links, and support contacts
2. **HTTPS Only**: All links must use HTTPS protocol
3. **Content Validation**: All content is validated before sending
4. **Error Handling**: System stops immediately on any compliance violations

## 🐛 Troubleshooting

### Common Issues

1. **"API Key not set" errors**
   - Ensure all required API keys are set in your `.env` file
   - Verify API keys are valid and have appropriate permissions

2. **"Email blocked" errors**
   - Check that your message doesn't contain banned terms or PII
   - Ensure message length is under 800 characters
   - Verify compliance elements are included in generated emails

3. **"Multiple handoffs requested" errors**
   - This indicates an agent configuration issue
   - Check that agent names are unique
   - Verify handoff configurations are correct

4. **"non-HTTPS links detected" errors**
   - Ensure all links in generated content use HTTPS
   - Check that the HTML converter is properly configured

### Debug Mode

Enable debug output by checking the console logs. The system provides detailed information about:
- API key validation status
- Link detection and conversion
- HTML sanitization process
- Guardrail trigger conditions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in the `docs/` directory

## 🔄 Version History

- **v1.0.0**: Initial release with comprehensive guardrails and multi-model support

---

**⚠️ Important**: This system is designed for legitimate business use only. Ensure compliance with all applicable laws and regulations, including CAN-SPAM Act, GDPR, and other relevant legislation in your jurisdiction.
