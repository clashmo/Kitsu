import os

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
    secret_key: str | None = Field(default=None)
    access_token_expire_minutes: int = Field(default=30)
    algorithm: str = Field(default="HS256")

    @classmethod
    def from_env(cls) -> "Settings":
        secret_key = os.getenv("SECRET_KEY", "").strip()
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable must be set")

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
            secret_key=secret_key,
            access_token_expire_minutes=int(
                os.getenv(
                    "ACCESS_TOKEN_EXPIRE_MINUTES",
                    cls.model_fields["access_token_expire_minutes"].default,
                )
            ),
            algorithm=os.getenv("ALGORITHM", cls.model_fields["algorithm"].default),
        )


settings = Settings.from_env()
