from fastrtc import get_tts_model

from ..base import TTSModel


class KokoroTTSModel(TTSModel):
    """Kokoro TTS model."""

    def __init__(self):
        self.model = get_tts_model()

    @property
    def sample_rate(self) -> int:
        return getattr(self.model, "sample_rate", 24000)

    def tts(self, text: str, **kwargs):
        return self.model.tts(text)

    def stream_tts(self, text: str, **kwargs):
        return self.model.stream_tts(text)