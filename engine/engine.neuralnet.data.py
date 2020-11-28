import os
from keras.preprocessing import image
import np

# Class NeuralNetDataEngine
# Neural network data functionality.

class NeuralNetDataEngine:
    def __init__(self, output):
        basePath = os.path.dirname(os.path.realpath(__file__))
        self.output = output
        self.output.log("Neural net data engine initialized.")

    def imageToData(self, path):
        img = image.load_img(path)
        input_arr = image.img_to_array(img)
        input_arr = np.array([input_arr])  # Convert single image to a batch.
        return input_arr

    # converts to ascii number
    def textToData(self, text):
        return int("".join([str(ord(c)) for c in s]))
