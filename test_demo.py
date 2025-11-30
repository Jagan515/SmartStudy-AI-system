# Create a test script that simulates user input
import sys
import os
sys.path.append('.')

from agents.coordinator import coordinator

def run_demo():
    print("🚀 STARTING AUTOMATED DEMO...")
    
    # Step 1: Onboard a test student
    print("\\n1. 👤 Onboarding test student...")
    student_data = {
        'student_id': 'demo_student_001',
        'name': 'Demo Student',
        'subjects': ['Operating Systems', 'Data Structures'],
        'available_hours': 8,
        'preferences': {'preferred_time': 'morning', 'learning_style': 'mixed'}
    }
    
    onboarding_result = coordinator.onboard_new_student(student_data)
    if onboarding_result:
        print("✅ Onboarding successful!")
    else:
        print("❌ Onboarding failed!")
        return
    
    # Step 2: Run a study session
    print("\\n2. 📚 Running study session...")
    session_data = {
        'subjects': ['Operating Systems'],
        'topics': ['Process Scheduling', 'Memory Management'],
        'duration': 90,
        'mcq_score': 4,
        'total_questions': 5,
        'difficulty': 'beginner'
    }
    
    session_result = coordinator.conduct_study_session('demo_student_001', session_data)
    if session_result:
        print("✅ Study session recorded!")
    else:
        print("❌ Study session failed!")
    
    # Step 3: Generate progress report
    print("\\n3. 📊 Generating progress report...")
    from agents.progress_tracker import progress_tracker
    progress = progress_tracker.get_student_progress('demo_student_001')
    
    if progress:
        print(f"✅ Progress report generated!")
        print(f"   - Sessions: {progress['metrics']['total_study_sessions']}")
        print(f"   - Hours: {progress['metrics']['total_study_hours']:.1f}h")
        print(f"   - Consistency: {progress['metrics']['consistency_score']}%")
    else:
        print("❌ Progress report failed!")
    
    # Step 4: Generate weekly review
    print("\\n4. 📈 Generating weekly review...")
    review = coordinator.generate_weekly_review('demo_student_001')
    if review:
        print("✅ Weekly review generated!")
        if review.get('weak_areas'):
            print(f"   - Weak areas: {review['weak_areas']}")
    else:
        print("❌ Weekly review failed!")
    
    print("\\n🎉 DEMO COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_demo()
