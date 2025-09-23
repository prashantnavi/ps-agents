#!/bin/bash
# AI Agents Global Environment Activation Script for Unix/Linux/Mac
# Usage: source activate.sh

echo "🚀 Activating AI Agents Global Environment..."

# Check if virtual environment exists
if [ -f ".venv/bin/activate" ]; then
    # Activate the virtual environment
    source .venv/bin/activate
    
    echo "✅ Virtual environment activated!"
    echo "📚 Available frameworks:"
    echo "   - CrewAI: Multi-agent framework"
    echo "   - OpenAI: GPT models and API"
    echo "   - LangChain: LLM application framework"
    echo "   - LangGraph: State machine workflows"
    echo "   - AutoGen: Microsoft's multi-agent framework"
    echo "   - FastAPI: Modern web API framework"
    echo "   - Gradio: ML model interfaces"
    echo "   - Streamlit: Data science web apps"
    echo ""
    echo "🔧 Quick commands:"
    echo "   python verify_setup.py    # Verify all frameworks"
    echo "   python setup.py           # Re-run setup if needed"
    echo ""
    echo "📁 Project structure:"
    echo "   startup_funding/          # Startup funding crew"
    echo "   career_conversation/      # Career conversation project"
    echo "   deep_research/            # Deep research project"
    echo "   email_sender/             # Email automation project"
    echo "   sales_agents_guardrails/  # Sales agents project"
    echo ""
    echo "🎯 Ready to build AI agents!"
else
    echo "❌ Virtual environment not found!"
    echo "Please run 'python setup.py' first to create the environment."
fi
