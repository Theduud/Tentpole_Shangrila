import cairo
import math
import random
import numpy as np
import sys
from SaveGifMod import SaveGif
import os
import json
from subprocess import check_output


def FormatColors(colorsHex):
    newArray = []
    for color in colorsHex:
        color = tuple(int(color[i: i + 2], 16) for i in (0, 2, 4))
        newArray.append([color[0] / 255, color[1] / 255, color[2] / 255])
    return newArray


def SetRGB(color, a=1):
    c.set_source_rgba(color[0], color[1], color[2], a)


def Clear():
    c.save()
    SetRGB(bgColor)
    c.paint()
    c.restore()


def Time_to_Frame(time):
    return math.floor(float(time) * FRAMES_PER_SECOND)


class ShapeObject:
    def __init__(self, keyPressObject, color, fill, dx=None, dy=None, dw=None, dh=None):
        shapeOption = keyPressInfo[keyPressObject["key"]]
        if "rectangle" in shapeOption:
            self.shape = Rectangle(
                shapeOptions[shapeOption]["x0"],
                shapeOptions[shapeOption]["y0"],
                shapeOptions[shapeOption]["w0"],
                shapeOptions[shapeOption]["h0"],
                shapeOptions[shapeOption]["xLambda"],
                shapeOptions[shapeOption]["yLambda"],
                shapeOptions[shapeOption]["wLambda"],
                shapeOptions[shapeOption]["hLambda"],
                color, fill)
        self.frameStart = Time_to_Frame(keyPressObject["time"])
        if dx is not None:
            self.shape.dx = dx
        if dy is not None:
            self.shape.dy = dy
        if dw is not None:
            self.shape.dw = dw
        if dh is not None:
            self.shape.dh = dh

    def Draw(self):
        self.shape.Draw()


class Rectangle:
    def __init__(self,   x0, y0, w0, h0, xLambda, yLambda, wLambda, hLambda, color, fill=True):
        self.x = x0
        self.y = y0
        self.w = w0
        self.h = h0
        self.xLambda = xLambda
        self.yLambda = yLambda
        self.wLambda = wLambda
        self.hLambda = hLambda
        self.color = color
        self.fill = fill
        self.dx = 0
        self.dy = 0
        self.dw = 0
        self.dh = 0

    def Draw(self):
        SetRGB(self.color)
        c.rectangle(self.x, self.y, self.w, self.h)
        if self.fill:
            c.fill()
        else:
            c.stroke()
        self.x = self.xLambda(self.x, self.dx)
        self.y = self.yLambda(self.y, self.dy)
        self.w = self.yLambda(self.w, self.dw)
        self.w = self.yLambda(self.h, self.dh)


FRAMES_PER_SECOND = 24
WIDTH = 600
HEIGHT = 600
s = cairo.SVGSurface("surface.svg", WIDTH, HEIGHT)
c = cairo.Context(s)

# rectangle1 : background rectangle that condenses into the center
# rectangle2 : background rectangle that expands from the center
# rectangle3u : quick vertical line that shoots up and expands across the screen horizontally
# rectangle3r : quick vertical line that shoots right and expands across the screen vertically
# rectangle3d : quick vertical line that shoots down and expands across the screen horizontally
# rectangle3l : quick vertical line that shoots left and expands across the screen vertically

colors = FormatColors(["edf2fb", "e2eafc", "d7e3fc",
                       "ccdbfd", "c1d3fe", "b6ccfe", "abc4ff"])

keyPressInfo = json.loads(open("keypressinfo.json").read())
keyPresses = json.loads(open("keypresses.json").read())

shapeObjects = []
dw = WIDTH / 100
dh = HEIGHT / 100
for i in range(len(keyPresses)):
    shapeObjects.append(ShapeObject(
        keyPresses[i], colors[i % len(colors)], True, dw, dh, dw, dh))


frames = 500
fileNames = []
for frame in range(0, frames):
    bgColor = (0, 0, 0)
    Clear()
    for shapeObject in shapeObjects:
        if frame >= shapeObject.frameStart:
            shapeObject.Draw()
    fileName = "output/" + str(frame) + ".png"
    s.write_to_png(fileName)
    fileNames.append(fileName)
    print(str(100*frame/frames) + "%")
# save gif
# SaveGif(fileNames, "output.gif", False)
working_dir = os.path.dirname(os.path.realpath(__file__))
command = "ffmpeg -y -framerate " + str(FRAMES_PER_SECOND) + " -i " + working_dir + \
    "\\output\\%d.png " + working_dir + "\\output\\output.mp4"
result = check_output(command, shell=True)
command = "ffmpeg -y -i " + working_dir + "/output/output.mp4 -i " + \
    working_dir + "/Assets/sound.mp3 -c copy -map 0:v:0 -map 1:a:0 " + \
    working_dir + "/output/output_w_audio.mp4"
result = check_output(command, shell=True)
for filename in fileNames:
    os.remove(filename)
