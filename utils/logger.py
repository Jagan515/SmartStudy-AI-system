import logging
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    """Setup application logger with observability"""
    
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('smart_study.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('SmartStudyAI')
    logger.info("✅ Logger setup completed successfully!")
    return logger

# Global logger instance
logger = setup_logger()