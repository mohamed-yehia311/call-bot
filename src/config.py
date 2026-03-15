from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GroqSettings(BaseModel):
    api_key: str = Field(default="", description="Groq API Key")
    base_url: str = Field(
        default="https://api.groq.com/openai/v1", description="Groq Base URL"
    )
    model: str = Field(default="openai/gpt-oss-20b", description="Groq Model to use")
    stt_model: str = Field(
        default="whisper-large-v3", description="Groq STT Model to use"
    )
# --- Gemini Configuration ---
class GeminiSettings(BaseModel):
    api_key: str = Field(default="", description="Gemini API Key")
    model: str = Field(default="gemini-2.5-flash", description="Gemini Model to use")

# --- Superlinked configuration ---
class SuperlinkedSettings(BaseModel):
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", description="Embedding model used by superlinked") 
    sqm_min_value : int = Field(default=20, description="Minimum value for appartment size in square meter")
    sqm_max_value : int = Field(default=2000, description="Maximum value for appartment size in square meter")
    price_min_value: int = Field(default=100000, description="Minimum value for appartment price in EGP")
    price_max_value: int = Field(default=10000000, description="Maximum value for appartment price in EGP")

# --- Qdrunt configuration ---
class QdrantSettings(BaseModel):
    host: str = Field(default="qdrant", description="Qdrant Host")
    port: int = Field(default=6333, description="Qdrant Port")
    api_key: str = Field(default="", description="Qdrant API Key")
    cluster_url: str = Field(default="", description="Qdrant Cluster URL")
    use_qdrant_cloud: bool = Field(default=True, description="Use Qdrant Cloud")



# --- Opik Configuration ---
class OpikSettings(BaseModel):
    api_key: str = Field(default="", description="Opik API Key")
    project_name: str = Field(default="", description="Opik Project Name")


# --- Twilio Configuration ---
class TwilioSettings(BaseModel):
    account_sid: str = Field(default="", description="Twilio Account SID")
    auth_token: str = Field(default="", description="Twilio Auth Token")


# --- Settings Configuration ---
class Settings(BaseSettings):
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)

    superlinked: SuperlinkedSettings = Field(default_factory=SuperlinkedSettings)
    
    qdrant: QdrantSettings = Field(default_factory=QdrantSettings)

    groq: GroqSettings = Field(default_factory=GroqSettings)

    stt_model: str = Field(default="faster-whisper", description="Family of STT models to use")

    tts_model: str = Field(default="orpheus-runpod", description="Family of TTS models to use")


    opik: OpikSettings = Field(default_factory=OpikSettings)

    twilio: TwilioSettings = Field(default_factory=TwilioSettings)

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=[".env"],
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )


settings = Settings()