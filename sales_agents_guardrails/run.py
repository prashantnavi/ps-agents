#!/usr/bin/env python3
"""
Simple run script for the Sales Agents with Guardrails application.

This script provides an easy way to run the application with different configurations.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.app import SalesAgentApplication
from config import config


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🚀 Sales Agents with Guardrails")
    print("   AI-powered sales email automation with compliance guardrails")
    print("=" * 60)
    print()


def print_usage_examples():
    """Print usage examples."""
    print("📖 Usage Examples:")
    print()
    print("1. Run with default test messages:")
    print("   python run.py")
    print()
    print("2. Run with custom message:")
    print("   python run.py --message 'Your custom message here'")
    print()
    print("3. Run basic workflow (without guardrails):")
    print("   python run.py --workflow basic")
    print()
    print("4. Run protected workflow (with guardrails):")
    print("   python run.py --workflow protected")
    print()
    print("5. Run comparison (both workflows):")
    print("   python run.py --workflow comparison")
    print()


async def run_application(workflow_type: str, custom_message: str = None):
    """
    Run the application with specified configuration.
    
    Args:
        workflow_type (str): Type of workflow to run ('basic', 'protected', 'comparison')
        custom_message (str): Custom message to use instead of default test messages
    """
    print_banner()
    
    # Initialize the application
    print("🔧 Initializing application...")
    app = SalesAgentApplication()
    
    # Validate setup
    print("✅ Validating configuration...")
    if not app.validate_setup():
        print("❌ Application setup validation failed!")
        print("   Please check your API keys and configuration.")
        return
    
    print("✅ Configuration validated successfully!")
    print()
    
    # Determine messages to use
    if custom_message:
        messages = [custom_message]
    else:
        messages = [
            "Send out a cold sales email addressed to Dear CEO from our sales team",
            "Send out a cold sales email addressed to Dear CEO from our business development team"
        ]
    
    # Run the specified workflow
    for i, message in enumerate(messages, 1):
        print(f"📧 Running test {i}: {message}")
        print("-" * 50)
        
        try:
            if workflow_type == "basic":
                await app.run_basic_workflow(message)
            elif workflow_type == "protected":
                await app.run_protected_workflow(message)
            elif workflow_type == "comparison":
                await app.run_comparison_workflow(message)
            else:
                print(f"❌ Unknown workflow type: {workflow_type}")
                return
                
            print(f"✅ Test {i} completed successfully!")
            
        except Exception as e:
            print(f"❌ Test {i} failed with error: {e}")
        
        print()
    
    print("🎉 All tests completed!")


def main():
    """Main entry point for the run script."""
    parser = argparse.ArgumentParser(
        description="Run the Sales Agents with Guardrails application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                                    # Run with default settings
  python run.py --message "Custom message"        # Run with custom message
  python run.py --workflow basic                  # Run basic workflow
  python run.py --workflow protected              # Run protected workflow
  python run.py --workflow comparison             # Run both workflows
        """
    )
    
    parser.add_argument(
        "--workflow",
        choices=["basic", "protected", "comparison"],
        default="protected",
        help="Type of workflow to run (default: protected)"
    )
    
    parser.add_argument(
        "--message",
        type=str,
        help="Custom message to use instead of default test messages"
    )
    
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show usage examples and exit"
    )
    
    args = parser.parse_args()
    
    if args.examples:
        print_usage_examples()
        return
    
    # Run the application
    try:
        asyncio.run(run_application(args.workflow, args.message))
    except KeyboardInterrupt:
        print("\n⏹️  Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
