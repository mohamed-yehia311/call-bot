from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np
from numpy.typing import NDArray

class TTSModel(ABC):
    """
    Abstract base class for Text-to-Speech (TTS) models.

    Implementations must provide logic for both standard batch synthesis 
    and chunked streaming synthesis.
    """

    @property
    @abstractmethod
    def sample_rate(self) -> int:
        """The native sampling rate of the model in Hz."""
        pass

    @abstractmethod
    def tts(self, text: str, **kwargs) -> NDArray[np.int16]:
        """
        Convert text to speech audio in a single batch.

        Args:
            text: Text to convert to speech.
            **kwargs: Model-specific parameters (e.g., voice ID, speed).

        Returns:
            NDArray[np.int16]: The synthesized audio waveform.
        """
        pass

    @abstractmethod
    def stream_tts(
        self, text: str, **kwargs
    ) -> Iterator[NDArray[np.int16]]:
        """
        Synthesize audio from text as a stream of chunks.

        Args:
            text: Text to convert to speech.
            **kwargs: Model-specific parameters.

        Yields:
            NDArray[np.int16]: Individual chunks of synthesized audio.
        """
        pass