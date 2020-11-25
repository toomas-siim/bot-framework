from tkinter import *
from tkinter import ttk
import os
import imp

class GuiEngine:
    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))

    def initWindow(self, scriptEngine):
        scripts = scriptEngine.getScriptNames()
        self.windowHandle = Tk()
        self.windowHandle.geometry("400x400")

        inputEngine = imp.load_source('input.engine', self.basePath + '/engine.input.py').InputEngine(self.output)
        container = imp.load_source('gui.container', self.basePath + '/features/gui/container.py').Container(self.output, self.windowHandle, scriptEngine, inputEngine)
        container.process()

        self.windowHandle.update()
        self.windowHandle.mainloop()

    def startBtnEvent(self):
        self.output.log("Start btn clicked")
