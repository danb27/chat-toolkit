import importlib
from typing import Union

from chat_toolkit.orchestrators.orchestrator_base import OrchestratorBase
from chat_toolkit.orchestrators.speech_to_text_orchestrator import (
    SpeechToTextOrchestrator,
)
from chat_toolkit.orchestrators.text_to_text_orchestrator import (
    TextToTextOrchestrator,
)

COMPONENTS = {
    "chatbot": {
        "chatgpt": "OpenAIChatBot",
    },
    "speech_to_text": {
        "whisper": "OpenAISpeechToText",
    },
}


def main(chatbot: str, speech_to_text: Union[str, None]) -> None:
    """
    Have a conversation in the terminal.

    :return:
    """
    chatbot_obj = getattr(
        importlib.import_module("chat_toolkit.components"),
        COMPONENTS["chatbot"][chatbot],
    )()
    orchestrator: Union[OrchestratorBase, None]
    if speech_to_text:
        speech_to_text_obj = getattr(
            importlib.import_module("chat_toolkit.components"),
            COMPONENTS["speech_to_text"][speech_to_text],
        )()
        orchestrator = SpeechToTextOrchestrator(
            chatbot_component=chatbot_obj,
            speech_to_text_component=speech_to_text_obj,
        )
    else:
        orchestrator = TextToTextOrchestrator(chatbot_component=chatbot_obj)

    orchestrator.terminal_conversation()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        "A script for quickly starting a conversation in your terminal."
    )
    parser.add_argument(
        "--chatbot",
        type=str,
        help="Chatbot to use. Default: chatgpt.",
        default="chatgpt",
        choices=("chatgpt",),
    )
    parser.add_argument(
        "--speech-to-text",
        type=str,
        help="Speech to text model to use. Without additional "
        "arguments, defaults to whisper. Defaults to None when argument "
        "is not present.",
        nargs="?",
        const="whisper",
        default=None,
        choices=("whisper",),
    )
    args = parser.parse_args()
    main(args.chatbot, args.speech_to_text)
