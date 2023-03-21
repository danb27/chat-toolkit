from sys import platform

import keyboard
import pyxhook
from pyxhook.pyxhook import PyxHookKeyEvent


class KeyTracker:
    def __init__(self):
        self._linux = platform == "linux"
        if self._linux:
            self._recording = False
            self._hook = pyxhook.HookManager()
            self._hook.KeyDown = self._key_down_event
            self._hook.KeyUp = self._key_up_event
            self._hook.HookKeyboard()
            self._hook.start()
            self._tracking_char = 32
        else:
            self._tracking_char = "space"

    def _key_down_event(self, event: PyxHookKeyEvent) -> None:
        """
        Process a key down event in linux to check if the space key has been
        hit to signify the user's intent to start recording.

        :param event: Key down event to process
        """
        if event.Ascii == self._tracking_char and not self._recording:
            self._recording = True

    def _key_up_event(self, event: PyxHookKeyEvent) -> None:
        """
        Process a key up event in linux to check if the space key has been
        released to signify the user's intent to start recording.

        :param event: Key up event to process
        """
        if event.Ascii == self._tracking_char and self._recording:
            self.stop_tracking()
            self._recording = False

    def _wait_for_recording_to_start(self) -> None:
        """
        Wait for user to signal for recording to start. Must be a blocking
        call.

        :return:
        """
        if self._linux:
            while True:
                if self._recording:
                    return
        else:
            keyboard.wait(self._tracking_char)
            self._recording = True

    def _check_if_still_recording(self) -> bool:
        """
        Check if user has stopped recording. Must be a non-blocking call.

        :return:
        """
        if not self._linux:
            self._recording = keyboard.is_pressed(self._tracking_char)
        return self._recording

    def wait_for_recording_to_start(self) -> None:
        """
        Prompt user to allow them to start recording, then block until
        recording can start.

        :return:
        """
        print("\n\tHold space to record...")
        self._wait_for_recording_to_start()
        print("\tRecording...")

    def check_if_still_recording(self) -> bool:
        """
        Check if user has released the tracking key. If so, notify that
        recording will stop.
        """
        self._check_if_still_recording()
        if not self._recording:
            print("\tRecording stopped.")
        return self._recording

    def stop_tracking(self):
        """
        Stop tracking keys if needed for user's OS.
        """
        if self._linux:
            self._hook.cancel()
