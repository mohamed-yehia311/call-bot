import httpx
import numpy as np
from typing import AsyncIterator, Optional
from loguru import logger
from numpy.typing import NDArray

from ..base import TTSModel
from .options import (
    DEFAULT_VOICES,
    TogetherTTSOptions,
)

class TogetherTTSModel(TTSModel):
    """
    Client for Together AI's TTS API using native async streaming.
    
    Streams raw binary PCM audio directly into numpy arrays for low-latency
    FastRTC/WebRTC transmission.
    """

    # Audio format constants
    CHANNELS = 1
    BYTES_PER_SAMPLE = 2  # 16-bit PCM = 2 bytes
    MIN_CHUNK_SIZE = 1024  # About 21ms at 24kHz

    def __init__(self, options: Optional[TogetherTTSOptions] = None):
        self.options = options or TogetherTTSOptions()
        
        if not self.options.api_key:
            raise ValueError("Together AI API key is required.")

        if not self.options.voice:
            self.options.voice = DEFAULT_VOICES.get(self.options.model, "tara")

        # Reuse a single client for connection pooling
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(300.0, connect=10.0),
            headers={
                "Authorization": f"Bearer {self.options.api_key}",
                "Content-Type": "application/json",
            }
        )
        logger.info(f"🎤 Together AI TTS ready ({self.options.model})")

    @property
    def sample_rate(self) -> int:
        return self.options.sample_rate

    async def tts(self, text: str, **kwargs) -> NDArray[np.int16]:
        """Synthesize full text and return a single audio array."""
        chunks = [chunk async for chunk in self.stream_tts(text, **kwargs)]
        return np.concatenate(chunks) if chunks else np.array([], dtype=np.int16)

    async def stream_tts(self, text: str, **kwargs) -> AsyncIterator[NDArray[np.int16]]:
        """
        Streams audio chunks asynchronously from Together AI.
        """
        if not text.strip():
            return

        payload = {
            "model": self.options.model,
            "input": text.strip(),
            "voice": self.options.voice,
            "stream": True,
            "response_format": "raw",
            "response_encoding": "pcm_s16le",
            "sample_rate": self.sample_rate,
        }

        pcm_buffer = b""
        
        try:
            async with self._client.stream(
                "POST", f"{self.options.api_url}/audio/speech", json=payload
            ) as response:
                response.raise_for_status()

                async for chunk in response.aiter_bytes():
                    pcm_buffer += chunk

                    # Yield chunks only when we have enough data and are 2-byte aligned
                    if len(pcm_buffer) >= self.MIN_CHUNK_SIZE:
                        # Ensure we don't split a 16-bit sample (2 bytes) in half
                        alignment_idx = (len(pcm_buffer) // self.BYTES_PER_SAMPLE) * self.BYTES_PER_SAMPLE
                        
                        yield np.frombuffer(pcm_buffer[:alignment_idx], dtype=np.int16)
                        pcm_buffer = pcm_buffer[alignment_idx:]

                # Final flush
                if len(pcm_buffer) >= self.BYTES_PER_SAMPLE:
                    yield np.frombuffer(pcm_buffer, dtype=np.int16)

        except Exception as e:
            logger.error(f"Together AI streaming failed: {e}")
            raise

    def get_stream_info(self) -> tuple[str, int, int]:
        """Returns metadata required for audio playback engines."""
        return ("pcm_s16le", self.CHANNELS, self.sample_rate)

    async def close(self):
        """Clean up the underlying HTTP client."""
        await self._client.aclose()