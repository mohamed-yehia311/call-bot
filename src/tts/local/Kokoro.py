from fastrtc import get_tts_model

from ..base import TTSModel


class KokoroTTSModel(TTSModel):
    """Kokoro TTS model."""

    def __init__(self):
        self.model = get_tts_model()

    def tts(self, text: str) -> bytes:
        return self.model.tts(text)

    def stream_tts(self, text: str):
        return self.model.stream_tts(text)