<!-- TOC -->
* [Chat Toolkit](#chat-toolkit)
  * [Installation](#installation)
  * [Quick Usage](#quick-usage)
  * [Components](#components)
    * [Chatbots](#chatbots)
    * [Speech to Text](#speech-to-text)
    * [Text to Speech](#text-to-speech)
  * [Orchestrator](#orchestrator)
    * [Text to Text](#text-to-text)
    * [Speech to Text](#speech-to-text-1)
    * [Text to Speech](#text-to-speech-1)
    * [Speech to Speech](#speech-to-speech)
<!-- TOC -->

# Chat Toolkit

Extensible package for creating machine learning powered chatbots.

Package supports Linux and Windows. Mac is not explicitly supported, although it is possible some, or many parts of this will still work.

**NOTE**: Some components require additional dependencies. See below for more information.

## Installation

`pip install -U chat-toolkit`

## Quick Usage

The main script has been provided for convenience. This allows you to easily
start a conversation in your terminal.

Usage:

```
usage: A script for quickly starting a conversation in your terminal. [-h] [--chatbot {chatgpt}]
                                                                      [--speech-to-text [{whisper}]]
                                                                      [--text-to-speech [{pyttsx3}]]

options:
  -h, --help                        show this help message and exit
  --chatbot {chatgpt}               Chatbot to use. Default: chatgpt.
  --speech-to-text [{whisper}]      Speech to text model to use. Without additional arguments, defaults to whisper. Defaults to
                                    None when argument is not present.
  --text-to-speech [{pyttsx3}]      Text to speech model to use. Without additional arguments, defaults to pyttsx3. Defaults to
                                    None when argument is not present.

```

To quickly start up a Text to Text conversation (default models):

`python -m chat_toolkit`

To quickly start up a Speech to Text conversation (default models):

`python -m chat_toolkit --speech-to-text`

To quickly start up a Text to Speech conversation (default models):

`python -m chat_toolkit --text-to-speech`

To quickly start up a Speech to Speech conversation (default models):

`python -m chat_toolkit --speech-to-text --text-to-speech`

## Components

Components are ML powered objects that accomplish tasks. Components should be
able to estimate session costs. You can build your own components to use in
isolation or as part of an orchestrator object.

**NOTE**: Cost estimates are based on pricing rates provided by the user. Users
should do their own due dilligence and are responsible for their own costs and
estimations.

> Advanced Usage: You can create your own component types by
> subclassing `chat_toolkit.base.ComponentBase`

### Chatbots

These components send and receive text messages.

| Class         | Requirements   | Model                   | Default Cost     | Reference                                                                    |
|---------------|----------------|-------------------------|------------------|------------------------------------------------------------------------------|
| OpenAIChatBot | OPENAI_API_KEY | gpt-3.5-turbo (ChatGPT) | $0.002/1k tokens | [OpenAI](https://platform.openai.com/docs/guides/chat/chat-completions-beta) |

Basic Usage:

```python
from chat_toolkit import OpenAIChatBot

chatbot = OpenAIChatBot()
chatbot.prompt_chatbot("You are a butler named Jeeves.")
chatbot_response, _ = chatbot.send_message("Hello, what is your name?")
```

> Advanced Usage: You can create your own chatbot components by
> subclassing `chat_toolkit.base.ChatbotComponentBase`

### Speech to Text

These components record speech and transform it into text.

| Class              | Requirements                          | Model    | Default Cost     | Reference                                                                            |
|--------------------|---------------------------------------|----------|------------------|--------------------------------------------------------------------------------------|
| OpenAISpeechToText | OPENAI_API_KEY, libportaudio2 (linux) | whiper-1 | $0.006/1k tokens | [OpenAI](https://platform.openai.com/docs/guides/speech-to-text/speech-to-text-beta) |

Basic Usage:

```python
from chat_toolkit import OpenAISpeechToText

speech_to_text = OpenAISpeechToText()
text, _ = speech_to_text.transcribe_speech()
```

**NOTE**: Recording quality is very sensitive to your hardware. Things can go wrong,
for example, if the input volume on your microphone is too loud.

> Advanced Usage: You can create your own speech to text components by
> subclassing `chat_toolkit.base.SpeechToTextComponentBase`

### Text to Speech

These components say pieces of text.

| ClassTextToSpeech   | Requirements   | Model  | Default Cost | Reference                                            |
|---------------------|----------------|--------|--------------|------------------------------------------------------|
| Pyttsx3TextToSpeech | espeak (linux) | n/a    | Free         | [Pyttsx3](https://pyttsx3.readthedocs.io/en/latest/) |

**NOTE**: Pyttsx3TextToSpeech currently defaults to English, but it may be configured using `set_pyttsx3_property()` method. See pyttsx3's documentation for more information.

Basic Usage:

```python
from chat_toolkit import Pyttsx3TextToSpeech

text_to_speech = Pyttsx3TextToSpeech()
text_to_speech.say_text("hello")
```

> Advanced Usage: You can create your own text to speech components by
> subclassing `chat_toolkit.base.TextToSpeechComponentBase`

## Orchestrator

The Orchestrator class also allow you to chat from the terminal. The Orchestrator
should work such that you can replace any component with another of the
same type, or a custom-built one, and still be able to use the orchestrator.

### Text to Text

Basic usage:

```python
from chat_toolkit import OpenAIChatBot
from chat_toolkit import Orchestrator

chat = Orchestrator(OpenAIChatBot())
chat.terminal_conversation()
```

### Speech to Text

Basic usage:

```python
from chat_toolkit import OpenAIChatBot, OpenAISpeechToText
from chat_toolkit import Orchestrator

chat = Orchestrator(OpenAIChatBot(), OpenAISpeechToText())
chat.terminal_conversation()
```

### Text to Speech

Basic usage:

```python
from chat_toolkit import OpenAIChatBot, Pyttsx3TextToSpeech
from chat_toolkit import Orchestrator

chat = Orchestrator(OpenAIChatBot(), text_to_speech_component=Pyttsx3TextToSpeech())
chat.terminal_conversation()
```


### Speech to Speech

Basic usage:

```python
from chat_toolkit import OpenAIChatBot, OpenAISpeechToText, Pyttsx3TextToSpeech
from chat_toolkit import Orchestrator

chat = Orchestrator(OpenAIChatBot(), OpenAISpeechToText(), Pyttsx3TextToSpeech())
chat.terminal_conversation()
```
