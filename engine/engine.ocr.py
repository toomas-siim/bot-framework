# Class OCREngine
# Logging etc...

class OCREngine:
    def __init__(self, output):
        self.output = output
        self.output.log("OCR engine initialized.")
