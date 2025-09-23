# Financial Research Crew

A CrewAI-based financial research agent that analyzes companies and generates comprehensive reports.

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Fill in your actual API keys:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_openai_api_key_here
     ```

3. **Run the crew:**
   ```bash
   uv run run_crew
   ```

## Configuration

The crew uses two agents:
- **Researcher**: Gathers information about the target company
- **Analyst**: Analyzes the research and creates a comprehensive report

## Output

The analysis report will be saved to `output/report.md`.

## Troubleshooting

If you encounter authentication errors:
1. Ensure your `.env` file exists and contains a valid `OPENAI_API_KEY`
2. Verify your OpenAI API key has sufficient credits
3. Check that the API key has the necessary permissions