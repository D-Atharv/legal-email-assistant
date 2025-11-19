"""
Configuration management using Pydantic Settings.

Purpose:
- Load environment variables
- Store Gemini API configuration
- Expose a reusable `settings` object across the backend
- Used by analyzer, drafter, and LangGraph workflow

"""


from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # === App settings ===
    APP_NAME: str = "Legal Email Assistant - Backend"
    LOG_LEVEL: str = "INFO"

    # === Frontend CORS ===
    FRONTEND_ORIGIN: str | None = Field(default="http://localhost:3000")

    # === LLM Provider (Gemini) ===
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model to use for analysis & drafting"
    )

    # === Audit Logs ===
    AUDIT_LOG_DIR: str = Field(default="static/audit_logs")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings object
settings = Settings()
