from abc import ABC, abstractmethod

from chat_toolkit.components.component_base import ComponentBase


class TextToSpeechComponentBase(ComponentBase, ABC):
    """
    Used to create text to speech components in standardized manner.
    """

    def __init__(self, **kwargs):
        super().__init__(model=None, **kwargs)

    @abstractmethod
    def say(self, text: str) -> dict:
        """
        Abstract method for synthesizing some text.

        :param text: Text to speak.
        :return: Any applicable metadata.
        """
        pass
