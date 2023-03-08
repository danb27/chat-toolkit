from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)
from chat_toolkit.components.component_base import ComponentBase
from chat_toolkit.components.speech_to_text.speech_to_text_component_base import (  # noqa: E501
    SpeechToTextComponentBase,
)
from chat_toolkit.orchestrators.orchestrator_base import OrchestratorBase


class SpeechToTextOrchestrator(OrchestratorBase):
    """
    Used to create speech to text conversation classes in a standardized
    manner.
    """

    def __init__(
        self,
        chatbot_component: ChatbotComponentBase,
        speech_to_text_component: SpeechToTextComponentBase,
    ):
        super().__init__(chatbot_component=chatbot_component)
        self._speech_to_text_component = speech_to_text_component

    def _terminal_conversation(self) -> None:
        """
        Core logic for orchestrating the conversation in the terminal.

        :return:
        """
        start_prompt = input("\nEnter a start prompt (Leave blank to skip): ")
        self._chatbot_component.prompt_chatbot(start_prompts=start_prompt)
        while self._check_user_input(
            user_input := self._speech_to_text_component.record_and_transcribe()[  # noqa: E501
                0
            ]
        ):
            print(f"\nUser (Say nothing to exit): {user_input}")
            chatbot_response, _ = self._chatbot_component.send_message(
                user_input
            )
            print(f"\nChatbot: {chatbot_response}")

    @staticmethod
    def _check_user_input(user_input: str) -> bool:
        """
        Validate user's input. If it is empty, invalid, or otherwise not
        useful, return False.

        :param user_input: Transcribed user input.
        :return: Whether the input is valid for continuing the conversation.
        """
        return all((user_input, any(char.isalpha() for char in user_input)))

    @property
    def components(self) -> tuple[ComponentBase, ...]:
        """
        Property representing the components that make up this orchestrator.

        :return: Components.
        """
        return self._chatbot_component, self._speech_to_text_component
