from typing import Dict, List, Any
from agents.student_profile_agent import student_agent
from agents.study_plan_agent import study_plan_agent
from agents.mcq_agent import mcq_agent
from agents.progress_tracker import progress_tracker
from utils.logger import logger

class MultiAgentCoordinator:
    """
    Coordinates multiple agents to work together
    Implements sequential and parallel workflows
    """
    
    def __init__(self):
        logger.info("✅ Multi-Agent Coordinator started!")
    
    def onboard_new_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sequential agent workflow for new student onboarding
        Step-by-step process:
        1. Create student profile
        2. Generate study plan
        3. Set up progress tracking
        """
        try:
            logger.info(f"👤 Onboarding new student: {student_data.get('name', 'Unknown')}")
            
            # Step 1: Student Profile Agent (Sequential)
            student_id = student_data.get('student_id', f"student_{len(student_agent.student_data) + 1}")
            profile = student_agent.collect_student_info(
                student_id=student_id,
                subjects=student_data['subjects'],
                available_hours=student_data['available_hours'],
                preferences=student_data.get('preferences', {})
            )
            
            logger.info("✅ Step 1: Student profile created")
            
            # Step 2: Study Plan Generator Agent (Sequential)
            study_plan = study_plan_agent.generate_study_plan(profile)
            
            logger.info("✅ Step 2: Study plan generated")
            
            # Step 3: Progress Tracker Setup (Sequential)
            initial_session = {
                'subjects': student_data['subjects'],
                'topics': ['Initial setup'],
                'duration': 0,
                'notes': 'Student onboarding completed'
            }
            progress_tracker.record_study_session(student_id, initial_session)
            
            logger.info("✅ Step 3: Progress tracking initialized")
            
            return {
                'student_id': student_id,
                'profile': profile,
                'study_plan': study_plan,
                'onboarding_status': 'completed'
            }
            
        except Exception as e:
            logger.error(f"❌ Error in student onboarding: {e}")
            return {}
    
    def conduct_study_session(self, student_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parallel agent workflow for study session
        Multiple agents work simultaneously
        """
        try:
            logger.info(f"📚 Conducting study session for {student_id}")
            
            # Parallel tasks that can happen at the same time
            parallel_results = {}
            
            # Task 1: Record session in progress tracker (Parallel)
            progress_task = progress_tracker.record_study_session(student_id, session_data)
            parallel_results['progress_tracked'] = progress_task
            
            # Task 2: Generate MCQs for topics studied (Parallel)
            topics = session_data.get('topics', [])
            if topics:
                mcq_task = mcq_agent.generate_mcqs(
                    topic=topics[0],  # Focus on first topic
                    difficulty=session_data.get('difficulty', 'beginner'),
                    num_questions=3
                )
                parallel_results['mcqs_generated'] = mcq_task
            
            # Task 3: Update learning patterns (Parallel)
            if session_data.get('mcq_score'):
                for subject in session_data.get('subjects', []):
                    progress_tracker.update_mcq_performance(
                        student_id, 
                        subject, 
                        session_data['mcq_score'], 
                        session_data.get('total_questions', 5)
                    )
            
            logger.info("✅ Parallel study session tasks completed")
            
            return {
                'student_id': student_id,
                'session_recorded': True,
                'parallel_results': parallel_results
            }
            
        except Exception as e:
            logger.error(f"❌ Error in study session: {e}")
            return {}
    
    def generate_weekly_review(self, student_id: str) -> Dict[str, Any]:
        """
        Comprehensive weekly review using multiple agents
        """
        try:
            logger.info(f"📊 Generating weekly review for {student_id}")
            
            # Sequential workflow for review
            review_data = {}
            
            # Step 1: Get student profile
            profile = student_agent.get_student_profile(student_id)
            review_data['profile'] = profile
            
            # Step 2: Get progress report
            progress_report = progress_tracker.get_student_progress(student_id)
            review_data['progress'] = progress_report
            
            # Step 3: Generate new MCQs based on weak areas
            weak_areas = self._identify_weak_areas(progress_report)
            review_data['weak_areas'] = weak_areas
            
            mcq_recommendations = []
            for area in weak_areas[:2]:  # Focus on top 2 weak areas
                mcqs = mcq_agent.generate_mcqs(area, 'beginner', 2)
                mcq_recommendations.append({
                    'area': area,
                    'practice_questions': mcqs
                })
            
            review_data['practice_recommendations'] = mcq_recommendations
            
            # Step 4: Generate insights for next week
            next_week_plan = self._generate_next_week_plan(profile, progress_report)
            review_data['next_week_plan'] = next_week_plan
            
            logger.info("✅ Weekly review generated successfully")
            return review_data
            
        except Exception as e:
            logger.error(f"❌ Error generating weekly review: {e}")
            return {}
    
    def interactive_learning_flow(self, student_id: str) -> Dict[str, Any]:
        """
        Interactive learning session with multiple agents
        Perfect for demonstrating the multi-agent system
        """
        try:
            print(f"\n{'='*60}")
            print("🎓 SMART STUDY AI - INTERACTIVE LEARNING SESSION")
            print(f"{'='*60}")
            
            # Get student profile
            profile = student_agent.get_student_profile(student_id)
            if not profile:
                print("❌ Student profile not found. Please onboard first.")
                return {}
            
            print(f"\n👤 Student: {student_id}")
            print(f"📚 Subjects: {', '.join(profile['subjects'])}")
            print(f"⏰ Available hours: {profile['available_hours']} per week")
            
            # Generate study plan
            print(f"\n📅 Generating your personalized study plan...")
            study_plan = study_plan_agent.generate_study_plan(profile)
            
            # Show weekly overview
            weekly_overview = study_plan.get('weekly_overview', {})
            if weekly_overview:
                print(f"\n📋 YOUR WEEKLY STUDY PLAN:")
                for day, tasks in weekly_overview.get('weekly_schedule', {}).items():
                    print(f"   {day}: {', '.join(tasks[:2])}...")
            
            # Generate practice questions
            first_subject = profile['subjects'][0]
            print(f"\n🎯 Generating practice questions for {first_subject}...")
            mcqs = mcq_agent.generate_mcqs(first_subject, 'beginner', 3)
            
            # Conduct quiz
            if mcqs:
                quiz_results = mcq_agent.conduct_quiz(mcqs)
                
                # Record session
                session_data = {
                    'subjects': [first_subject],
                    'topics': [f"{first_subject} Basics"],
                    'duration': 30,
                    'mcq_score': quiz_results['score'],
                    'total_questions': quiz_results['total_questions'],
                    'self_rating': 7,
                    'notes': 'Interactive learning session'
                }
                
                progress_tracker.record_study_session(student_id, session_data)
                progress_tracker.update_mcq_performance(
                    student_id, first_subject, 
                    quiz_results['score'], quiz_results['total_questions']
                )
                
                # Show progress
                progress = progress_tracker.get_student_progress(student_id)
                print(f"\n📊 Your Learning Progress:")
                print(f"   Total sessions: {progress['metrics']['total_study_sessions']}")
                print(f"   Study consistency: {progress['metrics']['consistency_score']}%")
                
                if progress['insights']:
                    print(f"   💡 Insight: {progress['insights'][0]}")
            
            return {
                'interactive_session_completed': True,
                'study_plan': study_plan,
                'quiz_results': quiz_results if 'quiz_results' in locals() else {}
            }
            
        except Exception as e:
            logger.error(f"❌ Error in interactive flow: {e}")
            return {}
    
    def _identify_weak_areas(self, progress_report: Dict[str, Any]) -> List[str]:
        """Identify subjects/topics that need improvement"""
        weak_areas = []
        mcq_trends = progress_report.get('metrics', {}).get('mcq_trends', {})
        
        for subject, trend in mcq_trends.items():
            if trend.get('current_score', 0) < 60:  # Below 60%
                weak_areas.append(subject)
            elif trend.get('improvement', 0) < 0:  # Negative improvement
                weak_areas.append(subject)
        
        return weak_areas
    
    def _generate_next_week_plan(self, profile: Dict[str, Any], progress: Dict[str, Any]) -> Dict[str, Any]:
        """Generate plan for next week based on progress"""
        weak_areas = self._identify_weak_areas(progress)
        
        next_week_plan = {
            'focus_areas': weak_areas if weak_areas else profile['subjects'],
            'recommended_hours': profile['available_hours'],
            'priority_subjects': weak_areas[:2] if weak_areas else profile['subjects'][:2],
            'revision_days': ['Wednesday', 'Sunday']
        }
        
        return next_week_plan

# Create a global coordinator
coordinator = MultiAgentCoordinator()