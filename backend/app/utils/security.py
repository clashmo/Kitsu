from datetime import datetime, timedelta, timezone
import hashlib
import hmac
from typing import Any

import jwt
from passlib.context import CryptContext

from ..config import settings

class TokenExpiredError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(payload: dict[str, Any]) -> str:
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError from exc
    except jwt.InvalidTokenError as exc:
        raise TokenInvalidError from exc


def create_refresh_token(user_id: Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    payload = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_refresh_token(raw: str, hashed: str) -> bool:
    expected_hash = hash_refresh_token(raw)
    return hmac.compare_digest(expected_hash, hashed)


def decode_refresh_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError from exc
    except jwt.InvalidSignatureError as exc:
        raise TokenInvalidError from exc
    except jwt.InvalidTokenError as exc:
        raise TokenInvalidError from exc

    if payload.get("type") != "refresh":
        raise TokenInvalidError
    return payload
