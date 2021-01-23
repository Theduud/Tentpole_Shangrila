from pynput.keyboard import Key, Listener
import time
from pygame import mixer  # Load the popular external library
import os


def on_press(key):
    global outputString
    try:
        outputString = outputString + str("{{\"time\":\"{0}\", \"key\":\"{1}\"}},".format(
            time.time() - startTime, key.char))
    except:
        if key == Key.esc:
            return False
        print('Key pressed is not a character')


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
with Listener(on_press=on_press) as listener:
    listener.join()
outputString = outputString[:len(outputString)-1] + "]"
outputFile.write(outputString)
