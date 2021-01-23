from pynput.keyboard import Key, Listener
import time
from pygame import mixer  # Load the popular external library
import os


def on_press(key):
    global outputString
    outputString = outputString + str("{{\"time\":\"{0}\", \"key\":\"{1}\"}},".format(
        time.time() - startTime, key))


def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False


outputString = ''
outputFileName = "keypresses.json"
if os.path.isfile(outputFileName):
    os.remove(outputFileName)
outputFile = open(outputFileName, "a")
outputFile.write('[')
print('Press keys in time with music. Press Escape to end')
print('')
startTime = time.time()
mixer.init()
mixer.music.load(
    'C:/Users/aiive/Documents/Generative/Tentpole Shangrila/Assets/sound.mp3')
mixer.music.play()
# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
outputString = outputString[:len(outputString)-1] + "]"
outputFile.write(outputString)
