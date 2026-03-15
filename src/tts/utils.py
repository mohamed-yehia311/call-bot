from src.tts.base import TTSModel
from src.tts.local import KokoroTTSModel
from loguru import logger

def get_tts_model(model_name: str) -> TTSModel:
    """Get a TTS model by name.

    Available options:
        - "kokoro": Local Kokoro TTS via FastRTC
        - "orpheus-runpod": Orpheus TTS via RunPod deployment
        - "together": Together AI API (supports Orpheus, Kokoro, Cartesia)
    """
    if model_name == "kokoro":
        return KokoroTTSModel()
    # elif model_name == "orpheus-runpod":
    #     orpheus_model = OrpheusTTSModel()
    #     logger.info("Warming up Orpheus TTS model...")
    #     orpheus_model.tts_blocking("This is just a simple message to warmup the model")
    #     return orpheus_model
    # elif model_name == "together":
    #     return TogetherTTSModel()
    else:
        raise ValueError(
            f"Invalid TTS model name: {model_name}. Available: kokoro, orpheus-runpod, together"
        )