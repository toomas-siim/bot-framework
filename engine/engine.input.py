import pynput.mouse
from pynput import keyboard
import time

# Class InputEngine
# Mouse, keyboard listening etc...

class InputEngine:
    mouseCallbacks = []
    keyboardCallbacks = []
    keysPressed = []
    mouseController = None
    keyboardController = None

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

    def initControllers(self):
        self.mouseController = pynput.mouse.Controller()
        self.keyboardController = keyboard.Controller()

    def initListeners(self):
        self.keyboardListener = keyboard.Listener(on_press=self.onKeyPress, on_release=self.onKeyRelease)
        self.keyboardListener.start()

        self.mouseListener = pynput.mouse.Listener(on_click=self.onMouseClick)
        self.mouseListener.start()

    def mouseMove(self, coords, speed):
        # Fetch current position
        curPosition = [self.mouseController.position[0], self.mouseController.position[1]]

        # Calculate step speeds for each axis
        steps = [1, 1]
        steps[0] = abs(self.mouseController.position[0] - coords[0]) / speed
        steps[1] = abs(self.mouseController.position[1] - coords[1]) / speed

        # Move mouse loop
        while not (coords[0] == curPosition[0] and coords[1] == curPosition[1]):
            # x axis
            if curPosition[0] < coords[0]:
                if curPosition[0] + steps[0] > coords[0]:
                    curPosition[0] = coords[0]
                else:
                    curPosition[0] += steps[0]
            elif curPosition[0] > coords[0]:
                if curPosition[0] - steps[0] < coords[0]:
                    curPosition[0] = coords[0]
                else:
                    curPosition[0] -= steps[0]

            # y axis
            if curPosition[1] < coords[1]:
                if curPosition[1] + steps[1] > coords[1]:
                    curPosition[1] = coords[1]
                else:
                    curPosition[1] += steps[1]
            elif curPosition[1] > coords[1]:
                if curPosition[1] - steps[1] < coords[1]:
                    curPosition[1] = coords[1]
                else:
                    curPosition[1] -= steps[1]

            self.mouseController.position = (curPosition[0], curPosition[1])
            time.sleep(1/60)

    def addMouseListener(self, method):
        self.mouseCallbacks.append(method)
        return len(self.mouseCallbacks) - 1

    def addKeyboardListener(self, method):
        self.keyboardCallbacks.append(method)
        return len(self.keyboardCallbacks) - 1

    def onMouseClick(self, x, y, button, pressed):
        if pressed:
            for callback in self.mouseCallbacks:
                callback((x, y), button, pressed)

    def onKeyPress(self, key):
        self.keysPressed.append(key)
        for callback in self.keyboardCallbacks:
            callback(key, 1)

    def onKeyRelease(self, key):
        if len(self.keysPressed) > 0:
            for keyPressed in self.keysPressed:
                if key in self.keysPressed:
                    self.keysPressed.remove(key)

        for callback in self.keyboardCallbacks:
            callback(key, 0)
