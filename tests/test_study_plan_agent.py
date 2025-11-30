import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.study_plan_agent import study_plan_agent

def test_study_plan_agent():
    print("🧪 Testing Study Plan Generator Agent...")
    
    # Create a test student profile
    test_profile = {
        'subjects': ['Operating Systems', 'Data Structures'],
        'available_hours': 6,
        'preferences': {'preferred_time': 'morning'}
    }
    
    # Test study plan generation
    plan = study_plan_agent.generate_study_plan(test_profile)
    
    # Check if plan has required components
    assert 'weekly_overview' in plan, "❌ Test 1 Failed: Weekly overview missing"
    assert 'daily_schedule' in plan, "❌ Test 2 Failed: Daily schedule missing"
    assert 'study_load_distribution' in plan, "❌ Test 3 Failed: Study load missing"
    
    print("✅ Test 1 PASSED: Weekly overview generated")
    print("✅ Test 2 PASSED: Daily schedule created")
    print("✅ Test 3 PASSED: Study load distribution included")
    
    # Print a sample of the plan
    print(f"\n📅 Sample Plan Overview:")
    print(f"   - Subjects: {test_profile['subjects']}")
    print(f"   - Study load: {plan['study_load_distribution']}")
    print(f"   - Schedule slots: {len(plan['daily_schedule'])}")
    
    print("🎉 Study Plan Generator Agent tests passed!")

if __name__ == "__main__":
    test_study_plan_agent()