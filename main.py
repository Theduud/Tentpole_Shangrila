import cairo
import math
import random
import numpy as np
import sys
from SaveGifMod import SaveGif
import os
import json


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
    return time * FRAMES_PER_SECOND


class ShapeObject:
    def __init__(self, keyPressObject, color, fill):
        test1 = keyPressObject["key"]
        test2 = keyPressInfo["keyValues"]
        shapeOption = keyPressInfo["keyValues"][keyPressObject["key"]]
        if "rectangle" in keyPressObject.shapeOption:
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
        self.frameStart = Time_to_Frame(keyPressObject.time)


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

    def Draw(self):
        SetRGB(self.color)
        c.rectangle(self.x, self.y, self.w, self.h)
        if self.fill:
            c.fill()
        else:
            c.stroke()


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

shapeOptions = {"rectangle1": {
    "priority": 0,
    "x0": 0,
    "y0": 0,
    "w0": WIDTH,
    "h0": HEIGHT,
    "xLambda": lambda x, dw: x + dw,
    "yLambda": lambda y, dh: y-dh,
    "wLambda": lambda w, dw: w-dw,
    "hLambda": lambda h, dh: h-dh},
    "rectangle2": {
    "priority": 1,
    "x0": 0,
    "y0": 0,
    "w0": 0,
    "h0": 0,
    "xLambda": lambda x, dw: x - dw,
    "yLambda": lambda y, dh: y+dh,
    "wLambda": lambda w, dw: w+dw,
    "hLambda": lambda h, dh: h+dh}, }

colors = FormatColors(["edf2fb", "e2eafc", "d7e3fc",
                       "ccdbfd", "c1d3fe", "b6ccfe", "abc4ff"])

keyPressInfo = json.loads(open("keypressinfo.json").read())
keyPresses = json.loads(open("keypresses.json").read())

shapeObjects = np.zeros(len(keyPresses))
for i in range(len(keyPresses)):
    shapeObjects[i] = (ShapeObject(
        keyPresses[i], colors[i % len(colors)], True))


frames = 50
fileNames = []
for frame in range(0, frames):
    bgColor = (0, 0, 0)
    Clear()
    fileName = "output" + str(frame) + ".png"
    s.write_to_png(fileName)
    fileNames.append(fileName)
# save gif
SaveGif(fileNames, "output.gif", True)
