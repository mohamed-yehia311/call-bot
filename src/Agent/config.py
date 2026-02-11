from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Groq Configuration ---
class GeminiSettings(BaseModel):
    api_key: str = Field(default="", description="Groq API Key")
    model: str = Field(default="gemini-2.5-flash", description="Groq Model to use")


# --- Settings Configuration ---
class Settings(BaseSettings):
    groq: GeminiSettings = Field(default_factory=GeminiSettings)

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()