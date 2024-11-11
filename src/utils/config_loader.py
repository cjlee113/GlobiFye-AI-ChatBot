import os
from dotenv import load_dotenv

def load_config():
    """Loads configuration settings and API keys."""
    load_dotenv()
    return {
        'YOUTUBE_API_KEY': os.getenv("AIzaSyAV9j3x5eSpKSNqELGYg5fZ5xzKNV-auYs")
    }