import time
import os
import imp
import win32gui
from tkinter import *
import _thread
import json

class Script:
    name = "AI"
    status = "stopped"
    recordStatus = False
    recordingThread = None

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)
        self.output.log("AI initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "AI Status")
        self.windowSelection = self.createSelection(self.container, self.captureEngine.activeWindows.items())
        self.actionType = self.createEntry(self.container, 'Action type')
        self.recordBtn = self.createButton(self.container, "Record", self.startRecord)
        self.statusLabel.set("AI process started.")
        self.recordingThread = _thread.start_new_thread(self.recordLoop, ())
        self.mouseRecordingThread = _thread.start_new_thread(self.mouseRecordLoop, ())

    def startRecord(self):
        if self.recordStatus == False:
            self.recordStatus = True
            self.statusLabel.set("Recording gameplay for data.")
            self.recordBtn.set('Recording')
        else:
            self.recordStatus = False
            self.statusLabel.set("Recording stopped.")
            self.recordBtn.set('Record')

    def readyForRecording(self):
        if self.recordStatus == True:
            activeHandle = win32gui.GetForegroundWindow()
            selectedWindow = self.windowSelection.get()
            selectedAction = self.actionType.get()
            if len(selectedAction) > 0 and len(selectedWindow) > 0:
                if str(activeHandle) in selectedWindow:
                    return True
        return False

    def logMouseData(self, coord, button, pressed):
        if self.readyForRecording() == True:
            self.keyLoggerData.append(('mouse', int(round(time.time() * 1000)), str(button), pressed))

    def logKeyboardData(self, key, pressed):
        if self.readyForRecording() == True:
            self.keyLoggerData.append(('keyboard', int(round(time.time() * 1000)), str(key), pressed))

    def getMousePosition(self):
        activeHandle = win32gui.GetForegroundWindow()
        if activeHandle:
            rect = win32gui.GetWindowRect(activeHandle)
            mouseAbs = self.inputEngine.mouseController.position
            return (mouseAbs[0] - rect[0], mouseAbs[1] - rect[1])

    def mouseRecordLoop(self):
        self.output.log("Mouse record loop started")
        self.inputEngine.addMouseListener(self.logMouseData)
        self.inputEngine.addKeyboardListener(self.logKeyboardData)
        self.keyLoggerData = []
        lastUpdate = time.time()
        while True:
            time.sleep(0.01)
            if self.readyForRecording() == True and time.time() > lastUpdate: # Update once per second, as with screen.
                lastUpdate = time.time()
                mousePos = self.getMousePosition()
                if mousePos:
                    self.keyLoggerData.append(('mouse-pos', int(round(time.time() * 1000)), mousePos))
                    if len(self.keyLoggerData) > 0:
                        self.writeRecord(self.keyLoggerData)
                        self.keyLoggerData = []

    def writeRecord(self, record):
        activeHandle = win32gui.GetForegroundWindow()
        selectedAction = self.actionType.get()
        windowTitle = win32gui.GetWindowText(activeHandle)

        f = open(self.basePath + '/../data/screenshot/' + windowTitle + '/data.' + selectedAction + '.' + str(time.time()) + '.json', "w")
        f.write(json.dumps(record))
        f.close()

    def recordLoop(self):
        self.output.log("Record loop started")
        while True:
            time.sleep(1)
            if self.readyForRecording() == True:
                activeHandle = win32gui.GetForegroundWindow()
                selectedAction = self.actionType.get()
                windowTitle = win32gui.GetWindowText(activeHandle)
                # Screenshot
                shot = self.captureEngine.screenshot(window_title = windowTitle)
                shot.save(self.basePath + '/../data/screenshot/' + windowTitle + '/screenshot.' + selectedAction + '.' + str(time.time()) + '.jpg')

    def changeWindow(self, event):
        selectedWindow = self.captureEngine.getWindowFromHandle(self.windowSelection.get())
        # Make data storage
        try:
            os.makedirs(self.basePath + '/../data/screenshot/' + selectedWindow[1])
        except OSError as e:
            self.output.log("Path already exists for " + selectedWindow[1])

    def halt(self):
        self.status = "stopped"

    def setContainer(self, container):
        self.container = container

    def setInputEngine(self, engine):
        self.inputEngine = engine
        self.inputEngine.initControllers()
        self.inputEngine.initListeners()

    def createEntry(self, frame, label):
        top = Frame(frame)
        top.pack()
        L1 = Label(top, text=label)
        L1.pack( side = LEFT)
        E1 = Entry(top, bd =5)
        E1.pack(side = RIGHT)

        return E1

    def createSelection(self, frame, options):
        variable = StringVar()

        w = OptionMenu(frame, variable, *options, command = self.changeWindow)
        w.config(width=20)
        w.pack()

        return variable

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v

    def createButton(self, frame, name, callback):
        v = StringVar()
        btn = Button(frame, textvariable=v, command = callback, padx = 60)
        btn.pack()
        v.set(name)

        return v
