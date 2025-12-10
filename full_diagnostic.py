import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 COMPLETE DIAGNOSTIC")
print("=" * 50)

# Check environment variables
print("📋 Environment Variables:")
print(f"AI_PROVIDER: {os.getenv('AI_PROVIDER')}")
print(f"OPENAI_API_KEY exists: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"OPENAI_API_KEY starts with 'sk-': {os.getenv('OPENAI_API_KEY', '').startswith('sk-')}")
print(f"OPENAI_API_KEY length: {len(os.getenv('OPENAI_API_KEY', ''))}")

# Check Python environment
print("\n🐍 Python Environment:")
try:
    import sys
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path[:3]}")
except:
    pass

# Test basic imports
print("\n📦 Testing Imports:")
try:
    import flask
    print("✅ flask imported")
except Exception as e:
    print(f"❌ flask import failed: {e}")

try:
    import requests
    print("✅ requests imported")
except Exception as e:
    print(f"❌ requests import failed: {e}")

# Test API handler
print("\n🤖 Testing API Handler:")
try:
    from api_handler import UniversalAIHandler
    print("✅ api_handler imported")
    
    handler = UniversalAIHandler()
    print(f"✅ AI Handler initialized: {handler.provider.get_provider_name()}")
    
    # Test a simple request
    test_response = handler.get_response("Say 'Hello'", "You are a helper", max_tokens=10)
    print(f"✅ API test successful: {test_response[:50]}...")
    
except Exception as e:
    print(f"❌ API Handler failed: {e}")
    import traceback
    traceback.print_exc()

# Test code reviewer
print("\n🔍 Testing Code Reviewer:")
try:
    from code_reviewer import CodeReviewer
    print("✅ code_reviewer imported")
    
    reviewer = CodeReviewer()
    print("✅ CodeReviewer initialized")
    
    # Test simple review
    test_code = "def hello(): return 'world'"
    result = reviewer.review_code(test_code)
    print("✅ Code review test passed")
    print(f"Result keys: {list(result.keys())}")
    
except Exception as e:
    print(f"❌ CodeReviewer failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🎯 DIAGNOSTIC COMPLETE")