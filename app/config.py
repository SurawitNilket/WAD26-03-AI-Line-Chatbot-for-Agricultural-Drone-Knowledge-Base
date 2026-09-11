import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Locate .env file relative to root directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings(BaseModel):
    # App Settings
    APP_NAME: str = "AgriDrone Knowledge Base Chatbot"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")

    # LINE Messaging API
    LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET", "dummy_line_channel_secret").strip().strip('"\'')
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "dummy_line_channel_access_token").strip().strip('"\'')
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip().strip('"\'')
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")

    # Official Citation Portals
    CAAT_UAS_PORTAL_URL: str = "https://uasportal.caat.or.th/"
    CAAT_INFOGRAPHIC_URL: str = "https://uasportal.caat.or.th/infographic"
    NBTC_REGIS_URL: str = "https://anyregis.nbtc.go.th/"
    DOAE_DRONE_MANUAL_URL: str = "https://esc.doae.go.th/wp-content/uploads/2024/05/%E0%B9%82%E0%B8%94%E0%B8%A3%E0%B8%99%E0%B9%80%E0%B8%9E%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%81%E0%B8%A9%E0%B8%95%E0%B8%A3.pdf"

settings = Settings()
