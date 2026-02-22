from abc import ABC, abstractmethod
from typing import Union


class STTModel(ABC):
    """
    Base abstract class for Speech-to-Text (STT) models.

    Any STT implementation must inherit from this class
    and provide an implementation for the `stt` method.
    """

    @abstractmethod
    async def stt(
        self,
        audio_data: Union[bytes, str],
        **kwargs
    ) -> str:
        """
        Transcribe speech audio into text.

        Parameters:
            audio_data (Union[bytes, str]):
                Either raw audio bytes or a file path to an audio file.
            **kwargs:
                Optional keyword arguments specific to the model implementation.

        Returns:
            str:
                The transcription result as text.

        Note:
            This method must be implemented by all subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `stt` method.")