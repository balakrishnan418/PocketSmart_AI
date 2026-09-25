import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME") or "PocketSmart AI"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT") or "8000")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-only-change-me")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    MAX_UPLOAD_MB: int = int(os.getenv("MAX_UPLOAD_MB") or "5")

settings = Settings()
