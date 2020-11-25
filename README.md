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

```
def process(self):
    self.output.log("My script process has started.")
```

# Available functionality
## InputEngine
This is used to handle input methods (mouse & keyboard)
Uses pynput library.
### Accessable variables
Variables that can be accessed through the class.
```
# Initialized using InputEngine.initControllers
InputEngine.mouseController
InputEngine.keyboardController
```

### addKeyboardListener
```
# Initialized using InputEngine.initListeners
InputEngine.addKeyboardListener(self.myFunction)
```
### addMouseListener
```
# Initialized using InputEngine.initListeners
InputEngine.addMouseListener(self.myFunction)
```
### setInputEngine
```
def setInputEngine(self, inputEngine):
    self.inputEngine = inputEngine
    self.inputEngine.initControllers()
    self.inputEngine.initListeners()
```
