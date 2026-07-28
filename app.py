"""Application factory and runner."""

from __future__ import annotations

import asyncio
import logging

from telegram import BotCommand
from telegram.ext import Application, ApplicationBuilder

from bot.config import Settings, get_settings
from bot.handlers import register_handlers
from bot.logging_config import setup_logging
from bot.services.background_removal import warmup

logger = logging.getLogger(__name__)


async def _post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Restart the bot"),
            BotCommand("help", "How to use the bot"),
        ]
    )
    # Load the model in the background so the first request is fast.
    asyncio.create_task(asyncio.to_thread(warmup))


def create_application(settings: Settings | None = None) -> Application:
    settings = settings or get_settings()

    application = (
        ApplicationBuilder()
        .token(settings.bot_token)
        .concurrent_updates(True)
        .post_init(_post_init)
        .build()
    )
    register_handlers(application)
    return application



def run() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)

    application = create_application(settings)

    if settings.use_webhook and settings.webhook_url:
        logger.info("Starting bot in webhook mode on port %s", settings.port)
        application.run_webhook(
            listen="0.0.0.0",
            port=settings.port,
            url_path="telegram",
            webhook_url=f"{settings.webhook_url.rstrip('/')}/telegram",
            drop_pending_updates=True,
        )
    else:
        logger.info("Starting bot with long polling")
        application.run_polling(drop_pending_updates=True)
