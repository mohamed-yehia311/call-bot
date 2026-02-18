from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Gemini Configuration ---
class GeminiSettings(BaseModel):
    api_key: str = Field(default="", description="Gemini API Key")
    model: str = Field(default="gemini-2.5-flash", description="Gemini Model to use")

# --- Superlinked configuration ---
class SuperlinkedSettings(BaseModel):
    embedding_model: str = Field(default="entence-transformers/all-MiniLM-L6-v2", description="Embedding model used by superlinked") 
    sqm_min_value : int = Field(default=20, description="Minimum value for appartment size in square meter")
    sqm_max_value : int = Field(default=2000, description="Maximum value for appartment size in square meter")
    price_min_value: int = Field(default=100000, description="Minimum value for appartment price in EGP")
    price_max_value: int = Field(default=10000000, description="Maximum value for appartment price in EGP")

# --- Qdrunt configuration ---
class QdrantSettings(BaseModel):
    host: str = Field(default="qdrant", description="Qdrant Host")
    port: int = Field(default=6333, description="Qdrant Port")
    api_key: str = Field(default="", description="Qdrant API Key")
    use_https: bool = Field(default=False, description="Use HTTPS for Qdrant")


# --- Settings Configuration ---
class Settings(BaseSettings):
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)

    superlinked: SuperlinkedSettings = Field(default_factory=SuperlinkedSettings)
    
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()