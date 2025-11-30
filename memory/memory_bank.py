import json
import os
from typing import Dict, List, Any
from datetime import datetime
from utils.logger import logger

class MemoryBank:
    """Long-term memory storage for student learning patterns"""
    
    def __init__(self, storage_path: str = "./memory_data/"):
        self.storage_path = storage_path
        self._ensure_storage_path()
        logger.info("✅ Memory Bank initialized")
    
    def _ensure_storage_path(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def save_student_memory(self, student_id: str, memory_data: Dict[str, Any]):
        """Save student learning patterns to long-term memory"""
        try:
            file_path = os.path.join(self.storage_path, f"{student_id}_memory.json")
            
            # Load existing memory if exists
            existing_data = {}
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
            
            # Update with new data
            existing_data.update({
                'last_updated': datetime.now().isoformat(),
                'learning_data': memory_data
            })
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            logger.info(f"✅ Memory saved for student {student_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving memory: {e}")
            return False
    
    def load_student_memory(self, student_id: str) -> Dict[str, Any]:
        """Load student learning patterns from long-term memory"""
        try:
            file_path = os.path.join(self.storage_path, f"{student_id}_memory.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    memory_data = json.load(f)
                logger.info(f"✅ Memory loaded for student {student_id}")
                return memory_data
            else:
                logger.info(f"📝 No existing memory found for student {student_id}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error loading memory: {e}")
            return {}
    
    def update_learning_pattern(self, student_id: str, subject: str, performance: float):
        """Update learning patterns based on recent performance"""
        memory = self.load_student_memory(student_id)
        
        if 'learning_patterns' not in memory:
            memory['learning_patterns'] = {}
        
        if subject not in memory['learning_patterns']:
            memory['learning_patterns'][subject] = []
        
        memory['learning_patterns'][subject].append({
            'timestamp': datetime.now().isoformat(),
            'performance': performance,
            'difficulty_level': self._calculate_difficulty(performance)
        })
        
        self.save_student_memory(student_id, memory)
        logger.info(f"✅ Learning pattern updated for {student_id} in {subject}")

    def _calculate_difficulty(self, performance: float) -> str:
        """Calculate difficulty level based on performance"""
        if performance >= 80:
            return 'advanced'
        elif performance >= 60:
            return 'intermediate'
        else:
            return 'beginner'

# Global memory bank instance
memory_bank = MemoryBank()