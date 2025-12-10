import os
import re
from api_handler import UniversalAIHandler

class CodeReviewer:
    def __init__(self):
        print("🚀 Initializing CodeReviewer...")
        self.ai_handler = UniversalAIHandler()
        self.system_message = "You are a code reviewer. Review code and provide feedback."
        print("✅ CodeReviewer initialized!")

    def detect_language(self, code):
        code_lower = code.lower()
        if 'def ' in code_lower or 'import ' in code_lower:
            return 'python'
        elif 'function' in code_lower or 'const ' in code_lower:
            return 'javascript'
        else:
            return 'python'

    def create_review_prompt(self, code, language, focus_areas=None):
        prompt = f"Review this {language} code:\n```{language}\n{code}\n```\n"
        prompt += "Provide feedback on bugs, security, performance, and code quality."
        return prompt

    def review_code(self, code, focus_areas=None, language=None):
        print("🔍 Starting code review...")
        try:
            if not language:
                language = self.detect_language(code)
            
            prompt = self.create_review_prompt(code, language, focus_areas)
            
            response = self.ai_handler.get_response(
                prompt=prompt,
                system_message=self.system_message,
                max_tokens=1000
            )
            
            return {
                "full_review": response,
                "summary": "Review completed successfully",
                "rating": 7,
                "language": language,
                "provider": self.ai_handler.provider.get_provider_name()
            }
            
        except Exception as e:
            print(f"❌ Error in review_code: {e}")
            return {"error": str(e)}

def test_simple():
    print("🧪 SIMPLE TEST STARTING...")
    
    # Very simple test code
    test_code = "def hello(): return 'world'"
    
    try:
        reviewer = CodeReviewer()
        print("✅ Reviewer created successfully")
        
        result = reviewer.review_code(test_code)
        print("✅ Review completed!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()

def _get_system_message(self):
    """System message for code review"""
    provider_name = self.ai_handler.provider.get_provider_name().lower()
    
    base_message = """You are an expert code reviewer. Perform comprehensive code reviews.

Provide STRUCTURED reviews with these sections:

1. **CODE SUMMARY** - What the code does and overall quality
2. **BUGS & LOGICAL ERRORS** 🔴 - Syntax/runtime errors, logical mistakes
3. **SECURITY ISSUES** 🛡️ - Vulnerabilities and security improvements  
4. **PERFORMANCE ISSUES** ⚡ - Inefficient patterns and optimizations
5. **CODE QUALITY** ✅ - Readability, naming, best practices
6. **MAINTAINABILITY** 🔧 - Organization, documentation, error handling
7. **SUGGESTED IMPROVEMENTS** 💡 - Actionable improvements with code examples
8. **OVERALL RATING** ⭐ - Rate 1-10 with justification

Be CRITICAL but CONSTRUCTIVE. Provide CODE EXAMPLES for fixes.
Use markdown formatting for better readability."""
    
    # Gemini-specific optimizations
    if 'gemini' in provider_name:
        base_message += """
        
Note: Please provide clear, structured analysis with practical coding examples. Focus on actionable improvements."""
    
    return base_message 