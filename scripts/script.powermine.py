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
import threading

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
        self.createLabel(self.container, "Shift + S to start script.")
        self.createLabel(self.container, "Shift + Q to halt script.")
        self.inputEngine.addKeyboardListener(self.onKeyboardRelease)

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v

    def halt(self):
        Script.status = "stopped"

    def setContainer(self, container):
        self.container = container

    def setRandomizer(self, randomizerEngine):
        self.randomizerEngine = randomizerEngine

    def setInputEngine(self, inputEngine):
        self.inputEngine = inputEngine
        self.inputEngine.initControllers()

    def startMining(self):
        self.statusLabel.set("Powerminer, interval 5 sec.")
        time.sleep(2)
        while 1:
            if Script.status == "stopped":
                self.statusLabel.set("Script stopped")
                break
            else:
                self.mineIteration()

        self.output.log("Powerminer script paused")

    def mineIteration(self):
        for rock in self.rockPositions:
             # Generate random paus if needed.
            self.randomizerEngine.randomPause()

            # Mine rock
            self.statusLabel.set("Mining rock")
            randPos = (rock[0] + (random.random() * 10), rock[1] + (random.random() * 10))
            self.inputEngine.mouseMove(randPos, 30 + (random.random() * 10))
            self.inputEngine.mouseController.press(mouseButton.left)
            time.sleep((random.random() * 2) + 3)

            # Drop rock
            self.statusLabel.set("Dropping rock")

            randPos = (self.inventoryLocation[0] + (random.random() * 10), self.inventoryLocation[1] + (random.random() * 10))
            self.inputEngine.mouseMove(randPos, 30 + (random.random() * 10))
            time.sleep(random.random() / 6)
            self.inputEngine.keyboardController.press(keyboard.Key.shift)
            time.sleep(random.random() / 4)
            self.inputEngine.mouseController.press(mouseButton.left)
            time.sleep(random.random() / 6)
            self.inputEngine.mouseController.release(mouseButton.left)
            time.sleep(random.random() / 4)
            self.inputEngine.keyboardController.release(keyboard.Key.shift)
            time.sleep(random.random() / 4)

    def onKeyboardRelease(self, keysPressed):
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("I") in keysPressed:
            self.inputEngine.keysPressed = [] # Clear keys
            self.statusLabel.set("Item position set.")
            self.inventoryLocation = self.inputEngine.mouseController.position
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("R") in keysPressed:
            self.inputEngine.keysPressed = [] # Clear keys
            if not (self.inputEngine.mouseController.position in self.rockPositions):
                self.rockPositions.append(self.inputEngine.mouseController.position)
                self.statusLabel.set("Rock position set. Total rocks: " + str(len(self.rockPositions)))
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("S") in keysPressed:
            self.inputEngine.keysPressed = [] # Clear keys
            if not (Script.status == "running"):
                Script.status = "running"
                self.output.log("Powerminer script running")
                # Async process
                thr = threading.Thread(target=self.startMining, args=(), kwargs={})
                thr.start()
        if keyboard.Key.shift in keysPressed and keyboard.KeyCode.from_char("Q") in keysPressed:
            self.inputEngine.keysPressed = [] # Clear keys
            self.statusLabel.set("Pausing script")
            self.halt()
