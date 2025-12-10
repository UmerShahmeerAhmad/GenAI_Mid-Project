from api_handler import AIProviderFactory
import time
import os

def compare_providers():
    """Compare response quality and speed between providers"""
    
    test_code = """
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
"""
    
    system_message = "You are an expert code reviewer. Provide structured feedback."
    prompt = f"Review this Python code for efficiency and suggest improvements:\n```python\n{test_code}\n```"
    
    providers_to_test = ['deepseek']  # Add 'openai' if you want to compare
    
    for provider_name in providers_to_test:
        print(f"\n{'='*50}")
        print(f"Testing: {provider_name.upper()}")
        print(f"{'='*50}")
        
        try:
            provider = AIProviderFactory.create_provider(provider_name)
            
            start_time = time.time()
            response = provider.generate_response(prompt, system_message, max_tokens=800)
            end_time = time.time()
            
            print(f"✅ Response time: {end_time - start_time:.2f} seconds")
            print(f"✅ Provider: {provider.get_provider_name()}")
            print(f"✅ Response preview:")
            print(response[:400] + "..." if len(response) > 400 else response)
            
        except Exception as e:
            print(f"❌ {provider_name} failed: {e}")

if __name__ == "__main__":
    compare_providers()