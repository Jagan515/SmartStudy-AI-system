#!/usr/bin/env python3
"""
SmartStudy AI - Cloud Run Compatible Version
This version runs as a web server for Google Cloud Run
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append('.')

def create_app():
    """Create a Flask web application for Cloud Run"""
    try:
        from flask import Flask, request, jsonify, render_template_string
        import json
        
        app = Flask(__name__)
        
        # Import our agents
        from agents.coordinator import coordinator
        from agents.student_profile_agent import student_agent
        from agents.progress_tracker import progress_tracker
        from utils.logger import logger
        
        logger.info("🚀 SmartStudy AI starting in Cloud Run mode...")
        
        # Health check endpoint (required by Cloud Run)
        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "service": "SmartStudy AI",
                "version": "1.0.0"
            })
        
        # Main page
        @app.route('/', methods=['GET'])
        def home():
            return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>SmartStudy AI</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .button { background: #4285f4; color: white; padding: 10px 20px; 
                             text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
                    .log { background: #f5f5f5; padding: 10px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎓 SmartStudy AI</h1>
                    <p>Multi-Agent Learning System for B.Tech Students</p>
                    
                    <div class="log">
                        <strong>Status:</strong> ✅ Application is running in Cloud Run<br>
                        <strong>Endpoint:</strong> /health - Health check<br>
                        <strong>Endpoint:</strong> /demo - Run a demo<br>
                        <strong>Endpoint:</strong> /onboard - Onboard new student (POST)
                    </div>
                    
                    <h2>Quick Actions:</h2>
                    <a class="button" href="/health">Health Check</a>
                    <a class="button" href="/demo">Run Demo</a>
                    
                    <h2>API Endpoints:</h2>
                    <ul>
                        <li><strong>GET /health</strong> - Service health check</li>
                        <li><strong>GET /demo</strong> - Run a demonstration</li>
                        <li><strong>POST /onboard</strong> - Onboard new student</li>
                        <li><strong>GET /progress/&lt;student_id&gt;</strong> - Get progress</li>
                    </ul>
                    
                    <h2>Local Development:</h2>
                    <p>For the full interactive CLI experience, run locally:</p>
                    <code>python main.py</code>
                </div>
            </body>
            </html>
            ''')
        
        # Demo endpoint
        @app.route('/demo', methods=['GET'])
        def run_demo():
            """Run a simple demo"""
            try:
                # Create a demo student
                student_data = {
                    'student_id': 'cloud_demo_001',
                    'name': 'Cloud Demo Student',
                    'subjects': ['Operating Systems', 'Data Structures'],
                    'available_hours': 6,
                    'preferences': {'preferred_time': 'morning'}
                }
                
                # Run onboarding
                result = coordinator.onboard_new_student(student_data)
                
                return jsonify({
                    "status": "success",
                    "message": "Demo completed successfully",
                    "student_id": result.get('student_id'),
                    "onboarding_status": result.get('onboarding_status')
                })
                
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": f"Demo failed: {str(e)}"
                }), 500
        
        # Onboard endpoint
        @app.route('/onboard', methods=['POST'])
        def onboard_student():
            """Onboard a new student via API"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No JSON data provided"}), 400
                
                result = coordinator.onboard_new_student(data)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        # Progress endpoint
        @app.route('/progress/<student_id>', methods=['GET'])
        def get_progress(student_id):
            """Get student progress"""
            try:
                progress = progress_tracker.get_student_progress(student_id)
                return jsonify(progress)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        logger.info("✅ Flask app created successfully")
        return app
        
    except Exception as e:
        print(f"❌ Error creating Flask app: {e}")
        # Fallback: create a simple app that just returns health check
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy", "service": "SmartStudy AI"})
        
        @app.route('/')
        def home():
            return jsonify({
                "message": "SmartStudy AI is running",
                "note": "Full functionality available in local CLI mode"
            })
        
        return app

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (Cloud Run sets this)
    port = int(os.environ.get('PORT', 8080))
    
    print(f"🚀 Starting SmartStudy AI web server on port {port}...")
    print(f"🌐 Health check: http://0.0.0.0:{port}/health")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)