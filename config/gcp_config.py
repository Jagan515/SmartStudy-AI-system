import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GCPConfig:
    """Google Cloud Platform configuration manager"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self._configure_genai()
    
    def _configure_genai(self):
        """Configure Google Generative AI with API key"""
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        print("✅ Google Generative AI configured successfully!")
    
    def get_model(self):
        """Get the configured Gemini model"""
        try:
            model = genai.GenerativeModel(self.model_name)
            print(f"✅ Gemini model '{self.model_name}' loaded successfully!")
            return model
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None

# Global configuration instance
gcp_config = GCPConfig()