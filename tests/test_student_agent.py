import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.student_profile_agent import student_agent

def test_student_profile_agent():
    print("🧪 Testing Student Profile Agent...")
    
    # Test data
    test_student = "john_doe_001"
    test_subjects = ["Operating Systems", "Data Structures", "Computer Networks"]
    test_hours = 15
    test_preferences = {"preferred_time": "morning", "learning_style": "visual"}
    
    # Test 1: Save student info
    profile = student_agent.collect_student_info(test_student, test_subjects, test_hours, test_preferences)
    assert profile['subjects'] == test_subjects, "❌ Test 1 Failed: Subjects not saved correctly"
    print("✅ Test 1 PASSED: Student info saved correctly")
    
    # Test 2: Retrieve student info
    retrieved_profile = student_agent.get_student_profile(test_student)
    assert retrieved_profile['available_hours'] == test_hours, "❌ Test 2 Failed: Profile retrieval failed"
    print("✅ Test 2 PASSED: Student profile retrieved correctly")
    
    # Test 3: Update preferences
    new_prefs = {"break_frequency": "every_2_hours"}
    student_agent.update_study_preferences(test_student, new_prefs)
    updated_profile = student_agent.get_student_profile(test_student)
    assert "break_frequency" in updated_profile['preferences'], "❌ Test 3 Failed: Preferences not updated"
    print("✅ Test 3 PASSED: Preferences updated correctly")
    
    print("🎉 All Student Profile Agent tests passed!")

if __name__ == "__main__":
    test_student_profile_agent()