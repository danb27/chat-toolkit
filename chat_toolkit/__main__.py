import importlib
from typing import Optional

from chat_toolkit.orchestrators.orchestrator_base import OrchestratorBase
from chat_toolkit.orchestrators.speech_to_speech_orchestrator import (
    SpeechToSpeechOrchestrator,
)
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
    "text_to_speech": {
        "pyttsx3": "Pyttsx3TextToSpeech",
    },
}
COMPONENT_MODULE = "chat_toolkit.components"


def main(
    chatbot: str, speech_to_text: Optional[str], text_to_speech: Optional[str]
) -> None:
    """
    Have a conversation in the terminal.

    :return:
    """
    chatbot_obj = getattr(
        importlib.import_module(COMPONENT_MODULE),
        COMPONENTS["chatbot"][chatbot],
    )()
    orchestrator: Optional[OrchestratorBase]
    kwargs = {"chatbot_component": chatbot_obj}

    if text_to_speech:
        text_to_speech_obj = getattr(
            importlib.import_module(COMPONENT_MODULE),
            COMPONENTS["text_to_speech"][text_to_speech],
        )()
        kwargs["text_to_speech_component"] = text_to_speech_obj
    if speech_to_text:
        speech_to_text_obj = getattr(
            importlib.import_module(COMPONENT_MODULE),
            COMPONENTS["speech_to_text"][speech_to_text],
        )()
        kwargs["speech_to_text_component"] = speech_to_text_obj

    if text_to_speech and speech_to_text:
        orchestrator = SpeechToSpeechOrchestrator(**kwargs)
    elif speech_to_text:
        orchestrator = SpeechToTextOrchestrator(**kwargs)
    else:
        orchestrator = TextToTextOrchestrator(**kwargs)

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
    parser.add_argument(
        "--text-to-speech",
        type=str,
        help="Text to speech model to use. Without additional "
        "arguments, defaults to pyttsx3. Defaults to None when argument "
        "is not present.",
        nargs="?",
        const="pyttsx3",
        default=None,
        choices=("pyttsx3",),
    )
    args = parser.parse_args()
    main(args.chatbot, args.speech_to_text, args.text_to_speech)
