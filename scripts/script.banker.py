class Script:
    name = "Banker"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Banker script initialized")

    def process(self):
        self.output.log("Banker process started.")
