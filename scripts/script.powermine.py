from __future__ import absolute_import
import logging
logging.basicConfig()
from pynput.mouse import Listener
from pynput.mouse import Button as mouseButton, Controller
from pynput import keyboard
from tkinter import *
import time
import random
import imp

class Script:
    name = "Powerminer"
    rockPositions = []
    inventoryLocation = None
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Powerminer script initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "Menu:")
        self.createLabel(self.container, "Shift + R to set new rock location.")
        self.createLabel(self.container, "Shift + I to set inventory item location.")
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

    def startMining(self):
        self.statusLabel.set("Powerminer, interval 5 sec.")
        time.sleep(2)
        self.status = "running"
        while 1:
            if self.status == "stopped":
                self.statusLabel.set("Script stopped")
                break
            self.mineIteration()

    def mineIteration(self):
        for rock in self.rockPositions:
            # Mine rock
            self.statusLabel.set("Mining rock")
            self.inputEngine.mouseMove(rock, 50 + (random.random() * 20))
            self.inputEngine.mouseController.press(mouseButton.left)
            time.sleep((random.random() * 2) + 3)

            # Drop rock
            self.statusLabel.set("Dropping rock")
            self.inputEngine.mouseMove(self.inventoryLocation, 50 + (random.random() * 20))
            time.sleep(random.random())
            self.inputEngine.keyboardController.press(keyboard.Key.shift)
            time.sleep(random.random() / 2)
            self.inputEngine.mouseController.press(mouseButton.left)
            time.sleep(random.random() / 4)
            self.inputEngine.mouseController.release(mouseButton.left)
            time.sleep(random.random() / 2)
            self.inputEngine.keyboardController.release(keyboard.Key.shift)
            time.sleep(random.random() / 2)

    def onKeyboardRelease(self, keysPressed):
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("I") in keysPressed:
            self.statusLabel.set("Item position set.")
            self.inventoryLocation = self.inputEngine.mouseController.position
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("R") in keysPressed:
            if not (self.inputEngine.mouseController.position in self.rockPositions):
                self.rockPositions.append(self.inputEngine.mouseController.position)
                self.statusLabel.set("Rock position set. Total rocks: " + str(len(self.rockPositions)))
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("S") in keysPressed:
            if self.status == "running":
                self.statusLabel.set("Pausing script")
                self.halt()
            else:
                self.startMining()
