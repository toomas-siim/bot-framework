# Generic Bot Framework
Basically this is a generic bot framework.
Solutions vary from simple autoclickers to advanced AI bots.
There are various libraries included to be used.
WIP - Integrated with an neural net (CNN).
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

    def process(self):
        self.output.log("My script process has started.")
```

## Neural net methods
### recordAction
Record an action for data collection.

Used in training bots.

```
recordAction("banking")
```

## Events & Methods
### setNeuralNet
This will give you a neural net class to call for functions.

```
def setNeuralNet(neuralNet):
    self.neuralNet = neuralNet
```

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
