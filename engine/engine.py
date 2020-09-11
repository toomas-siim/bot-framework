import imp


# Main operations
# Class: Engine
class Engine:
    def __init__(self):
        self.output = imp.load_source('output-engine', './engine/engine.output.py').OutputEngine()
        self.scriptEngine = imp.load_source('script-engine', './engine/engine.script.py').ScriptEngine(self.output)
        self.guiEngine = imp.load_source('gui-engine', './engine/engine.gui.py').GuiEngine(self.output)

    def start(self):
        self.output.log("========= Starting bot =========")
        self.output.log("Loading scripts")
        scriptList = self.scriptEngine.loadAll()
        self.guiEngine.initWindow(self.scriptEngine)

        # For fun, let's run the first script
        if scriptList is not None:
            scriptList[0].process()
