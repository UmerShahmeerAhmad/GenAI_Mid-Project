import os
import requests
import json
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class BaseAIProvider(ABC):
    """Abstract base class for all AI providers"""
    
    @abstractmethod
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        pass
    
    @abstractmethod
    def get_provider_name(self):
        pass
# ADD THIS CLASS TO YOUR EXISTING api_handler.py file

class DeepSeekProvider(BaseAIProvider):
    """DeepSeek API implementation"""
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        if not self.api_key:
            raise ValueError("❌ DEEPSEEK_API_KEY not found in .env file")
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",  # or "deepseek-coder" for code-specific model
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=45
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"DeepSeek API Error {response.status_code}: {response.text}")
    
    def get_provider_name(self):
        return "DeepSeek"

class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT API implementation"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
        if not self.api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in .env file")
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=45
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API Error {response.status_code}: {response.text}")
    
    def get_provider_name(self):
        return "OpenAI GPT"


class OllamaProvider(BaseAIProvider):
    """Ollama Local API implementation"""
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/api/chat')
        self.model = os.getenv('OLLAMA_MODEL', 'codellama')
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(
            self.base_url,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"Ollama API Error {response.status_code}: {response.text}")
    
    def get_provider_name(self):
        return f"Ollama ({self.model})"


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude API implementation"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.base_url = "https://api.anthropic.com/v1/messages"
        if not self.api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY not found in .env file")
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_message,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=45
        )
        
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            raise Exception(f"Anthropic API Error {response.status_code}: {response.text}")
    
    def get_provider_name(self):
        return "Anthropic Claude"

# ADD THIS CLASS TO YOUR api_handler.py

class GrokProvider(BaseAIProvider):
    """Grok API implementation (xAI)"""
    
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')
        self.base_url = "https://api.x.ai/v1/chat/completions"
        if not self.api_key:
            raise ValueError("❌ GROK_API_KEY not found in .env file")
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "grok-beta",  # Grok model name
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=45
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Grok API Error {response.status_code}: {response.text}")
    
    def get_provider_name(self):
        return "Grok (xAI)"

# ADD THIS CLASS TO YOUR api_handler.py


class GeminiProvider(BaseAIProvider):
    """Google Gemini API implementation - AUTO MODEL DETECTION"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")
        
        try:
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Auto-detect available model
            self.model_name = self._find_working_model()
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ Using model: {self.model_name}")
            
        except Exception as e:
            raise ValueError(f"❌ Gemini configuration failed: {e}")
    
    def _find_working_model(self):
        """Find a model that supports generateContent"""
        try:
            models = genai.list_models()
            
            # Try these model names in order
            preferred_models = [
                'gemini-pro',
                'models/gemini-pro',
                'gemini-1.0-pro',
                'models/gemini-1.0-pro'
            ]
            
            # Check available models
            available_model_names = [model.name for model in models]
            print(f"🔍 Available models: {available_model_names}")
            
            # Find first preferred model that exists and supports generateContent
            for model_name in preferred_models:
                for model in models:
                    if model.name == model_name and 'generateContent' in model.supported_generation_methods:
                        print(f"🎯 Selected model: {model_name}")
                        return model_name
            
            # If no preferred model found, use first available model that supports generateContent
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"⚡ Fallback model: {model.name}")
                    return model.name
            
            raise Exception("No models found that support generateContent")
            
        except Exception as e:
            print(f"⚠️  Could not list models: {e}")
            # Fallback to gemini-pro
            return 'gemini-pro'
    
    def generate_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        try:
            # Combine system message and prompt
            full_prompt = f"{system_message}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.8
                )
            )
            
            if not response.parts:
                if response.prompt_feedback.block_reason:
                    raise Exception(f"Content blocked: {response.prompt_feedback.block_reason}")
                else:
                    raise Exception("Empty response from Gemini")
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Gemini API Error: {str(e)}")
    
    def get_provider_name(self):
        return f"Gemini ({self.model_name})"
    

class AIProviderFactory:
    """Factory class to create AI providers"""
    
    @staticmethod
    def create_provider(provider_name):
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            return OpenAIProvider()
        elif provider_name == "ollama":
            return OllamaProvider()
        elif provider_name == "anthropic":
            return AnthropicProvider()
        elif provider_name == "deepseek":  # ADD THIS LINE
            return DeepSeekProvider()      # ADD THIS LINE
        elif provider_name == "grok":  # ADD THIS LINE
            return GrokProvider()      # ADD THIS LINE
        elif provider_name == "gemini":  # ADD THIS LINE
            return GeminiProvider()      # ADD THIS LINE
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")


class UniversalAIHandler:
    """
    Universal handler that works with any AI provider
    Only change the provider in .env file to switch models
    """
    
    def __init__(self):
        # Get provider from environment variable (default: openai)
        self.provider_name = os.getenv('AI_PROVIDER', 'openai').lower()
        self.provider = AIProviderFactory.create_provider(self.provider_name)
        print(f"✅ Initialized {self.provider.get_provider_name()}")
    
    def get_response(self, prompt, system_message, max_tokens=2000, temperature=0.3):
        """
        Universal method to get response from any provider
        
        Args:
            prompt (str): User prompt
            system_message (str): System instructions
            max_tokens (int): Maximum response length
            temperature (float): Creativity level (0-1)
        
        Returns:
            str: AI response
        """
        try:
            return self.provider.generate_response(
                prompt, 
                system_message, 
                max_tokens, 
                temperature
            )
        except Exception as e:
            return f"❌ Error from {self.provider.get_provider_name()}: {str(e)}"


# Test the universal handler
def test_providers():
    """Test all available providers"""
    test_prompt = "What is 2+2? Answer very briefly."
    system_message = "You are a helpful assistant."
    
    providers_to_test = ['openai']  # Add 'ollama', 'anthropic' if you have their keys
    
    for provider_name in providers_to_test:
        try:
            print(f"\n🧪 Testing {provider_name}...")
            handler = UniversalAIHandler()
            # Temporarily override provider for testing
            handler.provider = AIProviderFactory.create_provider(provider_name)
            
            response = handler.get_response(test_prompt, system_message)
            print(f"✅ {provider_name} Response: {response}")
            
        except Exception as e:
            print(f"❌ {provider_name} Failed: {e}")


if __name__ == "__main__":
    test_providers()