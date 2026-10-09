"""Application configuration using pydantic-settings."""

from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql+psycopg://jobmail:jobmail@localhost:5432/jobmail",
        description="Database connection URL (PostgreSQL or SQLite for dev)",
    )

    # LLM
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    classifier_model: str = Field(
        default="claude-haiku-4-5", description="Claude model for classification"
    )
    llm_max_body_chars: int = Field(
        default=4000, description="Maximum characters to send to LLM"
    )

    # Telegram
    telegram_bot_token: str = Field(default="", description="Telegram bot token")
    telegram_chat_id: str = Field(default="", description="Allowed Telegram chat ID")
    notify_mode: str = Field(
        default="job_only",
        description="Notification mode: all, job_only, or digest",
    )

    @field_validator("notify_mode")
    @classmethod
    def validate_notify_mode(cls, v: str) -> str:
        """Validate notification mode."""
        if v not in ("all", "job_only", "digest"):
            raise ValueError("notify_mode must be 'all', 'job_only', or 'digest'")
        return v

    # Gmail
    gmail_credentials_file: Path = Field(
        default=Path("secrets/gmail_client_secret.json"),
        description="Path to Gmail OAuth credentials",
    )
    gmail_token_file: Path = Field(
        default=Path("secrets/gmail_token.json"),
        description="Path to Gmail OAuth token",
    )
    gmail_pubsub_topic: str = Field(
        default="", description="Gmail Pub/Sub topic for push notifications"
    )
    gmail_poll_interval_sec: int = Field(
        default=60, description="Gmail polling interval in seconds"
    )

    # IMAP
    imap_accounts: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of IMAP account configurations",
    )

    # Logic
    ghosting_days: int = Field(
        default=30, description="Days without response before marking as ghosted"
    )
    backfill_months: int = Field(
        default=6, description="Months to backfill when initializing"
    )

    # App
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")


# Global settings instance
settings = Settings()
