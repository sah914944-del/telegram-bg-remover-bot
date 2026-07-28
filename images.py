"""Image handling: receive a picture and return it without a background."""

from __future__ import annotations

import asyncio
import logging

from telegram import Document, Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot import texts
from bot.services.background_removal import remove_background

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png"}
ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png")
MAX_FILE_SIZE = 20 * 1024 * 1024  # Telegram bot download limit


def _document_is_supported(document: Document) -> bool:
    mime = (document.mime_type or "").lower()
    name = (document.file_name or "").lower()
    return mime in ALLOWED_MIME_TYPES or name.endswith(ALLOWED_EXTENSIONS)


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    chat = update.effective_chat
    if message is None or chat is None:
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        file_size = message.photo[-1].file_size or 0
    elif message.document is not None:
        if not _document_is_supported(message.document):
            await message.reply_text(texts.UNSUPPORTED_FILE)
            return
        file_id = message.document.file_id
        file_size = message.document.file_size or 0
    else:
        await message.reply_text(texts.UNSUPPORTED_FILE)
        return

    if file_size and file_size > MAX_FILE_SIZE:
        await message.reply_text(texts.TOO_LARGE.format(limit_mb=MAX_FILE_SIZE // (1024 * 1024)))
        return

    await message.reply_text(texts.IMAGE_RECEIVED)
    status = await context.bot.send_message(chat.id, texts.PROCESSING)

    try:
        await context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_DOCUMENT)
        telegram_file = await context.bot.get_file(file_id)
        source_bytes = bytes(await telegram_file.download_as_bytearray())

        result = await asyncio.to_thread(remove_background, source_bytes)

        await context.bot.send_document(
            chat.id,
            document=result,
            filename="background_removed.png",
            caption=texts.SUCCESS_CAPTION,
            reply_markup=texts.channel_keyboard(),
        )
    except ValueError:
        logger.info("Rejected unsupported image content", exc_info=True)
        await context.bot.send_message(chat.id, texts.UNSUPPORTED_FILE)
    except Exception:  # noqa: BLE001
        logger.exception("Background removal failed")
        await context.bot.send_message(chat.id, texts.FAILED)
    finally:
        try:
            await status.delete()
        except Exception:  # noqa: BLE001
            pass


async def handle_unsupported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Politely reject anything that is not a JPG/JPEG/PNG image."""
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(texts.UNSUPPORTED_FILE)
