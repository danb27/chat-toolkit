<!-- TOC -->
* [Chat Toolkit](#chat-toolkit)
  * [Quick Usage](#quick-usage)
  * [Components](#components)
    * [Chatbots](#chatbots)
    * [Speech to Text](#speech-to-text)
  * [Orchestrators](#orchestrators)
    * [TextToTextOrchestrator](#texttotextorchestrator)
    * [SpeechToTextOrchestrator](#speechtotextorchestrator)
<!-- TOC -->

# Chat Toolkit

Extensible package for creating machine learning powered chatbots.

## Quick Usage

The main script has been provided for convenience. This allows you to easily
start a conversation in your terminal.

Usage:

```
usage: __main__.py [-h] [--chatbot {chatgpt}] [--speech-to-text {whisper}]

options:
  -h, --help                    show this help message and exit
  --chatbot {chatgpt}           Chatbot to use. Default: chatgpt.
  --speech-to-text {whisper}    Speech to text model to use. Default: None.
```

To quickly start up a TextToTextOrchestrator: `python -m chat_toolkit`
OR `python -m chat_toolkit --chatbot chatgpt`

To quickly start up a
SpeechToTextOrchestrator: `python -m chat_toolkit --speech-to-text whisper`
OR `python -m chat_toolkit --chatbot chatgpt --speech-to-text whisper`

## Components

Components are ML powered objects that accomplish tasks. Components should be
able to estimate session costs.
**NOTE**: Cost estimates are based on pricing rates provided by the user. Users
should do their own due dilligence and are responsible for their own costs and
estimations.

> Advanced Usage: You can create your own component types by
> subclassing `chat_toolkit.base.ComponentBase`

### Chatbots

These components send and receive text messages.

| Class         | Requirements   | Models Available        | Reference                                                                    |
|---------------|----------------|-------------------------|------------------------------------------------------------------------------|
| OpenAIChatBot | OPENAI_API_KEY | gpt-3.5-turbo (ChatGPT) | [OpenAI](https://platform.openai.com/docs/guides/chat/chat-completions-beta) |

Basic Usage:

```python
from chat_toolkit.components import OpenAIChatBot

chatbot = OpenAIChatBot()
chatbot.prompt_chatbot("You are a butler named Jeeves.")
chatbot_response, _ = chatbot.send_message("Hello, what is your name?")
```

> Advanced Usage: You can create your own chatbot components by
> subclassing `chat_toolkit.base.ChatbotComponentBase`

### Speech to Text

These components record speech and transform it into text.

| Class              | Requirements   | Models Available | Reference                                                                            |
|--------------------|----------------|------------------|--------------------------------------------------------------------------------------|
| OpenAISpeechToText | OPENAI_API_KEY | whiper-1         | [OpenAI](https://platform.openai.com/docs/guides/speech-to-text/speech-to-text-beta) |

Basic Usage:

```python
from chat_toolkit.components import OpenAISpeechToText

speech_to_text = OpenAISpeechToText()
text, _ = speech_to_text.record_and_transcribe()
```

> Advanced Usage: You can create your own speech to text components by
> subclassing `chat_toolkit.base.SpeechToTextComponentBase`

## Orchestrators

Orchestrators are modes of chatting that orchestrate one or more components
differently. They also allow you to chat from the terminal.

> Advanced Usage: You can create your own orchestration classes by
> subclassing `chat_toolkit.base.OrchestratorBase`

### TextToTextOrchestrator

Basic usage:

```python
from chat_toolkit.components import OpenAIChatBot
from chat_toolkit.orchestrators import TextToTextOrchestrator

chat = TextToTextOrchestrator(OpenAIChatBot())
chat.terminal_conversation()
```

### SpeechToTextOrchestrator

Basic usage:

```python
from chat_toolkit.components import OpenAIChatBot, OpenAISpeechToText
from chat_toolkit.orchestrators import SpeechToTextOrchestrator

chat = SpeechToTextOrchestrator(OpenAIChatBot(), OpenAISpeechToText())
chat.terminal_conversation()
```
