"""User-facing text and markup constants."""

from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CHANNEL_URL = "https://t.me/Eagle_earner_official"
CREATOR = "@bittu_bhaii"

WELCOME = (
    "👋 Hi, {first_name}!\n\n"
    "Welcome to our Background Remover Bot.\n\n"
    f"Made by {CREATOR}"
)

SEND_IMAGE_PROMPT = "🖼️ Please send the image whose background you want to remove."

IMAGE_RECEIVED = "📥 Image received..."
PROCESSING = "⏳ Processing image..."
SUCCESS_CAPTION = "✅ Your image has been generated successfully!"

UNSUPPORTED_FILE = (
    "⚠️ Sorry, I can only work with JPG, JPEG and PNG images.\n\n"
    "Please send your picture as a photo or as a JPG/PNG file."
)

TOO_LARGE = (
    "⚠️ That file is a bit too large for me.\n\n"
    "Please send an image smaller than {limit_mb} MB."
)

FAILED = (
    "❌ Something went wrong while processing your image.\n\n"
    "Please try again in a moment, or send a different picture."
)

HELP = (
    "ℹ️ <b>How to use this bot</b>\n\n"
    "1. Send me a photo (JPG, JPEG or PNG).\n"
    "2. Wait a few seconds while I remove the background.\n"
    "3. Receive your image back as a transparent PNG.\n\n"
    "Commands:\n"
    "/start — restart the bot\n"
    "/help — show this message"
)


def channel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_URL)]]
    )
