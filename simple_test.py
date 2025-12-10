print("🧪 Starting simple test...")

try:
    # Test basic imports
    import os
    import re
    print("✅ Basic imports work")
    
    # Test API handler
    from api_handler import UniversalAIHandler
    print("✅ API handler imported")
    
    # Test creating handler
    handler = UniversalAIHandler()
    print(f"✅ Handler created: {handler.provider.get_provider_name()}")
    
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()