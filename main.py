#!/usr/bin/env python3
"""
SmartStudy AI - Multi-Agent Learning System
Main application file that brings all agents together
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if we're in production (Cloud Run sets K_SERVICE)
if os.getenv('K_SERVICE'):
    from config.production import prod_config
    print("🚀 Running in PRODUCTION mode (Google Cloud Run)")
else:
    print("🔧 Running in DEVELOPMENT mode")

# Import our agents and coordinator
from agents.coordinator import coordinator
from agents.student_profile_agent import student_agent
from utils.logger import logger

# -----------------------------
# Health Check Endpoint
# -----------------------------
def health_check():
    """Simple health check for Google Cloud"""
    return {
        "status": "healthy",
        "service": "SmartStudy AI",
        "version": "1.0.0"
    }

def simple_web_server():
    """Basic web server for Cloud Run health checks"""
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = health_check()
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.end_headers()

    # Only start web server in production
    if os.getenv('K_SERVICE'):
        port = int(os.getenv('PORT', 8080))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🌐 Health check server running on port {port}")
        server.serve_forever()

# -----------------------------
# Main Application Entry Point
# -----------------------------
def main():
    # Your existing main function logic
    print("🤖 Starting SmartStudy AI agents...")
    # Example: start coordinator or other agents
    coordinator.run()
    # student_agent.run()  # Uncomment if you have a run method

# Optional: start simple web server if in production
if __name__ == "__main__":
    if os.getenv('K_SERVICE'):
        simple_web_server()
    else:
        main()
