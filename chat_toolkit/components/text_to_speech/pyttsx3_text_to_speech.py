from typing import Any

import pyttsx3

from chat_toolkit.components.text_to_speech.text_to_speech_component_base import (  # noqa E501
    TextToSpeechComponentBase,
)


class Pyttsx3TextToSpeech(TextToSpeechComponentBase):
    """
    Class for interacting with pyttsx, a free, offline text to speech package.
    """

    def __init__(self, speaking_rate: int = 175):
        super().__init__(
            model="pyttsx3", pricing_rate=0.0, speaking_rate=speaking_rate
        )
        self.engine = pyttsx3.init()
        self.set_pyttsx3_property("rate", self.speaking_rate)

    def set_pyttsx3_property(self, pyttsx3_property: str, value: Any) -> None:
        """
        Set/update a property in the pyttsx3 engine. See their documentation
        for more information.
        :param pyttsx3_property: property to alter
        :param value: value to set
        """
        self.engine.setProperty(pyttsx3_property, value)
        self.engine.runAndWait()

    def say_text(self, text: str) -> dict:
        """
        Synthesize some text.

        :param text: Text to say.
        :return: Any applicable metadata.
        """
        self.engine.say(text)
        self.engine.runAndWait()
        return {}

    @property
    def _cost_estimate_data(self) -> tuple[float, dict]:
        """
        Property representing cost estimate data for the conversation so
        far. In this case, this is a free package, so there is never a cost.

        :return: Cost estimate in dollars, any applicable metadata.
        """
        return 0.0, {}
