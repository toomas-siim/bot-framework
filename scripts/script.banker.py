from __future__ import absolute_import

from pynput import mouse

class Script:
    name = "Banker"
    itemPos = None
    bankPos = None

    def __init__(self, outputEngine):
        self.output = outputEngine
        self.output.log("Banker script initialized")

    def process(self, statusLabel):
        self.statusLabel = statusLabel
        statusLabel.set("Banker process started.")
        if self.itemPos == None:
            self.itemPos = self.requestItemPos()
        #if self.bankPos == None:
        #    self.bankPos = self.requestBankPos()

    def requestBankPos(self):
        self.statusLabel.set("Left click to bank to record position.")
        self.listeningType = "bank"

    def requestItemPos(self):
        self.statusLabel.set("Left click to item to record position.")
        self.listeningType = "item"
        listener = mouse.Listener(on_click=self.leftClick)
        listener.start()

    def leftClick(self, x, y, button, pressed):
        self.statusLabel.set("Left click pressed. Type: " + self.listeningType)
