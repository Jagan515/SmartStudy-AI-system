import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.gcp_config import gcp_config

def test_gcp_connection():
    """Test GCP configuration and model loading"""
    try:
        model = gcp_config.get_model()
        if model:
            print("✅ GCP Connection Test: PASSED")
            return True
        else:
            print("❌ GCP Connection Test: FAILED")
            return False
    except Exception as e:
        print(f"❌ GCP Connection Test: ERROR - {e}")
        return False

if __name__ == "__main__":
    test_gcp_connection()