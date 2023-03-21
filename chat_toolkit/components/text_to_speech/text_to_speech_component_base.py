from abc import ABC, abstractmethod

from chat_toolkit.common.exceptions import SpeakingRateError
from chat_toolkit.components.component_base import ComponentBase


class TextToSpeechComponentBase(ComponentBase, ABC):
    """
    Used to create text to speech components in standardized manner.
    """

    def __init__(self, speaking_rate: int, **kwargs):
        super().__init__(**kwargs)
        if speaking_rate <= 0:
            raise SpeakingRateError
        self.speaking_rate = speaking_rate

    @abstractmethod
    def say_text(self, text: str) -> dict:
        """
        Abstract method for synthesizing some text.

        :param text: Text to speak.
        :return: Any applicable metadata.
        """
        pass
