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
        scriptList = self.scriptEngine.loadAll()

        # For fun, let's run the first script
        if scriptList is not None:
            scriptList[0].process()
