"""/start and /help commands."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from bot import texts

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    if user is None or chat is None:
        return

    # 1. Send the user's Telegram profile photo first, if they have one.
    try:
        photos = await context.bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count and photos.photos:
            best = photos.photos[0][-1]
            await context.bot.send_chat_action(chat.id, ChatAction.UPLOAD_PHOTO)
            await context.bot.send_photo(chat.id, best.file_id)
    except Exception:  # noqa: BLE001 - profile photo is a nice-to-have
        logger.warning("Could not send profile photo for user %s", user.id, exc_info=True)

    # 2. Welcome message with the channel button.
    await context.bot.send_message(
        chat.id,
        texts.WELCOME.format(first_name=user.first_name or "there"),
        reply_markup=texts.channel_keyboard(),
    )

    # 3. Immediately ask for the image.
    await context.bot.send_message(chat.id, texts.SEND_IMAGE_PROMPT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None:
        return
    await context.bot.send_message(
        update.effective_chat.id, texts.HELP, parse_mode=ParseMode.HTML
    )
