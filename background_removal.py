"""Background removal service.

Uses `rembg` (ISNet general-use model) locally — no third-party API key
required. The heavy lifting is CPU-bound, so callers should run
`remove_background` in a worker thread.
"""

from __future__ import annotations

import io
import logging
import threading

from PIL import Image

logger = logging.getLogger(__name__)

# Highest-quality general purpose model shipped with rembg.
MODEL_NAME = "isnet-general-use"

_session = None
_session_lock = threading.Lock()


def _get_session():
    """Lazily create and cache the rembg session (model is loaded once)."""
    global _session
    if _session is None:
        with _session_lock:
            if _session is None:
                from rembg import new_session

                logger.info("Loading background removal model: %s", MODEL_NAME)
                _session = new_session(MODEL_NAME)
    return _session


def warmup() -> None:
    """Preload the model so the first user request is not slow."""
    try:
        _get_session()
    except Exception:  # pragma: no cover - best effort
        logger.exception("Background removal model warmup failed")


def remove_background(image_bytes: bytes) -> bytes:
    """Remove the background and return a transparent PNG as bytes.

    Raises:
        ValueError: if the input cannot be decoded as an image.
    """
    from rembg import remove

    try:
        source = Image.open(io.BytesIO(image_bytes))
        source.load()
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Unsupported or corrupted image file") from exc

    source = source.convert("RGBA")

    result = remove(
        source,
        session=_get_session(),
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
        post_process_mask=True,
    )

    buffer = io.BytesIO()
    result.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer.getvalue()
