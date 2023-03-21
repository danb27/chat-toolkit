from typing import Optional

import pytest

from chat_toolkit.common.exceptions import SpeakingRateError
from test_suite.unit.conftest import (
    TEXT_TO_SPEECH_MODEL_TYPES,
    Pyttsx3TextToSpeechFactoryType,
)


@pytest.mark.parametrize("model", TEXT_TO_SPEECH_MODEL_TYPES)
@pytest.mark.parametrize("speaking_rate", [100, 200, 150, None])
def test_init(
    patched_pyttsx3_text_to_speech_factory: Pyttsx3TextToSpeechFactoryType,
    model: str,
    speaking_rate: Optional[int],
) -> None:
    """
    Test that instantiation occurs as expected
    """
    text_to_speech = patched_pyttsx3_text_to_speech_factory(
        model,
        speaking_rate,
    )
    assert text_to_speech
    assert text_to_speech._model == model
    assert text_to_speech._pricing_rate == 0
    if isinstance(speaking_rate, int):
        assert text_to_speech.engine.getProperty("rate") == speaking_rate
    else:
        assert text_to_speech.engine.getProperty("rate") == 175


@pytest.mark.parametrize("model", TEXT_TO_SPEECH_MODEL_TYPES)
@pytest.mark.parametrize("speaking_rate", [-100, -20, 0])
def test_speaking_rate_sad(
    patched_pyttsx3_text_to_speech_factory: Pyttsx3TextToSpeechFactoryType,
    model: str,
    speaking_rate: Optional[int],
) -> None:
    """
    Test that value error is raised with inappropriate speaking rate
    """
    with pytest.raises(SpeakingRateError, match="Speaking rate must be > 0"):
        patched_pyttsx3_text_to_speech_factory(
            model,
            speaking_rate,
        )


@pytest.mark.parametrize("model", TEXT_TO_SPEECH_MODEL_TYPES)
def test_cost_estimate_data(
    patched_pyttsx3_text_to_speech_factory: Pyttsx3TextToSpeechFactoryType,
    model: str,
) -> None:
    """
    Test that cost estimate is calculated correctly.
    """
    text_to_speech = patched_pyttsx3_text_to_speech_factory(model)
    assert text_to_speech

    cost_estimate, metadata = text_to_speech.cost_estimate_data
    assert cost_estimate == 0
    assert metadata == {
        "pricing_rate": text_to_speech._pricing_rate,
    }
