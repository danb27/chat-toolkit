import pyttsx3

from chat_toolkit.components.text_to_speech.text_to_speech_component_base import (  # noqa E501
    TextToSpeechComponentBase,
)


class Pyttsx3TextToSpeech(TextToSpeechComponentBase):
    """
    Class for interacting with pyttsx, a free, offline text to speech package.
    """

    def __init__(self):
        super().__init__(pricing_rate=0.0)
        self.engine = pyttsx3.init()

    def say(self, text: str) -> dict:
        """
        Synthesize some text.

        :param text: Text to say.
        :return: Any applicable metadata.
        """
        self.engine.say(text)
        self.engine.runAndWait()
        return {}

    @property
    def cost_estimate_data(self) -> tuple[float, dict]:
        """
        Property representing cost estimate data for the conversation so
        far. In this case, this is a free package, so there is never a cost.

        :return: Cost estimate in dollars, any applicable metadata.
        """
        return 0.0, {}
