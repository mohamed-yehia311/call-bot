from .base import BaseVoiceEffect, AudioChunk
from .utils.audio_loader import load_audio_chunks
from typing import AsyncIterator, List
import asyncio

class KeyboardEffect(BaseVoiceEffect):
    "stream the keyboard sound for max_duration_s seconds"

    def __init__(self, sound_path: str, max_duration_s: float = 3.0, target_rate: int = 16000, chunck_ms: int = 100 ):
        self.sound_path = sound_path
        self.max_druation_s = max_duration_s
        self.target_rate =  target_rate
        self.chucks = load_audio_chunks(self.sound_path, target_rate=target_rate, chunk_ms=chunck_ms) 


    async def stream(self) -> AsyncIterator[AudioChunk]:
        if self.max_duration_s <= 0:
            return

        total_samples = 0
        total_samples_allowed = None

        for sample_rate, chunk in self.chunks:
            # lazy initialize allowed sample budget
            if total_samples_allowed is None:
                total_samples_allowed = int(self.max_duration_s * sample_rate)

            if total_samples >= total_samples_allowed:
                break

            remaining_samples = total_samples_allowed - total_samples

            # Trim last chunk if needed
            if len(chunk) > remaining_samples:
                chunk = chunk[:remaining_samples]

            if len(chunk) == 0:
                break

            yield (sample_rate, chunk)
            total_samples += len(chunk)

            await asyncio.sleep(0)
