import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.coordinator import coordinator

def test_coordinator():
    print("🧪 Testing Multi-Agent Coordinator...")
    
    # Test data for new student
    new_student = {
        'student_id': 'coordinator_test_001',
        'name': 'Test Student',
        'subjects': ['Operating Systems', 'Data Structures'],
        'available_hours': 10,
        'preferences': {'learning_style': 'visual', 'preferred_time': 'morning'}
    }
    
    # Test 1: Student onboarding (sequential agents)
    onboarding_result = coordinator.onboard_new_student(new_student)
    assert onboarding_result['onboarding_status'] == 'completed', "❌ Test 1 Failed: Onboarding failed"
    print("✅ Test 1 PASSED: Student onboarding completed")
    
    # Test 2: Study session (parallel agents)
    session_data = {
        'subjects': ['Operating Systems'],
        'topics': ['Process Management'],
        'duration': 90,
        'mcq_score': 3,
        'total_questions': 5,
        'difficulty': 'beginner'
    }
    
    session_result = coordinator.conduct_study_session(new_student['student_id'], session_data)
    assert session_result['session_recorded'] == True, "❌ Test 2 Failed: Study session failed"
    print("✅ Test 2 PASSED: Study session conducted")
    
    # Test 3: Weekly review
    review = coordinator.generate_weekly_review(new_student['student_id'])
    assert 'progress' in review, "❌ Test 3 Failed: Weekly review missing progress"
    assert 'next_week_plan' in review, "❌ Test 4 Failed: Weekly review missing next plan"
    
    print("✅ Test 3 PASSED: Progress report included")
    print("✅ Test 4 PASSED: Next week plan generated")
    
    print("🎉 Multi-Agent Coordinator tests passed!")
    print("\n💡 Try the interactive flow in main.py to see all agents working together!")

if __name__ == "__main__":
    test_coordinator()