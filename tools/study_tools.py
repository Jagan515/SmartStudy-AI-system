from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
from utils.logger import logger

class StudyTools:
    """Custom tools for study planning and management"""
    
    @staticmethod
    def calculate_study_load(subjects: List[str], available_hours: int) -> Dict[str, int]:
        """Calculate optimal study time distribution across subjects"""
        try:
            subject_count = len(subjects)
            if subject_count == 0:
                return {}
            
            base_hours = available_hours // subject_count
            extra_hours = available_hours % subject_count
            
            distribution = {}
            for i, subject in enumerate(subjects):
                hours = base_hours + (1 if i < extra_hours else 0)
                distribution[subject] = hours
            
            logger.info(f"✅ Study load calculated: {distribution}")
            return distribution
            
        except Exception as e:
            logger.error(f"❌ Error calculating study load: {e}")
            return {}
    
    @staticmethod
    def generate_revision_schedule(learned_topics: List[str], retention_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate spaced repetition schedule based on retention scores"""
        try:
            schedule = {}
            current_date = datetime.now()
            
            for topic in learned_topics:
                retention = retention_scores.get(topic, 50.0)
                
                # Calculate revision intervals based on retention
                if retention < 40:
                    intervals = [1, 3, 7, 14]  # Frequent revisions for low retention
                elif retention < 70:
                    intervals = [2, 7, 21]     # Moderate revisions
                else:
                    intervals = [7, 30]        # Less frequent for high retention
                
                revision_dates = []
                for days in intervals:
                    revision_date = current_date + timedelta(days=days)
                    revision_dates.append(revision_date.strftime("%Y-%m-%d"))
                
                schedule[topic] = {
                    'retention_score': retention,
                    'revision_dates': revision_dates,
                    'priority': 'high' if retention < 40 else 'medium' if retention < 70 else 'low'
                }
            
            logger.info(f"✅ Revision schedule generated for {len(learned_topics)} topics")
            return schedule
            
        except Exception as e:
            logger.error(f"❌ Error generating revision schedule: {e}")
            return {}
    
    @staticmethod
    def assess_difficulty_level(performance_history: List[float]) -> str:
        """Assess student's current difficulty level based on performance"""
        if not performance_history:
            return "beginner"
        
        avg_performance = sum(performance_history) / len(performance_history)
        
        if avg_performance >= 80:
            return "advanced"
        elif avg_performance >= 60:
            return "intermediate"
        else:
            return "beginner"

# Global tools instance
study_tools = StudyTools()