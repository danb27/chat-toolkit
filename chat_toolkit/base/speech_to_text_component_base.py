from abc import ABC, abstractmethod

from chat_toolkit.base.component_base import ComponentBase


class SpeechToTextComponentBase(ComponentBase, ABC):
    """
    Used to create speech to text components in a standardized manner.
    """

    @abstractmethod
    def record_and_transcribe(self) -> tuple[str, dict]:
        """
        Abstract method for recording a user's audio and transcribing it to
        text.

        :return: transcribed text, any applicable metadata.
        """
        pass
