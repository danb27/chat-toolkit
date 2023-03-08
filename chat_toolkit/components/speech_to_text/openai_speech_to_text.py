import io
from pathlib import Path
from typing import Union

import openai

from chat_toolkit.common.constants import TMP_DIR
from chat_toolkit.components.speech_to_text.speech_to_text_component_base import (  # noqa: E501
    SpeechToTextComponentBase,
)


class OpenAISpeechToText(SpeechToTextComponentBase):
    """
    Class for interacting with one of OpenAI's speech to text algorithms.
    Requires OPENAI_API_KEY environment variable.
    """

    _channels = 2

    def __init__(
        self,
        model: str = "whisper-1",
        pricing_rate: float = 0.006,
        device: Union[int, str] = 0,
        channels: int = 2,
        tmp_file_directory: Path = TMP_DIR,
    ):
        """
        Instantiate a speech to text interaction object.

        :param model: OpenAI's speech to text model to use.
        :param pricing_rate: Pricing rate per minute of audio transcribed.
        Used to calculate cost estimates of orchestrators. See notes about
        user responsibility re: costs + estimates in CostEstimatorBase.
        :param device: Device to use for capturing audio. Must be understood
        by sounddevice
        :param channels: Number of channels
        :param tmp_file_directory: Directory to use for temporary files,
        will use a default directory if not provided.
        """
        super().__init__(
            model=model,
            pricing_rate=pricing_rate,
            tmp_file_directory=tmp_file_directory,
            device=device,
            channels=channels,
        )

    @property
    def cost_estimate_data(self) -> tuple[float, dict]:
        """
        Property representing most recent cost estimate based on number of
        tokens charged by OpenAI so far in the object's usage. See notes about
        user responsibility regarding costs and estimates in CostEstimatorBase.

        :return: Cost estimate in dollars, any applicable metadata.
        """
        cost_estimate = self._seconds_transcribed / 60 * self._pricing_rate
        metadata = {"seconds_transcribed": self._seconds_transcribed}
        return cost_estimate, metadata

    def transcribe(self, audio_file: io.BufferedRandom) -> tuple[str, dict]:
        """
        Transcribe audio from a supported file type with OpenAI's api.

        :param audio_file: Open audio file.
        :return: Transcribed text.
        """
        transcription = openai.Audio.transcribe(self._model, audio_file)
        return transcription["text"], {}
