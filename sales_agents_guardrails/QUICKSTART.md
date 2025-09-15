# 🚀 Quick Start Guide

Get up and running with Sales Agents with Guardrails in 5 minutes!

## 1. Prerequisites

- Python 3.8 or higher
- OpenAI API key (required)
- SendGrid API key (required)

## 2. Installation

```bash
# Clone or download the project
cd sales_agents_guardrails

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Configuration

```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your API keys
# At minimum, you need:
OPENAI_API_KEY=your_openai_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
```

## 4. Run the Application

```bash
# Run with default settings (recommended for first time)
python run.py

# Or run with custom message
python run.py --message "Send out a cold sales email to potential customers"
```

## 5. What Happens

1. **Agent Creation**: Three AI agents (DeepSeek, Gemini, Llama) generate different email styles
2. **Email Selection**: The sales manager selects the best email
3. **Compliance Check**: System ensures all required elements are present
4. **Email Sending**: Email is formatted and sent via SendGrid

## 6. Expected Output

```
🚀 Sales Agents with Guardrails
   AI-powered sales email automation with compliance guardrails
================================================================

🔧 Initializing application...
✅ Validating configuration...
✅ Configuration validated successfully!

📧 Running test 1: Send out a cold sales email addressed to Dear CEO from our sales team
--------------------------------------------------
✅ Test 1 completed successfully!

🎉 All tests completed!
```

## 7. Troubleshooting

### Common Issues

**"API Key not set" error:**
- Make sure your `.env` file exists and contains valid API keys
- Check that the keys are not wrapped in quotes

**"Email blocked" error:**
- This is normal! The system blocks emails that don't meet compliance requirements
- Check the console output for specific blocking reasons

**"Multiple handoffs requested" error:**
- This indicates a configuration issue
- Try running with `--workflow basic` first

### Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Run `python run.py --examples` for usage examples
- Ensure all required API keys are set in your `.env` file

## 8. Next Steps

- Customize the email templates in `src/agents.py`
- Modify guardrail settings in `config/settings.py`
- Add your own test cases in `tests/`
- Explore the modular architecture in the `src/` directory

---

**🎯 You're ready to go!** The system will automatically handle compliance, security, and email delivery for you.
