from collections.abc import Generator
from typing import Any, Callable, Optional, Union
from unittest.mock import Mock

import pytest
from loguru import logger

from chat_toolkit.components.chatbots.openai_chatbot import OpenAIChatBot
from chat_toolkit.components.speech_to_text.openai_speech_to_text import (
    OpenAISpeechToText,
)

CHATBOT_MODEL_TYPES = ("gpt-3.5-turbo",)
SPEECH_TO_TEXT_MODEL_TYPES = ("whisper-1",)

TEST_TEXT = "foo"

OpenAIChatbotFactoryType = Callable[..., OpenAIChatBot]
OpenAISpeechToTextFactoryType = Callable[..., OpenAISpeechToText]


class TypeMatcher:
    """
    Helper object to use to test that Mock objects are called with the
    correct data types. For example:

        > mock = Mock()
        > mock(random.randint(0, 10))
        > mock.assert_called_once_with(TypeMatcher(int))

    This code example would not raise an AssertionError, even though we
    don't actually know the value used to call the mock at run time.
    """

    def __init__(self, expected_type: Any):
        self.expected_type = expected_type

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.expected_type)


@pytest.fixture
def loguru_caplog(
    caplog: pytest.LogCaptureFixture,
) -> Generator[pytest.LogCaptureFixture, None, None]:
    """
    Temporarily alters logger to allow for using pytest's caplog.
    """
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.fixture
def no_openai_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Fixture that ensures OPENAI_API_KEY is not present.
    """
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


@pytest.fixture
def patched_openai_chat_completion(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Monkeypatches openai.ChatCompletion as needed for testing.
    """
    monkeypatch.setattr(
        "openai.ChatCompletion.create",
        lambda model, messages: {
            "choices": [
                {
                    "message": {
                        "content": (
                            response := f"Response: {messages[-1]['content']}"
                        )
                    }
                }
            ],
            "usage": {
                "completion_tokens": (
                    completion_tokens := len(response.split())
                ),
                "prompt_tokens": (
                    prompt_tokens := sum(
                        len(msg["content"].split()) for msg in messages
                    )
                ),
                "total_tokens": completion_tokens + prompt_tokens,
            },
        },
    )


@pytest.fixture
def patched_openai_chatbot_factory(
    no_openai_api_key: None,
    patched_openai_chat_completion: None,
) -> OpenAIChatbotFactoryType:
    """
    Factory to create an openai chatbot with appropriate mocks and
    parameterized instantiation.
    """

    def _inner(
        model: str, pricing_rate: Optional[float] = None
    ) -> OpenAIChatBot:
        if isinstance(pricing_rate, float):
            return OpenAIChatBot(model, pricing_rate)
        else:
            return OpenAIChatBot(model)

    return _inner


@pytest.fixture
def patched_openai_speech_to_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Monkeypatches openai.Audio as needed for testing.
    """
    monkeypatch.setattr(
        "openai.Audio.transcribe",
        Mock(return_value={"text": TEST_TEXT}),
    )
    monkeypatch.setattr(
        "sounddevice.query_devices",
        Mock(return_value={"default_samplerate": "44100"}),
    )


@pytest.fixture
def patched_openai_speech_to_text_factory(
    no_openai_api_key: None,
    patched_openai_speech_to_text: None,
    tmp_path,
) -> OpenAISpeechToTextFactoryType:
    """
    Factory to create an openai speech to text component with appropriate
    mocks and parameterized instantiation.
    """

    def _inner(
        model: str,
        pricing_rate: Optional[float] = None,
        device: Union[int, str] = 0,
    ) -> OpenAISpeechToText:
        if isinstance(pricing_rate, float):
            return OpenAISpeechToText(model, pricing_rate, device, 2, tmp_path)

        return OpenAISpeechToText(
            model, device=device, tmp_file_directory=tmp_path
        )

    return _inner
