import json
from typing import Dict, List, Any
from config.gcp_config import gcp_config
from tools.study_tools import study_tools
from tools.schedule_tools import schedule_tools
from utils.logger import logger

class StudyPlanGeneratorAgent:
    """
    LLM-powered agent that creates personalized study plans
    Uses Google Gemini to make smart scheduling decisions
    """
    
    def __init__(self):
        # Get the Gemini model from our GCP configuration
        self.model = gcp_config.get_model()
        logger.info("✅ Study Plan Generator Agent started!")
    
    def generate_study_plan(self, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a personalized study plan using Gemini AI
        This is where the magic happens!
        """
        try:
            # Extract information from student profile
            subjects = student_profile.get('subjects', [])
            available_hours = student_profile.get('available_hours', 0)
            preferences = student_profile.get('preferences', {})
            
            logger.info(f"📚 Generating study plan for {len(subjects)} subjects")
            logger.info(f"⏰ Available hours: {available_hours}")
            
            # Step 1: Use our custom tool to calculate study load
            study_load = study_tools.calculate_study_load(subjects, available_hours)
            logger.info(f"📊 Study load calculated: {study_load}")
            
            # Step 2: Use Gemini AI to create a smart study plan
            prompt = self._create_plan_prompt(subjects, study_load, preferences)
            
            # Send prompt to Gemini AI
            response = self.model.generate_content(prompt)
            
            # Step 3: Parse the AI response
            study_plan = self._parse_ai_response(response.text)
            
            # Step 4: Create detailed daily schedule using our tools
            available_slots = self._generate_time_slots(available_hours)
            detailed_schedule = schedule_tools.create_daily_schedule(study_load, available_slots)
            
            # Combine everything into final plan
            final_plan = {
                'weekly_overview': study_plan,
                'daily_schedule': detailed_schedule,
                'study_load_distribution': study_load,
                'generated_at': self._get_current_timestamp()
            }
            
            logger.info("✅ Study plan generated successfully!")
            return final_plan
            
        except Exception as e:
            logger.error(f"❌ Error generating study plan: {e}")
            return {}
    
    def _create_plan_prompt(self, subjects: List[str], study_load: Dict[str, int], preferences: Dict) -> str:
        """Create a smart prompt for Gemini AI"""
        
        prompt = f"""
        You are an expert study planner for engineering students. Create a weekly study plan.
        
        STUDENT INFORMATION:
        - Subjects to study: {', '.join(subjects)}
        - Hours available per subject: {study_load}
        - Student preferences: {preferences}
        
        Please create a balanced weekly study plan that includes:
        1. Topic distribution for each subject
        2. Recommended study techniques
        3. Revision sessions
        4. Break times
        
        Format your response as JSON with this structure:
        {{
            "weekly_schedule": {{
                "Monday": ["Subject1: Topic1", "Subject2: Topic2"],
                "Tuesday": [...],
                ...
            }},
            "study_techniques": {{
                "Subject1": "Recommended study method",
                ...
            }},
            "revision_days": ["Thursday", "Sunday"],
            "weekly_goals": ["Goal1", "Goal2", "Goal3"]
        }}
        
        Make it practical and achievable!
        """
        
        return prompt
    
    def _parse_ai_response(self, ai_text: str) -> Dict[str, Any]:
        """Parse the AI's response into structured data"""
        try:
            # Try to extract JSON from the AI response
            # Sometimes AI adds extra text, so we look for JSON pattern
            start_idx = ai_text.find('{')
            end_idx = ai_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = ai_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, return a default structure
                logger.warning("⚠️  No JSON found in AI response, using default structure")
                return self._get_default_plan()
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parsing AI response: {e}")
            return self._get_default_plan()
    
    def _get_default_plan(self) -> Dict[str, Any]:
        """Return a default study plan if AI fails"""
        return {
            "weekly_schedule": {
                "Monday": ["Study session 1", "Study session 2"],
                "Tuesday": ["Study session 1", "Study session 2"],
                "Wednesday": ["Revision day"],
                "Thursday": ["Study session 1", "Study session 2"],
                "Friday": ["Practice problems"],
                "Saturday": ["Weekly review"],
                "Sunday": ["Rest day"]
            },
            "study_techniques": {
                "Default": "Pomodoro technique: 25min study, 5min break"
            },
            "revision_days": ["Wednesday", "Saturday"],
            "weekly_goals": ["Complete all planned topics", "Practice problems", "Weekly review"]
        }
    
    def _generate_time_slots(self, total_hours: int) -> List[str]:
        """Generate time slots for the schedule"""
        # Simple time slot generation (9 AM to 9 PM)
        slots = []
        start_time = 9  # 9 AM
        
        for i in range(total_hours):
            end_time = start_time + 1
            slot = f"{start_time}:00-{end_time}:00"
            slots.append(slot)
            start_time = end_time
            
            # Break for lunch
            if start_time == 13:  # 1 PM
                start_time = 14   # 2 PM
                
        return slots
    
    def _get_current_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

# Create a global instance
study_plan_agent = StudyPlanGeneratorAgent()