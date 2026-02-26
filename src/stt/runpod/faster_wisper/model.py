from fastrtc import audio_to_bytes
from openai import OpenAI
from typing import Optional

from ....stt.base import STTModel
from .options import FasterWhisperSTTOptions

class FasterWhisperSTT(STTModel):
    """Speech-to-Text model using Faster Whisper via OpenAI-compatible API."""

    def __init__(self, options: Optional[FasterWhisperSTTOptions] = None):
        self.options = options or FasterWhisperSTTOptions()
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        """Lazy initialization of the OpenAI client."""
        if self._client is None:
            self._client = OpenAI(
                api_key="not-required",  # Faster Whisper usually doesn't need a key, but OpenAI client requires a string
                base_url=f"{self.options.api_url.rstrip('/')}/v1",
            )
        return self._client

    def set_model(self, model: str) -> None:
        self.options.model = model

    def set_api_url(self, api_url: str) -> None:
        """Updates the API URL and resets the client to apply changes."""
        self.options.api_url = api_url
        self._client = None 

    def stt(self, audio_data: bytes) -> str:
        """
        Convert speech audio to text with basic error handling.
        """
        if not audio_data:
            return ""

        try:
            # Note: ensuring the filename/format matches what the server expects
            audio_file = ("audio.wav", audio_to_bytes(audio_data), "audio/wav")
            
            response = self.client.audio.transcriptions.create(
                file=audio_file,
                model=self.options.model,
                response_format="verbose_json",
            )
            return response.text
        except Exception as e:
            # In a production environment, use a proper logger here
            print(f"STT Error: {e}")
            return ""