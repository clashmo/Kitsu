import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class Settings(BaseModel):
    app_name: str = Field(default="Kitsu Backend")
    debug: bool = Field(default=False)
    database_url: str = Field(default="")
    allowed_origins: list[str] = Field(default_factory=list)
    secret_key: str | None = Field(default=None)
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=14)
    algorithm: str = Field(default="HS256")

    @classmethod
    def from_env(cls) -> "Settings":
        secret_key = os.getenv("SECRET_KEY", "").strip()
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable must be set")

        raw_allowed_origins = os.getenv("ALLOWED_ORIGINS", "").strip()
        if not raw_allowed_origins:
            raise ValueError("ALLOWED_ORIGINS environment variable must be set")

        allowed_origins = [
            origin.strip() for origin in raw_allowed_origins.split(",") if origin.strip()
        ]
        if not allowed_origins:
            raise ValueError("ALLOWED_ORIGINS must contain at least one origin")

        if "*" in allowed_origins:
            raise ValueError(
                "ALLOWED_ORIGINS cannot contain '*' when credentialed requests are used"
            )

        for origin in allowed_origins:
            parsed = urlparse(origin)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError(
                    "ALLOWED_ORIGINS must contain valid http/https origins with host"
                )

        database_url = os.getenv("DATABASE_URL", "").strip()
        if not database_url:
            raise ValueError("DATABASE_URL environment variable must be set")

        parsed_db = urlparse(database_url)
        if parsed_db.scheme != "postgresql+asyncpg":
            raise ValueError("DATABASE_URL must start with 'postgresql+asyncpg://'")
        if not parsed_db.hostname:
            raise ValueError("DATABASE_URL must include hostname")

        return cls(
            app_name=os.getenv("APP_NAME", cls.model_fields["app_name"].default),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=database_url,
            allowed_origins=allowed_origins,
            secret_key=secret_key,
            access_token_expire_minutes=int(
                os.getenv(
                    "ACCESS_TOKEN_EXPIRE_MINUTES",
                    cls.model_fields["access_token_expire_minutes"].default,
                )
            ),
            refresh_token_expire_days=int(
                os.getenv(
                    "REFRESH_TOKEN_EXPIRE_DAYS",
                    cls.model_fields["refresh_token_expire_days"].default,
                )
            ),
            algorithm=os.getenv("ALGORITHM", cls.model_fields["algorithm"].default),
        )


settings = Settings.from_env()
