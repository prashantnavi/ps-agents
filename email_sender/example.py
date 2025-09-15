"""
Example Script
Demonstrates how to use the modular email sender components.
"""

import asyncio
from config import validate_config
from workflows import (
    test_email,
    generate_email,
    generate_emails_parallel,
    select_best,
    run_simple_workflow
)


async def example_usage():
    """Example usage of the email sender modules."""
    
    print("🎯 Email Sender Example Usage")
    print("=" * 50)
    
    # Validate configuration
    try:
        validate_config()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Example 1: Test email service
    print("\n1️⃣ Testing email service...")
    try:
        status = await test_email()
        print(f"✅ Email test completed with status: {status}")
    except Exception as e:
        print(f"❌ Email test failed: {e}")
    
    # Example 2: Generate single email
    print("\n2️⃣ Generating single email...")
    try:
        email = await generate_email(agent_index=0)  # Professional agent
        print(f"✅ Generated email:\n{email[:200]}...")
    except Exception as e:
        print(f"❌ Email generation failed: {e}")
    
    # Example 3: Generate parallel emails
    print("\n3️⃣ Generating parallel emails...")
    try:
        emails = await generate_emails_parallel()
        print(f"✅ Generated {len(emails)} emails")
        for i, email in enumerate(emails):
            print(f"Email {i+1}: {email[:100]}...")
    except Exception as e:
        print(f"❌ Parallel generation failed: {e}")
    
    # Example 4: Select best email
    print("\n4️⃣ Selecting best email...")
    try:
        best_email = await select_best()
        print(f"✅ Best email selected:\n{best_email[:200]}...")
    except Exception as e:
        print(f"❌ Email selection failed: {e}")
    
    # Example 5: Run simple workflow
    print("\n5️⃣ Running simple workflow...")
    try:
        result = await run_simple_workflow()
        print(f"✅ Workflow completed:\n{result[:200]}...")
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
    
    print("\n🎉 Example usage completed!")


if __name__ == "__main__":
    asyncio.run(example_usage())
