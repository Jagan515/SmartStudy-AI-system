import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from memory.memory_bank import memory_bank

def test_memory_operations():
    """Test memory bank save/load operations"""
    test_student = "test_student_001"
    test_data = {
        'subjects': ['OS', 'DSA'],
        'preferred_study_time': 'morning',
        'performance_history': []
    }
    
    # Test save
    save_result = memory_bank.save_student_memory(test_student, test_data)
    assert save_result == True, "Save operation failed"
    
    # Test load
    loaded_data = memory_bank.load_student_memory(test_student)
    assert loaded_data.get('learning_data', {}).get('subjects') == ['OS', 'DSA'], "Load operation failed"
    
    # Test update pattern
    memory_bank.update_learning_pattern(test_student, 'OS', 85.0)
    
    print("✅ Memory Bank Tests: PASSED")

if __name__ == "__main__":
    test_memory_operations()