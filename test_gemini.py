import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Debugging Gemini Configuration...")
print(f"AI_PROVIDER: {os.getenv('AI_PROVIDER')}")
print(f"GEMINI_API_KEY exists: {bool(os.getenv('GEMINI_API_KEY'))}")
print(f"GEMINI_API_KEY length: {len(os.getenv('GEMINI_API_KEY', ''))}")

# Test basic imports
try:
    import google.generativeai as genai
    print("✅ google-generativeai imported successfully")
except Exception as e:
    print(f"❌ Failed to import google-generativeai: {e}")
    print("💡 Run: pip install google-generativeai")

# Test API handler
try:
    from api_handler import UniversalAIHandler
    print("✅ api_handler imported successfully")
    
    handler = UniversalAIHandler()
    print(f"✅ AI Handler initialized: {handler.provider.get_provider_name()}")
    
except Exception as e:
    print(f"❌ Failed to initialize AI Handler: {e}")
    import traceback
    traceback.print_exc()

# Test code reviewer
try:
    from code_reviewer import CodeReviewer
    print("✅ code_reviewer imported successfully")
    
    reviewer = CodeReviewer()
    print("✅ CodeReviewer initialized successfully")
    
    # Test a simple review
    result = reviewer.review_code("def test(): pass")
    print("✅ Simple review test passed!")
    print(f"Result: {result}")
    
except Exception as e:
    print(f"❌ Failed to initialize CodeReviewer: {e}")
    import traceback
    traceback.print_exc()