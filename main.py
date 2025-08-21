from flask import Flask, jsonify, send_from_directory, request, Response
from flask_cors import CORS
import os
import logging
import sys
import argparse
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import blueprints and services
from agent_routes import agent_bp
import personas
from services import AIService
from user_api_service import UserAPIService

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize AI services
ai_service = AIService()
user_api_service = UserAPIService()

# Register blueprints
app.register_blueprint(agent_bp, url_prefix='/api')

# Default route
@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "Synapse Backend is running"})

# Health check route
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

# Personas endpoint
@app.route('/api/personas', methods=['GET'])
def list_personas():
    """List available personas"""
    persona_list = []
    for persona_id, persona_data in personas.PERSONAS.items():
        persona_list.append({
            "id": persona_data["id"],
            "name": persona_data["name"],
            "icon": persona_data["icon"],
            "tagline": persona_data["tagline"]
        })
    return jsonify(persona_list)

# Templates endpoint
@app.route('/api/templates', methods=['GET'])
def list_templates():
    """List available templates"""
    templates = [
        {
            "id": "blog-post",
            "name": "Blog Post",
            "description": "Generate a well-structured blog post"
        },
        {
            "id": "social-media",
            "name": "Social Media Post",
            "description": "Create engaging social media content"
        },
        {
            "id": "email",
            "name": "Email",
            "description": "Write professional emails"
        },
        {
            "id": "code-explanation",
            "name": "Code Explanation",
            "description": "Explain code concepts and snippets"
        }
    ]
    return jsonify(templates)

# Models endpoint
@app.route('/api/models', methods=['GET'])
def list_models():
    """List available models"""
    models = user_api_service.list_available_models()
    return jsonify(models)

# Chat endpoint with user-provided API key
@app.route('/api/chat-with-key', methods=['POST'])
def chat_with_key():
    """Handle chat messages with user-provided API key"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get("message")
        persona_id = data.get("personaId", "synapse")
        api_key = data.get("apiKey")
        model = data.get("model", "microsoft/DialoGPT-large")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
            
        if not api_key:
            return jsonify({"error": "API key is required"}), 400
        
        # Get system instruction for the persona
        system_instruction = personas.get_system_instruction(persona_id)
        
        # Generate response using the user-provided API key
        response = user_api_service.generate_response_with_key(
            api_key=api_key,
            system_instruction=system_instruction,
            message=message,
            model=model
        )
        
        return jsonify({"response": response})
        
    except Exception as e:
        logger.error(f"Error in chat-with-key endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Chat endpoint with server-configured API key
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get("message")
        persona_id = data.get("personaId", "synapse")
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get system instruction for the persona
        system_instruction = personas.get_system_instruction(persona_id)
        
        # Generate response using the AI service
        def generate():
            try:
                import asyncio
                # For simplicity in this Flask app, we'll use the sync version
                from huggingface_service import HuggingFaceService
                hf_service = HuggingFaceService()
                response = hf_service.generate_response(system_instruction, message)
                yield response
            except Exception as e:
                yield f"Error: {str(e)}"
        
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# API key validation endpoint
@app.route('/api/validate-key', methods=['POST'])
def validate_key():
    """Validate a Hugging Face API key"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        api_key = data.get("apiKey")
        
        if not api_key:
            return jsonify({"error": "API key is required"}), 400
        
        is_valid = user_api_service.validate_api_key(api_key)
        
        return jsonify({"valid": is_valid})
        
    except Exception as e:
        logger.error(f"Error in validate-key endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Synapse Backend Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    args = parser.parse_args()
    
    port = int(os.environ.get('PORT', args.port))  # Use PORT environment variable if available (for Render)
    host = os.environ.get('HOST', args.host)  # Use HOST environment variable if available
    debug = args.debug
    
    print(f"Starting Synapse Backend server on {host}:{port}")
    
    app.run(host=host, port=port, debug=debug)