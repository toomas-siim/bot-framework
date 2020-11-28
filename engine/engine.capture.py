import pyautogui
import win32gui
import time
import os
import numpy as np
import PIL
from pynput.mouse import Controller

# Class CaptureEngine
# Screenshots etc...

class CaptureEngine:
    activeWindows = {}

    def __init__(self, output):
        self.output = output
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.output.log("Capture engine initialized.")
        win32gui.EnumWindows(self.windowHandler, None)

    def windowHandler(self, hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            if win32gui.GetWindowText(hwnd):
                self.activeWindows[hwnd] = win32gui.GetWindowText(hwnd)

    def getActiveWindowsTitles(self):
        result = []
        for handle in self.activeWindows.items():
            result.append(handle[1])

        return result

    def getWindowFromHandle(self, handle):
        for win in self.activeWindows.items():
            if str(win[0]) in handle:
                return win

    def compareImages(self, img1, img2):
        img_a_pixels = Image.open(img1).getdata()
        img_b_pixels = Image.open(img2).getdata()
        img_a_array = np.array(img_a_pixels)
        img_b_array = np.array(img_b_pixels)

        return (img_a_array == img_b_array).sum()

    def screenshot(self, window_title=None):
        if window_title:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                self.output.log("[" + str(time.strftime("%H:%M:%S")) + "] Capturing window '" + window_title + "' screenshot.")

                # get window positions
                x, y, x1, y1 = win32gui.GetClientRect(hwnd)
                x, y = win32gui.ClientToScreen(hwnd, (x, y))
                x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

                # take screenshot
                im = pyautogui.screenshot(region=(x, y, x1, y1))
                return self.formatImage(im)
            else:
                raise ValueError("CaptureEngine, screen not found.")
        else:
            im = pyautogui.screenshot()
            return self.formatImage(im)

    def formatImage(self, imageObj):
        maxsize = (512, 512)
        imageObj.thumbnail(maxsize, PIL.Image.ANTIALIAS)
        return imageObj

    def getPixel(self, x, y):
        px = PIL.ImageGrab.grab().load()
        return px[x, y]
