import os
from dotenv import load_dotenv

def load_config():
    """Loads configuration settings and API keys."""
    load_dotenv()
    return {
        'YOUTUBE_API_KEY': os.getenv("YOUTUBE_API_KEY")
    }