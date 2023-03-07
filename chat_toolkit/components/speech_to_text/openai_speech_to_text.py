import io
from math import ceil
from pathlib import Path
from queue import Queue
from typing import Union

import openai
import sounddevice as sd
import soundfile as sf
from loguru import logger

from chat_toolkit.base.speech_to_text_component_base import (
    SpeechToTextComponentBase,
)
from chat_toolkit.common.constants import TMP_DIR
from chat_toolkit.common.utils import (
    RecordingEndedWithKeyboardSignal,
    temporary_file,
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
        :param tmp_file_directory: Directory to use for temporary files,
        will use a default directory if not provided.
        """
        super().__init__(
            model=model,
            pricing_rate=pricing_rate,
        )
        self._seconds_transcribed = 0
        self.device = device
        self.sample_rate = int(
            sd.query_devices(self.device, "input")["default_samplerate"]
        )
        self.tmp_file_directory = tmp_file_directory

    def record_and_transcribe(self) -> tuple[str, dict]:
        """
        Record user's voice and transcribe into text.

        :return: Transcription text, any applicable metadata.
        """
        with temporary_file(
            "wav", tmp_file_directory=self.tmp_file_directory
        ) as tmp:
            try:
                self.record_unspecified_length_audio(tmp.name)
            except RecordingEndedWithKeyboardSignal:
                pass
            transcription = self.transcribe(tmp)
        return transcription, {}

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

    def record_unspecified_length_audio(self, file_path: str) -> None:
        """
        Record audio for an unspecified length of time - until a
        KeyboardInterrupt is raised.

        :param file_path: Path to save audio to.
        :return:
        """
        queue: Queue = Queue()

        def _callback(indata, frames, time, status):  # noqa: F841
            """
            This is called (from a separate thread) for each audio block.
            """
            if status:
                logger.error(
                    "Callback flag found",
                    status=str(status),
                    indatatype=type(indata),
                    frames=str(frames),
                    time=str(time),
                )
            queue.put(indata.copy())

        try:
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(
                file_path,
                mode="w+b",
                samplerate=self.sample_rate,
                channels=self._channels,
                closefd=False,
            ) as audio_file:
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    device=self.device,
                    channels=self._channels,
                    callback=_callback,
                ):
                    print("\n\tRecording... Press Ctrl+C to finish speaking.")
                    while True:
                        audio_file.write(queue.get())
        except KeyboardInterrupt:
            self._seconds_transcribed += ceil(
                audio_file.frames / self.sample_rate
            )
            raise RecordingEndedWithKeyboardSignal

    def transcribe(self, audio_file: io.BufferedRandom) -> str:
        """
        Transcribe audio from a supported file type with OpenAI's api.

        :param audio_file: Open audio file.
        :return: Transcribed text.
        """
        transcription = openai.Audio.transcribe(self._model, audio_file)
        return transcription["text"]

    @property
    def seconds_transcribed(self) -> int:
        """
        Read only property representing how many seconds of audio this
        object is estimated to have transcribed so far.

        :return:
        """
        return self._seconds_transcribed
