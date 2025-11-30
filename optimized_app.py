from flask import Flask, jsonify
import os
import sys
import threading
import time

# Add current directory to Python path
sys.path.append('.')

app = Flask(__name__)

# Global variable to track if agents are loaded
agents_loaded = False
loading_status = "Starting..."

def load_agents_in_background():
    """Load AI agents in background to avoid startup timeout"""
    global agents_loaded, loading_status
    
    try:
        loading_status = "Loading configuration..."
        from config.gcp_config import gcp_config
        loading_status = "Loading agents..."
        from agents.coordinator import coordinator
        from agents.student_profile_agent import student_agent
        loading_status = "Loading tools and memory..."
        from agents.progress_tracker import progress_tracker
        loading_status = "Initializing AI models..."
        
        # Test that agents work
        loading_status = "Testing AI connection..."
        model = gcp_config.get_model()
        
        agents_loaded = True
        loading_status = "Ready! All agents loaded successfully."
        print("✅ All AI agents loaded and ready!")
        
    except Exception as e:
        loading_status = f"Error: {str(e)}"
        print(f"❌ Agent loading failed: {e}")

@app.route('/')
def home():
    status = "ready" if agents_loaded else "loading"
    return jsonify({
        "message": "SmartStudy AI - Optimized Version",
        "status": status,
        "loading_status": loading_status,
        "endpoints": ["/health", "/demo", "/status"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "SmartStudy AI",
        "agents_loaded": agents_loaded
    })

@app.route('/status')
def status():
    return jsonify({
        "agents_loaded": agents_loaded,
        "loading_status": loading_status,
        "startup_time": "Optimized for Cloud Run"
    })

@app.route('/demo')
def demo():
    if not agents_loaded:
        return jsonify({
            "status": "loading",
            "message": "Agents are still loading, please wait...",
            "current_status": loading_status
        }), 503
    
    try:
        from agents.coordinator import coordinator
        
        # Run a simple demo
        student_data = {
            'student_id': 'cloud_demo_001',
            'name': 'Cloud Demo Student',
            'subjects': ['Operating Systems'],
            'available_hours': 5,
            'preferences': {'preferred_time': 'morning'}
        }
        
        result = coordinator.onboard_new_student(student_data)
        
        return jsonify({
            "status": "success",
            "message": "Demo completed!",
            "student_id": result.get('student_id'),
            "onboarding_status": result.get('onboarding_status')
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Demo failed: {str(e)}"
        }), 500

# Start background loading when app starts
@app.before_first_request
def startup():
    thread = threading.Thread(target=load_agents_in_background)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting optimized SmartStudy AI on port {port}")
    print("📝 Agents will load in background to avoid startup timeout...")
    
    # Start background loading immediately
    startup_thread = threading.Thread(target=load_agents_in_background)
    startup_thread.daemon = True
    startup_thread.start()
    
    app.run(host='0.0.0.0', port=port, debug=False)