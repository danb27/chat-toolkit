from abc import ABC, abstractmethod
from math import ceil
from pathlib import Path
from queue import Queue
from typing import Union

import sounddevice as sd
import soundfile as sf
from loguru import logger

from chat_toolkit.common.constants import TMP_DIR
from chat_toolkit.common.key_tracker import KeyTracker
from chat_toolkit.components.component_base import ComponentBase


class SpeechToTextComponentBase(ComponentBase, ABC):
    """
    Used to create speech to text components in a standardized manner.
    """

    def __init__(
        self,
        device: Union[int, str] = 0,
        channels: int = 2,
        tmp_file_directory: Path = TMP_DIR,
        **kwargs,
    ):
        """
        Instantiate a speech to text component object.

        :param device: Device to use for capturing audio. Must be understood
        by sounddevice
        :param channels: Number of channels
        :param tmp_file_directory: Directory to use for temporary files,
        will use a default directory if not provided.
        """
        super().__init__(**kwargs)
        self.tmp_file_directory = tmp_file_directory
        self.device = device
        self.sample_rate = int(
            sd.query_devices(self.device, "input")["default_samplerate"]
        )

        self._channels = channels
        self._seconds_transcribed = 0

    @abstractmethod
    def transcribe_speech(self) -> tuple[str, dict]:
        """
        Abstract method for transcribing speech.

        :return: Transcription text, any applicable metadata.
        """
        pass

    def record_unspecified_length_audio(self, file_path: str) -> None:
        """
        Wait for user to push space bar, then record while they are holding.

        :param file_path: Path to save audio to.
        :return:
        """
        queue: Queue = Queue()
        key_tracker = KeyTracker()

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
                key_tracker.wait_for_recording_to_start()

                with sd.InputStream(
                    samplerate=self.sample_rate,
                    device=self.device,
                    channels=self._channels,
                    callback=_callback,
                ):
                    while True:
                        audio_file.write(queue.get())
                        if not key_tracker.check_if_still_recording():
                            self._seconds_transcribed += ceil(
                                audio_file.frames / self.sample_rate
                            )
                            break

        except KeyboardInterrupt:
            key_tracker.stop_tracking()

    @property
    def seconds_transcribed(self) -> int:
        """
        Read only property representing how many seconds of audio this
        object is estimated to have transcribed so far.

        :return:
        """
        return self._seconds_transcribed
