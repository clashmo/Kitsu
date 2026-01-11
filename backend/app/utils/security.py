import secrets
from typing import Any


def create_access_token(subject: Any) -> str:
    """
    TODO: Replace with JWT implementation.
    """
    return secrets.token_urlsafe(32)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    TODO: Replace with secure password hashing and verification.
    """
    return plain_password == hashed_password

