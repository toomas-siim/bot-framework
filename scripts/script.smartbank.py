import time
import imp
from pynput.mouse import Button as mouseButton, Controller
from pynput import keyboard
from tkinter import *
import os

class Script:
    name = "Smart Banking"
    status = "stopped"
    itemData = []
    callback = None
    bankPos = None

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.output.log("SmartBank initialized")
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)

    def process(self):
        self.statusLabel.set("Shift + S to start configuration.")
        self.keyboardCallback = self.inputEngine.addKeyboardListener(self.onKeyboardRelease)

    def startBanking(self):
        self.statusLabel.set("Shift + Q to stop the bot.")
        self.status = "running"
        while 1:
            time.sleep(1)
            if self.status == "stopped":
                self.statusLabel.set("...")
                self.inputEngine.closeCallback("keyboard", self.keyboardCallback)
                break

            i = 0
            for item in self.itemData:
                i = i + 1
                color = self.captureEngine.getPixel(int(item[0][0]), int(item[0][1]))
                n = 0
                for reqColor in item[1]:
                    if reqColor is not color[n]:
                        self.output.log("Change in items: " + str(i))
                        self.dragMouse(item[0], self.bankPos)
                        break
                    n = n + 1

    def dragMouse(self, fromPos, toPos):
        mouse = Controller()
        originalPosition = mouse.position
        mouse.position = (fromPos[0], fromPos[1])
        time.sleep(0.5)
        mouse.press(mouseButton.left)
        time.sleep(0.25)
        mouse.position = (toPos[0], toPos[1])
        time.sleep(0.5)
        mouse.release(mouseButton.left)

    def onKeyboardRelease(self, keysPressed):
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("S") in keysPressed:
            if self.bankPos == None:
                self.requestBankPos()
            elif len(self.itemData) == 0:
                self.requestItems()
            else:
                if self.status == "running":
                    self.halt()
                else:
                    self.startBanking()
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("Q") in keysPressed:
            self.halt()

        # Set item
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("I") in keysPressed:
            mouse = Controller()
            time.sleep(1) # Allow time to move mouse away
            color = self.captureEngine.getPixel(mouse.position[0], mouse.position[1])
            self.itemData.append((mouse.position, color, time.time()))
            self.statusLabel.set("Item " + str(len(self.itemData)) + " saved, Shift+S to start botting.")

        # Set bank
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("B") in keysPressed:
            mouse = Controller()
            time.sleep(1) # Allow time to move mouse away
            self.bankPos = mouse.position
            self.statusLabel.set("Bank set, Shift + I to set empty item slot.")
            self.requestItems()

    def requestBankPos(self):
        self.statusLabel.set("Shift + B to set bank position.")
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)

    def requestItems(self):
        self.statusLabel.set("Shift + I to select an empty item slot.")
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)

    def halt(self):
        self.status = "stopped"
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)
            self.callback = None

    def setInputEngine(self, inputEngine):
        self.inputEngine = inputEngine


    def setContainer(self, container):
        self.container = container
        self.statusLabel = self.createLabel(self.container, "...")

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v
