# Eve-bot
Basically this is an EVE online bot framework made in python.
Few example scripts in /scripts/

## Usage
Using it is pretty simple, just run bot.py

```
python bot.py
```

You should see an UI momentarily and just select the script you need to run.

Guidelines should appear near the exit button, where the status label is located.

PS! You need to install dependencies as well. (recommend pip install)


## New script
To create a new script, you need to add a file in /scripts/

Ie script.myscript.py

Inside it, create a class named Script
### Example:
```
class Script:
    name = "MyScript"

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("My script initialized")

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("My script process has started.")

    def halt(self):
        self.status = "stopped"
```

## Events & Methods
### setContainer
A script has a designated area in the ui to access.

This will give you a tkinter Frame to handle.

```
def setContainer(container):
    self.container = container
```

### halt
Halt event, when a user presses the stop button.

```
def halt(self):
    self.status = "stopped"
```

### process
When a script is started the process method is called.

statusLabel is passed on, so the script can take over status monitoring.

```
def process(self, statusLabel):
    self.statusLabel = statusLabel
    statusLabel.set("My script process has started.")
```
