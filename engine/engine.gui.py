from tkinter import *
from tkinter import ttk

class GuiEngine:
    def __init__(self, outputEngine):
        self.output = outputEngine

    def initWindow(self, scripts):
        self.windowHandle = Tk()
        self.windowHandle.geometry("400x250")

        centerFrame = Frame(self.windowHandle)
        centerFrame.pack()

        leftFrame = Frame(self.windowHandle)
        leftFrame.pack(side=LEFT)

        rightFrame = Frame(self.windowHandle)
        rightFrame.pack(side=RIGHT)

        label = Label(centerFrame, text = "Eve Online Bot")
        label.pack()

        Combo = ttk.Combobox(leftFrame, values = scripts)
        Combo.set("Pick an Option")
        Combo.pack(padx = 5, pady = 5)

        startBtn = Button(centerFrame, text = "Start", command = self.startBtnEvent)
        startBtn.pack(side=RIGHT)

        self.windowHandle.mainloop()

    def startBtnEvent(self):
        self.output.log("Start btn clicked")
