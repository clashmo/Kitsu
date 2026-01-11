import imghdr
import secrets
from pathlib import Path

from fastapi import UploadFile


_BASE_DIR = Path(__file__).resolve().parents[2]
_AVATAR_DIR = _BASE_DIR / "uploads" / "avatars"
_MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB
_ALLOWED_IMAGE_TYPES = {"jpeg", "png", "gif", "bmp", "webp"}
_HEADER_BYTES = 1024
_CHUNK_SIZE = 1024 * 1024


def _ensure_avatar_dir() -> None:
    _AVATAR_DIR.mkdir(parents=True, exist_ok=True)


def _generate_avatar_name(original_name: str | None) -> str:
    suffix = Path(original_name or "").suffix
    return f"{secrets.token_hex(16)}{suffix}"


async def save_avatar_file(upload: UploadFile) -> str:
    _ensure_avatar_dir()
    filename = _generate_avatar_name(upload.filename)
    destination = _AVATAR_DIR / filename
    total_bytes = 0

    header = await upload.read(_HEADER_BYTES)
    if not header:
        raise ValueError("Empty file upload.")
    if len(header) > _MAX_AVATAR_SIZE:
        raise ValueError("Avatar file is too large.")

    detected_type = imghdr.what(None, h=header)
    if detected_type not in _ALLOWED_IMAGE_TYPES:
        raise ValueError("Invalid image upload.")

    try:
        with destination.open("wb") as buffer:
            buffer.write(header)
            total_bytes += len(header)
            if total_bytes > _MAX_AVATAR_SIZE:
                raise ValueError("Avatar file is too large.")

            while True:
                chunk = await upload.read(_CHUNK_SIZE)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > _MAX_AVATAR_SIZE:
                    raise ValueError("Avatar file is too large.")
                buffer.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise

    return destination.relative_to(_BASE_DIR).as_posix()


def delete_avatar_file(path_str: str) -> None:
    candidate = (_BASE_DIR / path_str).resolve()
    avatar_root = _AVATAR_DIR.resolve()
    if not candidate.is_relative_to(avatar_root):
        return
    if candidate.exists():
        candidate.unlink()
