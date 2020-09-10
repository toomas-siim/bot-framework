import imp


# Main operations
# Class: Engine
class Engine:
    def __init__(self):
        output = imp.load_source('output-engine', './engine/engine.output.py')
        script = imp.load_source('script-engine', './engine/engine.script.py')
        self.output = output.OutputEngine()
        self.scriptEngine = script.ScriptEngine(self.output)

    def start(self):
        self.output.log("========= Starting bot =========")
        self.output.log("Loading scripts")
        self.scriptList = self.scriptEngine.loadAll()
