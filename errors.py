"""Global error handler."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot import texts

logger = logging.getLogger(__name__)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled error while processing update", exc_info=context.error)

    if isinstance(update, Update) and update.effective_chat is not None:
        try:
            await context.bot.send_message(update.effective_chat.id, texts.FAILED)
        except Exception:  # noqa: BLE001
            logger.warning("Could not deliver the error message to the user")
