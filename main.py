"""Entry point for the Telegram Background Remover Bot."""

from __future__ import annotations

import sys

from bot.app import run
from bot.config import ConfigError


def main() -> int:
    try:
        run()
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Shutting down.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
