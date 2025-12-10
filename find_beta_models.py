import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def find_beta_models():
    print("🔍 Finding available models in v1beta API...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    try:
        genai.configure(api_key=api_key)
        
        # List all available models
        models = genai.list_models()
        
        print("✅ Available Models in your API:")
        for i, model in enumerate(models):
            print(f"\n{i+1}. 📦 {model.name}")
            print(f"   📝 Description: {model.description}")
            print(f"   🛠️  Methods: {model.supported_generation_methods}")
            
        # Find models that support generateContent
        print("\n🎯 Models that support generateContent:")
        working_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                working_models.append(model.name)
                print(f"✅ {model.name}")
        
        if working_models:
            print(f"\n💡 Use this model: {working_models[0]}")
        else:
            print("\n❌ No models support generateContent")
            
        return working_models
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_beta_models()