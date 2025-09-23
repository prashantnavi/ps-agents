#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from stock_planner.crew import StockPlanner
from dotenv import load_dotenv

# Path to your global .env (adjust if different)
root_env_path = r"D:\AIAgents\MY-WORK\my-workflows\.env"
load_dotenv(root_env_path)

# Set the environment variable for the current process
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    print("OPENAI_API_KEY set successfully")
else:
    print("OPENAI_API_KEY not found in .env file")


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the research crew.
    """
    inputs = {
        'sector': 'fintech',
        "current_date": str(datetime.now())
    }

    # Create and run the crew
    result = StockPlanner().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
