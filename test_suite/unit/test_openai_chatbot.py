import pytest

from chat_toolkit.common.custom_types import StartingPromptsType
from test_suite.unit.conftest import (
    SPEECH_TO_TEXT_MODEL_TYPES,
    OpenAIChatbotFactoryType,
)


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
@pytest.mark.parametrize("pricing_rate", [0.1, 0.05, 0.002, 1.0, 0.0])
def test_init(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    model: str,
    pricing_rate: float,
) -> None:
    """
    Test that instantiation occurs as expected
    """
    chatbot = patched_openai_chatbot_factory(model, pricing_rate)
    assert chatbot._model == model
    assert chatbot._pricing_rate == pricing_rate
    assert chatbot.tokens_used == {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0,
    }
    assert chatbot.history == []
    assert chatbot.latest_response is None


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
@pytest.mark.parametrize(
    "starting_prompts",
    [
        "You are an assistant",
        "Your name is LeAnn, you are CEO of an AI company.",
        None,
        ["You are an assistant", "You work for the CEO of a company"],
    ],
)
def test_openai_prompt(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    model: str,
    starting_prompts: StartingPromptsType,
) -> None:
    """
    Test that prompts are correctly handled and tokens are correctly counted.
    """
    chatbot = patched_openai_chatbot_factory(model)
    chatbot.prompt_chatbot(starting_prompts)

    if not starting_prompts:
        starting_prompts = []
    elif isinstance(starting_prompts, str):
        starting_prompts = [starting_prompts]

    assert chatbot.history == [
        {"role": "system", "content": prompt} for prompt in starting_prompts
    ]
    # prompts are handled lazily
    assert chatbot._tokens_used == {
        "completion_tokens": 0,
        "prompt_tokens": 0,
        "total_tokens": 0,
    }

    chatbot.send_message("")
    full_prompt_size = len(" ".join(starting_prompts).split())

    assert chatbot._tokens_used == {
        # "Response: " is one token in dummy response
        "completion_tokens": (completion_tokens := 1),
        "prompt_tokens": (prompt_tokens := full_prompt_size),
        "total_tokens": (total_tokens := completion_tokens + prompt_tokens),
    }

    assert chatbot.total_tokens_used == total_tokens


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
def test_send_message(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    model: str,
) -> None:
    """
    Test that tokens and history are recorded correctly when sending messages.
    """
    chatbot = patched_openai_chatbot_factory(model)
    test_message = "Hello! How are you?"
    chatbot.send_message(test_message)
    response = f"Response: {test_message}"
    assert chatbot.history == [
        {"role": "user", "content": test_message},
        {"role": "assistant", "content": response},
    ]
    assert chatbot._tokens_used == {
        "completion_tokens": (completion_tokens := len(response.split())),
        "prompt_tokens": (prompt_tokens := len(test_message.split())),
        "total_tokens": (total_tokens := completion_tokens + prompt_tokens),
    }
    assert chatbot.total_tokens_used == total_tokens


@pytest.mark.parametrize("model", SPEECH_TO_TEXT_MODEL_TYPES)
@pytest.mark.parametrize("pricing_rate", [0.1, 0.05, 0.002, 1.0, 0.0])
@pytest.mark.parametrize("tokens", [1000, 0, 5])
def test_cost_estimate_data(
    patched_openai_chatbot_factory: OpenAIChatbotFactoryType,
    model: str,
    pricing_rate: float,
    tokens: int,
) -> None:
    """
    Test that cost estimate calculations are correct.
    """
    chatbot = patched_openai_chatbot_factory(model, pricing_rate)
    tokens_used = {
        "completion_tokens": tokens,
        "prompt_tokens": tokens * 2,
        "total_tokens": tokens * 3,
    }
    chatbot._update_tokens_used(tokens_used)

    cost_estimate, metadata = chatbot.cost_estimate_data
    assert cost_estimate == tokens_used["total_tokens"] / 1000 * pricing_rate
    assert metadata == tokens_used
    assert chatbot.total_tokens_used == tokens * 3
