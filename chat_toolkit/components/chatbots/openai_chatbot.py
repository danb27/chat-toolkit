import logging
from typing import Union

import openai

from chat_toolkit.common.custom_types import StartingPromptsType
from chat_toolkit.components.chatbots.chatbot_component_base import (
    ChatbotComponentBase,
)

logger = logging.getLogger()


class OpenAIChatBot(ChatbotComponentBase):
    """
    Class for interacting with one of OpenAI's chat algorithm(s).
    Requires OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        pricing_rate: float = 0.002,
    ):
        """
        Instantiate a chatbot interaction object.

        :param model: OpenAI chat model to use.
        :param pricing_rate: Pricing rate per 1000 tokens used to
        calculate cost estimates of orchestrators. See notes about
        user responsibility re: costs + estimates in CostEstimatorBase.
        """
        super().__init__(
            model=model,
            pricing_rate=pricing_rate,
        )

        self.latest_response: Union[openai.ChatCompletion, None] = None
        self.history: list[dict] = []
        self._tokens_used = {
            "completion_tokens": 0,
            "prompt_tokens": 0,
            "total_tokens": 0,
        }

    def prompt_chatbot(
        self,
        start_prompts: StartingPromptsType = None,
    ) -> None:
        """
        Store prompts to conversation history in appropriate format to be
        passed to model with every subsequent message.

        :param start_prompts: Prompt(s) to give algorithm (optional).
        :return:
        """
        if not start_prompts:
            return
        elif isinstance(start_prompts, str):
            start_prompts = [start_prompts]

        for start_prompt in start_prompts:
            self._record_message("system", start_prompt)

    def send_message(self, message: str) -> tuple[str, dict]:
        """
        Send a message to the chatbot. Record inputs and outputs so
        that conversation may continue.

        :param message: User's desired message to the chatbot.
        :return: Chatbot's response.
        """
        self._record_message("user", message)
        self.latest_response = self._send_message()
        response_content = ""
        for choice in self.latest_response["choices"]:
            choice_message = choice["message"]["content"]
            self._record_message("assistant", choice_message)
            response_content = f"{response_content}{choice_message}"

        self._update_tokens_used(self.latest_response["usage"])

        return (
            response_content.lstrip("\n").rstrip("\n"),
            self.latest_response.copy(),
        )

    @property
    def cost_estimate_data(self) -> tuple[float, dict]:
        """
        Property representing most recent cost estimate based on number of
        tokens charged by OpenAI so far in the object's usage. See notes about
        user responsibility regarding costs and estimates in CostEstimatorBase.

        :return: Cost estimate in dollars, any applicable metadata.
        """
        cost_estimate = self.total_tokens_used / 1000 * self._pricing_rate
        metadata = self._tokens_used.copy()
        return cost_estimate, metadata

    @property
    def total_tokens_used(self) -> int:
        """
        Property representing the total number of tokens charged by OpenAI
        so far.

        :return: Total tokens used so far.
        """
        return self._tokens_used["total_tokens"]

    @property
    def tokens_used(self) -> dict[str, int]:
        """
        Read only property representing how many tokens this object is
        estimated to have processed so far.

        :return:
        """
        return self._tokens_used.copy()

    def _send_message(self) -> openai.ChatCompletion:
        """
        Send message to OpenAI, including all conversation history.

        :return: Response from OpenAI.
        """
        return openai.ChatCompletion.create(
            model=self._model, messages=self.history
        )

    def _record_message(self, role: str, content: str) -> None:
        """
        Record a message to keep the history up to date.

        :param role: Role, as defined by OpenAI's API. Validated by Role Enum.
        :param content: Content of message being recorded.
        :return:
        """
        self.history.append({"role": role, "content": content})

    def _update_tokens_used(self, usage: dict) -> None:
        """
        Update record of token counts in the conversation for cost
        estimation and reporting purposes.

        :param usage: Usage mapping provided in OpenAI's response for a
        single message.
        :return:
        """
        usage = usage.copy()
        for metric, value in usage.items():
            self._tokens_used[metric] += value
