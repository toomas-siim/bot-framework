import os
from keras.preprocessing import image

# Class NeuralNetDataEngine
# Neural network data functionality.

class NeuralNetDataEngine:
    def __init__(self, output):
        basePath = os.path.dirname(os.path.realpath(__file__))
        self.output = output
        self.output.log("Neural net data engine initialized.")

    def imageToData(self, path):
        image = image.load_img(path)
        input_arr = image.img_to_array(image)
        input_arr = np.array([input_arr])  # Convert single image to a batch.
        return input_arr

    # converts to ascii number
    def textToData(self, text):
        return "".join([str(ord(c)) for c in s])

    def processData(self, dataX, dataY):
        resolution = (1920, 1080)
        dataX = dataX.reshape(len(dataX), resolution[0], resolution[1], 1)
        dataY = dataY.reshape(len(dataY), resolution[0], resolution[1], 1)

    return (dataX, dataY)
