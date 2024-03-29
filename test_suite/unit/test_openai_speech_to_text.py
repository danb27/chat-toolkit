from pathlib import Path
from typing import Union
from unittest.mock import Mock

import pytest

from chat_toolkit.common.utils import temporary_file
from test_suite.unit.conftest import (
    SPEECH_TO_TEXT_MODEL_TYPES,
    TEST_TEXT,
    OpenAISpeechToTextFactoryType,
)


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
@pytest.mark.parametrize("pricing_rate", [0.1, 0.05, 0.002, 1.0, 0.0])
@pytest.mark.parametrize("device", [0])
def test_init(
    patched_openai_speech_to_text_factory: OpenAISpeechToTextFactoryType,
    model: str,
    pricing_rate: float,
    device: Union[str, int],
) -> None:
    """
    Test that instantiation occurs as expected
    """
    speech_to_text = patched_openai_speech_to_text_factory(
        model, pricing_rate, device
    )
    assert speech_to_text
    assert speech_to_text._model == model
    assert speech_to_text._pricing_rate == pricing_rate
    assert speech_to_text.seconds_transcribed == 0
    assert speech_to_text.sample_rate == 44100
    assert isinstance(speech_to_text.tmp_file_directory, Path)


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
def test_record_and_transcribe_sad(
    patched_openai_speech_to_text_factory: OpenAISpeechToTextFactoryType,
    model: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test that an exception is raised when another error is raised.
    """
    speech_to_text = patched_openai_speech_to_text_factory(model)
    assert speech_to_text
    monkeypatch.setattr(
        speech_to_text,
        "record_unspecified_length_audio",
        Mock(side_effect=Exception("Mock Error")),
    )
    with pytest.raises(Exception, match="Mock Error"):
        speech_to_text.transcribe_speech()


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
@pytest.mark.parametrize("pricing_rate", [0.1, 0.05, 0.002, 1.0, 0.0])
@pytest.mark.parametrize("seconds", [1000, 0, 5])
def test_cost_estimate_data(
    patched_openai_speech_to_text_factory: OpenAISpeechToTextFactoryType,
    model: str,
    pricing_rate: float,
    seconds: int,
) -> None:
    """
    Test that cost estimate is calculated correctly.
    """
    speech_to_text = patched_openai_speech_to_text_factory(model, pricing_rate)
    assert speech_to_text
    speech_to_text._seconds_transcribed = seconds

    cost_estimate, metadata = speech_to_text.cost_estimate_data
    assert cost_estimate == seconds / 60 * pricing_rate
    assert metadata == {
        "seconds_transcribed": seconds,
        "pricing_rate": speech_to_text._pricing_rate,
    }
    assert speech_to_text.seconds_transcribed == seconds


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
def test_transcribe(
    patched_openai_speech_to_text_factory: OpenAISpeechToTextFactoryType,
    model: str,
) -> None:
    """
    Test that transcribe is called correctly. Most of the logic is mocked,
    but we are also testing the logic, or lack thereof, around the external
    call.
    """
    speech_to_text = patched_openai_speech_to_text_factory(model)
    assert speech_to_text
    with temporary_file(
        "wav", tmp_file_directory=speech_to_text.tmp_file_directory
    ) as tmp:
        assert TEST_TEXT, {} == speech_to_text.transcribe(tmp)
