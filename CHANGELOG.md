# Changelog

## 1.1.1 (3/21/2023)
- Documentation fixes/improvements.

## 1.1.0 (3/21/2023)

### Added
- `Pyttsx3TextToSpeech` to allow for performing Speech to Speech conversation.
- Use space bar to start and stop recording from terminal. This process not uses `pyxhook` for linux and continues to use `keyboard` for windows. This prevents needing sudo access on Linux.
- Create a single `Orchestrator` class, capable of consuming any combination of components, so long as a chatbot component is present.
- Added `pricing_rate` to cost estimate metadata.
- Added and improved tests.
- Improved documentation.

### Removed
- `RecordingEndedWithKeyboardSignal` in favor of a new approach to recording (see above).
- `OrchestratorBase` and all subclasses in favor of Orchestrator (see above).

### Bugs
- Fixed linux incompatibilities by adding dependencies.

## 1.0.1 (3/8/2023)
- Improve terminal experience of orchestrators.
- Testing improvements.

## 1.0.0 (3/7/2023)
- Initial release.
