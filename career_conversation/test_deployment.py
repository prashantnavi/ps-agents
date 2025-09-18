"""
Test script to verify the app is ready for Hugging Face deployment
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import gradio as gr
        print(f"✅ Gradio {gr.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        from pypdf import PdfReader
        print("✅ PyPDF imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    return True

def test_app_structure():
    """Test that the app structure is correct"""
    print("\n🔍 Testing app structure...")
    
    import os
    
    required_files = [
        "app.py",
        "requirements.txt", 
        "README.md",
        ".gitignore"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True

def test_app_import():
    """Test that the app can be imported"""
    print("\n📱 Testing app import...")
    
    try:
        # Import the app module
        import sys
        sys.path.append('.')
        
        # Try to import the main components
        from app import Me, create_interface
        print("✅ App components imported successfully")
        
        # Test creating the interface
        interface = create_interface()
        print("✅ Interface created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 HUGGING FACE DEPLOYMENT TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("App Structure Test", test_app_structure),
        ("App Import Test", test_app_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 TEST RESULTS")
    print("=" * 30)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Your app is ready for Hugging Face deployment!")
        print("\nNext steps:")
        print("1. Create a new Space on Hugging Face")
        print("2. Upload all files to your Space")
        print("3. Set OPENAI_API_KEY environment variable")
        print("4. Deploy and test!")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    main()
