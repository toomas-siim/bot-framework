from tkinter import *
from tkinter import ttk
import imp

class GuiEngine:
    def __init__(self, outputEngine):
        self.output = outputEngine

    def initWindow(self, scriptEngine):
        scripts = scriptEngine.getScriptNames()
        self.windowHandle = Tk()
        self.windowHandle.geometry("400x250")

        inputEngine = imp.load_source('input.engine', './engine/engine.input.py').InputEngine(self.output)
        container = imp.load_source('gui.container', './engine/features/gui/container.py').Container(self.output, self.windowHandle, scriptEngine, inputEngine)
        container.process()

        self.windowHandle.update()
        self.windowHandle.mainloop()

    def startBtnEvent(self):
        self.output.log("Start btn clicked")
