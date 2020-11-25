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
    name = "Powerminer"
    itemPos = None
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Powerminer script initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "Menu:")
        self.createLabel(self.container, "Shift + I to set item location.")
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
        self.container = container

    def setInputEngine(self, inputEngine):
        self.inputEngine = inputEngine
        self.inputEngine.initControllers()

    def startBanking(self):
        self.statusLabel.set("Powerminer, interval 5 sec.")
        time.sleep(2)
        self.status = "running"
        while 1:
            self.statusLabel.set("Waiting")
            time.sleep(5)
            if self.status == "stopped":
                self.statusLabel.set("Script stopped")
                break
            self.statusLabel.set("Mining")
            self.inputEngine.mouseMove(self.itemPos, 100)

    def onKeyboardRelease(self, keysPressed):
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("I") in keysPressed:
            mouse = Controller()
            self.statusLabel.set("Item position set.")
            self.itemPos = mouse.position
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("S") in keysPressed:
            if self.status == "running":
                self.status = "stopped"
            else:
                self.startBanking()
