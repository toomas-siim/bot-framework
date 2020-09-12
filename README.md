# Eve-bot
Basically this is an EVE online bot framework made in python.
Few example scripts in /scripts/

## New script
To create a new script, you need to add a file in /scripts/
Ie script.myscript.py

Inside it, create a class named Script
### Example:
```
    class Script:
        name = "Banker"

        def __init__(self, outputEngine):
            self.output = outputEngine
            self.output.log("My script initialized")

        def process(self, statusLabel):
            self.statusLabel = statusLabel
            statusLabel.set("My script process has started.")
```
