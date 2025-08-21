#!/usr/bin/env python3
"""
Simple script to run the Flask backend server
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_server(port=8000, debug=False, host='0.0.0.0'):
    """Run the Flask server"""
    print(f"🚀 Starting server on {host}:{port}")
    print(f"   Debug mode: {debug}")
    print(f"   URL: http://{host}:{port}")
    print("=" * 50)
    
    try:
        # Import and run the app
        from main import app
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    parser = argparse.ArgumentParser(description="Run the Synapse Backend server")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to run on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    parser.add_argument("--install", "-i", action="store_true", help="Install requirements first")
    parser.add_argument("--test", "-t", action="store_true", help="Run tests after starting")
    
    args = parser.parse_args()
    
    # Install requirements if requested
    if args.install:
        if not install_requirements():
            sys.exit(1)
    
    # Check if requirements are installed
    try:
        import flask
    except ImportError:
        print("❌ Flask not found. Run with --install to install requirements.")
        sys.exit(1)
    
    # Run tests if requested
    if args.test:
        print("🧪 Running integration tests...")
        try:
            subprocess.check_call([sys.executable, "test_integration.py", "--wait", "--timeout", "10"])
            print("✅ All tests passed!")
        except subprocess.CalledProcessError:
            print("❌ Some tests failed")
            sys.exit(1)
    
    # Run the server
    run_server(args.port, args.debug, args.host)

if __name__ == "__main__":
    main()