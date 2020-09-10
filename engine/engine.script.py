from os import listdir
from os.path import isfile, join
import imp


# Class ScriptEngine
# Loads and initializes scripts.
class ScriptEngine:
    def __init__(self, outputEngine):
        self.output = outputEngine

    def loadAll(self):
        path = './scripts/'
        files = [f for f in listdir(path) if isfile(join(path, f))]

        for file in files:
            if file[:-9] == "script.":
                self.output.log("Loading script: " + file)
                script = imp.load_source('script-' + file, path + file)
                script = script.Script(self.output)
