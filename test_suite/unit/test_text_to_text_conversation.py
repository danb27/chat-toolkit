import pytest

from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)
from chat_toolkit.orchestrators.text_to_text_orchestrator import (
    TextToTextOrchestrator,
)
from test_suite.unit.conftest import (
    CHATBOT_MODEL_TYPES,
    OpenAIChatbotFactoryType,
)


@pytest.mark.parametrize("chatbot_model", CHATBOT_MODEL_TYPES)
def test_init(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    chatbot_model: str,
) -> None:
    """
    Test that instantiation occurs as expected
    """
    chatbot = patched_openai_chatbot_factory(chatbot_model)
    orchestrator = TextToTextOrchestrator(chatbot)

    assert isinstance(orchestrator._chatbot_component, ChatbotComponentBase)
    assert len(orchestrator.components) == 1
