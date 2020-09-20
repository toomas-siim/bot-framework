from pynput.mouse import Listener
from pynput import keyboard

# Class InputEngine
# Mouse, keyboard listening etc...

class InputEngine:
    mouseCallbacks = []
    keyboardCallbacks = []
    keysPressed = []

    def __init__(self, output):
        output.log("Input engine initialized.")
        self.output = output
        self.initListeners()

    def closeCallback(self, type, index):
        if type == "mouse":
            del self.mouseCallbacks[index]
        else:
            del self.keyboardCallbacks[index]

    def closeListeners(self):
        self.keyboardListener.stop()
        self.mouseListener.stop()

    def initListeners(self):
        self.keyboardListener = keyboard.Listener(on_press=self.onKeyPress, on_release=self.onKeyRelease)
        self.keyboardListener.start()

        self.mouseListener = Listener(on_click=self.onMouseClick)
        self.mouseListener.start()

    def addMouseListener(self, method):
        self.mouseCallbacks.append(method)
        return len(self.mouseCallbacks) - 1

    def addKeyboardListener(self, method):
        self.keyboardCallbacks.append(method)
        return len(self.keyboardCallbacks) - 1

    def onMouseClick(self, x, y, button, pressed):
        if pressed:
            for callback in self.mouseCallbacks:
                callback((x, y), button)

    def onKeyPress(self, key):
        self.keysPressed.append(key)

    def onKeyRelease(self, key):
        for callback in self.keyboardCallbacks:
            callback(self.keysPressed)
        if key in self.keysPressed:
            del self.keysPressed[self.keysPressed.index(key)]
