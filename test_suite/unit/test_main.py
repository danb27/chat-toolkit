from typing import Optional
from unittest.mock import Mock

import pytest

from chat_toolkit.__main__ import COMPONENTS, main


@pytest.mark.parametrize(
    "chatbot_model",
    COMPONENTS["chatbot"].keys(),
)
@pytest.mark.parametrize(
    "speech_to_text_model",
    list(COMPONENTS["speech_to_text"].keys()) + [None],
)
@pytest.mark.parametrize(
    "text_to_speech_model",
    list(COMPONENTS["text_to_speech"].keys()) + [None],
)
def test_main(
    chatbot_model: str,
    speech_to_text_model: Optional[str],
    text_to_speech_model: Optional[str],
    monkeypatch: pytest.MonkeyPatch,
    patched_openai_speech_to_text: None,
) -> None:
    """
    Test that errors are not raised when setting up the orchestrator
    dynamically.
    """
    monkeypatch.setattr(
        "chat_toolkit.common.orchestrator.Orchestrator"
        ".terminal_conversation",
        Mock(),
    )
    try:
        main(chatbot_model, speech_to_text_model, text_to_speech_model)
    except ImportError as e:
        raise AssertionError from e
