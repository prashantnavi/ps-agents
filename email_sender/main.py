"""
Main Application Module
Orchestrates all modules and provides a clean interface for the email sender application.
"""

import asyncio
import sys
from typing import Optional

# Import all modules
from config import validate_config
from workflows import (
    test_email,
    generate_email,
    generate_email_streamed,
    generate_emails_parallel,
    select_best,
    run_automated_workflow,
    run_simple_workflow
)


class EmailSenderApp:
    """Main application class for the Email Sender system."""
    
    def __init__(self):
        """Initialize the application."""
        self.setup_complete = False
    
    async def setup(self):
        """Setup and validate the application configuration."""
        try:
            print("🚀 Initializing Email Sender Application...")
            validate_config()
            self.setup_complete = True
            print("✅ Application setup completed successfully")
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            sys.exit(1)
    
    async def run_demo(self):
        """Run a complete demo of all features."""
        if not self.setup_complete:
            await self.setup()
        
        print("\n" + "="*60)
        print("🎬 EMAIL SENDER DEMO")
        print("="*60)
        
        # Test email service
        print("\n1️⃣ Testing email service...")
        await test_email()
        
        # Generate single email
        print("\n2️⃣ Generating single email...")
        email = await generate_email(agent_index=0)
        print(f"Generated email:\n{email[:200]}...")
        
        # Generate parallel emails
        print("\n3️⃣ Generating parallel emails...")
        emails = await generate_emails_parallel()
        print(f"Generated {len(emails)} emails")
        
        # Select best email
        print("\n4️⃣ Selecting best email...")
        best_email = await select_best()
        print(f"Best email:\n{best_email[:200]}...")
        
        # Run simple workflow
        print("\n5️⃣ Running simple workflow...")
        result = await run_simple_workflow()
        print(f"Workflow result:\n{result[:200]}...")
        
        print("\n✅ Demo completed successfully!")
    
    async def interactive_mode(self):
        """Run the application in interactive mode."""
        if not self.setup_complete:
            await self.setup()
        
        print("\n" + "="*60)
        print("🎮 INTERACTIVE MODE")
        print("="*60)
        print("Available commands:")
        print("1. test - Test email service")
        print("2. generate <agent> - Generate email (0=Professional, 1=Humorous, 2=Concise)")
        print("3. stream <agent> - Generate email with streaming")
        print("4. parallel - Generate emails from all agents")
        print("5. select - Generate and select best email")
        print("6. simple - Run simple workflow")
        print("7. automated - Run automated workflow")
        print("8. demo - Run complete demo")
        print("9. quit - Exit application")
        
        while True:
            try:
                command = input("\nEnter command: ").strip().lower()
                
                if command == "quit":
                    print("👋 Goodbye!")
                    break
                elif command == "test":
                    await test_email()
                elif command.startswith("generate "):
                    try:
                        agent_index = int(command.split()[1])
                        email = await generate_email(agent_index)
                        print(f"\nGenerated email:\n{email}")
                    except (IndexError, ValueError):
                        print("❌ Usage: generate <agent> (0, 1, or 2)")
                elif command.startswith("stream "):
                    try:
                        agent_index = int(command.split()[1])
                        await generate_email_streamed(agent_index)
                    except (IndexError, ValueError):
                        print("❌ Usage: stream <agent> (0, 1, or 2)")
                elif command == "parallel":
                    emails = await generate_emails_parallel()
                    for i, email in enumerate(emails):
                        print(f"\nEmail {i+1}:\n{email}")
                elif command == "select":
                    best_email = await select_best()
                    print(f"\nBest email:\n{best_email}")
                elif command == "simple":
                    result = await run_simple_workflow()
                    print(f"\nWorkflow result:\n{result}")
                elif command == "automated":
                    result = await run_automated_workflow()
                    print(f"\nWorkflow result:\n{result}")
                elif command == "demo":
                    await self.run_demo()
                else:
                    print("❌ Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Main entry point for the application."""
    app = EmailSenderApp()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            await app.run_demo()
        elif command == "test":
            await app.setup()
            await test_email()
        elif command == "generate":
            await app.setup()
            agent_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            email = await generate_email(agent_index)
            print(email)
        elif command == "parallel":
            await app.setup()
            emails = await generate_emails_parallel()
            for i, email in enumerate(emails):
                print(f"\nEmail {i+1}:\n{email}")
        elif command == "select":
            await app.setup()
            best_email = await select_best()
            print(best_email)
        elif command == "simple":
            await app.setup()
            result = await run_simple_workflow()
            print(result)
        elif command == "automated":
            await app.setup()
            result = await run_automated_workflow()
            print(result)
        else:
            print("❌ Unknown command. Available: demo, test, generate, parallel, select, simple, automated")
    else:
        # Run in interactive mode
        await app.interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())
