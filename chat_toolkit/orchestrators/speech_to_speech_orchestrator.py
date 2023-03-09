from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)
from chat_toolkit.components.component_base import ComponentBase
from chat_toolkit.components.speech_to_text.speech_to_text_component_base import (  # noqa: E501
    SpeechToTextComponentBase,
)
from chat_toolkit.components.text_to_speech.text_to_speech_component_base import (  # noqa: E501
    TextToSpeechComponentBase,
)
from chat_toolkit.orchestrators.speech_to_text_orchestrator import (
    SpeechToTextOrchestrator,
)


class SpeechToSpeechOrchestrator(SpeechToTextOrchestrator):
    """
    Used to create text to text orchestrator classes in a standardized
    manner.
    """

    def __init__(
        self,
        chatbot_component: ChatbotComponentBase,
        speech_to_text_component: SpeechToTextComponentBase,
        text_to_speech_component: TextToSpeechComponentBase,
    ):
        super().__init__(
            chatbot_component=chatbot_component,
            speech_to_text_component=speech_to_text_component,
        )
        self._text_to_speech_component = text_to_speech_component

    @property
    def components(self) -> tuple[ComponentBase, ...]:
        """
        Property representing the components that make up this conversation.

        :return: Components.
        """
        return (
            self._chatbot_component,
            self._speech_to_text_component,
            self._text_to_speech_component,
        )

    def respond_from_text(self, text: str) -> str:
        """
        Overwrite base method to also say the response.

        :param text: Text to say and get chatbot response for.
        :return: Chatbot's response in text.
        """
        chatbot_response = super().respond_from_text(text)
        self._text_to_speech_component.say(chatbot_response)
        return chatbot_response
