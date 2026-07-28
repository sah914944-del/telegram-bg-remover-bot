"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def _get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"
    use_webhook: bool = False
    webhook_url: str | None = None
    port: int = 8080

    @classmethod
    def load(cls) -> "Settings":
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            raise ConfigError(
                "TELEGRAM_BOT_TOKEN is not set. Add it to your .env file or "
                "to the environment variables of your hosting provider."
            )

        return cls(
            bot_token=token,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            use_webhook=_get_bool("USE_WEBHOOK", False),
            webhook_url=os.getenv("WEBHOOK_URL") or None,
            port=int(os.getenv("PORT", "8080")),
        )


settings_cache: Settings | None = None


def get_settings() -> Settings:
    global settings_cache
    if settings_cache is None:
        settings_cache = Settings.load()
    return settings_cache
