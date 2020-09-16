import pyautogui
#import win32gui
import time
from pynput.mouse import Controller

# Class CaptureEngine
# Screenshots etc...

class CaptureEngine:
    def __init__(self, output):
        self.output = output
        self.output.log("Capture engine initialized.")

    def screenshot(window_title=None):
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

    def screenshotMouse(size):
        mouse = Controller()
        x = mouse.position[0]
        y = mouse.position[1]

        # take screenshot
        im = pyautogui.screenshot(region=(x, y, x + size[0], y + size[1]))
        im.save('./data/screenshot/screenshot.' + time.time() + '.jpg')
        return im
