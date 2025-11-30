from flask import Flask, jsonify
import os
import sys

# Add current directory to Python path
sys.path.append('.')

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "SmartStudy AI is running! 🎓",
        "status": "active", 
        "version": "1.0.0",
        "endpoints": ["/health", "/demo", "/info"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "SmartStudy AI"})

@app.route('/demo')
def demo():
    return jsonify({
        "message": "Demo endpoint working!",
        "next_step": "Set GOOGLE_API_KEY environment variable"
    })

@app.route('/info')
def info():
    return jsonify({
        "project": "SmartStudy AI",
        "description": "Multi-agent learning system for B.Tech students",
        "agents": ["Student Profile", "Study Plan Generator", "MCQ Creator", "Progress Tracker"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting SmartStudy AI on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)