import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "linguaai-localstorage-2026")
    
    # Storage Engine Configuration
    # Supabase and external database dependencies have been removed.
    # All learner records persist directly in browser localStorage.
    STORAGE_ENGINE = "localStorage"
    
    # Gemini AI configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
