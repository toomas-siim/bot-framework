import time
import os
import imp

class Script:
    name = "AI"
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)
        self.output.log("AI initialized")

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("AI process started.")

        self.captureEngine.screenshotMouse((100, 100))

    def halt(self):
        self.status = "stopped"

    def setContainer(container):
        self.container = container
