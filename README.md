# Telegram Background Remover Bot

A production-ready project skeleton for a Telegram bot that removes image
backgrounds. Built with Python and the latest
[python-telegram-bot](https://docs.python-telegram-bot.org/) (v21).

Background removal runs **locally** with `rembg` (ISNet general-use model +
alpha matting) — no third-party API key needed.

## Features

- `/start` — sends the user's Telegram profile photo (if any), a welcome
  message with a "📢 Join Our Channel" inline button, then asks for an image.
- `/help` — short usage guide.
- Accepts JPG / JPEG / PNG (as photo or file), replies "📥 Image received...",
  shows "⏳ Processing image...", and returns a transparent PNG.
- Polite rejection of unsupported files and graceful global error handling.

## Project structure

```
.
├── bot/
│   ├── __init__.py
│   ├── app.py             # application factory + runner (polling/webhook)
│   ├── config.py          # env-var based settings
│   ├── logging_config.py  # logging setup
│   ├── texts.py           # user-facing copy + inline keyboard
│   ├── handlers/
│   │   ├── __init__.py    # register_handlers()
│   │   ├── start.py       # /start, /help
│   │   ├── images.py      # photo & document processing
│   │   └── errors.py      # global error handler
│   └── services/
│       └── background_removal.py
├── main.py                # entry point
├── requirements.txt
├── .env.example
├── Procfile               # Railway / Heroku-style worker
├── render.yaml            # Render blueprint
└── runtime.txt
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then fill in TELEGRAM_BOT_TOKEN
python main.py
```

## Configuration

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | yes | – | Token from [@BotFather](https://t.me/BotFather) |
| `LOG_LEVEL` | no | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `USE_WEBHOOK` | no | `false` | Long polling is used by default |
| `WEBHOOK_URL` | no | – | Public HTTPS base URL when webhooks are enabled |
| `PORT` | no | `8080` | Port bound in webhook mode |

Secrets are never committed — they are read from the environment (`.env`
locally, dashboard variables in production).

## Deployment

### Railway
1. Create a new project from this repository.
2. Add the `TELEGRAM_BOT_TOKEN` variable in **Variables**.
3. Railway picks up the `Procfile` and runs the `worker` process.

### Render
1. **New → Blueprint**, point at this repository (`render.yaml`).
2. Set `TELEGRAM_BOT_TOKEN` in the service environment.
3. Deploy — it runs as a background worker with long polling.

Long polling needs no public URL, so a worker/background service is the right
service type on both platforms.

## Notes

- The ISNet model (~180 MB) downloads on first run and is cached; it is also
  preloaded at startup so the first user request stays fast.
- Image processing runs in a worker thread, so the bot stays responsive.
- Max input size is 20 MB (Telegram's bot download limit).
