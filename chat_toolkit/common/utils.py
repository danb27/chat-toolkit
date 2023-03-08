import io
import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import openai
from loguru import logger

from chat_toolkit.common.constants import TMP_DIR


def print_banner(text: str, indent: int = 0) -> None:
    """
    Print a banner in the terminal.

    :param text: Text to wrap in a banner of pound signs.
    :param indent: How many characters to indent every line.
    :return:
    """
    len_text = len(text)
    indent_str = " " * indent
    print("\n\n")
    print(f"{indent_str}{'#' * (len_text + 8)}")
    print(f"{indent_str}##  {text}  ##")
    print(f"{indent_str}{'#' * (len_text + 8)}")
    print("\n")


class RecordingEndedWithKeyboardSignal(Exception):  # noqa: N818
    """
    Raised in place of KeyboardInterrupt when CTRL+C's to end a recording.
    Allows others KeyboardInterrupt to be caught differently.
    """

    pass


@contextmanager
def temporary_file(
    ending: str,
    delete_after: bool = True,
    tmp_file_directory: Path = TMP_DIR,
) -> Generator[io.BufferedRandom, None, None]:
    """
    Context manager for creating a temporary file and (optionally) removing it
    after it is done being used. Useful when working with OpenAI's API,
    for example, where using temporary files caused issues.

    :param ending: Desired file ending.
    :param delete_after: Whether to delete the file after it is done being
    used.
    :param tmp_file_directory: Directory to use for temporary files,
    will use a default directory if not provided.
    :return: None, but yields the temporary file.
    """
    tmp_file_directory.mkdir(parents=True, exist_ok=True)

    tmp_path = tmp_file_directory / f"{os.urandom(24).hex()}.{ending}"

    with tmp_path.open("w+b") as tmp:
        yield tmp

    if delete_after:
        tmp_path.unlink()


def set_openai_api_key():
    openai.api_key = os.environ.get("OPENAI_API_KEY", "")

    if not openai.api_key:
        logger.warning(
            "OPENAI_API_KEY not set. You will be unable to interact "
            "with OpenAI's APIs."
        )
