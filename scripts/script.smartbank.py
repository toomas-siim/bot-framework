import time
import imp
from pynput.mouse import Button as mouseButton, Controller
from pynput import keyboard
from tkinter import *

class Script:
    name = "Smart Banking"
    status = "stopped"
    itemData = []
    callback = None
    bankPos = None

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("SmartBank initialized")
        self.captureEngine = imp.load_source('capture.engine', './engine/engine.capture.py').CaptureEngine(self.output)

    def process(self):
        self.statusLabel.set("Shift + S to start configuration.")
        self.keyboardCallback = self.inputEngine.addKeyboardListener(self.onKeyboardRelease)

    def startBanking(self):
        self.statusLabel.set("Shift + Q to stop the bot.")
        self.status = "running"
        while 1:
            time.sleep(0.1)
            if self.status == "stopped":
                self.statusLabel.set("...")
                self.inputEngine.closeCallback("mouse", self.callback)
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
            else:
                self.startBanking()
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("Q") in keysPressed:
            self.halt()

    def requestBankPos(self):
        self.statusLabel.set("Left click to set bank position.")
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)
        self.callback = self.inputEngine.addMouseListener(self.onBankClick)

    def requestItems(self):
        self.statusLabel.set("Left click to select an item..")
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)
        self.callback = self.inputEngine.addMouseListener(self.onClick)

    def halt(self):
        self.status = "stopped"
        if self.callback is not None:
            self.inputEngine.closeCallback("mouse", self.callback)
            self.callback = None

    def setInputEngine(self, inputEngine):
        self.inputEngine = inputEngine

    def onBankClick(self, pos, button):
        if self.callback is not None:
            if mouseButton.left == button:
                mouse = Controller()
                self.bankPos = mouse.position
                self.statusLabel.set("Bank set, Left click to set item location.")
                self.requestItems()

    def onClick(self, pos, button):
        if self.callback is not None:
            if mouseButton.left == button:
                color = self.captureEngine.getPixel(pos[0], pos[1])
                self.itemData.append((pos, color, time.time()))
                self.statusLabel.set("Item " + str(len(self.itemData)) + " saved, Shift+S to start botting.")

    def setContainer(self, container):
        self.container = container
        self.statusLabel = self.createLabel(self.container, "...")

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v
