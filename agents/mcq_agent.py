import json
import random
from typing import Dict, List, Any
from config.gcp_config import gcp_config
from utils.logger import logger

class MCQCreatorAgent:
    """
    LLM-powered agent that creates practice questions
    Generates MCQs for any study topic
    """
    
    def __init__(self):
        self.model = gcp_config.get_model()
        logger.info("✅ MCQ Creator Agent started!")
    
    def generate_mcqs(self, topic: str, difficulty: str = 'beginner', num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate multiple-choice questions for a given topic
        """
        try:
            logger.info(f"🎯 Generating {num_questions} {difficulty} MCQs for: {topic}")
            
            prompt = self._create_mcq_prompt(topic, difficulty, num_questions)
            response = self.model.generate_content(prompt)
            
            mcqs = self._parse_mcq_response(response.text, num_questions)
            
            logger.info(f"✅ Generated {len(mcqs)} MCQs for {topic}")
            return mcqs
            
        except Exception as e:
            logger.error(f"❌ Error generating MCQs: {e}")
            return self._get_sample_mcqs(topic, num_questions)
    
    def _create_mcq_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        """Create prompt for MCQ generation"""
        
        prompt = f"""
        Create {num_questions} multiple-choice questions about {topic} for {difficulty} level engineering students.
        
        For each question, provide:
        1. A clear question
        2. Four options (a, b, c, d)
        3. The correct answer (just the letter)
        4. A brief explanation
        
        Format as JSON:
        [
          {{
            "question": "What is...?",
            "options": {{
              "a": "Option A",
              "b": "Option B", 
              "c": "Option C",
              "d": "Option D"
            }},
            "correct_answer": "a",
            "explanation": "Because..."
          }}
        ]
        
        Make the questions educational and relevant to {topic}.
        """
        
        return prompt
    
    def _parse_mcq_response(self, ai_text: str, expected_count: int) -> List[Dict[str, Any]]:
        """Parse AI response into MCQ list"""
        try:
            # Extract JSON from response
            start_idx = ai_text.find('[')
            end_idx = ai_text.rfind(']') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = ai_text[start_idx:end_idx]
                mcqs = json.loads(json_str)
                
                # Ensure we have the expected number
                if len(mcqs) >= expected_count:
                    return mcqs[:expected_count]
                else:
                    return mcqs
            else:
                logger.warning("⚠️  No JSON array found in AI response")
                return self._get_sample_mcqs("general", expected_count)
                
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parsing MCQ JSON: {e}")
            return self._get_sample_mcqs("general", expected_count)
    
    def _get_sample_mcqs(self, topic: str, count: int) -> List[Dict[str, Any]]:
        """Return sample MCQs if AI fails"""
        sample_mcqs = [
            {
                "question": f"What is a key concept in {topic}?",
                "options": {
                    "a": "Basic understanding",
                    "b": "Advanced techniques", 
                    "c": "Practical applications",
                    "d": "All of the above"
                },
                "correct_answer": "d",
                "explanation": "All these are important aspects to learn."
            },
            {
                "question": f"Why is {topic} important for engineers?",
                "options": {
                    "a": "It's not important",
                    "b": "Only for exams", 
                    "c": "Fundamental concept",
                    "d": "Optional knowledge"
                },
                "correct_answer": "c",
                "explanation": "This is a fundamental concept in computer science."
            }
        ]
        
        return sample_mcqs[:count]
    
    def conduct_quiz(self, mcqs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Conduct an interactive quiz with the generated questions
        """
        try:
            logger.info("🎯 Starting quiz session...")
            
            score = 0
            total_questions = len(mcqs)
            results = []
            
            print(f"\n{'='*50}")
            print("🎓 SMART STUDY QUIZ SESSION")
            print(f"{'='*50}")
            
            for i, mcq in enumerate(mcqs, 1):
                print(f"\nQ{i}: {mcq['question']}")
                print("Options:")
                for option, text in mcq['options'].items():
                    print(f"  {option}) {text}")
                
                # Get user answer
                user_answer = input("\nYour answer (a/b/c/d): ").strip().lower()
                
                # Check answer
                is_correct = user_answer == mcq['correct_answer']
                if is_correct:
                    score += 1
                    print("✅ Correct!")
                else:
                    print(f"❌ Incorrect! Correct answer is: {mcq['correct_answer']}")
                
                print(f"💡 Explanation: {mcq['explanation']}")
                
                # Store result
                results.append({
                    'question_number': i,
                    'user_answer': user_answer,
                    'correct_answer': mcq['correct_answer'],
                    'is_correct': is_correct
                })
            
            # Calculate percentage
            percentage = (score / total_questions) * 100
            
            print(f"\n{'='*50}")
            print(f"📊 QUIZ RESULTS")
            print(f"{'='*50}")
            print(f"Score: {score}/{total_questions} ({percentage:.1f}%)")
            
            if percentage >= 80:
                print("🎉 Excellent! You're mastering this topic!")
            elif percentage >= 60:
                print("👍 Good job! Keep practicing!")
            else:
                print("📚 Keep studying! You'll improve!")
            
            return {
                'total_questions': total_questions,
                'score': score,
                'percentage': percentage,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"❌ Error conducting quiz: {e}")
            return {}

# Create a global instance
mcq_agent = MCQCreatorAgent()