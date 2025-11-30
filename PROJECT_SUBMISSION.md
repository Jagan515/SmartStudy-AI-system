# 🎓 SmartStudy AI - Capstone Project Submission

## 📹 Video Demo
[![SmartStudy AI Demo](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://youtube.com/shorts/VIDEO_ID)

## 🎯 Problem Statement
B.Tech students struggle with managing complex subjects (OS, DSA, CN, DBMS) due to inefficient study planning, lack of personalized schedules, and inadequate progress tracking.

## 🤖 Why Agents?
- **Personalization**: Each student needs unique study plans
- **Adaptability**: Learning patterns change over time  
- **Multi-faceted**: Planning, assessment, tracking require different expertise
- **Scalability**: Handle thousands of students simultaneously


## 🛠️ Technical Implementation

### **Key Concepts Demonstrated:**
1. **Multi-agent System** (Sequential + Parallel + LLM agents)
2. **Custom Tools & Memory Bank** (Study planning tools, long-term memory)
3. **Session & State Management** (Student session handling)
4. **Observability** (Comprehensive logging and metrics)
5. **Agent Evaluation** (Performance tracking)

### **Agents Implemented:**
- **Student Profile Agent**: Session management
- **Study Plan Generator**: Gemini-powered planning  
- **MCQ Creator**: Gemini-powered assessment
- **Progress Tracker**: Memory-powered analytics
- **Multi-Agent Coordinator**: Workflow management

## 🚀 Getting Started

```bash
# 1. Clone and setup
git clone <repository>
cd smart-study-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
echo "GOOGLE_API_KEY=your_key" > .env

# 4. Run the system
python main.py
