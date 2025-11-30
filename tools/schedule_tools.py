from typing import Dict, List, Any
from datetime import datetime, timedelta
from utils.logger import logger

class ScheduleTools:
    """Tools for schedule optimization and time management"""
    
    @staticmethod
    def create_daily_schedule(study_plan: Dict[str, int], available_slots: List[str]) -> Dict[str, Any]:
        """Create detailed daily study schedule"""
        try:
            schedule = {}
            slot_index = 0
            
            for subject, hours in study_plan.items():
                if slot_index >= len(available_slots):
                    break
                
                schedule[available_slots[slot_index]] = {
                    'subject': subject,
                    'duration_hours': hours,
                    'activity': 'new_topic' if hours > 1 else 'revision'
                }
                slot_index += 1
            
            logger.info(f"✅ Daily schedule created with {len(schedule)} slots")
            return schedule
            
        except Exception as e:
            logger.error(f"❌ Error creating daily schedule: {e}")
            return {}
    
    @staticmethod
    def optimize_time_allocation(subjects: List[str], priority_weights: Dict[str, float], total_hours: int) -> Dict[str, int]:
        """Optimize time allocation based on subject priorities"""
        try:
            total_weight = sum(priority_weights.values())
            if total_weight == 0:
                # Equal distribution if no weights provided
                hours_per_subject = total_hours // len(subjects)
                return {subject: hours_per_subject for subject in subjects}
            
            allocation = {}
            for subject in subjects:
                weight = priority_weights.get(subject, 1.0)
                hours = int((weight / total_weight) * total_hours)
                allocation[subject] = max(1, hours)  # Minimum 1 hour per subject
            
            # Adjust for rounding
            allocated_total = sum(allocation.values())
            if allocated_total != total_hours:
                # Distribute remaining hours
                difference = total_hours - allocated_total
                subject_with_least = min(allocation.items(), key=lambda x: x[1])[0]
                allocation[subject_with_least] += difference
            
            logger.info(f"✅ Time allocation optimized: {allocation}")
            return allocation
            
        except Exception as e:
            logger.error(f"❌ Error optimizing time allocation: {e}")
            return {}

# Global schedule tools instance
schedule_tools = ScheduleTools()