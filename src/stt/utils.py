from src.stt.local import MoonshineSTT
from src.stt.groq import GroqWhisperSTT
from src.stt.base import STTModel




def get_stt_model(model: str) -> STTModel:
    """Get the STT model based on the model name."""
    if model == "moonshine":
        return MoonshineSTT()
    elif model == "groq":
        return GroqWhisperSTT()
    # elif model == "faster-whisper":
    #     return FasterWhisperSTT()
    else:
        raise ValueError(f"Invalid model: {model}")