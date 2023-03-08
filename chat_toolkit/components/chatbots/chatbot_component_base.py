from abc import ABC, abstractmethod

from chat_toolkit.common.custom_types import StartingPromptsType
from chat_toolkit.components.component_base import ComponentBase


class ChatbotComponentBase(ComponentBase, ABC):
    """
    Used to create chatbot components in standardized manner.
    """

    @abstractmethod
    def prompt_chatbot(
        self, start_prompts: StartingPromptsType = None
    ) -> None:
        """
        Abstract method for prompting chatbot before conversation. May be lazy
        or eager.

        :param start_prompts: Start prompts to send. If None, do nothing.
        :return:
        """
        pass

    @abstractmethod
    def send_message(self, *args, **kwargs) -> tuple[str, dict]:
        """
        Abstract method for sending a message and returning a response and
        some metadata.

        :return: Response text, any metadata applicable.
        """
        pass
