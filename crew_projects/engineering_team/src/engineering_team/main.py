#!/usr/bin/env python
import sys
import warnings
import os
import argparse
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

requirements = """
A simple account management system for a trading simulation platform.
The system should allow users to create an account, deposit funds, and withdraw funds.
The system should allow users to record that they have bought or sold shares, providing a quantity.
The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
The system should be able to report the holdings of the user at any point in time.
The system should be able to report the profit or loss of the user at any point in time.
The system should be able to list the transactions that the user has made over time.
The system should prevent the user from withdrawing funds that would leave them with a negative balance, or
 from buying more shares than they can afford, or selling shares that they don't have.
 The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
"""
module_name = "accounts.py"
class_name = "Account"


def run_minimal():
    """Run the minimal crew for simple projects"""
    print("🚀 Running Minimal Engineering Team (4 agents)")
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    result = EngineeringTeam().minimal_crew().kickoff(inputs=inputs)
    return result


def run_standard():
    """Run the standard crew for medium projects"""
    print("🚀 Running Standard Engineering Team (8 agents)")
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    result = EngineeringTeam().standard_crew().kickoff(inputs=inputs)
    return result


def run_full():
    """Run the full crew for complex projects"""
    print("🚀 Running Full Engineering Team (12 agents)")
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    result = EngineeringTeam().full_crew().kickoff(inputs=inputs)
    return result


def run_sequential():
    """Run the original sequential crew"""
    print("🚀 Running Sequential Engineering Team (12 agents)")
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }
    result = EngineeringTeam().crew().kickoff(inputs=inputs)
    return result


def run_minimal_with_params(req, mod_name, cls_name):
    """Run the minimal crew for simple projects with custom parameters"""
    print("🚀 Running Minimal Engineering Team (4 agents)")
    inputs = {
        'requirements': req,
        'module_name': mod_name,
        'class_name': cls_name
    }
    result = EngineeringTeam().minimal_crew().kickoff(inputs=inputs)
    return result


def run_standard_with_params(req, mod_name, cls_name):
    """Run the standard crew for medium projects with custom parameters"""
    print("🚀 Running Standard Engineering Team (8 agents)")
    inputs = {
        'requirements': req,
        'module_name': mod_name,
        'class_name': cls_name
    }
    result = EngineeringTeam().standard_crew().kickoff(inputs=inputs)
    return result


def run_full_with_params(req, mod_name, cls_name):
    """Run the full crew for complex projects with custom parameters"""
    print("🚀 Running Full Engineering Team (12 agents)")
    inputs = {
        'requirements': req,
        'module_name': mod_name,
        'class_name': cls_name
    }
    result = EngineeringTeam().full_crew().kickoff(inputs=inputs)
    return result


def run_sequential_with_params(req, mod_name, cls_name):
    """Run the original sequential crew with custom parameters"""
    print("🚀 Running Sequential Engineering Team (12 agents)")
    inputs = {
        'requirements': req,
        'module_name': mod_name,
        'class_name': cls_name
    }
    result = EngineeringTeam().crew().kickoff(inputs=inputs)
    return result


def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='Enhanced Engineering Team Crew')
    parser.add_argument(
        '--crew-type', 
        choices=['minimal', 'standard', 'full', 'sequential'],
        default='standard',
        help='Type of crew to run (default: standard)'
    )
    parser.add_argument(
        '--requirements',
        type=str,
        default=requirements,
        help='Custom requirements for the project'
    )
    parser.add_argument(
        '--module-name',
        type=str,
        default=module_name,
        help='Name of the module to create'
    )
    parser.add_argument(
        '--class-name',
        type=str,
        default=class_name,
        help='Name of the main class'
    )
    
    args = parser.parse_args()
    
    # Use local variables instead of global
    project_requirements = args.requirements
    project_module_name = args.module_name
    project_class_name = args.class_name
    
    print(f"📋 Project: {project_class_name} in {project_module_name}")
    print(f"📝 Requirements: {project_requirements[:100]}...")
    print(f"👥 Crew Type: {args.crew_type}")
    print("=" * 60)
    
    start_time = datetime.now()
    
    try:
        if args.crew_type == 'minimal':
            result = run_minimal_with_params(project_requirements, project_module_name, project_class_name)
        elif args.crew_type == 'standard':
            result = run_standard_with_params(project_requirements, project_module_name, project_class_name)
        elif args.crew_type == 'full':
            result = run_full_with_params(project_requirements, project_module_name, project_class_name)
        elif args.crew_type == 'sequential':
            result = run_sequential_with_params(project_requirements, project_module_name, project_class_name)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("=" * 60)
        print(f"✅ Engineering team completed successfully!")
        print(f"⏱️  Total execution time: {duration}")
        print(f"📁 Output files created in: ./output/")
        
        return result
        
    except Exception as e:
        print(f"❌ Error running engineering team: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()