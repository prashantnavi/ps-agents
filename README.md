# AI Agents Global Environment

This is the global environment setup for all AI agent projects in the MY-WORK directory.

## 🚀 Quick Start

### 1. Setup Global Environment

```bash
# Run the setup script
python setup.py

# Or manually:
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your actual API keys
# Required: OPENAI_API_KEY
# Optional: ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc.
```

### 3. Verify Installation

```bash
# Test CrewAI
python -c "import crewai; print('CrewAI version:', crewai.__version__)"

# Test OpenAI
python -c "import openai; print('OpenAI version:', openai.__version__)"
```

## 📁 Project Structure

```
my-workflows/
├── .venv/                 # Virtual environment
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── setup.py              # Setup script
├── env.example           # Environment variables template
├── README.md             # This file
├── startup_funding/      # Startup funding crew project
├── career_conversation/  # Career conversation project
├── deep_research/        # Deep research project
├── email_sender/         # Email automation project
└── sales_agents_guardrails/ # Sales agents project
```

## 🛠️ Available Frameworks

This global environment includes:

- **CrewAI**: Multi-agent framework for collaborative AI agents
- **OpenAI**: GPT models and API integration
- **LangChain**: LLM application framework
- **LangGraph**: State machine and agent workflows
- **AutoGen**: Microsoft's multi-agent conversation framework
- **FastAPI**: Modern web API framework
- **Gradio**: ML model interfaces
- **Streamlit**: Data science web apps

## 🔧 Development

### Adding New Dependencies

1. Add to `requirements.txt`
2. Update `pyproject.toml` if needed
3. Reinstall: `pip install -r requirements.txt`

### Creating New Projects

1. Create a new directory under `my-workflows/`
2. Use the global environment (no need for separate venv)
3. Import frameworks as needed

### Running Projects

```bash
# Activate global environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/Linux/Mac

# Navigate to project
cd startup_funding

# Run project
python src/startup_funding/main.py
```

## 🔑 Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `ANTHROPIC_API_KEY`: For Claude models
- `GOOGLE_API_KEY`: For Gemini models
- `CREWAI_VERBOSE`: Set to `true` for verbose logging
- `DATABASE_URL`: Database connection string

## 📚 Documentation

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

1. Make changes to the global environment
2. Test with existing projects
3. Update documentation as needed

## 📄 License

This project is part of the AI Agents learning environment.