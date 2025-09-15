"""
Legacy App Entry Point
Updated to use the new modular architecture and fix async issues.
This file maintains backward compatibility while using the new modular structure.
"""

import asyncio
from config import validate_config
from workflows import (
    test_email,
    generate_email,
    generate_email_streamed,
    generate_emails_parallel,
    select_best,
    run_simple_workflow,
    run_automated_workflow
)


async def main():
    """Main function that demonstrates the modular email sender functionality."""
    
    print("🚀 Email Sender Application - Modular Version")
    print("=" * 60)
    
    # Validate configuration
    try:
        validate_config()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Test email service
    print("\n🧪 Testing email service...")
    try:
        status = await test_email()
        print(f"✅ Email test completed with status: {status}")
    except Exception as e:
        print(f"❌ Email test failed: {e}")
    
    # Generate single email with streaming
    print("\n📧 Generating single email with streaming...")
    try:
        await generate_email_streamed(agent_index=0)
    except Exception as e:
        print(f"❌ Streaming email generation failed: {e}")
    
    # Generate parallel emails
    print("\n🚀 Generating parallel emails...")
    try:
        emails = await generate_emails_parallel()
        print(f"✅ Generated {len(emails)} emails")
        
        # Display all emails
        for i, email in enumerate(emails):
            print(f"\nEmail {i+1}:\n{email}\n")
    except Exception as e:
        print(f"❌ Parallel generation failed: {e}")
    
    # Select best email
    print("\n🎯 Selecting best email...")
    try:
        best_email = await select_best()
        print(f"✅ Best email selected:\n{best_email}")
    except Exception as e:
        print(f"❌ Email selection failed: {e}")
    
    # Run simple workflow
    print("\n📧 Running simple workflow...")
    try:
        result = await run_simple_workflow()
        print(f"✅ Simple workflow completed:\n{result}")
    except Exception as e:
        print(f"❌ Simple workflow failed: {e}")
    
    # Run automated workflow
    print("\n🤖 Running automated workflow...")
    try:
        result = await run_automated_workflow()
        print(f"✅ Automated workflow completed:\n{result}")
    except Exception as e:
        print(f"❌ Automated workflow failed: {e}")
    
    print("\n🎉 All workflows completed successfully!")


if __name__ == "__main__":
    # Fix for async/await issue: wrap in asyncio.run()
    asyncio.run(main())
