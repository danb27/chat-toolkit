import json
from typing import Optional

from chat_toolkit.common.utils import print_banner
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


class Orchestrator:
    """
    Used to orchestrate one or more chatbot components in a terminal session.
    """

    def __init__(
        self,
        chatbot_component: ChatbotComponentBase,
        speech_to_text_component: Optional[SpeechToTextComponentBase] = None,
        text_to_speech_component: Optional[TextToSpeechComponentBase] = None,
    ):
        """
        Instantiates orchestrator.

        :param chatbot_component: Prebuilt or custom chatbot component to use.
        :param speech_to_text_component: Prebuilt or custom speech to text
        component to use. Optional.
        :param text_to_speech_component: Prebuilt or custom text to speech
        component to use. Optional.
        """
        self._chatbot_component = chatbot_component
        self._speech_to_text_component = speech_to_text_component
        self._text_to_speech_component = text_to_speech_component

    @property
    def components(self) -> tuple[ComponentBase, ...]:
        """
        Abstract property for defining all components used by the orchestrator.

        :return: All components in orchestrator.
        """
        components = tuple(
            component
            for component in (
                self._chatbot_component,
                self._speech_to_text_component,
                self._text_to_speech_component,
            )
            if component is not None
        )

        return components

    def terminal_conversation(self) -> None:
        """
        Starts a conversation in the user's terminal. Wraps implementation's
        method with greetings, error swallowing, and logic that prints cost
        summary at the end of the conversation.

        :return:
        """
        print("\nWelcome to the chat!")
        print("Ctrl+C or send an empty message at any point to exit.")

        try:
            start_prompt = self.get_start_prompt()
            self._chatbot_component.prompt_chatbot(start_prompt)
            while True:
                if self._speech_to_text_component:
                    user_input = (
                        self._speech_to_text_component.transcribe_speech()[0]
                    )
                    print(f"\nUser: {user_input}")
                else:
                    user_input = input("\nUser: ")

                if not self._check_user_input(user_input):
                    break

                chatbot_response, _ = self._chatbot_component.send_message(
                    user_input
                )
                print(f"\nChatbot: {chatbot_response}")

                if self._text_to_speech_component:
                    self._text_to_speech_component.say_text(chatbot_response)
        except KeyboardInterrupt:
            # Swallow user Keyboard Interrupts
            pass
        finally:
            print("\nBye!\n")
            self.print_cost_summary()

    def print_cost_summary(self) -> None:
        """
        Helper method to print cost summary of conversation so far. Note:
        this is based on pricing rates provided by the user. Costs and
        estimates are the user's responsibility.

        :return:
        """
        total = 0.0
        print_banner("Cost Summary (Estimated with pricing rates provided)")
        for component in self.components:
            cost_estimate, metadata = component.cost_estimate_data
            print(
                f"\n- {type(component).__qualname__}:",
                f"\tSpent ${cost_estimate:.4f}",
                f"\tMetadata: {json.dumps(metadata)}",
                sep="\n",
            )
            total += cost_estimate
        print(f"\n\nTotal Estimated Cost: ${total:.4f}\n")

    def get_start_prompt(self) -> str:
        """
        Get a start prompt from the user

        :return: start prompt
        """
        if self._speech_to_text_component:
            print("\nRecord a start prompt (Say nothing to skip)")
            start_prompt = self._speech_to_text_component.transcribe_speech()[
                0
            ]
            print(f"\nPrompt: {start_prompt}")
        else:
            start_prompt = input(
                "\nEnter a start prompt (Leave blank to skip): "
            )
        self._chatbot_component.prompt_chatbot(start_prompts=start_prompt)
        return start_prompt

    @staticmethod
    def _check_user_input(user_input: str) -> bool:
        """
        Validate user's input. If it is empty, invalid, or otherwise not
        useful, return False.

        :param user_input: Transcribed user input.
        :return: Whether the input is valid for continuing the conversation.
        """
        return all((user_input, any(char.isalpha() for char in user_input)))
