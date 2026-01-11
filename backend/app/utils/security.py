from typing import Any

from passlib.context import CryptContext


def create_access_token(subject: Any) -> str:
    """
    TODO: Replace with JWT implementation.
    """
    raise NotImplementedError("Access token generation is not implemented yet.")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt. Replace or configure as needed for production security policies.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed value."""
    return pwd_context.verify(plain_password, hashed_password)
