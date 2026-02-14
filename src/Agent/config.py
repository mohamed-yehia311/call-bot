from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Gemini Configuration ---
class GeminiSettings(BaseModel):
    api_key: str = Field(default="", description="Gemini API Key")
    model: str = Field(default="gemini-2.5-flash", description="Gemini Model to use")


# --- Settings Configuration ---
class Settings(BaseSettings):
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()