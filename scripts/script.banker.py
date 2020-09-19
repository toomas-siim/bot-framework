from __future__ import absolute_import
import logging
logging.basicConfig()
from pynput.mouse import Listener
from pynput.mouse import Button, Controller
from pynput import keyboard
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

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("Banker process started.")
        self.inputEngine.addKeyboardListener(self.onKeyboardRelease)


    def halt(self):
        self.status = "stopped"

    def setContainer(self, container):
        self.container = container

    def setInputEngine(self, inputEngine):
        self.inputEngine = inputEngine

    def startBanking(self):
        self.statusLabel.set("Banking, bank deposit interval 20 sec.")
        time.sleep(2)
        self.status = "running"
        while 1:
            self.statusLabel.set("Waiting")
            time.sleep(20)
            self.statusLabel.set("Banking")
            self.dragMouse(self.itemPos, self.bankPos)
            if self.status == "stopped":
                self.statusLabel.set("Script stopped")
                break


    def dragMouse(self, fromPos, toPos):
        mouse = Controller()
        originalPosition = mouse.position
        mouse.position = (fromPos[0], fromPos[1])
        time.sleep(0.5)
        mouse.press(Button.left)
        time.sleep(0.25)
        mouse.position = (toPos[0], toPos[1])
        time.sleep(0.5)
        mouse.release(Button.left)

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
            self.startBanking()
