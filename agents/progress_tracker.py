import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from memory.memory_bank import memory_bank
from utils.logger import logger

class ProgressTrackerAgent:
    """
    Memory-powered agent that tracks student progress over time
    Uses long-term memory to store and analyze learning patterns
    """
    
    def __init__(self):
        logger.info("✅ Progress Tracker Agent started!")
    
    def record_study_session(self, student_id: str, session_data: Dict[str, Any]):
        """
        Record a study session in long-term memory
        This helps us track progress over time
        """
        try:
            # Load existing progress
            progress_data = self._load_progress_data(student_id)
            
            # Add new session
            session_record = {
                'session_id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'subjects_studied': session_data.get('subjects', []),
                'topics_covered': session_data.get('topics', []),
                'duration_minutes': session_data.get('duration', 0),
                'mcq_score': session_data.get('mcq_score', None),
                'self_rating': session_data.get('self_rating', None),
                'notes': session_data.get('notes', '')
            }
            
            # Add to sessions list
            if 'study_sessions' not in progress_data:
                progress_data['study_sessions'] = []
            
            progress_data['study_sessions'].append(session_record)
            
            # Update learning patterns in memory bank
            self._update_learning_patterns(student_id, progress_data)
            
            # Save updated progress
            self._save_progress_data(student_id, progress_data)
            
            logger.info(f"✅ Study session recorded for {student_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error recording study session: {e}")
            return False
    
    def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """
        Get comprehensive progress report for a student
        """
        try:
            progress_data = self._load_progress_data(student_id)
            
            # Calculate progress metrics
            metrics = self._calculate_progress_metrics(progress_data)
            
            # Generate insights
            insights = self._generate_progress_insights(progress_data, metrics)
            
            progress_report = {
                'student_id': student_id,
                'generated_at': datetime.now().isoformat(),
                'metrics': metrics,
                'insights': insights,
                'recent_sessions': progress_data.get('study_sessions', [])[-5:],  # Last 5 sessions
                'learning_patterns': progress_data.get('learning_patterns', {})
            }
            
            logger.info(f"✅ Progress report generated for {student_id}")
            return progress_report
            
        except Exception as e:
            logger.error(f"❌ Error getting student progress: {e}")
            return {}
    
    def update_mcq_performance(self, student_id: str, subject: str, score: float, total_questions: int):
        """
        Update MCQ performance in long-term memory
        """
        try:
            # Update in memory bank
            memory_bank.update_learning_pattern(student_id, subject, score)
            
            # Also update in progress data
            progress_data = self._load_progress_data(student_id)
            
            if 'mcq_performance' not in progress_data:
                progress_data['mcq_performance'] = {}
            
            if subject not in progress_data['mcq_performance']:
                progress_data['mcq_performance'][subject] = []
            
            performance_record = {
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'total_questions': total_questions,
                'percentage': (score / total_questions) * 100
            }
            
            progress_data['mcq_performance'][subject].append(performance_record)
            self._save_progress_data(student_id, progress_data)
            
            logger.info(f"✅ MCQ performance updated for {student_id} in {subject}: {score}/{total_questions}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating MCQ performance: {e}")
            return False
    
    def _load_progress_data(self, student_id: str) -> Dict[str, Any]:
        """Load progress data from memory bank"""
        memory_data = memory_bank.load_student_memory(student_id)
        return memory_data.get('learning_data', {})
    
    def _save_progress_data(self, student_id: str, progress_data: Dict[str, Any]):
        """Save progress data to memory bank"""
        memory_bank.save_student_memory(student_id, progress_data)
    
    def _calculate_progress_metrics(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate various progress metrics"""
        sessions = progress_data.get('study_sessions', [])
        mcq_performance = progress_data.get('mcq_performance', {})
        
        metrics = {
            'total_study_sessions': len(sessions),
            'total_study_hours': sum(session.get('duration_minutes', 0) for session in sessions) / 60,
            'average_session_duration': self._calculate_average_duration(sessions),
            'subjects_studied': self._get_unique_subjects(sessions),
            'mcq_trends': self._calculate_mcq_trends(mcq_performance),
            'consistency_score': self._calculate_consistency(sessions)
        }
        
        return metrics
    
    def _calculate_average_duration(self, sessions: List[Dict]) -> float:
        """Calculate average study session duration"""
        if not sessions:
            return 0.0
        
        total_minutes = sum(session.get('duration_minutes', 0) for session in sessions)
        return total_minutes / len(sessions)
    
    def _get_unique_subjects(self, sessions: List[Dict]) -> List[str]:
        """Get list of unique subjects studied"""
        subjects = set()
        for session in sessions:
            subjects.update(session.get('subjects_studied', []))
        return list(subjects)
    
    def _calculate_mcq_trends(self, mcq_performance: Dict[str, List]) -> Dict[str, Any]:
        """Calculate MCQ performance trends"""
        trends = {}
        for subject, performances in mcq_performance.items():
            if performances:
                recent_scores = [p['percentage'] for p in performances[-3:]]  # Last 3 attempts
                trends[subject] = {
                    'current_score': recent_scores[-1] if recent_scores else 0,
                    'improvement': recent_scores[-1] - recent_scores[0] if len(recent_scores) > 1 else 0,
                    'attempt_count': len(performances)
                }
        return trends
    
    def _calculate_consistency(self, sessions: List[Dict]) -> float:
        """Calculate study consistency score (0-100)"""
        if len(sessions) < 2:
            return 0.0
        
        # Check if sessions are regularly spaced
        timestamps = [datetime.fromisoformat(session['timestamp']) for session in sessions]
        timestamps.sort()
        
        if len(timestamps) < 2:
            return 0.0
            
        # Calculate average gap between sessions
        gaps = []
        for i in range(1, len(timestamps)):
            gap = (timestamps[i] - timestamps[i-1]).days
            gaps.append(gap)
        
        avg_gap = sum(gaps) / len(gaps)
        
        # Consistency score: lower average gap = higher consistency
        max_reasonable_gap = 7  # 1 week
        consistency = max(0, 100 * (1 - (avg_gap / max_reasonable_gap)))
        
        return round(consistency, 1)
    
    def _generate_progress_insights(self, progress_data: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate intelligent insights from progress data"""
        insights = []
        
        # Study consistency insight
        consistency = metrics.get('consistency_score', 0)
        if consistency > 80:
            insights.append("🎉 Excellent study consistency! Keep up the regular practice.")
        elif consistency > 60:
            insights.append("👍 Good study habits. Try to maintain your schedule.")
        else:
            insights.append("💡 Consider studying more regularly for better retention.")
        
        # MCQ performance insights
        mcq_trends = metrics.get('mcq_trends', {})
        for subject, trend in mcq_trends.items():
            improvement = trend.get('improvement', 0)
            if improvement > 10:
                insights.append(f"🚀 Great improvement in {subject}! Your scores increased by {improvement:.1f}%")
            elif improvement < -5:
                insights.append(f"📚 {subject} needs more focus. Consider revising the basics.")
        
        # Study duration insights
        avg_duration = metrics.get('average_session_duration', 0)
        if avg_duration > 120:
            insights.append("⏰ Long study sessions detected. Remember to take regular breaks!")
        elif avg_duration < 30:
            insights.append("🕒 Short study sessions. Try extending your focus time gradually.")
        
        return insights
    
    def _update_learning_patterns(self, student_id: str, progress_data: Dict[str, Any]):
        """Update learning patterns based on recent progress"""
        # This method analyzes patterns and updates memory bank
        sessions = progress_data.get('study_sessions', [])
        
        if len(sessions) >= 3:
            # Analyze recent performance trends
            recent_sessions = sessions[-3:]
            avg_mcq_score = self._calculate_recent_mcq_average(recent_sessions)
            
            if avg_mcq_score > 0:
                # Update learning pattern for each subject studied
                for session in recent_sessions:
                    for subject in session.get('subjects_studied', []):
                        memory_bank.update_learning_pattern(student_id, subject, avg_mcq_score)
    
    def _calculate_recent_mcq_average(self, recent_sessions: List[Dict]) -> float:
        """Calculate average MCQ score from recent sessions"""
        scores = []
        for session in recent_sessions:
            if session.get('mcq_score') is not None:
                scores.append(session['mcq_score'])
        
        return sum(scores) / len(scores) if scores else 0

# Create a global instance
progress_tracker = ProgressTrackerAgent()