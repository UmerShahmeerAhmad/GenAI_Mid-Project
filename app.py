from flask import Flask, request, jsonify, render_template
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to initialize code reviewer with better error handling
reviewer = None
provider_name = "Unknown"

try:
    from code_reviewer import CodeReviewer
    reviewer = CodeReviewer()
    provider_name = reviewer.ai_handler.provider.get_provider_name()
    logger.info(f"✅ AI Code Reviewer initialized with {provider_name}")
except Exception as e:
    logger.error(f"❌ Failed to initialize CodeReviewer: {e}")
    provider_name = f"Error: {str(e)}"

@app.route('/')
def home():
    """Main page with code input form"""
    return render_template('index.html', provider_name=provider_name)

@app.route('/review', methods=['POST'])
def review_code():
    """Handle code review requests"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', '')
        focus_areas = data.get('focus_areas', [])
        
        logger.info(f"📥 Received review request - Language: {language}, Code length: {len(code)}")
        
        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        if reviewer is None:
            return jsonify({"error": "Code review service unavailable. Check your API configuration."}), 500
        
        # Perform code review
        result = reviewer.review_code(code, focus_areas, language)
        
        logger.info(f"✅ Review completed - Rating: {result.get('rating', 'N/A')}/10")
        
        return jsonify({
            "success": True,
            "review": result
        })
        
    except Exception as e:
        logger.error(f"💥 Review error: {e}")
        return jsonify({"error": f"Review failed: {str(e)}"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    if reviewer:
        return jsonify({
            "status": "healthy", 
            "service": "AI Code Reviewer",
            "provider": provider_name,
            "message": "Ready to review your code! 🚀"
        })
    else:
        return jsonify({
            "status": "unhealthy",
            "message": "Service not available. Check API configuration.",
            "error": provider_name
        }), 500

@app.route('/providers')
def get_providers():
    """Return available AI providers"""
    providers = [
        {"id": "openai", "name": "OpenAI GPT", "enabled": bool(os.getenv('OPENAI_API_KEY'))},
        {"id": "ollama", "name": "Ollama Local", "enabled": bool(os.getenv('OLLAMA_BASE_URL'))},
        {"id": "anthropic", "name": "Anthropic Claude", "enabled": bool(os.getenv('ANTHROPIC_API_KEY'))},
        {"id": "deepseek", "name": "DeepSeek", "enabled": bool(os.getenv('DEEPSEEK_API_KEY'))},
        {"id": "grok", "name": "Grok (xAI)", "enabled": bool(os.getenv('GROK_API_KEY'))},  # ADD THIS LINE
        {"id": "gemini", "name": "Google Gemini", "enabled": bool(os.getenv('GEMINI_API_KEY'))}  # ADD THIS LINE
    ]
    return jsonify({"providers": providers})

if __name__ == '__main__':
    print(f"🚀 Starting AI Code Reviewer Server...")
    print(f"🤖 Provider Status: {provider_name}")
    print(f"📖 Open: http://localhost:5000")
    print(f"🔧 Health check: http://localhost:5000/health")
    print(f"⏹️  Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)