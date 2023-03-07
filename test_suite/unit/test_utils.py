import pytest

from chat_toolkit.common.utils import set_openai_api_key


@pytest.fixture
def no_openai_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Fixture that ensures OPENAI_API_KEY is not present
    """
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


def test_missing_api_key_warning(
    loguru_caplog: pytest.LogCaptureFixture, no_openai_api_key: None
) -> None:
    """
    Test that warning message is raised when no API key is present.
    """
    set_openai_api_key()

    assert (
        sum(
            record.msg.startswith("OPENAI_API_KEY not set.")
            and record.levelname == "WARNING"
            for record in loguru_caplog.records
        )
        == 1
    )
