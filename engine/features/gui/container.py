from __future__ import absolute_import
from tkinter import *

class Container:
    scriptStatus = 0

    def __init__(self, outputEngine, windowHandle, scriptEngine):
        self.output = outputEngine
        self.windowHandle = windowHandle
        self.scriptEngine = scriptEngine

    def process(self):
        self.createLabel(self.createContainer(TOP, 160, 10, 20), "Eve online bot")
        self.createLabel(self.createContainer(TOP, 20, 60, 20), "Choose your script")
        self.selectedScript = self.createScriptList(self.createContainer(TOP, 200, 40, 60), self.scriptEngine.getScriptNames())
        self.startBtn = self.createBtn(self.createContainer(TOP, 320, 200, 60), "Start", self.startBtnEvent)
        self.createBtn(self.createContainer(TOP, 20, 200, 60), "Exit", self.exitBtnEvent)
        self.statusLabel = self.createLabel(self.createContainer(TOP, 20, 160, 20), "...")

    def exitBtnEvent(self):
        exit()

    def startBtnEvent(self):
        selectedList = self.selectedScript.get(ACTIVE)
        self.statusLabel.set("Running script '" + selectedList + "'")
        self.output.log("Selected list: " + selectedList)
        # Run script process
        for item in self.scriptEngine.scriptList:
            if item.name == selectedList:
                if self.scriptStatus == 0:
                    self.startBtn.config(text="Stop")
                    item.process(self.statusLabel)
                else:
                    self.startBtn.config(text="Start")
                    item.halt()


    def createBtn(self, frame, name, command):
        btn = Button(frame, text = name, command = command)
        btn.pack()

        return btn

    def createScriptList(self, frame, scripts):
        list = Listbox(frame, selectmode=SINGLE)
        for item in scripts:
            list.insert(END, item)
        list.pack()

        return list

    def createLabel(self, frame, text):
        v = StringVar()
        label = Label(frame, textvariable=v)
        label.pack()
        v.set(text)

        return v

    def createContainer(self, side, x, y, h):
        frame = Frame(self.windowHandle)
        frame.place(x=x,y=y,height=h)
        #frame.pack(side=side, fill=X)

        return frame
