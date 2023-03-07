import pytest

from chat_toolkit.base.chatbot_component_base import ChatbotComponentBase
from chat_toolkit.base.speech_to_text_component_base import (
    SpeechToTextComponentBase,
)
from chat_toolkit.orchestrators.speech_to_text_orchestrator import (
    SpeechToTextOrchestrator,
)
from test_suite.unit.conftest import (
    CHATBOT_MODEL_TYPES,
    SPEECH_TO_TEXT_MODEL_TYPES,
    OpenAIChatbotFactoryType,
    OpenAISpeechToTextFactoryType,
)


@pytest.mark.parametrize("chatbot_model", CHATBOT_MODEL_TYPES)
@pytest.mark.parametrize("speech_to_text_model", SPEECH_TO_TEXT_MODEL_TYPES)
def test_init(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    patched_openai_speech_to_text_factory: OpenAISpeechToTextFactoryType,
    chatbot_model: str,
    speech_to_text_model: str,
) -> None:
    """
    Test that instantiation occurs as expected
    """
    chatbot = patched_openai_chatbot_factory(chatbot_model)
    speech_to_text = patched_openai_speech_to_text_factory(
        speech_to_text_model
    )
    orchestrator = SpeechToTextOrchestrator(chatbot, speech_to_text)

    assert isinstance(
        orchestrator._speech_to_text_component, SpeechToTextComponentBase
    )
    assert isinstance(orchestrator._chatbot_component, ChatbotComponentBase)
    assert len(orchestrator.components) == 2
