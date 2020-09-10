from tkinter import *

class GuiEngine:
    def __init__(self, outputEngine):
        self.output = outputEngine
        self.initWindow()

    def initWindow(self):
        self.windowHandle = Tk()
        self.windowHandle.geometry("400x250")
        frame = Frame(self.windowHandle)
        frame.pack()

        button = Button(frame, text = "Button1", command = self.btnClick)
        button.pack()

        self.windowHandle.mainloop()
        sleep(5)

    def btnClick(self):
        self.output.log("Btn clicked")
