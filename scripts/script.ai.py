import time
import os
import imp
import win32gui
from tkinter import *
import _thread
import json
import glob

class Script:
    name = "AI"
    status = "stopped"
    recordStatus = False
    recordingThread = None
    selectedWindowTitle = None

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.basePath = os.path.dirname(os.path.realpath(__file__))
        self.captureEngine = imp.load_source('capture.engine', self.basePath + '/../engine/engine.capture.py').CaptureEngine(self.output)
        self.neuralEngine = imp.load_source('neural.engine', self.basePath + '/../engine/engine.neuralnet.py').NeuralNetEngine(self.output)
        self.output.log("AI initialized")

    def process(self):
        self.statusLabel = self.createLabel(self.container, "AI Status")
        self.windowSelection = self.createSelection(self.container, self.captureEngine.activeWindows.items())
        self.actionType = self.createEntry(self.container, 'Action type')
        self.recordBtn = self.createButton(self.container, "Record", self.startRecord)
        self.trainButtons()
        self.statusLabel.set("AI process started.")
        self.recordingThread = _thread.start_new_thread(self.recordLoop, ())
        self.mouseRecordingThread = _thread.start_new_thread(self.mouseRecordLoop, ())

        # Debug - remove later
        #self.actionType.delete(0, END)
        #self.actionType.insert(0, 'smelting')
        #self.selectedWindowTitle = "RuneLite - Chuthulun"
        #self.startTrain()

    def trainButtons(self):
        top = Frame(self.container)
        top.pack()
        self.trainBtn = self.createButton(top, "Train", self.startTrain, LEFT)
        self.runBtn = self.createButton(top, "Run", self.startRun, RIGHT)

    def startTrain(self):
        self.output.log("Training started.")
        self.statusLabel.set("Starting training...")
        (inputData, outputData) = self.generateDataForModel()
        inputDimensions = inputData[0].shape
        outputDimension = len(outputData[0])

        inputData = self.neuralEngine.dataEngine.reshapeData(inputData, inputDimensions, True)
        inputDimensions = inputData[0].shape
        outputData = self.neuralEngine.dataEngine.reshapeData(outputData, ( outputDimension ), True)
        outputDimension = len(outputData[0])

        (inputData, outputData) = self.neuralEngine.dataEngine.normalizeData(inputData, outputData)
        self.neuralEngine.buildModel(inputDimensions[0], outputDimension)
        self.neuralEngine.compileModel()
        self.neuralEngine.trainModel(inputData, outputData)
        self.output.log("Training finished")


    def generateDataForModel(self):
        self.neuralEngine.dataEngine.extractZipData(self.getZippedPath(), self.getDataPath());
        screenData = self.getTrainingScreenData()
        actionData = self.getTrainingActionData()

        absoluteInputData = []
        absoluteOutputData = []

        # Handle
        for key in actionData.keys():
            if int(int(key) / 1000) in screenData.keys():
                absoluteOutputData.append(actionData[key])
                screenshot = screenData.get(int(int(key) / 1000))
                absoluteInputData.append(screenshot)
            else:
                self.output.log("Missing screenshot for: " + str(int(int(key) / 1000)))

        return (absoluteInputData, absoluteOutputData)

    def getTrainingScreenData(self):
        selectedAction = self.actionType.get()
        # Fetch screenshots
        screens = glob.glob(self.getDataPath() + 'screenshot.' + selectedAction + '.*.jpg')
        screenshotData = {}
        for screen in screens:
            basename = str(os.path.basename(screen))
            screenInfo = basename.split(".")
            if len(screenInfo) == 4 and screenInfo[0] == "screenshot":
                screenshotData[int(screenInfo[2])] = self.neuralEngine.dataEngine.imageToData(screen)
        return screenshotData

    def getTrainingActionData(self):
        selectedAction = self.actionType.get()
        # Fetch action data
        data = glob.glob(self.getDataPath() + 'data.' + selectedAction + '.*.json')
        actionData = {}
        for action in data:
            actionInfo = os.path.basename(action).split(".")
            if len(actionInfo) == 4 and actionInfo[0] == "data":
                f = open(action, "r")
                content = json.loads(f.read())
                formatted = []
                for v in content:
                    # Action type
                    if v[0] == "mouse-pos":
                        v[0] = 1
                    elif v[0] == "mouse":
                        v[0] = 2
                    elif v[0] == "keyboard":
                        v[0] = 3
                    else:
                        v[0] = 4
                    # Button / Key type
                    if v[2] == 'Button.left':
                        v[2] = 1
                    elif v[2] == 'Button.right':
                        v[2] = 2
                    else:
                        v[2] = 3
                    actionData[int(v[1])] = v
        return actionData

    def startRun(self):
        self.output.log("Running started.")
        self.statusLabel.set("Running...")

    def startRecord(self):
        if self.recordStatus == False:
            self.recordStatus = True
            self.statusLabel.set("Recording gameplay for data.")
            self.recordBtn.set('Stop recording')
        else:
            selectedAction = self.actionType.get()
            self.recordStatus = False
            self.statusLabel.set("Recording stopped, saving zip file.")
            self.neuralEngine.dataEngine.zipData(self.getZippedPath(), self.getDataPath() + '*.' + selectedAction + '.*')
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
        lastUpdate = int(time.time())
        while True:
            time.sleep(0.01)
            if self.readyForRecording() == True and int(time.time()) > lastUpdate: # Update once per second, as with screen.
                lastUpdate = int(time.time())
                mousePos = self.getMousePosition()
                if mousePos:
                    self.keyLoggerData.append(('mouse-pos', int(round(time.time() * 1000)), mousePos, 0))
                    if len(self.keyLoggerData) > 0:
                        self.writeRecord(self.keyLoggerData)
                        self.keyLoggerData = []

    def getDataPath(self):
        return self.basePath + '/../data/screenshot/' + self.selectedWindowTitle + "/"

    def getZippedPath(self):
        selectedAction = self.actionType.get()
        return self.basePath + '/../data/zipped/' + 'data.' + selectedAction + '.zip'

    def writeRecord(self, record):
        selectedAction = self.actionType.get()
        f = open(self.getDataPath() + 'data.' + selectedAction + '.' + str(int(time.time())) + '.json', "w")
        f.write(json.dumps(record))
        f.close()

    def createScreen(self):
        activeHandle = win32gui.GetForegroundWindow()
        selectedAction = self.actionType.get()
        windowTitle = win32gui.GetWindowText(activeHandle)
        # Screenshot
        shot = self.captureEngine.screenshot(window_title = windowTitle)
        shot.save(self.basePath + '/../data/screenshot/' + windowTitle + '/screenshot.' + selectedAction + '.' + str(int(time.time())) + '.jpg')

    def recordLoop(self):
        self.output.log("Record loop started")
        while True:
            time.sleep(1)
            if self.readyForRecording() == True:
                self.createScreen()

    def changeWindow(self, event):
        selectedWindow = self.captureEngine.getWindowFromHandle(self.windowSelection.get())
        # Make data storage
        try:
            self.selectedWindowTitle = selectedWindow[1]
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

    def createButton(self, frame, name, callback, side = TOP):
        v = StringVar()
        btn = Button(frame, textvariable=v, command = callback, padx = 20)
        btn.pack(side = side)
        v.set(name)

        return v
