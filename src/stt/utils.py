from .models import FasterWhisperSTT, GroqWhisperSTT, MoonshineSTT, STTModel



def get_stt_model(model: str) -> STTModel:
    """Get the STT model based on the model name."""
    if model == "moonshine":
        return MoonshineSTT()
    elif model == "groq":
        return GroqWhisperSTT()
    elif model == "faster-whisper":
        return FasterWhisperSTT()
    else:
        raise ValueError(f"Invalid model: {model}")