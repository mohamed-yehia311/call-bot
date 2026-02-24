import json
import httpx
import numpy as np
from typing import AsyncIterator, Optional
from loguru import logger
from numpy.typing import NDArray

from ...base import TTSModel
from .options import (
    CUSTOM_TOKEN_PREFIX,
    OrpheusTTSOptions,
)
from .token_decoder import convert_to_audio


class OrpheusTTSModel(TTSModel):
    """
    Orpheus TTS Model implementation using native async streaming.
    """

    def __init__(self, options: Optional[OrpheusTTSOptions] = None):
        self.options = options or OrpheusTTSOptions()
        self._client = httpx.AsyncClient(timeout=None)

    @property
    def sample_rate(self) -> int:
        return self.options.sample_rate

    async def tts(self, text: str, **kwargs) -> NDArray[np.int16]:
        """Synthesize full audio by collecting all streamed chunks."""
        chunks = [chunk async for chunk in self.stream_tts(text, **kwargs)]
        if not chunks:
            return np.array([], dtype=np.int16)
        return np.concatenate(chunks)

    async def stream_tts(self, text: str, **kwargs) -> AsyncIterator[NDArray[np.int16]]:
        """
        Streams audio chunks from the RunPod API.
        """
        opts = self.options # In a real app, merge kwargs into a copy of opts
        payload = self._build_payload(text, opts)
        
        try:
            async with self._client.stream(
                "POST", 
                f"{opts.api_url}/v1/completions", 
                json=payload, 
                headers=opts.headers
            ) as response:
                response.raise_for_status()
                
                async for chunk in self._parse_api_stream(response):
                    yield chunk

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise

    async def _parse_api_stream(self, response: httpx.Response) -> AsyncIterator[NDArray[np.int16]]:
        """Handles the Server-Sent Events (SSE) and Orpheus token buffering."""
        buffer: list[int] = []
        token_count = 0
        
        async for line in response.aiter_lines():
            if not line.startswith("data: "):
                continue
            
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break

            try:
                data = json.loads(data_str)
                token_text = data["choices"][0].get("text", "")
                if not token_text:
                    continue
                
                token_id = self._decode_token_id(token_text, token_count)
                if token_id is not None:
                    buffer.append(token_id)
                    token_count += 1

                    # Orpheus Logic: Process every 7 tokens once we have at least 28
                    if token_count >= 28 and token_count % 7 == 0:
                        yield self._convert_to_pcm(buffer[-28:], token_count)
            
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Skipping malformed stream data: {e}")

    def _decode_token_id(self, token_string: str, index: int) -> Optional[int]:
        """Extracts and de-indexes the Orpheus-specific token ID."""
        token_string = token_string.strip()
        start_idx = token_string.rfind(CUSTOM_TOKEN_PREFIX)
        
        if start_idx == -1 or not token_string.endswith(">"):
            return None

        try:
            # Format: <custom_token_XXXXX>
            raw_id = int(token_string[len(CUSTOM_TOKEN_PREFIX) + 1 : -1])
            # Orpheus positional de-indexing logic
            return raw_id - 10 - ((index % 7) * 4096)
        except (ValueError, IndexError):
            return None

    def _convert_to_pcm(self, token_ids: list[int], count: int) -> NDArray[np.int16]:
        """Converts a window of token IDs into a NumPy PCM array."""
        audio_bytes = convert_to_audio(token_ids, count)
        if audio_bytes:
            return np.frombuffer(audio_bytes, dtype=np.int16)
        return np.array([], dtype=np.int16)

    def _build_payload(self, text: str, opts: OrpheusTTSOptions) -> dict:
        """Formats the Orpheus-specific prompt and API payload."""
        prompt = f"<|audio|>{opts.voice}: {text}<|eot_id|>"
        return {
            "model": opts.model,
            "prompt": prompt,
            "max_tokens": opts.max_tokens,
            "temperature": opts.temperature,
            "stream": True,
            **opts.model_extra_params # Hypothetical field for repetition_penalty etc.
        }

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()