#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from financial_research.crew import FinancialResearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Check for required environment variables
def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 To fix this:")
        print("   1. Create a .env file in the project root")
        print("   2. Add your API keys:")
        for var in missing_vars:
            print(f"      {var}=your_actual_api_key_here")
        print("   3. Or set the environment variable directly:")
        for var in missing_vars:
            print(f"      export {var}=your_actual_api_key_here")
        return False
    
    return True

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Check environment before running
    if not check_environment():
        sys.exit(1)
    
    inputs = {
        'company': 'Apple',
        'current_year': str(datetime.now().year)
    }
    
    try:
        FinancialResearch().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "company": "Apple",
        'current_year': str(datetime.now().year)
    }
    try:
        FinancialResearch().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FinancialResearch().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "company": "Apple",
        "current_year": str(datetime.now().year)
    }
    
    try:
        FinancialResearch().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
