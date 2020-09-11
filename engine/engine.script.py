from os import listdir
from os.path import isfile, join
import imp


# Class ScriptEngine
# Loads and initializes scripts.
class ScriptEngine:
    scriptList = []

    def __init__(self, outputEngine):
        self.output = outputEngine

    def loadAll(self):
        path = './scripts/'
        files = [f for f in listdir(path) if isfile(join(path, f))]

        for file in files:
            if file[:-9] == "script.":
                self.output.log("Loading script: " + file)
                self.scriptList.append(imp.load_source(file, path + file).Script(self.output))
        return self.scriptList

    def getScriptNames(self):
        names = []
        for scriptHandle in self.scriptList:
            names.append(scriptHandle.name)
        return names
