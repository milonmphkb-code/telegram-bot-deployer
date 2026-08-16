"""
Central configuration for the bot.
Everything is loaded from environment variables (.env in local dev).
Never hard-code secrets here.
"""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram
    BOT_TOKEN: str
    ADMIN_IDS: str = ""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./bot.db"

    # Redis / job queue (Phase 5+)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    ENCRYPTION_KEY: str = ""

    # Uploads (Phase 4+)
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_MB: int = 50

    # Support
    SUPPORT_USERNAME: str = ""

    @property
    def admin_ids(self) -> set[int]:
        """Parses ADMIN_IDS='123,456' into a set of ints. Ignores blanks/bad values."""
        ids: set[int] = set()
        for raw in self.ADMIN_IDS.split(","):
            raw = raw.strip()
            if raw.isdigit():
                ids.add(int(raw))
        return ids

    @property
    def upload_dir_path(self) -> Path:
        path = Path(self.UPLOAD_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
