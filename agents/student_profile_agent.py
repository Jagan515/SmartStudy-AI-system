import json
from typing import Dict, List, Any
from datetime import datetime
from utils.logger import logger

class StudentProfileAgent:
    """
    Simple agent to manage student information
    Uses session memory to remember student preferences
    """
    
    def __init__(self):
        # This will store student data during the session
        self.student_data = {}
        logger.info("✅ Student Profile Agent started!")
    
    def collect_student_info(self, student_id: str, subjects: List[str], available_hours: int, preferences: Dict = None):
        """
        Collect basic student information
        This is like filling out a form about your study needs
        """
        try:
            # Store student information
            self.student_data[student_id] = {
                'subjects': subjects,
                'available_hours': available_hours,
                'preferences': preferences or {},
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Student info saved for: {student_id}")
            logger.info(f"   Subjects: {subjects}")
            logger.info(f"   Available hours: {available_hours}")
            
            return self.student_data[student_id]
            
        except Exception as e:
            logger.error(f"❌ Error saving student info: {e}")
            return {}
    
    def get_student_profile(self, student_id: str) -> Dict[str, Any]:
        """Get stored student information"""
        if student_id in self.student_data:
            return self.student_data[student_id]
        else:
            logger.warning(f"📝 No profile found for student: {student_id}")
            return {}
    
    def update_study_preferences(self, student_id: str, new_preferences: Dict):
        """Update student's study preferences"""
        try:
            if student_id in self.student_data:
                self.student_data[student_id]['preferences'].update(new_preferences)
                self.student_data[student_id]['last_updated'] = datetime.now().isoformat()
                logger.info(f"✅ Preferences updated for: {student_id}")
                return True
            else:
                logger.error(f"❌ Student {student_id} not found")
                return False
        except Exception as e:
            logger.error(f"❌ Error updating preferences: {e}")
            return False

# Create a global instance of this agent
student_agent = StudentProfileAgent()