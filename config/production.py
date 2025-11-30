import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProductionConfig:
    """Production configuration for Google Cloud"""
    
    def __init__(self):
        self.setup_production_logging()
    
    def setup_production_logging(self):
        """Setup logging for production environment"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()  # Log to console in Cloud Run
            ]
        )
        print("✅ Production logging configured")
    
    def get_google_api_key(self):
        """Get Google API key from environment"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        return api_key
    
    def is_production(self):
        """Check if we're running in production"""
        return os.getenv('K_SERVICE') is not None  # Cloud Run sets this

# Create production config instance
prod_config = ProductionConfig()