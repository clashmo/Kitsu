import os
import secrets
import warnings

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class Settings(BaseModel):
    app_name: str = Field(default="Kitsu Backend")
    debug: bool = Field(default=False)
    database_url: str = Field(
        default="postgresql+asyncpg://kitsu:kitsu@db:5432/kitsu"
    )
    allowed_origins: list[str] = Field(default_factory=lambda: ["*"])
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_minutes: int = Field(default=60 * 24 * 7)

    @classmethod
    def from_env(cls) -> "Settings":
        secret_from_env = os.getenv("SECRET_KEY")
        if not secret_from_env:
            warnings.warn(
                "SECRET_KEY is not set; generating a transient key. "
                "Set SECRET_KEY in the environment to keep tokens valid across restarts.",
                stacklevel=1,
            )
        return cls(
            app_name=os.getenv("APP_NAME", cls.model_fields["app_name"].default),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv(
                "DATABASE_URL", cls.model_fields["database_url"].default
            ),
            allowed_origins=[
                origin.strip()
                for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
                if origin.strip()
            ],
            secret_key=secret_from_env or cls.model_fields["secret_key"].default_factory(),
            jwt_algorithm=os.getenv(
                "JWT_ALGORITHM", cls.model_fields["jwt_algorithm"].default
            ),
            access_token_expire_minutes=int(
                os.getenv(
                    "ACCESS_TOKEN_EXPIRE_MINUTES",
                    cls.model_fields["access_token_expire_minutes"].default,
                )
            ),
            refresh_token_expire_minutes=int(
                os.getenv(
                    "REFRESH_TOKEN_EXPIRE_MINUTES",
                    cls.model_fields["refresh_token_expire_minutes"].default,
                )
            ),
        )


settings = Settings.from_env()
