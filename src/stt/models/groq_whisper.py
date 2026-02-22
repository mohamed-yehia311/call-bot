from openai import OpenAI, OpenAIError
from .base import STTModel
from ...config import settings
from fastrtc import audio_to_bytes


class GroqWhisperSTT(STTModel):
    """Speech-to-Text implementation utilizing Groq's high-speed Whisper API."""

    def __init__(self, model_name: str = settings.groq.stt_model):
        # Renamed 'groq_client' to 'client' for standard convention
        self.client = OpenAI(
            api_key=settings.groq.api_key, 
            base_url=settings.groq.base_url
        )
        self.model_name = model_name

    def stt(self, audio_data: bytes) -> str:
        """Converts raw audio bytes into transcribed text."""

        response = self.client.audio.transcriptions.create(
            file=("audio.wav", audio_to_bytes(audio_data)),
            model=self.model_name,
            response_format="verbose_json"
        )
        return response.text
