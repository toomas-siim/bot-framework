import pyautogui
#import win32gui
import time
import os
from PIL import ImageGrab
from pynput.mouse import Controller

# Class CaptureEngine
# Screenshots etc...

class CaptureEngine:
    def __init__(self, output):
        self.output = output
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.output.log("Capture engine initialized.")

    def screenshot(self, window_title=None):
        if window_title:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                # Set window to foreground
                win32gui.SetForegroundWindow(hwnd)

                # get window positions
                x, y, x1, y1 = win32gui.GetClientRect(hwnd)
                x, y = win32gui.ClientToScreen(hwnd, (x, y))
                x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

                # take screenshot
                im = pyautogui.screenshot(region=(x, y, x1, y1))
                return im
            else:
                raise ValueError("CaptureEngine, screen not found.")
        else:
            im = pyautogui.screenshot()
            return im

    def screenshotMouse(self, size):
        mouse = Controller()
        x = mouse.position[0]
        y = mouse.position[1]

        # take screenshot
        im = pyautogui.screenshot(region=(x, y, x + size[0], y + size[1]))
        im.save(self.basePath + '/data/screenshot/screenshot.' + str(time.time()) + '.jpg')
        return im

    def getPixel(self, x, y):
        px = ImageGrab.grab().load()
        return px[x, y]
