import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.mcq_agent import mcq_agent

def test_mcq_agent():
    print("🧪 Testing MCQ Creator Agent...")
    
    # Test MCQ generation
    topic = "Operating Systems"
    difficulty = "beginner"
    num_questions = 3
    
    mcqs = mcq_agent.generate_mcqs(topic, difficulty, num_questions)
    
    # Check if MCQs are generated
    assert len(mcqs) > 0, "❌ Test 1 Failed: No MCQs generated"
    print(f"✅ Test 1 PASSED: Generated {len(mcqs)} MCQs")
    
    # Check MCQ structure
    first_mcq = mcqs[0]
    assert 'question' in first_mcq, "❌ Test 2 Failed: Question missing"
    assert 'options' in first_mcq, "❌ Test 3 Failed: Options missing"
    assert 'correct_answer' in first_mcq, "❌ Test 4 Failed: Correct answer missing"
    assert 'explanation' in first_mcq, "❌ Test 5 Failed: Explanation missing"
    
    print("✅ Test 2 PASSED: Question field present")
    print("✅ Test 3 PASSED: Options field present")
    print("✅ Test 4 PASSED: Correct answer present")
    print("✅ Test 5 PASSED: Explanation present")
    
    # Print a sample MCQ
    print(f"\n📝 Sample MCQ:")
    print(f"   Q: {first_mcq['question']}")
    print(f"   A) {first_mcq['options']['a']}")
    print(f"   Correct: {first_mcq['correct_answer']}")
    
    print("🎉 MCQ Creator Agent tests passed!")

if __name__ == "__main__":
    test_mcq_agent()