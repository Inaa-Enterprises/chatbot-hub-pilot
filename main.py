from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import sys
import argparse

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

# Import blueprints
from agent_routes import agent_bp
import personas

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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