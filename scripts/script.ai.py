import time
import imp

class Script:
    name = "AI"
    status = "stopped"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.captureEngine = imp.load_source('capture.engine', './engine/engine.capture.py').CaptureEngine(self.output)
        self.output.log("AI initialized")

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("AI process started.")
        
        self.captureEngine.screenshotMouse((100, 100))

    def halt(self):
        self.status = "stopped"

    def setContainer(container):
        self.container = container
