import imp
import os

# Main operations
# Class: Engine
class Engine:
    def __init__(self):
        basePath = os.path.dirname(os.path.realpath(__file__))
        self.output = imp.load_source('output.engine', basePath + '/engine.output.py').OutputEngine()
        self.scriptEngine = imp.load_source('script.engine', basePath + '/engine.script.py').ScriptEngine(self.output)
        self.guiEngine = imp.load_source('gui.engine', basePath + '/engine.gui.py').GuiEngine(self.output)

    def start(self):
        self.output.log("========= Starting bot =========")
        self.output.log("Loading scripts")
        scriptList = self.scriptEngine.loadAll()
        self.guiEngine.initWindow(self.scriptEngine)
