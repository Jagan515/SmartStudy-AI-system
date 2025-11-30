from flask import Flask, jsonify
import os
import signal
import sys

# Create Flask app IMMEDIATELY
app = Flask(__name__)

# Basic health check endpoint
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "SmartStudy AI",
        "message": "Server is working! 🎓"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/ready')
def ready():
    return jsonify({"status": "ready"})

# Start the server IMMEDIATELY when the script runs
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting web server on port {port}...")
    print(f"📡 Listening on: 0.0.0.0:{port}")
    
    # Start Flask development server
    app.run(
        host='0.0.0.0',  # CRITICAL: Must be 0.0.0.0, not localhost
        port=port,
        debug=False
    )