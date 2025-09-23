# AI Agents Global Environment Activation Script for PowerShell
# Usage: .\activate.ps1

Write-Host "🚀 Activating AI Agents Global Environment..." -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    # Activate the virtual environment
    & .venv\Scripts\Activate.ps1
    
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
    Write-Host "📚 Available frameworks:" -ForegroundColor Cyan
    Write-Host "   - CrewAI: Multi-agent framework" -ForegroundColor White
    Write-Host "   - OpenAI: GPT models and API" -ForegroundColor White
    Write-Host "   - LangChain: LLM application framework" -ForegroundColor White
    Write-Host "   - LangGraph: State machine workflows" -ForegroundColor White
    Write-Host "   - AutoGen: Microsoft's multi-agent framework" -ForegroundColor White
    Write-Host "   - FastAPI: Modern web API framework" -ForegroundColor White
    Write-Host "   - Gradio: ML model interfaces" -ForegroundColor White
    Write-Host "   - Streamlit: Data science web apps" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Quick commands:" -ForegroundColor Yellow
    Write-Host "   python verify_setup.py    # Verify all frameworks" -ForegroundColor White
    Write-Host "   python setup.py           # Re-run setup if needed" -ForegroundColor White
    Write-Host ""
    Write-Host "📁 Project structure:" -ForegroundColor Yellow
    Write-Host "   startup_funding/          # Startup funding crew" -ForegroundColor White
    Write-Host "   career_conversation/      # Career conversation project" -ForegroundColor White
    Write-Host "   deep_research/            # Deep research project" -ForegroundColor White
    Write-Host "   email_sender/             # Email automation project" -ForegroundColor White
    Write-Host "   sales_agents_guardrails/  # Sales agents project" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Ready to build AI agents!" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run 'python setup.py' first to create the environment." -ForegroundColor Yellow
}
