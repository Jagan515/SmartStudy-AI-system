#!/usr/bin/env python3
"""
SmartStudy AI - Multi-Agent Learning System
Main application file that brings all agents together
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our agents and coordinator
from agents.coordinator import coordinator
from agents.student_profile_agent import student_agent
from utils.logger import logger

def main():
    """
    Main function - SmartStudy AI application entry point
    """
    print("\n" + "="*70)
    print("🎓 WELCOME TO SMARTSTUDY AI")
    print("🤖 Multi-Agent Learning System for B.Tech Students")
    print("="*70)
    
    # Current active student
    current_student = None
    
    while True:
        print("\n📚 MAIN MENU:")
        print("1. 👤 New Student Onboarding")
        print("2. 🎓 Interactive Learning Session")
        print("3. 📊 View Progress Report")
        print("4. 🧪 Test All Agents")
        print("5. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            current_student = new_student_onboarding()
            
        elif choice == '2':
            if not current_student:
                print("❌ Please complete onboarding first!")
                continue
            interactive_learning_session(current_student)
            
        elif choice == '3':
            if not current_student:
                print("❌ Please complete onboarding first!")
                continue
            view_progress_report(current_student)
            
        elif choice == '4':
            run_all_tests()
            
        elif choice == '5':
            print("\n👋 Thank you for using SmartStudy AI!")
            print("🎯 Keep learning and growing!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def new_student_onboarding():
    """Guide new student through onboarding process"""
    print("\n" + "="*50)
    print("👤 NEW STUDENT ONBOARDING")
    print("="*50)
    
    # Collect student information
    print("\nLet's create your personalized learning profile!")
    
    name = input("Enter your name: ").strip()
    
    print("\n📚 Enter your subjects (comma-separated):")
    print("Example: Operating Systems, Data Structures, Computer Networks, DBMS")
    subjects_input = input("Subjects: ").strip()
    subjects = [s.strip() for s in subjects_input.split(',')]
    
    available_hours = int(input("\n⏰ How many hours can you study per week? "))
    
    print("\n🎯 Any learning preferences?")
    print("Example: preferred_time=morning, learning_style=visual")
    preferences_input = input("Preferences (or press Enter for default): ").strip()
    
    # Parse preferences
    preferences = {}
    if preferences_input:
        for pref in preferences_input.split(','):
            if '=' in pref:
                key, value = pref.split('=')
                preferences[key.strip()] = value.strip()
    
    # Create student data
    student_data = {
        'student_id': f"student_{name.lower().replace(' ', '_')}",
        'name': name,
        'subjects': subjects,
        'available_hours': available_hours,
        'preferences': preferences
    }
    
    print(f"\n⏳ Creating your personalized learning plan...")
    
    # Use coordinator to onboard student
    result = coordinator.onboard_new_student(student_data)
    
    if result and result['onboarding_status'] == 'completed':
        print("\n✅ ONBOARDING COMPLETED SUCCESSFULLY!")
        print(f"🎯 Student ID: {result['student_id']}")
        print(f"📚 Subjects: {len(subjects)} subjects configured")
        print(f"⏰ Study hours: {available_hours} hours per week")
        
        return result['student_id']
    else:
        print("❌ Onboarding failed. Please try again.")
        return None

def interactive_learning_session(student_id: str):
    """Run an interactive learning session with all agents"""
    print(f"\n🎓 Starting interactive learning session for {student_id}...")
    
    # Use coordinator to run interactive flow
    result = coordinator.interactive_learning_flow(student_id)
    
    if result and result.get('interactive_session_completed'):
        print("\n✅ LEARNING SESSION COMPLETED!")
    else:
        print("\n❌ Learning session encountered an issue.")

def view_progress_report(student_id: str):
    """Display student progress report"""
    from agents.progress_tracker import progress_tracker
    
    print(f"\n📊 Generating progress report for {student_id}...")
    
    progress = progress_tracker.get_student_progress(student_id)
    
    if not progress:
        print("❌ No progress data found.")
        return
    
    metrics = progress['metrics']
    insights = progress['insights']
    
    print(f"\n📈 PROGRESS REPORT")
    print("="*40)
    print(f"📅 Total Study Sessions: {metrics['total_study_sessions']}")
    print(f"⏰ Total Study Hours: {metrics['total_study_hours']:.1f}h")
    print(f"📚 Subjects Studied: {len(metrics['subjects_studied'])}")
    print(f"🎯 Consistency Score: {metrics['consistency_score']}%")
    
    if insights:
        print(f"\n💡 RECOMMENDATIONS:")
        for insight in insights[:3]:
            print(f"   • {insight}")

def run_all_tests():
    """Run all agent tests to verify system functionality"""
    print("\n🧪 RUNNING SYSTEM TESTS...")
    print("="*50)
    
    tests_to_run = [
        'test_student_agent',
        'test_study_plan_agent', 
        'test_mcq_agent',
        'test_progress_tracker',
        'test_coordinator'
    ]
    
    all_passed = True
    
    for test_name in tests_to_run:
        try:
            module = __import__(f'tests.{test_name}', fromlist=[''])
            if hasattr(module, 'main'):
                print(f"\n🔍 Running {test_name}...")
                success = module.main()
                if not success:
                    all_passed = False
        except Exception as e:
            print(f"❌ Error running {test_name}: {e}")
            all_passed = False
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the system.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
