import json
from abc import ABC, abstractmethod

from chat_toolkit.common.utils import print_banner
from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)
from chat_toolkit.components.component_base import ComponentBase


class OrchestratorBase(ABC):
    """
    Used to create orchestrators in a standardized manner
    """

    def __init__(self, chatbot_component: ChatbotComponentBase):
        """
        Instantiates orchestrator.

        :param chatbot_component: Chatbot component to use.
        """
        self._chatbot_component = chatbot_component

    @abstractmethod
    def _terminal_conversation(self) -> None:
        """
        Abstract method for orchestrating a conversation flow without
        boilerplate logic.

        :return:
        """
        pass

    @property
    @abstractmethod
    def components(self) -> tuple[ComponentBase, ...]:
        """
        Abstract property for defining all components used by the orchestrator.

        :return: All components in orchestrator.
        """
        pass

    def terminal_conversation(self) -> None:
        """
        Starts a conversation in the user's terminal. Wraps implementation's
        method with greetings, error swallowing, and logic that prints cost
        summary at the end of the conversation.

        :return:
        """
        print("\nWelcome to the chat!")
        try:
            self._terminal_conversation()
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
