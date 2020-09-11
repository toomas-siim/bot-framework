from tkinter import *

class Container:
    def __init__(self, outputEngine, windowHandle, scriptEngine):
        self.output = outputEngine
        self.windowHandle = windowHandle
        self.scriptEngine = scriptEngine

    def process(self):
        self.createLabel(self.createContainer(TOP, 20, 10, 20), "Eve online bot")
        self.createScriptList(self.createContainer(TOP, 20, 40, 60), self.scriptEngine.getScriptNames())

    def createScriptList(self, frame, scripts):
        list = Listbox(frame, selectmode=SINGLE)
        for item in scripts:
            list.insert(END, item)
        list.pack()

    def createLabel(self, frame, text):
        label = Label(frame, text = text)
        label.pack()

        return label

    def createContainer(self, side, x, y, h):
        frame = Frame(self.windowHandle)
        frame.place(x=x,y=y,height=h)
        #frame.pack(side=side, fill=X)

        return frame
