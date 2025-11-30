import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.study_tools import study_tools
from tools.schedule_tools import schedule_tools

def test_study_tools():
    """Test study tools functionality"""
    
    # Test study load calculation
    subjects = ['OS', 'DSA', 'CN', 'DBMS']
    distribution = study_tools.calculate_study_load(subjects, 10)
    assert sum(distribution.values()) == 10, "Study load calculation incorrect"
    
    # Test revision schedule
    topics = ['Process Scheduling', 'Binary Trees']
    retention = {'Process Scheduling': 30.0, 'Binary Trees': 80.0}
    schedule = study_tools.generate_revision_schedule(topics, retention)
    assert len(schedule) == 2, "Revision schedule generation failed"
    
    print("✅ Study Tools Tests: PASSED")

def test_schedule_tools():
    """Test schedule tools functionality"""
    
    study_plan = {'OS': 3, 'DSA': 2, 'CN': 2}
    slots = ['9:00-11:00', '11:00-13:00', '14:00-16:00']
    schedule = schedule_tools.create_daily_schedule(study_plan, slots)
    assert len(schedule) == 3, "Daily schedule creation failed"
    
    print("✅ Schedule Tools Tests: PASSED")

if __name__ == "__main__":
    test_study_tools()
    test_schedule_tools()