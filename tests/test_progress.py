import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.progress_tracker import progress_tracker
from datetime import datetime

def test_progress_tracker():
    print("🧪 Testing Progress Tracker Agent...")
    
    test_student = "test_progress_001"
    
    # Test 1: Record study session
    session_data = {
        'subjects': ['Operating Systems'],
        'topics': ['Process Scheduling', 'Memory Management'],
        'duration': 120,
        'mcq_score': 4,
        'self_rating': 8,
        'notes': 'Good understanding of process scheduling'
    }
    
    result = progress_tracker.record_study_session(test_student, session_data)
    assert result == True, "❌ Test 1 Failed: Session recording failed"
    print("✅ Test 1 PASSED: Study session recorded")
    
    # Test 2: Update MCQ performance
    mcq_result = progress_tracker.update_mcq_performance(test_student, 'Operating Systems', 4, 5)
    assert mcq_result == True, "❌ Test 2 Failed: MCQ performance update failed"
    print("✅ Test 2 PASSED: MCQ performance updated")
    
    # Test 3: Get progress report
    progress_report = progress_tracker.get_student_progress(test_student)
    assert 'metrics' in progress_report, "❌ Test 3 Failed: Progress report missing metrics"
    assert 'insights' in progress_report, "❌ Test 4 Failed: Progress report missing insights"
    
    print("✅ Test 3 PASSED: Progress metrics generated")
    print("✅ Test 4 PASSED: Progress insights generated")
    
    # Display sample progress data
    print(f"\n📊 Sample Progress Report:")
    print(f"   - Total sessions: {progress_report['metrics']['total_study_sessions']}")
    print(f"   - Study hours: {progress_report['metrics']['total_study_hours']:.1f}h")
    print(f"   - Consistency: {progress_report['metrics']['consistency_score']}%")
    print(f"   - Insights: {len(progress_report['insights'])} generated")
    
    print("🎉 Progress Tracker Agent tests passed!")

if __name__ == "__main__":
    test_progress_tracker()