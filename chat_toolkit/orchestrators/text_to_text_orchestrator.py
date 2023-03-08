from chat_toolkit.components.component_base import ComponentBase
from chat_toolkit.orchestrators.orchestrator_base import OrchestratorBase


class TextToTextOrchestrator(OrchestratorBase):
    """
    Used to create text to text orchestrator classes in a standardized
    manner.
    """

    def _terminal_conversation(self):
        """
        Core logic for orchestrating the conversation in the terminal.

        :return:
        """
        start_prompt = input("\nEnter a start prompt (Leave blank to skip): ")
        self._chatbot_component.prompt_chatbot(start_prompts=start_prompt)
        while user_input := input("\nUser (Leave blank to exit): "):
            chatbot_response, _ = self._chatbot_component.send_message(
                user_input
            )
            print(f"\nChatbot: {chatbot_response}")

    @property
    def components(self) -> tuple[ComponentBase, ...]:
        """
        Property representing the components that make up this conversation.

        :return: Components.
        """
        # noinspection PyRedundantParentheses
        return (self._chatbot_component,)
