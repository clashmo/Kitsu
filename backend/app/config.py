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

    @classmethod
    def from_env(cls) -> "Settings":
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
        )


settings = Settings.from_env()
