# Deep Research with Handoffs

This enhanced version of the deep research system includes powerful handoff capabilities that allow agents to transfer control to other agents, human reviewers, or external systems during the research process.

## 🚀 What are Handoffs?

Handoffs are a way for AI agents to:
- **Request human input** when they need human judgment
- **Consult with experts** for specialized knowledge
- **Perform quality checks** on their work
- **Request approval** before taking important actions
- **Transfer control** to other specialized agents

## 📁 Files Overview

### Core Handoff Files
- `handoff_models.py` - Data models for handoff requests and responses
- `handoff_agents.py` - Specialized agents that handle different types of handoffs
- `enhanced_research_manager.py` - Research manager with handoff capabilities
- `enhanced_deep_research.py` - Main application with handoff support

### Demo and Examples
- `demo_handoffs.py` - Simple demonstration of handoff capabilities
- `handoff_examples.py` - Example scenarios showing different handoff types

## 🔧 Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   # Required for OpenAI API
   export OPENAI_API_KEY="your-openai-api-key"
   
   # Required for email functionality
   export SENDGRID_API_KEY="your-sendgrid-api-key"
   ```

3. **Run the Enhanced Research System**
   ```bash
   python enhanced_deep_research.py
   ```

## 🎯 Handoff Types

### 1. 🤖 Expert Consultation
**When triggered:** Medical, legal, technical, financial, or scientific queries
**Purpose:** Get specialized knowledge from domain experts

**Example triggers:**
- "What are the medical implications of new diabetes treatments?"
- "What are the legal requirements for AI-generated content?"
- "What are the engineering challenges in quantum computing?"

### 2. 👤 Human Review
**When triggered:** Complex analysis, comparisons, evaluations, or strategic decisions
**Purpose:** Get human judgment for complex decisions

**Example triggers:**
- "Compare and analyze renewable energy strategies"
- "Evaluate the effectiveness of different marketing approaches"
- "Assess the risks and benefits of cryptocurrency investment"

### 3. ✅ Quality Checks
**When triggered:** After report generation
**Purpose:** Validate report quality, completeness, and accuracy

**Checks performed:**
- Content completeness
- Accuracy validation
- Formatting standards
- Clarity assessment

### 4. 📋 Approval Workflows
**When triggered:** Before important actions (sending emails, extensive searches)
**Purpose:** Get approval for significant actions

**Approval scenarios:**
- Sending research reports via email
- Performing more than 5 web searches
- Accessing sensitive information

## 🚀 Usage Examples

### Basic Usage
```python
from enhanced_research_manager import EnhancedResearchManager

# Create manager with handoffs enabled
manager = EnhancedResearchManager(enable_handoffs=True)

# Run research with handoffs
async for chunk in manager.run("What are the latest AI trends?"):
    print(chunk)
```

### Disable Handoffs
```python
# Create manager without handoffs
manager = EnhancedResearchManager(enable_handoffs=False)

# Run research without handoffs (faster, less interactive)
async for chunk in manager.run("What are the latest AI trends?"):
    print(chunk)
```

### Custom Handoff Logic
```python
# You can customize when handoffs are triggered by modifying
# the _needs_expert_consultation() and _needs_human_review() methods
# in the EnhancedResearchManager class
```

## 🎮 Interactive Demo

Run the enhanced research interface:
```bash
python enhanced_deep_research.py
```

Features:
- ✅ Toggle handoffs on/off
- ✅ Real-time progress updates
- ✅ Handoff notifications
- ✅ Quality check results
- ✅ Approval confirmations

## 🔍 Handoff Flow Example

Here's what happens when you ask: *"What are the medical implications of new diabetes treatments?"*

1. **🔍 Query Analysis**
   - System detects "medical" keyword
   - Triggers expert consultation handoff

2. **🎓 Expert Consultation**
   - Requests medical expert input
   - Gets specialized search recommendations
   - Receives domain-specific guidance

3. **📊 Research Planning**
   - Plans searches based on expert input
   - May request approval for extensive searches

4. **🔍 Web Research**
   - Performs targeted searches
   - Collects medical information

5. **📝 Report Writing**
   - May request human review for complex medical analysis
   - Writes comprehensive report

6. **✅ Quality Check**
   - Validates medical accuracy
   - Checks completeness
   - Ensures proper formatting

7. **📧 Email Approval**
   - Requests approval to send medical report
   - Confirms recipient list
   - Sends approved report

## 🛠️ Customization

### Adding New Handoff Types
1. Add new enum value to `HandoffType` in `handoff_models.py`
2. Create new request/response models
3. Implement handoff agent in `handoff_agents.py`
4. Add handoff logic to `enhanced_research_manager.py`

### Customizing Trigger Conditions
Modify these methods in `EnhancedResearchManager`:
- `_needs_expert_consultation()` - When to request expert help
- `_needs_human_review()` - When to request human review

### Adding New Agents
1. Create agent class in `handoff_agents.py`
2. Add function tools for the agent
3. Integrate into research workflow

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   Solution: Set OPENAI_API_KEY environment variable
   ```

2. **Import Errors**
   ```
   Solution: Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Handoffs Not Triggering**
   ```
   Solution: Check trigger conditions in _needs_expert_consultation() and _needs_human_review()
   ```

### Debug Mode
Enable verbose logging:
```python
from agents import enable_verbose_stdout_logging
enable_verbose_stdout_logging()
```

## 📚 Advanced Features

### Session Management
The system supports session-based handoffs for complex workflows:
```python
from agents import SQLiteSession

# Create session for persistent handoff state
session = SQLiteSession("research_session.db")
```

### Custom Handoff Recipients
You can integrate with external systems:
- Slack notifications
- Email alerts
- Webhook endpoints
- Database logging

### Batch Processing
Process multiple research queries with handoffs:
```python
queries = ["AI trends", "Medical research", "Legal implications"]
for query in queries:
    async for chunk in manager.run(query):
        print(f"{query}: {chunk}")
```

## 🤝 Contributing

To add new handoff capabilities:
1. Fork the repository
2. Add new handoff types
3. Implement agents
4. Update documentation
5. Submit pull request

## 📄 License

This project follows the same license as the main AI Agents project.
