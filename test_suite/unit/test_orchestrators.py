from unittest.mock import Mock

import pytest

from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)
from chat_toolkit.components.speech_to_text.speech_to_text_component_base import (  # noqa: E501
    SpeechToTextComponentBase,
)
from chat_toolkit.components.text_to_speech.text_to_speech_component_base import (  # noqa: E501
    TextToSpeechComponentBase,
)
from test_suite.unit.conftest import PatchedOrchestratorType


def test_init(patched_orchestrator: PatchedOrchestratorType) -> None:
    """
    Test that instantiation occurs as expected
    """
    orchestrator, subrequest = patched_orchestrator
    (
        chatbot_model,
        speech_to_text_model,
        text_to_speech_model,
    ) = subrequest.param

    if speech_to_text_model:
        assert isinstance(
            orchestrator._speech_to_text_component, SpeechToTextComponentBase
        )

    if text_to_speech_model:
        assert isinstance(
            orchestrator._text_to_speech_component, TextToSpeechComponentBase
        )

    assert isinstance(orchestrator._chatbot_component, ChatbotComponentBase)
    assert len(orchestrator.components) == sum(
        1
        for component in (
            chatbot_model,
            speech_to_text_model,
            text_to_speech_model,
        )
        if component
    )


def test_keyboard_error_swallowed(
    patched_orchestrator: PatchedOrchestratorType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test that terminal conversation correctly swallows a user's
    KeyboardInterrupt.
    """
    orchestrator, _ = patched_orchestrator

    monkeypatch.setattr(
        orchestrator,
        "get_start_prompt",
        Mock(side_effect=KeyboardInterrupt()),
    )
    try:
        orchestrator.terminal_conversation()
    except KeyboardInterrupt as e:
        raise AssertionError from e
