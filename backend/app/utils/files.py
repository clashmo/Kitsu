import secrets
from pathlib import Path

from fastapi import UploadFile


_BASE_DIR = Path(__file__).resolve().parents[2]
_AVATAR_DIR = _BASE_DIR / "uploads" / "avatars"


def _ensure_avatar_dir() -> None:
    _AVATAR_DIR.mkdir(parents=True, exist_ok=True)


def _generate_avatar_name(original_name: str | None) -> str:
    suffix = Path(original_name or "").suffix
    return f"{secrets.token_hex(16)}{suffix}"


async def save_avatar_file(upload: UploadFile) -> str:
    _ensure_avatar_dir()
    filename = _generate_avatar_name(upload.filename)
    destination = _AVATAR_DIR / filename
    content = await upload.read()
    with destination.open("wb") as buffer:
        buffer.write(content)
    return destination.relative_to(_BASE_DIR).as_posix()


def delete_avatar_file(path_str: str) -> None:
    candidate = (_BASE_DIR / path_str).resolve()
    try:
        candidate.relative_to(_AVATAR_DIR.resolve())
    except ValueError:
        return
    if candidate.exists():
        candidate.unlink()
