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
def test_easy_terminal_session_imports(
    chatbot_model: str,
    speech_to_text_model: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test that errors are not raised when setting up the orchestrator
    dynamically.
    """
    monkeypatch.setattr(
        "chat_toolkit.orchestrators.orchestrator_base.OrchestratorBase"
        ".terminal_conversation",
        Mock(),
    )
    try:
        main(chatbot_model, speech_to_text_model)
    except ImportError as e:
        raise AssertionError from e
