from __future__ import absolute_import
import logging
logging.basicConfig()
from pynput.mouse import Listener
from pynput.mouse import Button as mouseButton, Controller
from pynput import keyboard
from tkinter import *
import time
import imp

class Script:
    name = "Banker"
    itemPos = None
    bankPos = None
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Banker script initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "Menu:")
        self.createLabel(self.container, "Shift + I to set item location.")
        self.createLabel(self.container, "Shift + B to set bank location.")
        self.createLabel(self.container, "Shift + S to start/stop script.")
        self.inputEngine.addKeyboardListener(self.onKeyboardRelease)

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v

    def halt(self):
        self.status = "stopped"

    def setContainer(self, container):
        self.output.log("Container set for banker script.")
        self.container = container

    def setInputEngine(self, inputEngine):
        self.output.log("InputEngine set for banker script.")
        self.inputEngine = inputEngine

    def startBanking(self):
        self.statusLabel.set("Banking, bank deposit interval 20 sec.")
        time.sleep(2)
        self.status = "running"
        while 1:
            self.statusLabel.set("Waiting")
            time.sleep(60)
            if self.status == "stopped":
                self.statusLabel.set("Script stopped")
                break
            self.statusLabel.set("Banking")
            self.dragMouse(self.itemPos, self.bankPos)


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
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("I") in keysPressed:
            mouse = Controller()
            self.statusLabel.set("Item position set.")
            self.itemPos = mouse.position
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("B") in keysPressed:
            mouse = Controller()
            self.statusLabel.set("Bank position set.")
            self.bankPos = mouse.position
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("S") in keysPressed:
            if self.status == "running":
                self.status = "stopped"
            else:
                self.startBanking()
