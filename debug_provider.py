import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Debugging AI Provider Configuration...")
print(f"AI_PROVIDER: {os.getenv('AI_PROVIDER')}")
print(f"DEEPSEEK_API_KEY exists: {bool(os.getenv('DEEPSEEK_API_KEY'))}")
print(f"OPENAI_API_KEY exists: {bzool(os.getenv('OPENAI_API_KEY'))}")

# Test the API handler directly
try:
    from api_handler import UniversalAIHandler
    print("✅ api_handler imported successfully")
    
    handler = UniversalAIHandler()
    print(f"✅ AI Handler initialized: {handler.provider.get_provider_name()}")
    
except Exception as e:
    print(f"❌ Failed to initialize AI Handler: {e}")
    print("💡 Checking .env file...")
    
    # Check if .env file exists and has content
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            print("📄 .env file content:")
            print(env_content)
    except Exception as env_error:
        print(f"❌ Cannot read .env file: {env_error}")

# Test code reviewer
try:
    from code_reviewer import CodeReviewer
    print("✅ code_reviewer imported successfully")
    
    reviewer = CodeReviewer()
    print("✅ CodeReviewer initialized successfully")
    
except Exception as e:
    print(f"❌ Failed to initialize CodeReviewer: {e}")