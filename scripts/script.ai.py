import time
import os
import imp
from tkinter import *

class Script:
    name = "AI"
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)
        self.output.log("AI initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "AI Status")
        self.statusLabel.set("AI process started.")

        self.captureEngine.screenshotMouse((100, 100))

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
